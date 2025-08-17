import random
import string
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
import random
from gamecreation.models import PokerBoard,pokermember

User = get_user_model()

# Helper to create random strings
def random_string(length=8):
    chars = string.ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))

# Create 20 users, 20 groups, and add all users to all groups
def func():
    users = []
    passwords = {}

    # Create 20 users
    for i in range(1, 21):
        username = f"user{i}"
        email = f"user{i}@example.com"
        password = 'somepass'
        passwords[username] = password  # store for reference

        user = User(username=username, email=email)
        user.set_password(password)  # hash before saving
        users.append(user)

    # Bulk insert users
    User.objects.bulk_create(users)

    # Reload from DB with IDs
    users = list(User.objects.filter(username__startswith="user"))

    # Create 20 groups with random names
    groups = []
    for i in range(1, 21):
        group_name = f"{random_string(5)}Group{i}"
        groups.append(Group(name=group_name))

    # Bulk insert groups
    Group.objects.bulk_create(groups)

    # Reload groups from DB with IDs
    groups = list(Group.objects.all())

    # Add all users to all groups
    for group in groups:
        group.user_set.add(*users)

    # Output
    print("✅ Created 20 users, 20 groups, and added all users to all groups.")
    print("\nGenerated Users and Passwords:")
    for username, password in passwords.items():
        print(f"{username} | {password}")

def createb():
    users = list(User.objects.filter(username__startswith="user")[:20])

    # Create 20 PokerBoards
    boards = []
    for i in range(1, 21):
        boards.append(
            PokerBoard(
                game_name=f"Poker Game {i}",
                game_description=f"Description for Poker Game {i}"
            )
        )
    PokerBoard.objects.bulk_create(boards)

    # Reload boards from DB with IDs
    boards = list(PokerBoard.objects.all())

    # Create pokermember entries
    memberships = []
    for board in boards:
        for user in users:
            memberships.append(
                pokermember(
                    poker=board,
                    member=user,
                    role=random.choice([0, 1, 2, 3])  # random role
                )
            )
    pokermember.objects.bulk_create(memberships)

    print(f"✅ Created {len(boards)} poker boards and added {len(memberships)} memberships.")\
    


from django.contrib.auth import get_user_model
from gamecreation.models import PokerBoard
from ticket.models import ticket, estimate
import random

User = get_user_model()

def fd():
    try:
        board = PokerBoard.objects.get(pokerid=7)
    except PokerBoard.DoesNotExist:
        print("❌ PokerBoard with ID 6 does not exist.")
        return

    # Create 30 tickets
    ticket_objs = []
    for i in range(1, 31):
        ticket_objs.append(
            ticket(
                pokerid=board,
                summary=f"Ticket {i+1}",
                description=f"Description for Ticket {i+1}",
                type=random.choice([0, 1, 2, 3, 4]),  # Random type
                Timer=random.randint(1, 60),
                finalEstimate=random.randint(1, 1000)
            )
        )
    ticket.objects.bulk_create(ticket_objs)
    print("✅ Created 30 tickets for PokerBoard 5.")

    # Reload tickets (to have IDs)
    all_tickets = list(ticket.objects.filter(pokerid=board).order_by("id")[:30])

    # Get User 5
    try:
        user6 = User.objects.get(username='user6')
    except User.DoesNotExist:
        print("❌ User with ID 5 does not exist.")
        return

    # Create estimates for first 15 tickets
    estimate_objs = []
    for t in all_tickets[:15]:
        estimate_objs.append(
            estimate(
                user=user6,
                ticket=t,
                estimate=random.randint(1, 60)  # Random estimate between 1 and 60
            )
        )
    estimate.objects.bulk_create(estimate_objs)
    print(f"✅ Added estimates for first 15 tickets for user {user6.username}.")

