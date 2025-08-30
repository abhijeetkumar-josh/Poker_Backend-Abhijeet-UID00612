import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poker.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import gamecreation.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poker.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(gamecreation.routing.websocket_urls)
    ),
})

