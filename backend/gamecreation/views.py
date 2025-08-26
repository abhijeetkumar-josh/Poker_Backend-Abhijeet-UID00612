from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from api_keys.models import ApiKeys
from Invite.models import Invite
from ticket.models import ticket,estimate
from gamecreation.models import PokerBoard,pokermember
from django.contrib.auth import get_user_model
import json
import os
import math
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth

User = get_user_model()

maxResults=100

# {'email': '', 'gameName': 'odisnvisdb', 'gameDescription': 'sdoivnds', 'site': 'abhijeetkumarjosh7985.atlassian.net',
#   'apiToken': 'ATATT3xFfGF0X7JtPT0xQpTPqZI9jPDyNBhKl5uM0u5mbM3imx8wFrj9qQAoAnlawjQ_cTsVooNMCWjJ5jTvwuuGt--qei6--pZ9oQNehAYV5flZJj50Z4_lY5pEWYbNMrIrYbcI3nidzo-'
#   'tmFnjAIsNEoPkIvXY1BDCLrlASO33XwkiNGCkk74=D9D5BFA1', 'importType': '', 'importValue': '', 'users': [{'invite': True, 'email': 'sdvisdv', 'role': 0}, 
# {'invite': True, 'email': 'sscjdbvj', 'role': 0}], 'group': {'name': '', 'users': []}, 'creating': True, 'error': '', 'tickets': ['KAN-1', 'KAN-2']}


class CreateGameView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email='abhijeet.kumar.josh.7985@gmail.com'
        token=request.data.get('apiToken')
        site=request.data.get('site')
        user=request.user
        importType=request.data.get('importType')
        importValue=request.data.get('importValue')
        api=ApiKeys.objects.create(user=user,apikey=request.data['apiToken'],cloudsite=request.data['site'])
        board=PokerBoard.objects.create(game_name=request.data['gameName'],game_description=request.data['gameDescription'])   
        pokermember.objects.create(poker=board, member=user, role=3)
        for userinfo in request.data.get('users'):
            if (not userinfo.get('invite')):
                pokermember.objects.create(poker=board, member_id=userinfo.get('id'), role=userinfo.get('role'))
            else :
                Invite.objects.create(pokerboard=board,host=user,guest=userinfo.get('email'),accept=False,role=userinfo.get('role'))
        
        if(importType=='tickets'):
            for Ticket in request.data.get('tickets'):
                url = f"https://{site}/rest/api/3/search"
                try:
                    response1 = requests.get(
                       url,
                       auth=HTTPBasicAuth(email, token),
                       headers={"Accept": "application/json"},
                       params={"jql": 'ORDER BY created DESC', "maxResults": 0}  
                    )
                    total = response1.json()['total']
                    data= []
                    for i in range(0,math.ceil(total/maxResults)):
                        response2 = requests.get(
                           url,
                           auth=HTTPBasicAuth(email, token),
                           headers={"Accept": "application/json"},
                           params={"jql": 'ORDER BY created DESC', "maxResults": maxResults}  
                        )
                        data.extend(response2.json()['issues'])
                    
                    tracking_set = set(request.data.get('tickets',[]))
                    for jira_data in data :
                        ticket_key = jira_data['key']
                        if(ticket_key in tracking_set) :
                            tracking_set.discard(ticket_key)

                    if(len(tracking_set)!=0):
                        return Response({
                            'failed_tickets':tracking_set,
                        }, status=status.HTTP_400_BAD_REQUEST)
  
                    tickets_set = set(request.data.get('tickets',[]))
                    for jira_data in data :
                        ticket_key = jira_data['key']
                        if(ticket_key in tickets_set) :
                            tickets_set.discard(ticket_key)
                            key=jira_data["key"]
                            priority=jira_data["fields"]["priority"]["name"]
                            summary = jira_data["fields"]["summary"]
                            description = jira_data["fields"]["description"]["content"][0]["content"][0]["text"]
                            issue_type = jira_data["fields"]["issuetype"]["name"]          
                            
                            new_ticket = ticket.objects.create(
                                key=key,
                                pokerid=board,
                                priority=priority,
                                summary=summary,
                                description=description,
                                import_type="ticketId",
                                ticket=ticket_key
                            )
                            for userinfo in request.data.get('users',[]):
                                if(not userinfo.get('invite')) :
                                    estimate.objects.create(
                                        user_id=userinfo.get('id'),
                                        ticket=new_ticket,
                                    )
                    if(len(tickets_set)!=0):
                        return Response({
                            'failed_tickets':tickets_set,
                            'pokerid':board.pokerid
                        }, status=status.HTTP_201_CREATED)
                except requests.RequestException as e:
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                

        if(importType=='sprintId'):
            url = f"https://{site}/rest/agile/1.0/sprint/{importValue}/issue"
            try:
                response = requests.get(
                    url,
                    auth=HTTPBasicAuth(email, token),
                    headers={"Accept": "application/json"}
                )
                data=response.json()
                issues_list = data['issues']
                
                for jira_data in issues_list :
                        ticket_key = jira_data['key']
                        priority=jira_data["fields"]["priority"]["name"]
                        summary = jira_data["fields"]["summary"]
                        description = jira_data["fields"]["description"]["content"][0]["content"][0]["text"]
                        issue_type = jira_data["fields"]["issuetype"]["name"]   
                        new_ticket = ticket.objects.create(
                            key=key,
                            priority=priority,
                            pokerid=board,
                            summary=summary,
                            description=description,
                            import_type="ticketId",
                            ticket=ticket_key
                        )
                        for userinfo in request.data.get('users',[]):
                            if(not userinfo.get('invite')) :
                                estimate.objects.create(
                                    user_id=userinfo.get('id'),
                                    ticket=new_ticket,
                                )
                # return Response(response, status=response.status_code)
            except requests.RequestException as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if(importType=='jql'):
            url = f"https://{site}/rest/api/3/search"
            try:
                response = requests.get(
                    url,
                    auth=HTTPBasicAuth(email, token),
                    headers={"Accept": "application/json"},
                    params={"jql": importValue, "maxResults": 100}  
                )
    
                data=response.json()
                issues_list = data['issues']
                for jira_data in issues_list :
                    ticket_key=jira_data["key"]
                    summary = jira_data["fields"]["summary"]
                    priority=jira_data["fields"]["priority"]["name"]
                    description = jira_data["fields"]["description"]["content"][0]["content"][0]["text"]
                    issue_type = jira_data["fields"]["issuetype"]["name"] 
                    ticket_key = jira_data["key"]  

                    new_ticket = ticket.objects.create(
                        key=key,
                        pokerid=board,
                        priority=priority,
                        summary=summary,
                        description=description,
                        import_type="ticketId",
                        ticket=ticket_key
                    )
                    for userinfo in request.data.get('users',[]):
                        if(not userinfo.get('invite')) :
                            estimate.objects.create(
                                user_id=userinfo.get('id'),
                                ticket=new_ticket,
                            ) 
    
                
            except requests.RequestException as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response({'Game Created Successfully'},status.HTTP_201_CREATED)
        
class CreateGroupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
       return Response(json.dumps(request.data),status=status.HTTP_201_CREATED)

class ValidationView(APIView):
    permission_classes = [AllowAny]
    def post(self , request):
        type = request.data.get('type') or ''
        site = request.data.get('site') or ''
        email = request.data.get('email') or ''
        token = request.data.get('token') or ''
        ticket = request.data.get('ticket') or ''
        if(type=='validate'):
            url = f"https://{site}/rest/api/3/myself"
            try:
                response = requests.get(
                    url,
                    auth=HTTPBasicAuth(email, token),
                    headers={"Accept": "application/json"}
                )
                try:
                    data = response.json()
                except ValueError:
                    data = {"raw_text": response.text} 
                
                return Response(data, status=response.status_code)
            
            except requests.RequestException as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        elif(type=='ticket'):
            url = f"https://{site}/rest/api/3/issue/{ticket}"
            try:
                response = requests.get(
                    url,
                    auth=HTTPBasicAuth(email, token),
                    headers={"Accept": "application/json"}
                )
                return Response(response, status=response.status_code)
            
            except requests.RequestException as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else :
            return Response({'error':'Not a valid request'},status=status.HTTP_400_BAD_REQUEST)


