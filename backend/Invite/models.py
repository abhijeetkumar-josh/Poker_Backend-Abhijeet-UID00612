from django.conf import settings
from django.db import models
from gamecreation.models import PokerBoard


class Invite(models.Model):   
    """
       
    """
    pokerboard = models.ForeignKey(
        PokerBoard,
        on_delete=models.CASCADE,
        related_name='invite'
    )
    host=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='host')
    guest=models.EmailField(blank=False,null=False)
    accept = models.BooleanField(default=False)

    def __str__(self):
        return self.name
