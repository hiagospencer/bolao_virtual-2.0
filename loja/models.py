# apps/loja/models.py
from django.db import models
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField

from usuarios.models import Usuario


class Loja(models.Model):
    nome = models.CharField(max_length=100)
    dono = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    descricao = models.TextField(blank=True)
    logo = CloudinaryField('imagem')
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    cor_primaria = models.CharField(max_length=7, default='#6c757d',
                                  help_text="Cor primária no formato HEX (#RRGGBB)")
    cor_secundaria = models.CharField(max_length=7, default='#495057',
                                    help_text="Cor secundária no formato HEX (#RRGGBB)")
    cor_texto = models.CharField(max_length=7, default='#ffffff',
                                help_text="Cor do texto no formato HEX (#RRGGBB)")

    def __str__(self):
        return self.nome


class CategoriaItem(models.Model):
    nome = models.CharField(max_length=50,blank=True, null=True)
    icone = models.CharField(max_length=50,blank=True, null=True)

    def __str__(self):
        return self.nome


class ItemLoja(models.Model):
    TIPO_ITEM = [
        ('camisa', 'Camisa'),
        ('camiseta', 'Camiseta'),
        ('calcao', 'Calção'),
        ('basquete', 'Camisa de Basquete'),
        ('acessorios', 'Acessórios'),
        ('games', 'Games'),
    ]

    nome = models.CharField(max_length=100)
    descricao = RichTextField()
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name='itens', blank=True, null=True)
    categoria = models.ForeignKey(CategoriaItem, on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_ITEM)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem_preview = CloudinaryField('imagem')
    disponivel = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    telefone = models.CharField(max_length=20,blank=True, null=True)
    whatsapp_link = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return self.nome if self.nome else "Item sem nome"

    def save(self, *args, **kwargs):
        if not self.whatsapp_link and self.telefone:
            self.whatsapp_link = f"https://wa.me/{self.telefone}"
        super().save(*args, **kwargs)


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
