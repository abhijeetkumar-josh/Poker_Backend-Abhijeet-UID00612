from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from api_keys.models import ApiKeys
from gamecreation.models import PokerBoard,pokermember
from django.contrib.auth import get_user_model
import json
import requests

User = get_user_model()

# {'email': 'amrish@gmail.com', 'gameName': 'new game', 'gameDescription': 'some dedopvd',
#   'site': 'dvndkfnifborvb', 'apiToken': 'sldmvkndkvnefiv', 'importType': 'tickets',
#     'importValue': 'sdlvmvninvi', 'users': ['dvmdfnvidnifvd', 'dvpndivudb'],
#       'group': {'name': 'dvnkdnfvid', 'users': ['sdlvnkdn', 'sd;lnnvid', 'a;ldvnikdnvi']},
#         'creating': True, 'error': ''}
class CreateGameView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user=User.objects.get(email='amrish@gmail.com')
        ApiKeys.objects.create(user=user,apikey=request.data['apiToken'],cloudsite=request.data['site'])
        board=PokerBoard.objects.create(game_name=request.data['gameName'],game_description=request.data['gameDescription'])
        # for i in range(0,len(request.data.users)):
            
        pokermember.objects.create(poker=board, member=user)
        return Response({'Game Created Successfully'},status.HTTP_201_CREATED)
        

class CreateGroupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
       print(request.data)
       print('hello')
       print(request.user)
       return Response(json.dumps(request.data),status=status.HTTP_201_CREATED)
