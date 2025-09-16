# apps/loja/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import CategoriaItem, ItemLoja, InventarioUsuario, Transacao, Loja

@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dono', 'ativo', 'data_criacao', 'logo_preview',)
    list_filter = ('ativo', 'data_criacao')
    search_fields = ('nome', 'dono__username')
    readonly_fields = ('data_criacao',)
    list_editable = ('ativo',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.logo.url)
        return "Sem logo"
    logo_preview.short_description = 'Logo'

@admin.register(CategoriaItem)
class CategoriaItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'icone', 'quantidade_itens')
    search_fields = ('nome', 'icone')

    def quantidade_itens(self, obj):
        return obj.itemloja_set.count()
    quantidade_itens.short_description = 'Itens na categoria'

@admin.register(ItemLoja)
class ItemLojaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'loja', 'categoria','whatsapp_link','telefone', 'tipo', 'preco', 'disponivel', 'imagem_preview', 'data_criacao')
    list_filter = ('loja', 'categoria', 'tipo', 'disponivel', 'data_criacao')
    search_fields = ('nome', 'descricao', 'loja__nome')
    list_editable = ('preco', 'disponivel','whatsapp_link','telefone',) #'imagem_preview'
    readonly_fields = ('data_criacao',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'loja', 'categoria', 'tipo')
        }),
        ('Valores e Disponibilidade', {
            'fields': ('preco', 'disponivel')
        }),
        ('Imagem', { 
            'fields': ('imagem_preview',)
        }),
        ('Datas', {
            'fields': ('data_criacao',),
            'classes': ('collapse',)
        }),
    )

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.imagem.url)
        return "Sem imagem"
    imagem_preview.short_description = 'Preview'
    imagem_preview.allow_tags = True


@admin.register(InventarioUsuario)
class InventarioUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'item', 'utilizado', 'data_compra')
    list_filter = ('utilizado', 'data_compra')
    search_fields = ('usuario__username', 'item__nome')
    readonly_fields = ('data_compra',)
    raw_id_fields = ('usuario', 'item')


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'valor_formatado', 'descricao', 'data')
    list_filter = ('data',)
    search_fields = ('usuario__username', 'descricao')
    readonly_fields = ('data',)
    date_hierarchy = 'data'

    def valor_formatado(self, obj):
        return f"R$ {obj.valor:,.2f}"
    valor_formatado.short_description = 'Valor'
    valor_formatado.admin_order_field = 'valor'
