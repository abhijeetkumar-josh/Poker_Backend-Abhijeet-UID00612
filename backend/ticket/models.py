from django.db import models
from django.contrib.auth import get_user_model
from gamecreation.models import PokerBoard
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, MaxLengthValidator

User = get_user_model()

class ticket(models.Model):   
    """
    Represents a task or issue in a PokerBoard.

    Fields:
        pokerid (ForeignKey): The PokerBoard this ticket belongs to.
        key (CharField): Unique key of the ticket
        priority (CharField): Priority level of the ticket 
        summary (CharField): Short description of the ticket.
        description (TextField): Detailed description (max 1000 chars).
        type (IntegerField): Type of ticket (task, bug, epic, story, subtask).
        import_type (IntegerField): Source of ticket import (ticketId, sprintId, jql).
        ticket (CharField): Optional external ticket identifier.
        finalEstimate (IntegerField): Optional final estimate (1-1000).
    """
    TICKET_CHOICES = [
        [0,'task'],
        [1,'bug'],
        [2,'epic'],
        [3,'story'],
        [4,'subtask']
    ]
    IMPORT_CHOICES = [
        [0,'ticketId'],
        [1,'sprintId'],
        [2,'jql'],
    ]
    pokerid = models.ForeignKey(PokerBoard, on_delete=models.CASCADE, related_name='ticket_membership')
    key=models.CharField(max_length=125,default='SPP-1')
    priority=models.CharField(max_length=125,default='Medium')
    summary=models.CharField(max_length=125, blank=False, null=False)
    description=models.TextField(validators=[MaxLengthValidator(1000)])
    type=models.CharField(choices=TICKET_CHOICES, default=0)
    Timer=models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(60)])
    import_type = models.CharField(choices=IMPORT_CHOICES, default=0)
    ticket = models.CharField(max_length=125,blank=True,null=True)
    finalEstimate=models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(1000)])

    def __str__(self):
        return self.summary
    
class estimate(models.Model):   
    """
    Represents an estimate provided by a user for a ticket.

    Fields:
        user (ForeignKey): The user providing the estimate.
        ticket (ForeignKey): The ticket being estimated.
        estimate (IntegerField): The estimate value in minutes (1-60, optional).
        estimate_date (DateField): Date of the estimate (optional).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estimate_membership')
    ticket = models.ForeignKey(ticket, on_delete=models.CASCADE, related_name='ticket_ref')
    estimate = models.IntegerField(blank=True,null=True,validators=[MinValueValidator(1),MaxValueValidator(60)])
    estimate_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.ticket.summary
