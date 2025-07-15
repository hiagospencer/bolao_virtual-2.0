from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.db import models
import uuid
from django.conf import settings

class Usuario(AbstractUser):
    foto_perfil = CloudinaryField('imagem')
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


    def convites_recebidos(self):
        return Convite.objects.filter(convidado=self)

    def convites_enviados(self):
        try:
            codigo = self.codigoconvite
            return codigo.usos.all()
        except CodigoConvite.DoesNotExist:
            return Convite.objects.none()

    def convidados_pagantes(self):
        return self.convites_enviados().filter(convidado__userprofile__pagamento=True).count()

    def total_convidados(self):
        return self.convites_enviados().filter(convidado__isnull=False).count()

    def convidados_pagantes_disponiveis(self):
        convites = self.convites_enviados().filter(convidado__userprofile__pagamento=True)
        usados = Usuario.objects.filter(recompensas_usadas__in=self.recompensas.all())
        return convites.exclude(convidado__in=usados)

    def verificar_e_aplicar_recompensa(self, request=None):
        convites_validos = self.convidados_pagantes_disponiveis()
        if convites_validos.count() >= 3:
            convidados_para_usar = list(convites_validos[:3].values_list('convidado', flat=True))
            recompensa = RecompensaPremium.objects.create(usuario=self)
            recompensa.convidados_utilizados.set(convidados_para_usar)
            recompensa.save()
            if request:
                request.session['mostrar_modal_recompensa'] = True  # <- Sinaliza para o frontend
            return True
        return False

    def total_boloes_premium(self):
        return self.recompensas.count()


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
            recompensa = int(100 * (1.1 ** (self.level - 1)))
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
            recompensa = int(100 * (1.1 ** (self.level - 1)))
            self.moedas += recompensa
            self.xp_para_proximo_level = self.calcular_xp_necessario()
        self.save()


class CodigoConvite(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    codigo = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return f"Código de {self.usuario.username}"


class Convite(models.Model):
    codigo = models.ForeignKey(CodigoConvite, on_delete=models.CASCADE, related_name='usos')
    convidado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='convite_recebido')
    data_aceito = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo.usuario.username} convidou {self.convidado.username if self.convidado else 'Aguardando'}"


class RecompensaPremium(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='recompensas')
    data = models.DateTimeField(auto_now_add=True)
    convidados_utilizados = models.ManyToManyField(Usuario, related_name='recompensas_usadas')

    def __str__(self):
        return f"{self.usuario.username} ganhou Bolão Premium em {self.data.strftime('%d/%m/%Y')}"

class Rodada(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Rodada {self.numero}"


class DestaqueDaSemana(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rodada = models.IntegerField()
    acertos = models.PositiveIntegerField(default=0)
    total_jogos = models.PositiveIntegerField(default=0)
    dica_do_mestre = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rodada', 'usuario')
        ordering = ['-rodada']

    def __str__(self):
        return f"{self.usuario.username} - Rodada {self.rodada}"

    @property
    def porcentagem_acertos(self):
        if not self.total_jogos or self.total_jogos == 0:
            return 0
        return round((self.acertos / self.total_jogos) * 100, 2)
