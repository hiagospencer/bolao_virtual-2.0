from django.contrib import admin
from django.utils.html import format_html
from .models import PagamentoPIX

@admin.register(PagamentoPIX)
class PagamentoPIXAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'valor',
        'status',
        'data_criacao',
        'data_aprovacao',
        'codigo_transacao',
        'exibir_qrcode',
    )
    list_filter = ('status', 'data_criacao')
    search_fields = ('usuario__username', 'codigo_transacao', 'chave_pix')
    readonly_fields = ('data_criacao', 'data_aprovacao', 'exibir_qrcode')

    def exibir_qrcode(self, obj):
        if obj.qr_code_image:
            return format_html('<img src="{}" width="150" />', obj.qr_code_image.url)
        return "QR Code não gerado"
    exibir_qrcode.short_description = 'QR Code'

