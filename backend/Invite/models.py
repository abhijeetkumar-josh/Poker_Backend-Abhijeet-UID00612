from django.conf import settings
from django.db import models
from gamecreation.models import PokerBoard


class Invite(models.Model):   
    """
       
    """
    ROLE_CHOICES = [
        [0, 'Spectator'],
        [1, 'Developer'],
        [2, 'Guest'],
        [3, 'Manager']
    ]

    pokerboard = models.ForeignKey(
        PokerBoard,
        on_delete=models.CASCADE,
        related_name='invite'
    )
    host=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='host')
    guest=models.EmailField(blank=False,null=False)
    accept = models.BooleanField(default=False)
    role=models.IntegerField(choices=ROLE_CHOICES,default=0)

    class Meta:
        db_table = "invite_invite"

    def __str__(self):
        return f"{self.host.email} invited by {self.guest}"
