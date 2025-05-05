from django.urls import path

from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('perfil/', perfil, name='perfil'),
    path('perfil/atualizar/', atualizar_perfil, name='atualizar_perfil'),
    path('regras/', regras, name='regras'),
    path('configuracao/', configuracao, name='configuracao'),
    path('termos/', termos, name='termos'),
    path('privacidade/', privacidade, name='privacidade'),
]
