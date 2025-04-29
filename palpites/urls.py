from django.urls import path

from .views import *

urlpatterns = [
    path('novo-palpites/', criar_palpites, name='criar_palpites'),
    path('meus-palpites/', meus_palpites, name='meus_palpites'),
]
