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

class BloquearPartidasAdmin(admin.ModelAdmin):
    model = BloquearPartida
    list_display = ["usuario", "rodada_bloqueada", "partida_atual", "partida_final"]
    list_filter = ["usuario", "rodada_atual"]
    list_editable = ("rodada_bloqueada" ,"partida_atual", "partida_final",)
    search_fields = ("usuario", "partida_atual", "partida_final")


class PontuacaoRodadaAdmin(admin.ModelAdmin):
    model = PontuacaoRodada
    list_display = ["usuario","pontos", "rodada"]
    list_editable = ("pontos" ,"rodada",)
    list_filter = ["rodada"]
    list_per_page = 10
    search_fields = ("rodada",)


@admin.register(CampeaoBolao)
class CampeaoBolaoAdmin(admin.ModelAdmin):
    # Campos a serem exibidos na lista
    list_display = (
        'foto_miniatura',
        'nome_usuario',
        'pontos',
        'edicao',
        'titulos_conquistados',
        'data_coroado',
        'link_perfil'
    )

    # Campos editáveis diretamente na lista
    list_editable = (
        'pontos',
        'edicao',
        'titulos_conquistados'
    )

    # Campos para filtro lateral
    list_filter = (
        'edicao',
        'data_coroado',
    )

    # Campos de busca
    search_fields = (
        'usuario__username',
        'edicao',
    )

    # Ordenação padrão
    ordering = ('-edicao', '-data_coroado')

    # Campos agrupados no formulário de edição
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'edicao',)
        }),
        ('Estatísticas', {
            'fields': ('pontos', 'titulos_conquistados')
        }),
    )

    # Métodos customizados para list_display
    def foto_miniatura(self, obj):
        if obj.usuario.foto_perfil:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.usuario.foto_perfil.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; border-radius: 50%; background: #eee; display: flex; align-items: center; justify-content: center; font-weight: bold;">{}</div>',
            obj.usuario.username[0].upper()
        )
    foto_miniatura.short_description = 'Foto'

    def nome_usuario(self, obj):
        return obj.usuario.username
    nome_usuario.short_description = 'Usuário'
    nome_usuario.admin_order_field = 'usuario__username'

    def link_perfil(self, obj):
        return format_html(
            '<a href="/admin/auth/user/{}/change/" target="_blank">🔍 Ver perfil</a>',
            obj.usuario.id
        )
    link_perfil.short_description = 'Ações'

    # Personalização do formulário de adição
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Quando editando um objeto existente
            return ['data_coroado'] + list(self.readonly_fields)
        return list(self.readonly_fields)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_data_coroado_info'] = True
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

    # Melhorando a seleção de usuário no formulário
    raw_id_fields = ('usuario',)
    autocomplete_fields = ('usuario',)


admin.site.register(Classificacao, ClassificacaoAdmin)
admin.site.register(RodadaOriginal, RodadaOriginalAdmin)
admin.site.register(Rodada, RodadaAdmin)
admin.site.register(Palpite, PalpiteAdmin)
admin.site.register(BloquearPartida, BloquearPartidasAdmin)
admin.site.register(PontuacaoRodada, PontuacaoRodadaAdmin)
admin.site.register(DataBolao)
admin.site.register(ConfiguracaoRodada)
