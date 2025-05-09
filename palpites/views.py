from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
import pytz
import pandas as pd

from .utils import *
from .models import *
from usuarios.models import UserProfile


@login_required
def criar_palpites(request):
    todos = UserProfile.objects.filter(pagamento=True)
    data_preencher_palpites = DataBolao.objects.all().order_by('data_final').first()

    if request.user.is_authenticated:
        user = request.user
        time_casa = []
        time_visitante = []
        rodada_dict = []
        placar_casa = []
        placar_visitante = []
        img_casa = []
        img_visitante = []
        verificacao_partida, criado = BloquearPartida.objects.get_or_create(usuario=user)
        rodadas = Rodada.objects.filter(rodada_atual=verificacao_partida.rodada_atual)

        if verificacao_partida.rodada_atual <= verificacao_partida.partida_final:
            verificacao_partida.rodada_bloqueada = False
            verificacao_partida.save()
        else:
            verificacao_partida.rodada_bloqueada = True
            verificacao_partida.save()

        for rodada in rodadas:
            time_casa.append(rodada.time_casa)
            time_visitante.append(rodada.time_visitante)
            img_casa.append(rodada.imagem_casa)
            img_visitante.append(rodada.imagem_fora)

        if request.method == "POST":
            dados = request.POST
            resultados = dict(dados)


            if Palpite.objects.filter(rodada_atual=verificacao_partida.rodada_atual,usuario=user).exists():
                return HttpResponse('Rodada já existe')

            if resultados["resultado_casa"] and resultados["resultado_visitante"]:

                for resultado_casa in resultados["resultado_casa"]:
                    placar_casa.append(resultado_casa)

                for resultado_visitante in resultados["resultado_visitante"]:
                    placar_visitante.append(resultado_visitante)

            resultado_tabela = {
                    "time_casa": time_casa,
                    "img_casa": img_casa,
                    "placar_casa": placar_casa,
                    "placar_visitante": placar_visitante,
                    "time_visitante": time_visitante,
                    "img_visitante": img_visitante,
            }

            df_tabela = pd.DataFrame(resultado_tabela)
            for _, row in df_tabela.iterrows():
                jogos_rodada_criado  = Palpite.objects.create(
                    time_casa=row['time_casa'],
                    imagem_casa=row['img_casa'],
                    placar_casa=row['placar_casa'],
                    placar_visitante=row['placar_visitante'],
                    time_visitante=row['time_visitante'],
                    imagem_fora=row['img_visitante'],
                    usuario=user,
                    rodada_atual=verificacao_partida.rodada_atual,
                    )


            messages.success(request, f"{verificacao_partida.rodada_atual}ª rodada salva com sucesso!")
            verificacao_partida.rodada_atual += 1
            verificacao_partida.save()
            return redirect('criar_palpites')
        context = {"rodadas":rodadas, 'verificacao_partida':verificacao_partida,"data_preencher_palpites":data_preencher_palpites}
        return render(request, "palpites/palpites.html",context)


@login_required
def meus_palpites(request):
    user = request.user

    usuarios = UserProfile.objects.filter(pagamento=True)
    rodadas_distintas = Palpite.objects.values_list('rodada_atual', flat=True).distinct().order_by('rodada_atual')
    rodadas = Palpite.objects.filter(usuario=user).order_by('rodada_atual')[:10]
    rodadas_original = RodadaOriginal.objects.all().order_by('rodada_atual')[:10]
    context = {'rodadas':rodadas, "usuarios":usuarios, "rodadas_distintas":rodadas_distintas, "rodadas_original": rodadas_original}
    return render(request, "palpites/meus_palpites.html", context)


def filtrar_palpites(request):
    usuario_id = request.GET.get("usuario")
    rodada = request.GET.get("rodada")
    usuario = UserProfile.objects.get(id=usuario_id)
    palpites = Palpite.objects.all()
    rodadas_original = RodadaOriginal.objects.all().order_by('rodada_atual')[:10]

    if usuario_id:
        palpites = palpites.filter(usuario__id=usuario_id)

    if rodada:
        palpites = palpites.filter(rodada_atual=rodada)
        rodadas_original = RodadaOriginal.objects.filter(rodada_atual=rodada)
    context = {
        'rodadas': palpites,
        "usuario":usuario,
        "rodada_atual": rodada,
        "rodadas_original": rodadas_original
    }
    html = render_to_string('palpites/partials/palpites_lista.html', context)
    return HttpResponse(html)
