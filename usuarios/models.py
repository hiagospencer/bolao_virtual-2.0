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

    def __str__(self):
        return self.username

    def adicionar_xp(self, quantidade):
        nivel_anterior = self.level
        self.xp += quantidade
        while self.xp >= self.xp_para_proximo_level:
            self.xp -= self.xp_para_proximo_level
            self.level += 1
            self.xp_para_proximo_level = self.calcular_xp_necessario()
            # Recompensa ao subir de nível:
            self.moedas += self.level * 100  # Exemplo: 100 moedas por nível
        self.save()
        if self.level > nivel_anterior:
            return True  # Indica que houve level up
        return False

    def calcular_xp_necessario(self):
        # Fórmula de progressão (exemplo: 1000 * level^1.5)
        return int(1000 * (self.level ** 1.5))

class UserProfile(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    chave_pix = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
