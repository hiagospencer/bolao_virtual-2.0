# apps/estatisticas/tasks.py
from django.core.management.base import BaseCommand
from estatisticas.models import MetricasDiarias

class Command(BaseCommand):
    help = 'Atualiza as métricas diárias do site'

    def handle(self, *args, **options):
        MetricasDiarias.atualizar_metricas()
        self.stdout.write(self.style.SUCCESS('Métricas diárias atualizadas com sucesso!'))
