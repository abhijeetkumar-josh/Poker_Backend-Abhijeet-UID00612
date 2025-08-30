from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login
from rest_framework.permissions import AllowAny,IsAuthenticated
from api_keys.serializers import ApiKeySerializer
from django.contrib.auth import get_user_model
import json
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PokerBoardSerializer,UserDashboardSerializer
from rest_framework import generics,status
from utils.utils import JiraValidation

User = get_user_model()
maxResults=100

        
class CreateGroupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
       return Response(json.dumps(request.data),status=status.HTTP_201_CREATED)


class ValidationView(JiraValidation,generics.GenericAPIView):
    serializer_class = ApiKeySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        site = validated_data["cloudsite"]
        token = validated_data["apikey"]

        data, code = self.validate_and_store_api(token, site, request.user, save=False)
        return Response(data, status=code)


class CreateGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PokerBoardSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            board = serializer.save() 
            return Response({"message": "Game Created Successfully", "pokerid": board.pokerid}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserDashboardSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

