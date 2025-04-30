from django.urls import path

from .views import *

urlpatterns = [
    path('trofeus/', trofeus, name='trofeus'),
    path("minhas-conquistas/",minhas_conquistas, name="minhas_conquistas"),
    path("meus-premios/",meus_premios, name="meus_premios"),
]
