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

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    chave_pix = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
