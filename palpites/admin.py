# apps/palpites/admin.py
from django.contrib import admin
from .models import *
from django.utils.html import format_html


class ClassificacaoAdmin(admin.ModelAdmin):
    model = Classificacao
    list_display = ["usuario", "pontos", "placar_exato", "vitorias","empates","posicao_atual", "posicao_anterior", "posicao_variacao"]
    list_editable = ("pontos", "placar_exato", "vitorias","empates","posicao_atual", "posicao_anterior", "posicao_variacao")
    list_filter = ["usuario", "pontos",]
    search_fields = ("usuario",)


class PalpiteAdmin(admin.ModelAdmin):
    model = Palpite
    list_display = ["usuario","rodada_atual","time_casa", "placar_casa", "placar_visitante", "time_visitante", "vencedor","placar_exato","vitorias", "finalizado", "tipo_class"]
    list_filter = ["usuario", "rodada_atual"]
    list_per_page = 10
    search_fields = ("usuario", "rodada_atual")

class RodadaOriginalAdmin(admin.ModelAdmin):
    model = RodadaOriginal
    list_display = ["rodada_atual","time_casa", "placar_casa", "placar_visitante",  "time_visitante", "vencedor", "finalizado"]
    list_filter = ["rodada_atual"]
    list_editable = ("placar_casa", "placar_visitante", "vencedor",)
    list_per_page = 10
    search_fields = ("usuario", "rodada_atual")

class RodadaAdmin(admin.ModelAdmin):
    model = Palpite
    list_display = ["rodada_atual","time_casa", "placar_casa", "placar_visitante",  "time_visitante"]
    list_filter = ["rodada_atual"]
    list_per_page = 10
    search_fields = ("rodada_atual",)


admin.site.register(Classificacao, ClassificacaoAdmin)
admin.site.register(RodadaOriginal, RodadaOriginalAdmin)
admin.site.register(Rodada, RodadaAdmin)
admin.site.register(Palpite, PalpiteAdmin)
admin.site.register(BloquearPartida)
admin.site.register(PontuacaoRodada)
admin.site.register(DataBolao)
