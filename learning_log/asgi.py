import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import broadcast.routing  # import my app’s routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dropbear.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),             # standard Django views
    "websocket": AuthMiddlewareStack(           # WebSocket connections
        URLRouter(
            broadcast.routing.websocket_urlpatterns
        )
    ),
})
