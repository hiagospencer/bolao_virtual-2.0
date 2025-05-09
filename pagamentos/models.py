# models.py
from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO
import qrcode
from usuarios.models import Usuario
from pixqrcodegen import Payload



class PagamentoPIX(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('recusado', 'Recusado'),
        ('reembolsado', 'Reembolsado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=30.00)
    chave_pix = models.CharField(max_length=100, default='hiagosouzadev10@gmail.com')
    destinatario = models.CharField(max_length=100, default='Hiago José de Souza')
    cidade = models.CharField(max_length=100, default='Areia Branca')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    codigo_transacao = models.CharField(max_length=100, unique=True)
    qr_code_image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return f"PIX de R${self.valor} - {self.usuario}"

    def gerar_qrcode(self):
        payload = Payload(
        self.destinatario,
        self.chave_pix,
        f"{self.valor:.2f}",
        self.cidade,
        self.codigo_transacao[:35]
        )

        codigo_pix = payload.gerarPayload()

        qr = qrcode.make(codigo_pix)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        file_name = f'qrcode_pix_{self.codigo_transacao}.png'
        self.qr_code_image.save(file_name, ContentFile(buffer.getvalue()), save=False)
        buffer.close()
