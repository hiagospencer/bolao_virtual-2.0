# apps/palpites/models.py
from django.db import models
from core.models import Partida
from usuarios.models import Usuario

# class Palpite(models.Model):
#     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
#     partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
#     placar_casa = models.PositiveSmallIntegerField()
#     placar_visitante = models.PositiveSmallIntegerField()
#     data_palpite = models.DateTimeField(auto_now_add=True)
#     pontos_ganhos = models.PositiveSmallIntegerField(default=0)

#     class Meta:
#         unique_together = ('usuario', 'partida')
#         ordering = ['-data_palpite']

#     def __str__(self):
#         return f"{self.usuario}: {self.partida} - {self.placar_casa}x{self.placar_visitante}"

#     def calcular_pontos(self):
#         # Lógica para calcular pontos baseado no resultado real
#         if not self.partida.encerrada:
#             return 0

#         if (self.placar_casa == self.partida.placar_casa and
#             self.placar_visitante == self.partida.placar_visitante):
#             return 5  # Placar exato

#         vencedor_palpite = None
#         if self.placar_casa > self.placar_visitante:
#             vencedor_palpite = 'casa'
#         elif self.placar_visitante > self.placar_casa:
#             vencedor_palpite = 'visitante'
#         else:
#             vencedor_palpite = 'empate'

#         vencedor_real = None
#         if self.partida.placar_casa > self.partida.placar_visitante:
#             vencedor_real = 'casa'
#         elif self.partida.placar_visitante > self.partida.placar_casa:
#             vencedor_real = 'visitante'
#         else:
#             vencedor_real = 'empate'

#         if vencedor_palpite == vencedor_real:
#             return 2  # Acertou o vencedor

#         return 0  # Errou o resultado

class Palpite(models.Model):
    usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE)
    rodada_atual = models.IntegerField(default=1)
    time_casa = models.CharField(max_length=50)
    placar_casa = models.IntegerField(default=0)
    time_visitante = models.CharField(max_length=50)
    placar_visitante = models.IntegerField(default=0)
    data_jogo = models.CharField(max_length=50, null=True, blank=True)
    imagem_casa = models.ImageField(upload_to='emblemas_times', null=True, blank=True)
    imagem_fora = models.ImageField(upload_to='emblemas_times', null=True, blank=True)
    vencedor = models.CharField(max_length=50)
    finalizado = models.BooleanField(default=False)
    tipo_class = models.CharField(max_length=50, default='none')
    placar_exato = models.IntegerField(default=0)
    vitorias = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.placar_casa > self.placar_visitante:
            self.vencedor = self.time_casa
        elif self.placar_casa < self.placar_visitante:
            self.vencedor = self.time_visitante
        else:
            self.vencedor = 'empate'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.time_casa} x {self.time_visitante}"

class RodadaOriginal(models.Model):
    rodada_atual = models.IntegerField(default=1)
    time_casa = models.CharField(max_length=50)
    placar_casa = models.IntegerField(default=0)
    time_visitante = models.CharField(max_length=50)
    placar_visitante = models.IntegerField(default=0)
    vencedor = models.CharField(max_length=50)
    finalizado = models.BooleanField(default=False)
    data_jogo = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.placar_casa > self.placar_visitante:
            self.vencedor = self.time_casa
        elif self.placar_casa < self.placar_visitante:
            self.vencedor = self.time_visitante
        else:
            self.vencedor = 'empate'

        if self.placar_casa == 9999 and self.placar_visitante == 9999:
            self.vencedor = 'andamento'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.time_casa} x {self.time_visitante}"

class Rodada(models.Model):
    rodada_atual = models.IntegerField(default=1)
    time_casa = models.CharField(max_length=50)
    placar_casa = models.CharField(null=True, blank=True)
    time_visitante = models.CharField(max_length=50)
    placar_visitante = models.CharField(null=True, blank=True)
    imagem_casa = models.ImageField(upload_to='emblemas_times')
    imagem_fora = models.ImageField(upload_to='emblemas_times')
    preenchido = models.BooleanField(default=False)
    data_jogo = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.time_casa} x {self.time_visitante}"


class Classificacao(models.Model):
    usuario = models.OneToOneField(Usuario, null=True, blank=True, on_delete=models.CASCADE)
    pontos = models.IntegerField(default=0)
    placar_exato = models.IntegerField(default=0)
    vitorias = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)
    posicao_atual = models.IntegerField(null=True, blank=True)
    posicao_anterior = models.IntegerField(null=True, blank=True)
    posicao_variacao = models.IntegerField(null=True, blank=True)


class PontuacaoRodada(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rodada = models.IntegerField()
    pontos = models.IntegerField(default=0)

    class Meta:
        unique_together = ('usuario', 'rodada')

    def __str__(self):
        return f"Usuario: {self.usuario} - Pontos: {self.pontos}"


class BloquearPartida(models.Model):
    usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE)
    rodada_atual = models.IntegerField(default=1)
    rodada_bloqueada = models.BooleanField(default=False)
    bloquear_grafico = models.BooleanField(default=False)
    bloquear_pagamento = models.BooleanField(default=False)
    data_final = models.CharField(max_length=50, null=True, blank=True)
    partida_atual = models.IntegerField(default=1)
    partida_final = models.IntegerField(default=39)


    def __str__(self):
        return f'Rodadas bloqueadas: {self.rodada_bloqueada} - partida atual: {self.partida_atual}ª - partida final: {self.partida_final}ª'
