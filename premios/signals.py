# apps/premios/signals.py
from django.db.models.signals import post_save
from django.utils.functional import SimpleLazyObject
from django.dispatch import receiver
from palpites.models import Palpite
from .services import VerificadorConquistas
from premios.models import ConquistaUsuario, HistoricoConquista


@receiver(post_save, sender=Palpite)
def verificar_conquistas_apos_palpite(sender, instance, created, **kwargs):
    if created:
        usuario = instance.usuario
        if isinstance(usuario, SimpleLazyObject):
            usuario = usuario._wrapped if hasattr(usuario, "_wrapped") else usuario.__wrapped__()

        if not usuario or not hasattr(usuario, "id"):
            print("Usuário inválido no signal")
            return

        VerificadorConquistas.verificar_meta_usuario(
            instance.usuario,
            lambda m: m.tipo in ['placar_exato', 'pontos_rodada', 'sequencia']
        )


@receiver(post_save, sender=ConquistaUsuario)
def atualizar_xp_moedas(sender, instance, **kwargs):
    if instance.concluida:
        # Atualiza XP e moedas do usuário
        instance.usuario.xp += instance.meta.xp_recompensa
        instance.usuario.moedas += instance.meta.moedas_recompensa
        instance.usuario.save()

        # Registra no histórico
        HistoricoConquista.objects.create(
            usuario=instance.usuario,
            meta=instance.meta,
            xp_ganho=instance.meta.xp_recompensa,
            moedas_ganhas=instance.meta.moedas_recompensa
        )
