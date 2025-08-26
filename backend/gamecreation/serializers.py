from user.serializers import UserSerializer
from rest_framework import serializers
from gamecreation.models import pokermember,PokerBoard


class PokerMemberSerializer(serializers.ModelSerializer):
    # manager = serializers.SerializerMethodField()
    class Meta:
        model = pokermember
        fields = ['id', 'role', 'poker','accept']
        depth=2
    
    # def get_manager(self,obj) :
    #     poker = PokerBoard.objects.(poker)

