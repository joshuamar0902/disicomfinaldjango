# chat/plc_thread.py
import time
import snap7
import struct
from snap7.util import get_bool
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# --- Configuración del PLC ---
PLC_IP = "192.168.0.120"
RACK = 0
SLOT = 1
DB_NUMERO = 3
DIRECCION_INICIO = 0
TAMAÑO_A_LEER = 10

def read_plc_data_continuously():
    """
    Bucle infinito que lee datos del PLC y los envía al Channel Layer.
    Esta es la función que correrá en nuestro hilo.
    """
    channel_layer = get_channel_layer()
    client = snap7.client.Client()

    while True:
        try:
            if not client.get_connected():
                client.connect(PLC_IP, RACK, SLOT)

            raw_data = client.db_read(DB_NUMERO, DIRECCION_INICIO, TAMAÑO_A_LEER)
            valor_booleano = get_bool(raw_data, 0, 0)
            valor_int_1, valor_real, valor_int_2 = struct.unpack('>hfh', raw_data[2:10])

            current_values = {
                "Bit_1": valor_booleano,
                "Valor_int": valor_int_1,
                "Valor_float": round(valor_real, 2),
                "Contador": valor_int_2
            }

            print(f"Datos leídos (desde hilo): {current_values}")

            async_to_sync(channel_layer.group_send)(
                'plc_data',
                {
                    'type': 'plc.data.update',
                    'data': current_values,
                }
            )

        except Exception as e:
            print(f"!!! EXCEPCIÓN EN HILO PLC: {e} !!!")
            client.disconnect()
            time.sleep(5)

        time.sleep(1)