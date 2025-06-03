# apps/premios/models.py
from django.db import models
from cloudinary.models import CloudinaryField

from usuarios.models import Usuario
from loja.models import Loja

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


class TipoMeta(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class MetaConquista(models.Model):
    tipo_trofeu = models.ForeignKey(TipoTrofeu, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo = models.ForeignKey(TipoMeta, on_delete=models.CASCADE)
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


class CategoriaPremio(models.Model):
    nome = models.CharField(max_length=50)  # Ex.: "Títulos", "Vouchers", "Produtos"
    icone = models.CharField(max_length=30, blank=True)  # Opcional: para exibir ícones (ex.: "fa-trophy")

    def __str__(self):
        return self.nome


class Premio(models.Model):
    TIPO_CHOICES = [
        ('titulo', 'Título/Apelido'),
        ('voucher', 'Voucher de Desconto'),
        ('produto', 'Produto Físico'),
        ('moeda', 'Moedas Extras'),
    ]

    nome = models.CharField(max_length=100)  # Ex.: "O Profeta"
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='titulo')
    categoria = models.ForeignKey(CategoriaPremio, on_delete=models.SET_NULL, null=True)
    descricao = models.TextField()  # Ex.: "Estudo estatísticas como um oráculo..."
    preco_moedas = models.PositiveIntegerField(default=100)
    imagem = CloudinaryField('imagem',null=True,blank=True)  # Opcional
    estoque = models.PositiveIntegerField(default=1)  # -1 = ilimitado
    disponivel = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    loja = models.ForeignKey(
        'loja.Loja',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Loja Parceira"
    )
    url_parceiro = models.URLField(blank=True)
    valor_desconto = models.CharField(max_length=20, blank=True, null=True)
    data_expiracao = models.DateField(null=True, blank=True)
    whatsapp_loja = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class PedidoPremio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    premio = models.ForeignKey(Premio, on_delete=models.CASCADE)
    data_compra = models.DateTimeField(auto_now_add=True)
    utilizado = models.BooleanField(default=False)  # Para vouchers/produtos resgatados
    codigo_voucher = models.CharField(max_length=20, blank=True, null=True)
    data_resgate = models.DateTimeField(null=True, blank=True)
    data_utilizacao = models.DateTimeField(null=True, blank=True)
    utilizado = models.BooleanField(default=False)
    data_expiracao = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.premio.nome}"

class TituloAtivo(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    titulo = models.ForeignKey(PedidoPremio, on_delete=models.CASCADE, limit_choices_to={'premio__tipo': 'titulo'})

    def __str__(self):
        return f"Título ativo de {self.usuario.username}: {self.titulo.premio.nome}"



class PremioUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='premios')
    premio = models.ForeignKey(Premio, on_delete=models.CASCADE)
    data_premiacao = models.DateTimeField(auto_now_add=True)
    valor_recebido = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario} - {self.premio} (R${self.valor_recebido})"


class HistoricoConquista(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historico')
    meta = models.ForeignKey(MetaConquista, on_delete=models.CASCADE)
    data_conquista = models.DateTimeField(auto_now_add=True)
    xp_ganho = models.PositiveIntegerField()
    moedas_ganhas = models.PositiveIntegerField()

    class Meta:
        ordering = ['-data_conquista']

    def __str__(self):
        return f"{self.usuario} conquistou {self.meta} em {self.data_conquista}"
