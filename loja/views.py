from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import *


def loja(request):
    categoria_id = request.GET.get('categoria')
    loja_id = request.GET.get('loja')

    is_htmx = request.headers.get('HX-Request') == 'true'
    # Obter todos os produtos inicialmente
    produtos = ItemLoja.objects.all().order_by("-data_criacao")

    # Aplicar filtros se existirem
    if categoria_id and categoria_id != 'all':
        produtos = produtos.filter(categoria__id=categoria_id)

    if loja_id and loja_id != 'all':
        produtos = produtos.filter(loja__id=loja_id)

    # Obter todas as categorias e lojas para os dropdowns
    categorias = CategoriaItem.objects.all()
    lojas = Loja.objects.filter(ativo=True)

    context = {
        "produtos": produtos,
        'categorias': categorias,
        'lojas': lojas,
        'categoria_selecionada': categoria_id or 'all',
        'loja_selecionada': loja_id or 'all',
    }

    if is_htmx:
        html = render_to_string("outros/partials/produtos_grid.html", context)
        return HttpResponse(html)

    return render(request, "outros/shop.html", context)
