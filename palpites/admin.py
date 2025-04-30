# apps/palpites/admin.py
from django.contrib import admin
from .models import Palpite
from django.utils.html import format_html

class PalpiteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'partida', 'placar_casa', 'placar_visitante', 'data_palpite', 'pontos_ganhos', 'calcular_pontos_display')
    list_filter = ('usuario', 'partida', 'data_palpite')
    search_fields = ('usuario__username', 'partida__time_casa__nome', 'partida__time_visitante__nome')
    readonly_fields = ('data_palpite', 'pontos_ganhos')

    def calcular_pontos_display(self, obj):
        return obj.calcular_pontos()
    calcular_pontos_display.short_description = 'Pontos Ganhos'

    def save_model(self, request, obj, form, change):
        # Calcula os pontos ao salvar o palpite
        obj.pontos_ganhos = obj.calcular_pontos()
        super().save_model(request, obj, form, change)

admin.site.register(Palpite, PalpiteAdmin)
