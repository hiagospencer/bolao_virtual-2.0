from django.shortcuts import render
from .utils import *
from .models import *

def criar_palpites(request):
    if request.user.is_authenticated:
        user = request.user
        verificacao_partida, criado = BloquearPartida.objects.get_or_create(usuario=user)
        rodadas = Rodada.objects.filter(rodada_atual=verificacao_partida.rodada_atual)

        if request.method == "POST":
            dados = request.POST
            resultados = dict(dados)
            print(resultados)
        context = {"rodadas":rodadas, 'verificacao_partida':verificacao_partida}
    return render(request, "palpites/palpites.html",context)

def meus_palpites(request):

    return render(request, "palpites/meus_palpites.html")
