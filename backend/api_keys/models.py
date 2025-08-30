from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator,MaxLengthValidator
from gamecreation.models import PokerBoard

User = get_user_model()


class ApiKeys(models.Model):   
    """
    Represents an API key associated with a user for a specific cloud site.

    Fields:
        user (ForeignKey): The user to whom this API key belongs.
        apikey (CharField): The API key string (maximum length 256 characters).
        cloudsite (CharField): The cloud site this API key is for (maximum length 125 characters).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userkey_membership')
    apikey = models.CharField(max_length=256,blank=False,null=False)
    cloudsite = models.CharField(max_length=125,blank=False,null=False)
    # pokerid = models.ForeignKey(PokerBoard, on_delete=models.CASCADE, related_name="pokerkey_membership")

    def __str__(self):
        return f"{self.user.email} - {self.cloudsite}"

