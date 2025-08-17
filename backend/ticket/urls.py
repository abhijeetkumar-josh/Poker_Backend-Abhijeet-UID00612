from django.urls import path
from ticket.views import FilterTicketView

app_name = 'ticket'

urlpatterns = [
    path('filter/', FilterTicketView.as_view(), name="filter"),
]
