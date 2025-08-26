from django.urls import path

from gamecreation.views import CreateGroupView,CreateGameView,ValidationView

app_name = 'profile'

urlpatterns = [
    path('group/', CreateGroupView.as_view(), name="creategroup"),
    path('game/', CreateGameView.as_view(), name="creategame"),
    path('validate/', ValidationView.as_view(), name="validation")
]
