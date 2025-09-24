# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)('plc_data', self.channel_name)
        self.accept()
        print("Cliente WebSocket conectado y unido al grupo 'plc_data'")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)('plc_data', self.channel_name)
        print("Cliente WebSocket desconectado")

    # Este método se llama cuando recibimos un mensaje del hilo del PLC
    def plc_data_update(self, event):
        plc_data = event['data'] # Obtenemos el diccionario completo

        # Enviamos el diccionario al cliente WebSocket
        self.send(text_data=json.dumps({
            'type': 'plc_update',
            'data': plc_data
        }))