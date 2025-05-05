from django.shortcuts import render
from palpites.models import Classificacao
from usuarios.models import UserProfile
from premios.models import ConquistaUsuario
from django.db.models import Prefetch
from core.models import PremiacaoBolao


def homepage(request):
    usuarios_pagantes = UserProfile.objects.filter(pagamento=True).values_list('user_id', flat=True)

    usuario = None
    if request.user.is_authenticated:
        try:
            usuario = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            usuario = None  # Caso não tenha um perfil ainda
    premiacoes = PremiacaoBolao.objects.all()
    conquistas_concluidas = Prefetch(
        'usuario__conquistas',
        queryset=ConquistaUsuario.objects.filter(concluida=True).select_related('meta__tipo_trofeu'),
        to_attr='conquistas_ativas'
    )

    classificacao = (
        Classificacao.objects
        .filter(usuario__in=usuarios_pagantes)
        .select_related('usuario')
        .prefetch_related(conquistas_concluidas)
        .order_by('-pontos', '-placar_exato', '-vitorias', '-empates')
    )

    context = {'classificacao': classificacao, "premiacoes":premiacoes, "usuario": usuario}
    return render(request, 'index.html', context)

def perfil(request):
    user = request.user
    usuario = UserProfile.objects.get(user=user)
    context = {"usuario":usuario}
    return render(request, "perfil.html", context)

def regras(request):
    return render(request,"regras.html")

def configuracao(request):
    return render(request,"outros/configuracoes.html")

def termos(request):
    return render(request,"termos/termos.html")

def privacidade(request):
    return render(request,"termos/privacidade.html")
