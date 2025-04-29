from django.db import models
from usuarios.models import Usuario

class PagamentoPIX(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('recusado', 'Recusado'),
        ('reembolsado', 'Reembolsado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    chave_pix = models.CharField(max_length=100)
    destinatario = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    codigo_transacao = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"PIX de R${self.valor} - {self.usuario}"

    def gerar_qrcode(self):
        # Lógica para gerar QR Code PIX
        payload = {
            "chave": self.chave_pix,
            "valor": float(self.valor),
            "nome": self.destinatario,
            "cidade": "Rio de Janeiro",
            "txId": self.codigo_transacao[:25]
        }
        # Implementação real dependerá da API PIX utilizada
        return payload
