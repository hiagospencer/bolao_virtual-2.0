from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, Convite, RecompensaPremium

from django.contrib import messages

@receiver(post_save, sender=UserProfile)
def verificar_pagamento_e_recompensa(sender, instance, created, **kwargs):
    if not created and instance.pagamento:
        convite = Convite.objects.filter(convidado=instance.user).first()
        if convite:
            convidador = convite.codigo.usuario
            if convidador.verificar_e_aplicar_recompensa():
                print(f"🎉 {convidador.username} ganhou um Bolão Premium!")
