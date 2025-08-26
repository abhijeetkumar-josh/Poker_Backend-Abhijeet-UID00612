# gamecreation/routing.py
from django.urls import re_path
from gamecreation.consumers import PokerWebsocket

websocket_urls = [
    re_path(r"ws/poker/(?P<pokerid>\d+)/$", PokerWebsocket.as_asgi()),
]

