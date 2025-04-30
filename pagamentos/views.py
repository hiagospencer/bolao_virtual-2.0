from django.shortcuts import render, get_object_or_404
from .models import PagamentoPIX


def pagamento(request):
    pagamento = get_object_or_404(PagamentoPIX)

    if not pagamento.qr_code_image:
        pagamento.gerar_qrcode()
        pagamento.save()
    return render(request, "outros/pagamento.html",{'pagamento': pagamento})
