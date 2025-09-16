from django.db import models
from django.utils import timezone
from usuarios.models import Usuario
from palpites.models import Palpite

class VisitaSite(models.Model):
    usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.SET_NULL)
    ip = models.CharField(max_length=45)
    pagina = models.CharField(max_length=200)
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Visita em {self.pagina} - {self.timestamp}"

class MetricasDiarias(models.Model):
    data = models.DateField(unique=True)
    visitas_totais = models.PositiveIntegerField(default=0)
    usuarios_novos = models.PositiveIntegerField(default=0)
    palpites_realizados = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Métricas para {self.data}"

    @classmethod
    def atualizar_metricas(cls):
        hoje = timezone.now().date()
        metricas, created = cls.objects.get_or_create(data=hoje)

        # Atualizar contagem de visitas
        metricas.visitas_totais = VisitaSite.objects.filter(
            timestamp__date=hoje
        ).count()

        # Atualizar novos usuários
        metricas.usuarios_novos = Usuario.objects.filter(
            date_joined__date=hoje
        ).count()

        # Atualizar palpites realizados
        metricas.palpites_realizados = Palpite.objects.filter(
            data_palpite__date=hoje
        ).count()

        metricas.save()
        return metricas
