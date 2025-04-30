from django.contrib import admin
from .models import CategoriaItem, ItemLoja, InventarioUsuario, Transacao
from django.utils.html import format_html

@admin.register(CategoriaItem)
class CategoriaItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'icone')
    search_fields = ('nome', 'icone')

@admin.register(ItemLoja)
class ItemLojaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'tipo', 'preco', 'disponivel', 'data_criacao', 'imagem_preview')
    list_filter = ('tipo', 'disponivel', 'categoria')
    search_fields = ('nome', 'descricao')
    autocomplete_fields = ('categoria',)
    readonly_fields = ('data_criacao', 'imagem_preview')
    ordering = ('-data_criacao',)

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" style="height: 40px;" />', obj.imagem.url)
        return "Sem imagem"
    imagem_preview.short_description = 'Imagem'

@admin.register(InventarioUsuario)
class InventarioUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'item', 'data_compra', 'utilizado')
    list_filter = ('utilizado', 'data_compra')
    search_fields = ('usuario__username', 'item__nome')
    autocomplete_fields = ('usuario', 'item')
    readonly_fields = ('data_compra',)
    ordering = ('-data_compra',)

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'valor', 'data', 'descricao')
    list_filter = ('data',)
    search_fields = ('usuario__username', 'descricao')
    autocomplete_fields = ('usuario',)
    date_hierarchy = 'data'
    ordering = ('-data',)
    readonly_fields = ('data',)
