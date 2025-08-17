from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ticket.models import ticket,estimate

class ticketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ticket
        fields = ['summary','description','type']
        depth=1

class estimateSerializer(serializers.ModelSerializer):
    ticket = ticketSerializer(read_only=True)
    class Meta:
        model = estimate
        fields = ['estimate','ticket']
