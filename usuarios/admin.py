from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, UserProfile, Rodada, DestaqueDaSemana, RecompensaPremium
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = (
        'username', 'email', 'first_name', 'last_name', "xp",
        'is_staff', 'is_verified', 'pontos_totais', 'moedas_virtuais', 'foto_perfil_preview'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_verified', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined', 'foto_perfil_preview')
    # list_editable = ("xp", "moedas ", "level ","xp_para_proximo_level ","nivel_maximo")
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informações pessoais'), {
            'fields': (
                'first_name', 'last_name', 'email', 'foto_perfil_preview', 'foto_perfil', 'data_nascimento',
                'pontos_totais', 'moedas_virtuais', 'is_verified'
            )
        }),
        (_('Permissões'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        (_('Datas importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    def foto_perfil_preview(self, obj):
        if obj.foto_perfil:
            return format_html('<img src="{}" style="height: 40px; border-radius: 50%;" />', obj.foto_perfil.url)
        return "Sem imagem"
    foto_perfil_preview.short_description = 'Foto de Perfil'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefone', 'chave_pix', 'pagamento', 'xp', 'moedas', 'level', 'xp_para_proximo_level', 'nivel_maximo')
    search_fields = ('user__username', 'telefone', 'chave_pix')
    autocomplete_fields = ('user',)
    list_editable = ( 'pagamento', 'xp', 'moedas', 'level', 'xp_para_proximo_level', 'nivel_maximo')

    def bio_resumida(self, obj):
        return (obj.bio[:50] + '...') if len(obj.bio) > 50 else obj.bio
    bio_resumida.short_description = 'Bio'

@admin.register(Rodada)
class RodadaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'data_inicio', 'data_fim')
    search_fields = ('numero',)
    ordering = ('-numero',)
    list_per_page = 20


@admin.register(DestaqueDaSemana)
class DestaqueDaSemanaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rodada', 'acertos', 'total_jogos', 'porcentagem_acertos', 'criado_em')
    list_filter = ('rodada', 'usuario')
    search_fields = ('usuario__username', 'rodada')
    readonly_fields = ('porcentagem_acertos', 'criado_em')
    ordering = ('-rodada',)
    list_per_page = 20

    # @admin.display(description="Acertos (%)")
    # def porcentagem_acertos(self, obj):
    #     if not obj.total_jogos:
    #         return "0%"
    #     return f"{(obj.acertos / obj.total_jogos) * 100:.1f}%"

@admin.register(RecompensaPremium)
class RecompensaPremiumAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data', 'convidados_utilizados_display')

    def convidados_utilizados_display(self, obj):
        return ", ".join([u.username for u in obj.convidados_utilizados.all()])
    convidados_utilizados_display.short_description = "Convidados Utilizados"
