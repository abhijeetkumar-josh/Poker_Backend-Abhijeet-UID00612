from django.conf import settings
from django.db import models
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class PokerBoard(models.Model):   
    """
    Represents a PokerBoard game where users can be members with different roles.

    Fields:
        member (ManyToManyField): Users who are members of the board, through 'pokermember'.
        pokerid (AutoField): Primary key for the PokerBoard.
        game_name (CharField): Name of the game (minimum 3 characters).
        game_description (TextField): Description of the game (minimum 3 characters).
    """

    member = models.ManyToManyField(
        User,
        through='pokermember',
        related_name='poker'
    )
    pokerid = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=125,validators=[MinLengthValidator(1)])
    game_description=models.TextField(validators=[MaxLengthValidator(1000)])

    def __str__(self):
        return self.game_name

class pokermember(models.Model):
    """
    Represents the membership of a user in a PokerBoard with a specific role.

    Fields:
        poker (ForeignKey): The PokerBoard the member belongs to.
        member (ForeignKey): The user who is a member of the board.
        role (IntegerField): Role of the member (Spectator, Developer, Guest, Manager).
        accept (BooleanField): Whether the invitation to join is accepted.
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
    accept =models.BooleanField(default=False)


    class Meta:
        unique_together = ('poker', 'member')

    def __str__(self):
        return f"{self.member.email} in {self.poker.pokerid} (Accepted: {self.accept})"
    
