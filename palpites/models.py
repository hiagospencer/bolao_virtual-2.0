# apps/palpites/models.py
from django.db import models
from core.models import Partida
from usuarios.models import Usuario



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

class CampeaoBolao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='campeonatos')
    pontos = models.PositiveIntegerField()
    edicao = models.CharField(max_length=50)  # Ex: "2023", "Copa 2022"
    data_coroado = models.DateField(auto_now_add=True)
    titulos_conquistados = models.PositiveIntegerField(default=1)  # Contagem de títulos

    class Meta:
        ordering = ['-edicao']
        verbose_name_plural = 'Campeões do Bolão'
        unique_together = ('usuario', 'edicao')  # Evita duplicatas

    def __str__(self):
        return f"{self.usuario.username} - {self.edicao} ({self.titulos_conquistados}º título)"

class ConfiguracaoRodada(models.Model):
    numero_rodada = models.IntegerField(unique=True, null=True, blank=True)
    editar_rodada = models.BooleanField(default=False)
    data_limite_edicao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Rodada {self.numero_rodada} - Edição {'Liberada' if self.editar_rodada else 'Bloqueada'}"


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


class DataBolao(models.Model):
    data_final = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Data Final para preencher os palpites: {self.data_final}"
