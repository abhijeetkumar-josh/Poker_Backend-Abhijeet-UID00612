from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
import uuid
import random
from datetime import timedelta

class UserManager(BaseUserManager):
    """
    Add manager methods here to create user and super user
    """
    def create_user(self,username,email,password,**extra_fields):
        if not email:
            raise ValueError("Please Enter a valid email")
        email=self.normalize_email(email)
        user=self.model(username=username , email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username, email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(username,email,password,**extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Needed fields
    - password (already inherited from AbstractBaseUser; encrypt password before saving to database)
    - last_login (already inherited from AbstractBaseUser)
    - is_superuser
    - first_name (max_length=30)
    - email (should be unique)
    - is_staff
    - date_joined (default should be time of object creation)
    - last_name (max_length=150)
    """
    username=models.CharField(max_length=125,unique=True,blank=False,null=False)
    email = models.EmailField(unique=True, blank=False, null= False)
    firstname = models.CharField(max_length=125, blank=True, null= True)
    lastname = models.CharField(max_length=125, blank=True, null= True)
    dob = models.DateField(blank=True, null= True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, null=True, blank=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    EMAIL_FIELD='email'
    
    objects = UserManager()

    def __str__(self):
        return self.email
    
class SignUpInfo(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=125)
    password = models.CharField(max_length=255)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    token_created_at = models.DateTimeField(auto_now_add=True)

    def is_token_valid(self, expiry_hours=24):
        expiry_time = self.token_created_at + timedelta(hours=expiry_hours)
        return timezone.now() <= expiry_time


    def __str__(self):
        return f"Signup pending for {self.email}"
