# models.py
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
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
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=30.00)
    chave_pix = models.CharField(max_length=100, default='hiaguinhospencer@gmail.com')
    destinatario = models.CharField(max_length=100, default='Hiago José de Souza')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    codigo_transacao = models.CharField(max_length=100, unique=True)
    qr_code_image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return f"PIX de R${self.valor} - {self.usuario}"

    def gerar_qrcode(self):
        payload = f"pix:chave={self.chave_pix}&nome={self.destinatario}&valor={self.valor}&txid={self.codigo_transacao[:25]}"
        qr = qrcode.make(payload)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        file_name = f'qrcode_pix_{self.codigo_transacao}.png'
        self.qr_code_image.save(file_name, ContentFile(buffer.getvalue()), save=False)
        buffer.close()
