from django.db import models
from django.contrib.auth import get_user_model
from gamecreation.models import PokerBoard
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, MaxLengthValidator

User = get_user_model()

class ticket(models.Model):   
    """
      ticket
    """
    TICKET_CHOICES = [
        [0,'task'],
        [1,'bug'],
        [2,'epic'],
        [3,'story'],
        [4,'subtask']
    ]
    pokerid = models.ForeignKey(PokerBoard, on_delete=models.CASCADE, related_name='ticket_membership')
    summary=models.CharField(max_length=125,blank=False, null=False)
    description=models.TextField(validators=[MaxLengthValidator(1000)])
    type=models.CharField(choices=TICKET_CHOICES, default=0)
    Timer=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(60)])
    finalEstimate=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])

    def __str__(self):
        return self.user.ticket_summary
    
class estimate(models.Model):   
    """
      estimate
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estimate_membership')
    ticket = models.ForeignKey(ticket, on_delete=models.CASCADE, related_name='ticket_ref')
    estimate = models.IntegerField(blank=False,null=True,validators=[MinValueValidator(1),MaxValueValidator(60)])
    estimate_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.ticket.summary
