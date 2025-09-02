from user.serializers import UserSerializer
from rest_framework import serializers
from gamecreation.models import pokermember,PokerBoard


class PokerMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = pokermember
        fields = ['id', 'role', 'poker','accept']
        depth=1
