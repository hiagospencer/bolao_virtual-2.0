from django.shortcuts import render
from .models import *


def loja(request):
    produtos = ItemLoja.objects.all().order_by("-data_criacao")
    categorias = CategoriaItem.objects.all()
    context = {"produtos": produtos, 'categorias':categorias}
    return render(request, "outros/shop.html", context)
