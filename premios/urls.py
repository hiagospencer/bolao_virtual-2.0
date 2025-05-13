from django.urls import path

from .views import *

urlpatterns = [
    path('trofeus/', trofeus, name='trofeus'),
    path("minhas-conquistas/",minhas_conquistas, name="minhas_conquistas"),
    path("meus-premios/",meus_premios, name="meus_premios"),

    # Prêmios
    path('todos-premios/', lista_premios, name='lista_premios'),
    path('meus-premios/', meus_premios, name='meus_premios'),
    path('comprar/<int:premio_id>/', comprar_premio, name='comprar_premio'),
    path('ativar/<int:pedido_id>/', ativar_titulo, name='ativar_titulo'),
    path('voucher/<int:pedido_id>/resgatar/', resgatar_voucher, name='resgatar_voucher'),
    path('voucher/<int:pedido_id>/utilizado/', marcar_como_utilizado, name='marcar_como_utilizado'),
]
