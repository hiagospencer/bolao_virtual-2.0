# apps/premios/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from palpites.models import Palpite
from .services import VerificadorConquistas

@receiver(post_save, sender=Palpite)
def verificar_conquistas_apos_palpite(sender, instance, created, **kwargs):
    if created:
        VerificadorConquistas.verificar_meta_usuario(
            instance.usuario,
            lambda m: m.tipo in ['placar_exato', 'pontos_rodada', 'sequencia']
        )
