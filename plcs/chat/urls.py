# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/reajustar_int/', views.reajustar_valor_int_view, name='reajustar_valor_int'),
    
]
