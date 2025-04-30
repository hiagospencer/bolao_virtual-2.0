# apps/premios/management/commands/premiar_ranking.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.premios.models import Premio, PremioUsuario

class Command(BaseCommand):
    help = 'Distribui prêmios para os usuários no topo do ranking'

    def handle(self, *args, **options):
        # Obter os prêmios disponíveis
        premios = Premio.objects.filter(disponivel=True)

        if not premios.exists():
            self.stdout.write(self.style.WARNING('Nenhum prêmio disponível para distribuir.'))
            return

        # Obter top usuários (exemplo: top 3)
        top_usuarios = Usuario.objects.order_by('-pontos_totais')[:3]

        # Distribuir prêmios
        for i, usuario in enumerate(top_usuarios):
            premio = premios.first()  # Ou lógica mais complexa para escolher o prêmio

            # Calcular valor do prêmio (pode ser aleatório dentro do range)
            valor = premio.valor_minimo  # Simplificado

            PremioUsuario.objects.create(
                usuario=usuario,
                premio=premio,
                valor_recebido=valor
            )

            self.stdout.write(self.style.SUCCESS(
                f'Prêmio de R${valor} concedido a {usuario.username} (posição {i+1})'
            ))
