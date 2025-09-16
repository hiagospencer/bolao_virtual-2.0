from django.contrib import admin
from .models import Time, Campeonato, Partida, PremiacaoBolao

@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'escudo_preview')
    search_fields = ('nome', 'sigla')
    readonly_fields = ('escudo_preview',)

    def escudo_preview(self, obj):
        if obj.escudo:
            return f'<img src="{obj.escudo.url}" style="height: 40px;"/>'
        return "Sem escudo"
    escudo_preview.short_description = 'Escudo'
    escudo_preview.allow_tags = True

@admin.register(Campeonato)
class CampeonatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'temporada')
    list_filter = ('temporada',)
    search_fields = ('nome',)
    filter_horizontal = ('times',)

@admin.register(Partida)
class PartidaAdmin(admin.ModelAdmin):
    list_display = ('campeonato', 'rodada', 'data', 'time_casa', 'placar_casa', 'placar_visitante', 'time_visitante', 'encerrada')
    list_filter = ('campeonato', 'rodada', 'encerrada', 'data')
    search_fields = (
        'time_casa__nome',
        'time_visitante__nome',
        'campeonato__nome',
    )
    autocomplete_fields = ('time_casa', 'time_visitante', 'campeonato')
    date_hierarchy = 'data'
    ordering = ('-data',)

@admin.register(PremiacaoBolao)
class PremiacaoBolaoAdmin(admin.ModelAdmin):
    list_display = ('posicao', 'premiacao', )
