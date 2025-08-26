from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()


class ApiKeys(models.Model):   
    """
      user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='key_membership')
    apikey=models.TextField(validators=[MinLengthValidator(20)])
    cloudsite=models.CharField(max_length=125,validators=[MinLengthValidator(10)])

    def __str__(self):
        return self.user.email

