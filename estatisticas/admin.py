from django.contrib import admin
from .models import VisitaSite, MetricasDiarias

@admin.register(VisitaSite)
class VisitaSiteAdmin(admin.ModelAdmin):
    list_display = ('ip', 'usuario', 'pagina', 'timestamp', 'user_agent_curto')
    list_filter = ('pagina', 'timestamp')
    search_fields = ('ip', 'pagina', 'usuario__username', 'user_agent')
    readonly_fields = ('ip', 'usuario', 'pagina', 'user_agent', 'timestamp')
    ordering = ('-timestamp',)

    def user_agent_curto(self, obj):
        return (obj.user_agent[:50] + "...") if len(obj.user_agent) > 50 else obj.user_agent
    user_agent_curto.short_description = 'User Agent'

@admin.register(MetricasDiarias)
class MetricasDiariasAdmin(admin.ModelAdmin):
    list_display = ('data', 'visitas_totais', 'usuarios_novos', 'palpites_realizados')
    list_filter = ('data',)
    ordering = ('-data',)
    date_hierarchy = 'data'
    readonly_fields = ('visitas_totais', 'usuarios_novos', 'palpites_realizados')
