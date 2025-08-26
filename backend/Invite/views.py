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


class AcceptInvitationView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pkuid):
        try:
           poker=pokermember.objects.get(id=pkuid)
        except pokermember.DoesNotExist:
           return Response('Wrong Invitation',status=status.HTTP_400_BAD_REQUEST)
        print(poker)
        poker.accept=True
        poker.save()
        return Response('Invitation Accepted',status=status.HTTP_200_OK)

        
