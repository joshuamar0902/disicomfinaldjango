# chat/apps.py

from django.apps import AppConfig
import os # <-- Importante
import threading
from . import plc_thread

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        # Esta comprobación evita que el código se ejecute dos veces
        if os.environ.get('RUN_MAIN') == 'true':
            print("Iniciando hilo de lectura del PLC...")
            thread = threading.Thread(target=plc_thread.read_plc_data_continuously)
            thread.daemon = True
            thread.start()
            print("Hilo del PLC iniciado.")