# chat/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt 

# Importa la función que creaste para escribir en el PLC
from .plc_thread import write_plc_int_value 


# 1. Vista principal (Se mantiene igual)
def index(request):
    return render(request, 'chat/chat.html')


# 2. Nueva Vista para Reajustar Valor INT
@csrf_exempt # Desactiva la protección CSRF (Solo para desarrollo rápido)
@require_http_methods(["POST"])
def reajustar_valor_int_view(request):
    """
    Recibe la señal del botón y escribe un valor alto (30000)
    en la dirección de la variable Valor_int en el PLC.
    """
    
    # Define un valor positivo alto para sacar al manómetro del rango negativo
    VALOR_ALTO_INICIAL = 30000 
    
    success = write_plc_int_value(VALOR_ALTO_INICIAL)
    
    if success:
        # Respuesta de éxito que el JavaScript espera
        return JsonResponse({'success': True, 'message': f'Valor INT reajustado a {VALOR_ALTO_INICIAL}.'})
    else:
        # Respuesta de error si falló la conexión o la escritura
        return JsonResponse({'success': False, 'error': 'Fallo al escribir en PLC.'}, status=500)