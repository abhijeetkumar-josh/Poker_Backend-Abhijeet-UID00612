from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()


class ApiKeys(models.Model):   
    """
    Represents an API key associated with a user for a specific cloud site.

    Fields:
        user (ForeignKey): The user to whom this API key belongs.
        apikey (CharField): The API key string (maximum length 256 characters).
        cloudsite (CharField): The cloud site this API key is for (maximum length 125 characters).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='key_membership')
    apikey=models.TextField(validators=[MinLengthValidator(20)])
    cloudsite=models.CharField(max_length=125,validators=[MinLengthValidator(10)])

    def __str__(self):
      return f"{self.user.email} - {self.cloudsite}"
