from django.urls import path
from Invite.views import AcceptInvitationView

app_name = 'Invite'

urlpatterns = [
    path('accept/<pkuid>/', AcceptInvitationView.as_view(), name='invite'),
]
