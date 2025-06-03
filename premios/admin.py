# apps/premios/admin.py
from django.contrib import admin
from .models import *

@admin.register(TipoTrofeu)
class TipoTrofeuAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nivel', 'cor')
    list_filter = ('nivel',)

@admin.register(MetaConquista)
class MetaConquistaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'valor_requerido', 'xp_recompensa', 'moedas_recompensa')
    list_editable = ('tipo', 'valor_requerido', 'xp_recompensa', 'moedas_recompensa')
    list_filter = ('tipo', 'tipo_trofeu')
    search_fields = ('nome', 'descricao')

@admin.register(ConquistaUsuario)
class ConquistaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'meta', 'concluida', 'progresso_atual', 'data_conquista')
    list_filter = ('concluida', 'meta')
    search_fields = ('usuario__username', 'meta__nome')
    readonly_fields = ('data_conquista',)

@admin.register(Premio)
class PremioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'preco_moedas', 'estoque', 'disponivel')
    list_filter = ('tipo', 'categoria', 'disponivel')


@admin.register(PremioUsuario)
class PremioUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'premio', 'valor_recebido', 'pago', 'data_premiacao')
    list_filter = ('pago', 'premio')
    search_fields = ('usuario__username', 'premio__nome')
    readonly_fields = ('data_premiacao',)
    actions = ['marcar_como_pago']

    def marcar_como_pago(self, request, queryset):
        queryset.update(pago=True)
    marcar_como_pago.short_description = "Marcar selecionados como pagos"


@admin.register(HistoricoConquista)
class HistoricoConquistaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'meta', 'xp_ganho', 'moedas_ganhas')
    list_filter = ('usuario',)

class PedidoPremioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'premio', 'utilizado')
    list_filter = ('utilizado',)
    search_fields = ('usuario__username', 'premio__nome')


@admin.register(TipoMeta)
class TipoMetaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo']
    search_fields = ['nome', 'codigo']


admin.site.register(PedidoPremio, PedidoPremioAdmin)

admin.site.register([CategoriaPremio, TituloAtivo])
