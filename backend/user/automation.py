# from your_app.models import Ticket  # replace with your actual app/model import
from ticket.models import ticket
from gamecreation.models import PokerBoard
from django.contrib.auth import get_user_model
User=get_user_model()
from ticket.models import estimate
def fd():
    # Ticket details
    key = "SAMPLE-KEY"
    board = 3  # pokerid
    priority = "Medium"
    summary = "Sample Summary"
    description = "Sample Description"
    ticket_key = "TICKET-123"
    
    # Generate emails user6@example.com to user20@example.com
    emails = [f"user{i}@example.com" for i in range(6, 21)]
    # Loop through emails and create tickets
    pokerid=PokerBoard.objects.filter(pokerid=2).first()
    new_tickets = []
    for i in range (11,20):
        key = "SAMPLE-KEY-{i}"
        board = 3  # pokerid
        priority = "Medium"
        summary = "Sample Summary-{i}"
        description = "Sample Description-{1}"
        ticket_key = "TICKET-{i}"
        for email in emails:
            user=User.objects.filter(email=email).first()
            new_ticket = ticket.objects.create(
                key=key,
                pokerid=pokerid,
                priority=priority,
                summary=summary,
                description=description,
                import_type="ticketId",
                ticket=ticket_key,
            )
            estimate.objects.create(
                ticket=new_ticket,
                user=user
            )
            new_tickets.append(new_ticket)
    
    
    print(f"Created {len(new_tickets)} tickets successfully!")
