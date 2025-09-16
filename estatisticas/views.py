from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from .models import VisitaSite, MetricasDiarias


@user_passes_test(lambda u: u.is_staff)
def estatisticas_visitas(request):
    hoje = timezone.now().date()
    semana_passada = hoje - timedelta(days=7)
    mes_passado = hoje - timedelta(days=30)

    # Visitas hoje
    visitas_hoje = VisitaSite.objects.filter(timestamp__date=hoje).count()

    # Visitas semana
    visitas_semana = VisitaSite.objects.filter(
        timestamp__date__range=[semana_passada, hoje]
    ).count()

    # Visitas mês
    visitas_mes = VisitaSite.objects.filter(
        timestamp__date__range=[mes_passado, hoje]
    ).count()

    # Visitas por página
    paginas_populares = VisitaSite.objects.values('pagina').annotate(
        total=Count('id')
    ).order_by('-total')[:10]

    # Métricas diárias
    metricas = MetricasDiarias.objects.order_by('-data')[:30]

    context = {
        'visitas_hoje': visitas_hoje,
        'visitas_semana': visitas_semana,
        'visitas_mes': visitas_mes,
        'paginas_populares': paginas_populares,
        'metricas': metricas,
    }

    return render(request, 'outros/estatisticas.html', context)
