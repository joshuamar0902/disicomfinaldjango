# mi_proyecto/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plcs.settings')

# Esta es la parte importante
application = ProtocolTypeRouter({
    # Maneja las peticiones HTTP normales con Django
    "http": get_asgi_application(),

    # Maneja las conexiones WebSocket con nuestro enrutador de Channels
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})