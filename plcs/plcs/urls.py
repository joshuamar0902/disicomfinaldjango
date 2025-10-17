# mi_proyecto/urls.py
from django.contrib import admin
from django.urls import path, include # <-- Asegúrate de importar 'include'

urlpatterns = [
    path('chat/', include('chat.urls')), # <-- AÑADE ESTO
    path('admin/', admin.site.urls),
    
]