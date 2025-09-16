from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import PagamentoPIX
import uuid


@login_required
def pagamento(request):
    usuario = request.user
    pagamento = PagamentoPIX.objects.filter(usuario=usuario, status='pendente').first()

    if not pagamento:
        codigo_transacao = str(uuid.uuid4()).replace("-", "")[:25]  # Sem hífens
        pagamento = PagamentoPIX.objects.create(
            usuario=usuario,
            valor=30.00,
            chave_pix='hiaguinhospencer@gmail.com',
            destinatario='Hiago Jose de Souza',
            cidade='Areia Branca',
            codigo_transacao=codigo_transacao
        )

    if not pagamento.qr_code_image:
        pagamento.gerar_qrcode()
        pagamento.save()

    return render(request, "outros/pagamento.html", {'pagamento': pagamento})
