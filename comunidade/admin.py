# apps/comunidade/admin.py
from django.contrib import admin
from .models import TopicoForum, ComentarioForum, Enquete, OpcaoEnquete

class ComentarioForumInline(admin.TabularInline):
    model = ComentarioForum
    extra = 1  # Número de campos em branco a serem exibidos no formulário de tópico

class TopicoForumAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_criacao', 'atualizado_em', 'visualizacoes')
    search_fields = ('titulo', 'autor__username')
    list_filter = ('autor', 'data_criacao')
    inlines = [ComentarioForumInline]  # Exibe os comentários diretamente na edição do tópico

class ComentarioForumAdmin(admin.ModelAdmin):
    list_display = ('topico', 'autor', 'data_criacao', 'conteudo_resumido')
    search_fields = ('topico__titulo', 'autor__username', 'conteudo')
    list_filter = ('topico', 'autor')

    def conteudo_resumido(self, obj):
        return obj.conteudo[:50]  # Exibe um resumo do conteúdo do comentário
    conteudo_resumido.short_description = 'Resumo do Conteúdo'

class EnqueteAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'criador', 'data_criacao', 'data_encerramento')
    search_fields = ('pergunta', 'criador__username')
    list_filter = ('criador', 'data_criacao')

class OpcaoEnqueteAdmin(admin.ModelAdmin):
    list_display = ('texto', 'enquete', 'votos')
    search_fields = ('texto', 'enquete__pergunta')
    list_filter = ('enquete',)

admin.site.register(TopicoForum, TopicoForumAdmin)
admin.site.register(ComentarioForum, ComentarioForumAdmin)
admin.site.register(Enquete, EnqueteAdmin)
admin.site.register(OpcaoEnquete, OpcaoEnqueteAdmin)
