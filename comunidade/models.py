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
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Resposta de {self.autor} em {self.topico}"

class Enquete(models.Model):
    pergunta = models.CharField(max_length=200)
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_encerramento = models.DateTimeField()

    def __str__(self):
        return self.pergunta

    def usuario_ja_votou(self, user):
        """Verifica se o usuário já votou nesta enquete"""
        if not user.is_authenticated:
            return False
        return self.votoenquete_set.filter(usuario=user).exists()

    def get_voto_usuario(self, user):
        """Retorna a opção em que o usuário votou"""
        if not user.is_authenticated:
            return None
        try:
            return self.votoenquete_set.get(usuario=user).opcao
        except VotoEnquete.DoesNotExist:
            return None


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


class VotoEnquete(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE)
    opcao = models.ForeignKey(OpcaoEnquete, on_delete=models.CASCADE)
    data_voto = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'enquete')
        verbose_name = 'Voto de Enquete'
        verbose_name_plural = 'Votos de Enquetes'

    def __str__(self):
        return f"Voto de {self.usuario} em {self.enquete}"
