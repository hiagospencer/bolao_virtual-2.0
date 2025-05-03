from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    foto_perfil = models.ImageField(upload_to='perfis/', null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    pontos_totais = models.PositiveIntegerField(default=0)
    moedas_virtuais = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    xp = models.PositiveIntegerField(default=0)
    moedas = models.PositiveIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=1)
    xp_para_proximo_level = models.PositiveIntegerField(default=500)
    nivel_maximo = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.username

    def adicionar_xp(self, quantidade):
        """
        Adiciona XP e atualiza nível quando necessário
        Retorna: (level_up, moedas_ganhas)
        """
        if self.level >= self.nivel_maximo:
            moedas_ganhas = quantidade * 10
            self.moedas += moedas_ganhas
            self.save()
            return (False, moedas_ganhas)

        nivel_anterior = self.level
        self.xp += quantidade
        level_up = False
        moedas_ganhas = 0

        while self.xp >= self.xp_para_proximo_level and self.level < self.nivel_maximo:
            self.xp -= self.xp_para_proximo_level
            self.level += 1
            level_up = True

            # Recompensa por level up
            recompensa = self.level * 100
            self.moedas += recompensa
            moedas_ganhas += recompensa

            # Atualiza para o próximo nível
            self.xp_para_proximo_level = self.calcular_xp_necessario()

        self.save()
        return (level_up, moedas_ganhas)

    def calcular_xp_necessario(self):

        """Calcula o XP necessário para o próximo nível com progressão exponencial"""
        base_xp = 500  # Valor base
        multiplicador = 1.5  # Fator de crescimento
        return int(base_xp * (multiplicador ** (self.level - 1)))

class UserProfile(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    chave_pix = models.CharField(max_length=100, blank=True)
    pagamento = models.BooleanField(default=False)
    xp = models.PositiveIntegerField(default=0)
    moedas = models.PositiveIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=1)
    xp_para_proximo_level = models.PositiveIntegerField(default=500)
    nivel_maximo = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def adicionar_xp(self, quantidade):
        """
        Adiciona XP e atualiza nível quando necessário
        Retorna: (level_up, moedas_ganhas)
        """
        if self.level >= self.nivel_maximo:
            moedas_ganhas = quantidade * 10
            self.moedas += moedas_ganhas
            self.save()
            return (False, moedas_ganhas)

        nivel_anterior = self.level
        self.xp += quantidade
        level_up = False
        moedas_ganhas = 0

        while self.xp >= self.xp_para_proximo_level and self.level < self.nivel_maximo:
            self.xp -= self.xp_para_proximo_level
            self.level += 1
            level_up = True
            recompensa = self.level * 100
            self.moedas += recompensa
            moedas_ganhas += recompensa
            self.xp_para_proximo_level = self.calcular_xp_necessario()

        self.save()
        return (level_up, moedas_ganhas)

    def calcular_xp_necessario(self):

        """Calcula o XP necessário para o próximo nível com progressão exponencial"""
        base_xp = 500  # Valor base
        multiplicador = 1.5  # Fator de crescimento
        return int(base_xp * (multiplicador ** (self.level - 1)))

    def corrigir_nivel(self):
        while self.xp >= self.xp_para_proximo_level and self.level < self.nivel_maximo:
            self.xp -= self.xp_para_proximo_level
            self.level += 1
            self.xp_para_proximo_level = self.calcular_xp_necessario()
        self.save() 
