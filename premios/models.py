# apps/premios/models.py
from django.db import models
from usuarios.models import Usuario

class TipoTrofeu(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    icone = models.CharField(max_length=50)  # Nome do ícone FontAwesome
    nivel = models.PositiveSmallIntegerField(default=1)  # 1=Bronze, 2=Prata, 3=Ouro
    cor = models.CharField(max_length=20, default='#FFD700')  # Código hex da cor

    def __str__(self):
        return f"{self.nome} (Nível {self.nivel})"

    def conquistado_por(self, usuario):
        return ConquistaUsuario.objects.filter(
            usuario=usuario,
            meta__tipo_trofeu=self,
            concluida=True
        ).exists()


class MetaConquista(models.Model):
    TIPO_META = [
        ('placar_exato', 'Placar Exato'),
        ('pontos_rodada', 'Pontos em uma Rodada'),
        ('sequencia', 'Sequência de Acertos'),
        ('participacao', 'Participação em Rodadas'),
        ('top_ranking', 'Posição no Ranking'),
        ('pontos_totais', 'Pontos Totais Acumulados'),
        ('total_conquistas', 'Total de Conquistas Únicas'),
    ]

    tipo_trofeu = models.ForeignKey(TipoTrofeu, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_META)
    valor_requerido = models.PositiveIntegerField()
    xp_recompensa = models.PositiveIntegerField(default=100)
    moedas_recompensa = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

class ConquistaUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='conquistas')
    meta = models.ForeignKey(MetaConquista, on_delete=models.CASCADE)
    data_conquista = models.DateTimeField(auto_now_add=True)
    progresso_atual = models.PositiveIntegerField(default=0)
    concluida = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario', 'meta')

    def __str__(self):
        return f"{self.usuario} - {self.meta} ({'Concluída' if self.concluida else 'Em progresso'})"

class Premio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    valor_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class PremioUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='premios')
    premio = models.ForeignKey(Premio, on_delete=models.CASCADE)
    data_premiacao = models.DateTimeField(auto_now_add=True)
    valor_recebido = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario} - {self.premio} (R${self.valor_recebido})"
