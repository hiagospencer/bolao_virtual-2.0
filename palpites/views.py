from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils import timezone
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
        rodadas = Rodada.objects.filter(rodada_atual=verificacao_partida.partida_atual)
        if verificacao_partida.partida_atual == verificacao_partida.partida_final:
            verificacao_partida.rodada_bloqueada = True
            verificacao_partida.save()
        # else:
        #     verificacao_partida.rodada_bloqueada = True
        #     verificacao_partida.save()

        for rodada in rodadas:
            time_casa.append(rodada.time_casa)
            time_visitante.append(rodada.time_visitante)
            img_casa.append(rodada.imagem_casa)
            img_visitante.append(rodada.imagem_fora)

        if request.method == "POST":
            dados = request.POST
            resultados = dict(dados)


            if Palpite.objects.filter(rodada_atual=verificacao_partida.partida_atual,usuario=user).exists():
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
                    rodada_atual=verificacao_partida.partida_atual,
                    )
            messages.success(request, f"{verificacao_partida.partida_atual}ª rodada salva com sucesso!")
            verificacao_partida.partida_atual += 1
            verificacao_partida.save()
            return redirect('criar_palpites')
        context = {"rodadas":rodadas, 'verificacao_partida':verificacao_partida,"data_preencher_palpites":data_preencher_palpites}
        return render(request, "palpites/palpites.html",context)


@login_required
def meus_palpites(request):
    user = request.user
    participante = UserProfile.objects.get(id=user.id)
    usuarios = UserProfile.objects.filter(pagamento=True)
    rodadas_distintas = Palpite.objects.values_list('rodada_atual', flat=True).distinct().order_by('rodada_atual')
    rodadas = Palpite.objects.filter(usuario=user).order_by('rodada_atual')[:10]
    rodadas_original = RodadaOriginal.objects.all().order_by('rodada_atual')[:10]

    # Obter todas as configurações de uma vez
    configs_rodadas = {config.numero_rodada: config for config in ConfiguracaoRodada.objects.all()}
    context = {'rodadas':rodadas, "usuarios":usuarios, "rodadas_distintas":range(1, 39), "rodadas_original": rodadas_original,'configs_rodadas': configs_rodadas,"participante":participante}
    return render(request, "palpites/meus_palpites.html", context)


def filtrar_palpites(request):
    usuario_id = request.GET.get("usuario")
    rodada = request.GET.get("rodada")

    try:
        usuario = UserProfile.objects.get(id=usuario_id)
    except (UserProfile.DoesNotExist, ValueError):
        return HttpResponse("Usuário não encontrado", status=404)

    # Verifica se o usuário está tentando editar seus próprios palpites
    is_own_profile = (str(request.user.id) == str(usuario_id))
    palpites = Palpite.objects.filter(usuario__id=usuario_id)
    rodadas_original = RodadaOriginal.objects.all().order_by('rodada_atual')[:10]

    if rodada:
        try:
            rodada_int = int(rodada)
            palpites = palpites.filter(rodada_atual=rodada_int)
            rodadas_original = RodadaOriginal.objects.filter(rodada_atual=rodada_int)

            # Verificar se a rodada pode ser editada
            config_rodada = ConfiguracaoRodada.objects.filter(numero_rodada=rodada_int).first()
            editavel = (config_rodada.editar_rodada if config_rodada else False) and is_own_profile

            # Verifica data limite se existir
            if editavel and config_rodada and config_rodada.data_limite_edicao:
                editavel = timezone.now() < config_rodada.data_limite_edicao
        except ValueError:
            return HttpResponse("Rodada inválida", status=400)

    context = {
        'rodadas': palpites,
        'usuario': usuario,
        'rodada_atual': rodada,
        'rodadas_original': rodadas_original,
        'editavel': editavel if rodada else False,
        'is_own_profile': is_own_profile
    }
    html = render_to_string('palpites/partials/palpites_lista.html', context)
    return HttpResponse(html)


@login_required
@require_http_methods(["GET", "POST"])
def editar_palpite(request, palpite_id):
    try:
        palpite = Palpite.objects.get(id=palpite_id, usuario=request.user)
        # Verificação EXTRA de segurança
        if palpite.usuario.id != request.user.id:
            return JsonResponse({
                'status': 'error',
                'message': 'Você só pode editar seus próprios palpites'
            }, status=403)

    except Palpite.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Palpite não encontrado'
        }, status=404)
    except Palpite.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Palpite não encontrado'}, status=404)

    # Verificar se a rodada pode ser editada
    config_rodada = ConfiguracaoRodada.objects.filter(numero_rodada=palpite.rodada_atual).first()
    if not config_rodada or not config_rodada.editar_rodada:
        return JsonResponse({'status': 'error', 'message': 'Edição não permitida para esta rodada'}, status=403)

    if config_rodada.data_limite_edicao and timezone.now() > config_rodada.data_limite_edicao:
        return JsonResponse({'status': 'error', 'message': 'Prazo para edição expirado'}, status=403)

    if request.method == 'GET':
        context = {'palpite': palpite}
        return render(request, 'palpites/partials/editar_palpite_form.html', context)

    placar_casa = request.POST.get('placar_casa')
    placar_visitante = request.POST.get('placar_visitante')

    try:
        palpite.placar_casa = int(placar_casa)
        palpite.placar_visitante = int(placar_visitante)
        palpite.save()
        return JsonResponse({'status': 'success'})
    except (ValueError, TypeError) as e:
        print(f"Erro ao converter placar: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Placar inválido'}, status=400)
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Erro ao salvar palpite'}, status=500)
