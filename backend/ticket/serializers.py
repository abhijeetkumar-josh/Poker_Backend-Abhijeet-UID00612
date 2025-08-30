from rest_framework import serializers
from ticket.models import ticket,estimate


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = ticket
        fields = ['id','key','summary','description','type','pokerid','priority']

class TicketTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ticket
        fields = ['import_type']


class EstimateSerializer(serializers.ModelSerializer):

    ticket = TicketSerializer(read_only=True)
    class Meta:
        model = estimate
        fields = ['estimate','ticket']


class TicketFilterSerializer(serializers.Serializer):

    filterType = serializers.ChoiceField(
        choices=[str(choice[0]) for choice in ticket.TICKET_CHOICES],
        required=False,
        allow_blank=True
    )
    estimateDate = serializers.DateField(required=False,allow_null=True)

