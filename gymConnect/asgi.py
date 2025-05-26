import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

from course.routing import websocket_urlpatterns as course_ws
from network.routing import websocket_urlpatterns as network_ws

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gymConnect.settings")
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            course_ws + network_ws 
        )
    ),
})
