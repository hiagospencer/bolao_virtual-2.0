# apps/palpites/models.py
from django.db import models
from core.models import Partida
from usuarios.models import Usuario

class Palpite(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    placar_casa = models.PositiveSmallIntegerField()
    placar_visitante = models.PositiveSmallIntegerField()
    data_palpite = models.DateTimeField(auto_now_add=True)
    pontos_ganhos = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('usuario', 'partida')
        ordering = ['-data_palpite']

    def __str__(self):
        return f"{self.usuario}: {self.partida} - {self.placar_casa}x{self.placar_visitante}"

    def calcular_pontos(self):
        # Lógica para calcular pontos baseado no resultado real
        if not self.partida.encerrada:
            return 0

        if (self.placar_casa == self.partida.placar_casa and
            self.placar_visitante == self.partida.placar_visitante):
            return 5  # Placar exato

        vencedor_palpite = None
        if self.placar_casa > self.placar_visitante:
            vencedor_palpite = 'casa'
        elif self.placar_visitante > self.placar_casa:
            vencedor_palpite = 'visitante'
        else:
            vencedor_palpite = 'empate'

        vencedor_real = None
        if self.partida.placar_casa > self.partida.placar_visitante:
            vencedor_real = 'casa'
        elif self.partida.placar_visitante > self.partida.placar_casa:
            vencedor_real = 'visitante'
        else:
            vencedor_real = 'empate'

        if vencedor_palpite == vencedor_real:
            return 2  # Acertou o vencedor

        return 0  # Errou o resultado
