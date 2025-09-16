# apps/core/models.py
from django.db import models

class Time(models.Model):
    nome = models.CharField(max_length=100)
    escudo = models.ImageField(upload_to='times/')
    sigla = models.CharField(max_length=3)

    def __str__(self):
        return self.nome

class Campeonato(models.Model):
    nome = models.CharField(max_length=100)
    temporada = models.CharField(max_length=20)
    times = models.ManyToManyField(Time)

    def __str__(self):
        return f"{self.nome} {self.temporada}"

class Partida(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    time_casa = models.ForeignKey(Time, related_name='partidas_casa', on_delete=models.CASCADE)
    time_visitante = models.ForeignKey(Time, related_name='partidas_visitante', on_delete=models.CASCADE)
    data = models.DateTimeField()
    placar_casa = models.PositiveSmallIntegerField(null=True, blank=True)
    placar_visitante = models.PositiveSmallIntegerField(null=True, blank=True)
    rodada = models.PositiveSmallIntegerField()
    encerrada = models.BooleanField(default=False)

    class Meta:
        ordering = ['data']

    def __str__(self):
        return f"{self.time_casa} x {self.time_visitante} - {self.data.strftime('%d/%m/%Y')}"


class PremiacaoBolao(models.Model):
    posicao = models.CharField(max_length=100,null=True, blank=True)
    premiacao = models.DecimalField(default=0, max_digits=100, decimal_places=2)

    def __str__(self):
        return f'Posicao: {self.posicao} - Premiação: {self.premiacao}'
