from user.serializers import GroupSerializer
from rest_framework import serializers
from gamecreation.models import pokermember,PokerBoard
from django.contrib.auth import get_user_model
from Invite.models import Invite 
import requests
import math
from requests.auth import HTTPBasicAuth
from Invite.models import Invite
from ticket.models import ticket,estimate
from gamecreation.models import PokerBoard,pokermember
from ticket.serializers import EstimateSerializer
from django.db import transaction
from utils.utils import JiraValidation
from ticket.models import ticket,estimate


User = get_user_model()
MaxResults=100


class PokerMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = pokermember
        fields = ['id', 'role', 'poker','accept']
        depth=2


class UserEntrySerializer(serializers.Serializer):

    invite = serializers.BooleanField()
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=pokermember.ROLE_CHOICES)

    def validate(self, attrs):
        invite = attrs.get("invite")
        email = attrs.get("email")

        if not invite:
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"email": f"User with email {email} does not exist."}
                )
        return attrs
    

class PokerBoardSerializer(JiraValidation,serializers.ModelSerializer):

    users = UserEntrySerializer(many=True, write_only=True, required=False)
    cloudsite = serializers.CharField(write_only=True, required=True)
    apikey = serializers.CharField(write_only=True, required=True)
    import_type = serializers.CharField(write_only=True, required=True)
    import_value = serializers.CharField(write_only=True, required=False, allow_blank=True)
    tickets = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = PokerBoard
        fields = [
            "game_name", "game_description", "users", "apikey", "cloudsite",
            "import_type", "import_value", "tickets"
        ]



    def _check_tickets(self, apikey, cloudsite, host, tickets):
        url = f"https://{cloudsite}/rest/api/3/search"
        try:
            response1 = requests.get(
                url,
                auth=HTTPBasicAuth(host.email, apikey),
                headers={"Accept": "application/json"},
                params={"jql": "ORDER BY created DESC", "maxResults": 0},
            )
            response1.raise_for_status()
            total = response1.json().get("total", 0)

            data = []
            for i in range(0, math.ceil(total / MaxResults)):
                response2 = requests.get(
                    url,
                    auth=HTTPBasicAuth(host.email, apikey),
                    headers={"Accept": "application/json"},
                    params={
                        "jql": "ORDER BY created DESC",
                        "maxResults": MaxResults,
                        "startAt": i * MaxResults,
                    },
                )
                response2.raise_for_status()
                data.extend(response2.json().get("issues", []))

            jira_ticket_keys = {issue["key"] for issue in data}
            missing_tickets = set(tickets) - jira_ticket_keys

            if missing_tickets:
                raise serializers.ValidationError(
                    {"failed_tickets": list(missing_tickets)}
                )
            
            return [issue for issue in data if issue["key"] in tickets]

        except requests.RequestException as e:
            raise serializers.ValidationError({"jira_api_error": str(e)})

        

    def _validate_sprint(self, site, host, token, sprintId):
        url = f"https://{site}/rest/agile/1.0/sprint/{sprintId}/issue"
        response = requests.get(url, auth=HTTPBasicAuth(host.email, token), headers={"Accept": "application/json"})
        response.raise_for_status()
        issues_list = response.json().get("issues", [])
        if not issues_list:
            raise serializers.ValidationError({"failed_sprint": sprintId})
        else :
            return response.json().get("issues", [])

    def _validate_jql(self, site, host, token, jql):
        url = f"https://{site}/rest/api/3/search"
        response = requests.get(
            url,
            auth=HTTPBasicAuth(host.email, token),
            headers={"Accept": "application/json"},
            params={"jql": jql, "maxResults": 1},
        )
        response.raise_for_status()
        issues_list = response.json().get("issues", [])
        if not issues_list:
            raise serializers.ValidationError({"failed_jql": jql})
        else :
            return issues_list
        
    def _validate_api(self,apikey,site,host) :
        data, code = self.validate_and_store_api(apikey, site, host, save=True)
        if code != 200:
            raise serializers.ValidationError({"api_validation": "validation failed"})
            

    def validate(self, attrs):

        apikey = attrs.get("apikey")
        cloudsite = attrs.get("cloudsite")
        import_type = attrs.get("import_type")
        import_value = attrs.get("import_value")
        tickets = attrs.get("tickets", [])
        host = self.context["request"].user
         
        self. _validate_api(apikey,cloudsite,host)

        if import_type == "tickets":
            if not tickets:
                raise serializers.ValidationError({"tickets": "Tickets list is required"})
            issues = self._check_tickets(apikey, cloudsite, host, tickets)
            self.context["verified_issues"] = issues

        elif import_type == "sprintId":
            if not import_value:
                raise serializers.ValidationError({"import_value": "sprintId is required"})
            issues = self._validate_sprint(cloudsite, host, apikey, import_value)
            self.context["verified_issues"] = issues

        elif import_type == "jql":
            if not import_value:
                raise serializers.ValidationError({"import_value": "JQL query is required"})
            issues = self._validate_jql(cloudsite, host, apikey, import_value)
            self.context["verified_issues"] = issues

        else:
            raise serializers.ValidationError({"import_type": "Invalid import type"})

        return attrs
    

    def create(self, validated_data):
        request = self.context.get("request")
        host = request.user
        users_data = validated_data.pop("users", [])
        game_name=validated_data.pop("game_name")
        game_description=validated_data.pop("game_description","")

        pokerboard = PokerBoard.objects.create(game_name=game_name,game_description=game_description)
        pokermember.objects.create(poker=pokerboard, member=host, role=3, accept=True)

        member_emails = [u["email"] for u in users_data if not u["invite"]]
        users_map = {u.email: u for u in User.objects.filter(email__in=member_emails)}
        with transaction.atomic():

            invites, members = [], []
            for user_data in users_data:
                if user_data["invite"]:
                    invites.append(
                        Invite(
                            pokerboard=pokerboard,
                            host=host,
                            guest=user_data["email"],
                            role=user_data["role"],
                            accept=False,
                        )
                    )
                else:
                    user_instance = users_map.get(user_data["email"])
                    if not user_instance:
                        raise serializers.ValidationError(
                            {"email": f"User {user_data['email']} not found"}
                        )
                    members.append(
                        pokermember(
                            poker=pokerboard,
                            member=user_instance,
                            role=user_data["role"],
                            accept=False,
                        )
                    )

            if invites:
                Invite.objects.bulk_create(invites)
            if members:
                pokermember.objects.bulk_create(members)

        verified_issues = self.context.get("verified_issues", [])

        tickets_to_create = []

        for jira_data in verified_issues:
            tickets_to_create.append(
                ticket(
                    key=jira_data["key"],
                    pokerid=pokerboard,
                    priority=jira_data["fields"]["priority"]["name"],
                    summary=jira_data["fields"]["summary"],
                    description=(
                        jira_data["fields"]
                        .get("description", {})
                        .get("content", [{}])[0]
                        .get("content", [{}])[0]
                        .get("text", "")
                    ),
                    import_type=validated_data["import_type"],
                    type=jira_data["fields"]["issuetype"]["name"],
                )
            )


        created_tickets = ticket.objects.bulk_create(tickets_to_create)
        
        estimates_to_create = []
        for new_ticket in created_tickets:
            for user in users_data:
                if not user["invite"]:
                    estimates_to_create.append(
                        estimate(user=users_map.get(user_data["email"]), ticket=new_ticket)
                    )
        
        estimate.objects.bulk_create(estimates_to_create)
        return pokerboard


class UserDashboardSerializer(serializers.ModelSerializer):
    PokerInfo = serializers.SerializerMethodField()
    TicketInfo = serializers.SerializerMethodField()
    GroupInfo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["PokerInfo", "TicketInfo", "GroupInfo"]

    def get_PokerInfo(self, obj):
        return PokerMemberSerializer(obj.poker_membership.all(), many=True).data

    def get_TicketInfo(self, obj):
        return EstimateSerializer(
            estimate.objects.select_related("ticket").filter(user_id=obj.id),
            many=True
        ).data

    def get_GroupInfo(self, obj):
        return GroupSerializer(obj.groups.all(), many=True).data


