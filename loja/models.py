# apps/loja/models.py
from django.db import models
from usuarios.models import Usuario

class CategoriaItem(models.Model):
    nome = models.CharField(max_length=50)
    icone = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class ItemLoja(models.Model):
    TIPO_ITEM = [
        ('badge', 'Emblema'),
        ('boost', 'Boost'),
        ('theme', 'Tema'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.ForeignKey(CategoriaItem, on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_ITEM)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='itens_loja/')
    disponivel = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class InventarioUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemLoja, on_delete=models.CASCADE)
    data_compra = models.DateTimeField(auto_now_add=True)
    utilizado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario', 'item')

    def __str__(self):
        return f"{self.usuario} - {self.item}"

class Transacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f"Transação de {self.usuario} - R${self.valor}"
