from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.template.loader import render_to_string
from .models import *


def loja(request):
    categoria_id = request.GET.get('categoria', 'all')
    loja_id = request.GET.get('loja', 'all')

    is_htmx = request.headers.get('HX-Request') == 'true'
    # Obter todos os produtos inicialmente
    produtos = ItemLoja.objects.all().order_by("-data_criacao")
    lojas = Loja.objects.filter(ativo=True)\
                .annotate(num_itens=Count('itens'))\
                .filter(num_itens__gt=0)


    if loja_id != 'all':
        produtos = produtos.filter(loja__id=loja_id)
        # Filtra categorias apenas da loja selecionada
        categorias = CategoriaItem.objects.filter(
            itemloja__loja__id=loja_id
        ).distinct()
    else:
        categorias = CategoriaItem.objects.all()

    # Obter todas as categorias e lojas para os dropdowns
    if categoria_id != 'all':
        produtos = produtos.filter(categoria__id=categoria_id)

    loja_selecionada = Loja.objects.filter(id=loja_id).first() if loja_id != 'all' else None

    context = {
        "produtos": produtos,
        'categorias': categorias,
        'lojas': lojas,
        'categoria_selecionada': categoria_id,
        'loja_selecionada': loja_id,
        'loja_obj': loja_selecionada,
    }

    if is_htmx:
        html = render_to_string("outros/partials/produtos_grid.html", context)
        return HttpResponse(html)

    return render(request, "outros/shop.html", context)


def loja_api_detail(request, pk):
    loja = get_object_or_404(Loja, pk=pk)
    data = {
        'id': loja.id,
        'nome': loja.nome,
        'descricao': loja.descricao,
        'cor_primaria': loja.cor_primaria,
        'cor_secundaria': loja.cor_secundaria,
        'cor_texto': loja.cor_texto,
        'logo': loja.logo.url if loja.logo else None,
    }
    return JsonResponse(data)
