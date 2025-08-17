from django.conf import settings
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class PokerBoard(models.Model):   
    """
        
    """
    member = models.ManyToManyField(
        User,
        through='pokermember',
        related_name='poker'
    )
    pokerid = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=125,validators=[MinLengthValidator(3)])
    game_description=models.TextField(MinLengthValidator(3))

    def __str__(self):
        return self.game_name

class pokermember(models.Model):
    """
    Needed fields
    
    """
    ROLE_CHOICES = [
        [0, 'Spectator'],
        [1, 'Developer'],
        [2, 'Guest'],
        [3, 'Manager']
    ]
    poker = models.ForeignKey(PokerBoard, on_delete=models.CASCADE, related_name='pokerboard_membership')
    member = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='poker_membership')
    role=models.IntegerField(choices=ROLE_CHOICES,default=0)
    class Meta:
        unique_together = ('poker', 'member')

    def __str__(self):
        return f"{self.poker.pokerid} in {self.member.email}"
    
