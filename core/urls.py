from django.urls import path

from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('perfil/', perfil, name='perfil'),
    path('perfil/atualizar/', atualizar_perfil, name='atualizar_perfil'),
    path('regras/', regras, name='regras'),
    path('manutencao/', manutencao, name='manutencao'),


    #configurações
    path('configuracao/', configuracao, name='configuracao'),
    path('configurar-rodadas/', configurar_rodadas, name='configurar_rodadas'),
    path('acoes-rodada/', acoes_rodada, name='acoes_rodada'),
    path('atualizar-classificacao/', atualizar_classificacao, name='atualizar_classificacao'),
    path('controle-partidas/', controle_partidas, name='controle_partidas'),

    path('termos/', termos, name='termos'),
    path('privacidade/', privacidade, name='privacidade'),
]
