from django.urls import path

from .views import *

urlpatterns = [
    path('novo-palpites/', criar_palpites, name='criar_palpites'),
    path('meus-palpites/', meus_palpites, name='meus_palpites'),
    path('filtrar-palpites/', filtrar_palpites, name='filtrar_palpites'),
    path('editar-palpite/<int:palpite_id>/', editar_palpite, name='editar_palpite'),
]
