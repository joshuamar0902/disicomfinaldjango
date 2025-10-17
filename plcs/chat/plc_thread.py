# chat/plc_thread.py
import time
import snap7
import struct
from snap7.util import get_bool
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random 

# --- Configuración del PLC ---
PLC_IP = "192.168.0.120"
RACK = 0
SLOT = 1
DB_NUMERO = 3
DIRECCION_INICIO = 0
TAMAÑO_A_LEER = 10

def write_plc_int_value(new_value):
    """
    Fuerza el valor de Valor_int a un nivel visible.
    """
    client = snap7.client.Client()
    try:
        client.connect(PLC_IP, RACK, SLOT)
        
        data_to_write = struct.pack('<h', new_value) 
        
        client.db_write(DB_NUMERO, DIRECCION_INICIO, data_to_write)

        time.sleep(0.5) 
        
        print(f"VALOR INT reajustado a {new_value}.")
        return True
    except Exception as e:
        print(f"!!! ERROR AL ESCRIBIR EN PLC: {e} !!!")
        return False
    finally:
        if client.get_connected():
            client.disconnect()


def read_plc_data_continuously():
    """
    Bucle infinito que lee datos del PLC y los envía al Channel Layer.
    """
    channel_layer = get_channel_layer()
    client = snap7.client.Client()

    current_demo_value = 50.0 

    while True:
        try:
            if not client.get_connected():
                client.connect(PLC_IP, RACK, SLOT)

            raw_data = client.db_read(DB_NUMERO, DIRECCION_INICIO, TAMAÑO_A_LEER)
            valor_booleano = get_bool(raw_data, 0, 0)
            

            valor_int_1 = snap7.util.get_uint(raw_data, 2)
            valor_real = snap7.util.get_real(raw_data, 4)
            valor_int_2 = snap7.util.get_int(raw_data, 8)
            
            
            change = random.uniform(-2.0, 2.0)
            current_demo_value += change
            
            # Limita el valor entre 0 y 100
            current_demo_value = max(0, min(100, current_demo_value))
            
            valor_demo_simulado = round(current_demo_value, 2)
            # -----------------------------------------------

            current_values = {
                "Bit_1": valor_booleano,
                "Valor_int": valor_int_1,
                "Valor_float": round(valor_real, 2),
                "Contador": valor_int_2,
                "Valor_Demo": valor_demo_simulado, # 🚨 VARIABLE AÑADIDA
            }

            print(f"Datos leídos (con demo): {current_values}")

            async_to_sync(channel_layer.group_send)(
                'plc_data',
                {
                    'type': 'plc_data_update',
                    'data': current_values,
                }
            )

        except Exception as e:
            print(f"!!! EXCEPCIÓN EN HILO PLC: {e} !!!")
            client.disconnect()
            time.sleep(5)

        time.sleep(.2) # Cambiado a 0.2 para un dashboard más rápido

