import json
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import serializers

from rest_framework.authtoken.models import Token
from user.serializers import GroupSerializer
from gamecreation.serializers import PokerMemberSerializer
from ticket.models  import estimate,ticket
from ticket.serializers import estimateSerializer,ticketSerializer
from .serializers import RegisterSerializer
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate,login
from django.contrib.auth import get_user_model
from gamecreation.models import pokermember
from channels.routing import URLRouter
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from .models import SignUpInfo
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from .models import SignUpInfo, CustomUser
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

def send_verification_email(user, request):
    token = user.token
    PATH = "192.168.2.223:5177"
    verify_url = f"http://{PATH}/verified/{token}/"
    
    send_mail(
      subject="Verify your email",
      message=f"Click the link to verify your account: {verify_url}",
      from_email=os.environ.get('EMAIL_USER'),
      recipient_list=[user.email],
      fail_silently=False,
    )
  

class VerifyEmailView(APIView):
    permission_classes=[AllowAny]
    def get(self,request,token):
        signup = get_object_or_404(SignUpInfo, token=token)
    
        if not signup.is_token_valid():
            return Response({"error": "Token expired, Please Signup again!"}, status=status.HTTP_400_BAD_REQUEST)
    
        user = CustomUser.objects.create_user(
            email=signup.email,
            username=signup.username,
            password=signup.password 
        )
    
        signup.delete()
    
        token, created = Token.objects.get_or_create(user=user)
        users=PokerMemberSerializer(user.poker_membership.all(),many=True)
        tickets=estimateSerializer(estimate.objects.select_related('ticket').filter(user_id=user.id),many=True)
        GroupInfo=GroupSerializer(user.groups.all(),many=True)
        userdata={'PokerInfo':users.data,'TicketInfo':tickets.data,'GroupInfo':GroupInfo.data,'token':token.key}
        return Response(userdata, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if not username or not email or not password or not confirm_password:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"error": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                signup_user = SignUpInfo.objects.create(
                    username=username,
                    email=email,
                    password=make_password(password)
                )
                send_verification_email(signup_user, request)
            return Response({"message": "Signup successfull. Please verify your email."}, status=status.HTTP_201_CREATED)


        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email= request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)

        if user is not None:
            find = User.objects.get(email=user)
            print(user.username, user.id)
            token, created = Token.objects.get_or_create(user=find)
            users=PokerMemberSerializer(user.poker_membership.all(),many=True)
            tickets=estimateSerializer(estimate.objects.select_related('ticket').filter(user_id=find.id),many=True)
            GroupInfo=GroupSerializer(user.groups.all(),many=True)
            userdata={'PokerInfo':users.data,'TicketInfo':tickets.data,'GroupInfo':GroupInfo.data,'token':token.key}
            return Response(userdata, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        email = request.GET.get('email')
        print(email)
        try:
           user = User.objects.get(email=email)
           return Response({'username':user.username,'email':email,'id':user.id},status=status.HTTP_200_OK )
        except User.DoesNotExist :
            return Response({'username':'not_found','email':'not_registered'},status=status.HTTP_404_NOT_FOUND)


class EditView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        find = User.objects.get(email=request.data.email)
        if(find.firstname):
            find.firstname = request.data.firstname
        if(find.lastname) :
            find.lastname = request.data.lastname
        if(find.dob) :
            find.dob = request.data.dob
        find.save()
        return Response({'Profile Updated successfully'}, status=status.HTTP_204_NO_CONTENT)
    

