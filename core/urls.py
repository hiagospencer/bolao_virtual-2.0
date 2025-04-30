from django.urls import path

from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('perfil/', perfil, name='perfil'),
    path('regras/', regras, name='regras'),
    path('configuracao/', configuracao, name='configuracao'),
]
