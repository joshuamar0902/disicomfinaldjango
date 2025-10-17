# chat/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Aseguramos que la URL sea la que usa el JavaScript
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]