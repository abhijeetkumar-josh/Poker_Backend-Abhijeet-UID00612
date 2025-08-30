import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer,LoginSerializer,UserSearchInputSerializer,UserSerializer
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import SignUpInfo
from django.shortcuts import get_object_or_404
from .models import SignUpInfo, CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins

from utils.utils import decrypt_message


User = get_user_model()
PATH = "192.168.2.223:5177"


def get_public_key(request):
    with open("public.pem") as f:
        return JsonResponse({"public_key": f.read()})


def send_verification_email(user, request):

    verify_url = f"http://{PATH}/verified/{user.token}/"
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
            signup.delete()
            return Response({"error": "Token expired, Please Signup again!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.create_user(
                email=signup.email,
                username=signup.username,
            )
            user.password = signup.password 
            signup.delete()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key,'username':user.username,'email':user.email}, status=status.HTTP_200_OK)
        
        except IntegrityError as e:
            Response({"User with this username or email already exists"},status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        credentials = request.data.get("credentials")
        if not credentials:
            return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decrypted = decrypt_message(credentials)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=decrypted)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        credentials = request.data.get("credentials") 
        

        if not credentials:
            return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decrypted = decrypt_message(credentials)
            print(decrypted)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoginSerializer(data=decrypted)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


class UserSearchView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        email = self.request.GET.get("email")
        if not email:
            raise ValidationError({"email": "This query param is required."})
        
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound({"username": "not_found", "email": "not_registered"})

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


