# apps/comunidade/models.py
from django.db import models
from django.db.models import Sum
from usuarios.models import Usuario

class TopicoForum(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    visualizacoes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

    @property
    def total_comentarios(self):
        return self.comentarios.count()

class ComentarioForum(models.Model):
    topico = models.ForeignKey(TopicoForum, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor} em {self.topico}"

class Enquete(models.Model):
    pergunta = models.CharField(max_length=200)
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_encerramento = models.DateTimeField()

    def __str__(self):
        return self.pergunta

    @property
    def total_votos(self):
        return self.opcoes.aggregate(total=Sum('votos'))['total'] or 0

    def porcentagem_votos(self, opcao):
        if self.total_votos == 0:
            return 0
        return round((opcao.votos / self.total_votos) * 100)

class OpcaoEnquete(models.Model):
    enquete = models.ForeignKey(Enquete, related_name='opcoes', on_delete=models.CASCADE)
    texto = models.CharField(max_length=100)
    votos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.texto} ({self.enquete})"
