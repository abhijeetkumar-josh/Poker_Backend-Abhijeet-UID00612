from user.serializers import UserSerializer
from rest_framework import serializers
from gamecreation.models import pokermember


class PokerMemberSerializer(serializers.ModelSerializer):
    member = UserSerializer(read_only=True)

    class Meta:
        model = pokermember
        fields = ['id', 'role', 'member', 'poker']
        depth=1
