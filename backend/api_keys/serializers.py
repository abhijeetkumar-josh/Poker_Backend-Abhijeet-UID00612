from rest_framework import serializers
from api_keys.models import ApiKeys
from django.contrib.auth import get_user_model
User = get_user_model()


class ApiKeySerializer(serializers.ModelSerializer):


    class Meta:
        model = ApiKeys
        fields = ["apikey", "cloudsite"]

    def create(self, validated_data):
        user = self.context.get("request").user
        return ApiKeys.objects.create(user=user, **validated_data)

