from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from ticket.serializers import ticketSerializer
import json
from django.contrib.auth import get_user_model

from ticket.models  import ticket,estimate
from ticket.serializers import estimateSerializer

from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class FilterTicketView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        print(request.user)
        ticket_type = request.data.get('filterType')
        estimate_date = request.data.get('estimateDate') 

        queryset = estimate.objects.select_related('ticket').filter(
            user_id=request.user.id
        )
        
        if ticket_type and estimate_date :
            queryset = queryset.filter(ticket__type=ticket_type, estimate_date=estimate_date)
        elif ticket_type:
            queryset = queryset.filter(ticket__type=ticket_type)
        if estimate_date:
            queryset = queryset.filter(estimate_date=estimate_date)

        tickets = estimateSerializer(queryset, many=True)
        return Response(tickets.data, status=status.HTTP_200_OK)
