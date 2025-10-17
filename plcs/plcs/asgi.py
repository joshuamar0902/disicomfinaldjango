# plcs/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing
import threading
from django.core.asgi import get_asgi_application
from chat.plc_thread import read_plc_data_continuously

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plcs.settings')

application = get_asgi_application()

# Iniciar el hilo del PLC
threading.Thread(target=read_plc_data_continuously, daemon=True).start()


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})