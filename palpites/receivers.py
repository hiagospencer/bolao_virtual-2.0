from django.dispatch import receiver
from .signals import classificacao_finalizada
from usuarios.models import DestaqueDaSemana


@receiver(classificacao_finalizada)
def pos_classificacao_finalizada(sender, rodada_atualizada=None, **kwargs):
    print(f"✅ Classificação finalizada para a rodada {rodada_atualizada}!")

    try:
        destaque = DestaqueDaSemana.objects.get(rodada__numero=rodada_atualizada)
        print(f"🏅 Destaque da semana: {destaque.usuario.username} com {destaque.acertos} acertos!")
    except DestaqueDaSemana.DoesNotExist:
        print("Nenhum destaque registrado para essa rodada.")
