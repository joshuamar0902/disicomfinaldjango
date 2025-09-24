# chat/apps.py

from django.apps import AppConfig
import threading
# Ya no necesitamos 'os'

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        print("Método ready() de AppConfig ejecutado.") # Mensaje de diagnóstico

        # Eliminamos la condición 'if' y ejecutamos el código directamente
        from . import plc_thread
        
        print("Iniciando hilo de lectura del PLC...")
        plc_thread_instance = threading.Thread(target=plc_thread.read_plc_data_continuously, daemon=True)
        plc_thread_instance.start()
        print("Hilo del PLC iniciado.")