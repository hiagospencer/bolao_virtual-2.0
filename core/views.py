from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Max, Prefetch
import requests
from django.conf import settings
from django.views.decorators.cache import cache_page

from usuarios.models import Usuario, UserProfile, DestaqueDaSemana,Rodada
from premios.models import *
from premios.conquistas import verificar_conquistas
from core.models import PremiacaoBolao
from palpites.models import Classificacao,PontuacaoRodada, Palpite
from palpites.utils import *
from palpites.tasks import *
from .utils import calcular_total_pontos_rodadas_usuarios



def homepage(request):
    usuario_logado = request.user
    ultimo_premio = None
    level_up = False
    new_level = None

    usuarios_pagantes = UserProfile.objects.filter(pagamento=True).values_list('user_id', flat=True)
    destaque = DestaqueDaSemana.objects.order_by('-rodada').first()
    usuario = None
    if request.user.is_authenticated:
        ultimo_premio = Premio.objects.filter(disponivel=True).order_by('-data_criacao').first()
        participante = UserProfile.objects.get(user=usuario_logado)

        # Armazena o nível antes da correção
        nivel_anterior = participante.level

        participante.corrigir_nivel()
        verificar_conquistas(participante)
        # Verifica se houve mudança de nível
        if participante.level > nivel_anterior:
            level_up = True
            new_level = participante.level

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

    titulo_ativo_destaque = None
    if destaque:
        titulo_ativo_destaque = TituloAtivo.objects.select_related('titulo__premio').filter(usuario=destaque.usuario).first()

    pontuacao_rodada = None
    if PontuacaoRodada.objects.all().exists():
        pontuacao_rodada = PontuacaoRodada.objects.filter(usuario=destaque.usuario).order_by('-rodada').first()

    context = {'classificacao': classificacao, "premiacoes":premiacoes, "usuario": usuario, 'destaque': destaque, 'titulo_ativo_destaque': titulo_ativo_destaque,"pontuacao_rodada":pontuacao_rodada, 'ultimo_premio': ultimo_premio,'level_up': level_up,'new_level': new_level,}
    return render(request, 'index.html', context)

@login_required
def perfil(request):
    user = request.user
    usuario = UserProfile.objects.get(user=user)
    context = {"usuario":usuario}
    return render(request, "perfil.html", context)


@login_required
def atualizar_perfil(request):
    if request.method == 'POST':
        try:
            # Obtém os objetos relacionados
            usuario = request.user
            perfil = usuario.userprofile

            # Obtém os dados do formulário
            whatsapp = request.POST.get('whatsapp')
            pix = request.POST.get('pix')
            imagem = request.FILES.get('img')

            # Atualiza os campos do perfil
            if whatsapp is not None:
                perfil.telefone = whatsapp
            if pix is not None:
                perfil.chave_pix = pix

            # Atualiza a foto do usuário (não do perfil)
            if imagem is not None:
                usuario.foto_perfil = imagem

            # Salva as alterações
            perfil.save()
            usuario.save()

            messages.success(request, 'Perfil atualizado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar perfil: {str(e)}')

        return redirect('perfil')
    return redirect('perfil')

def regras(request):
    return render(request,"regras.html")


@user_passes_test(lambda u: u.is_superuser)
def configuracao(request):
    return render(request,"outros/configuracoes.html",{'faixa_rodadas': range(1, 38)},)


@user_passes_test(lambda u: u.is_superuser)
def configurar_rodadas(request):
    if request.method == 'POST':
        rodada_inicial = request.POST.get('rodada_inicial')
        rodada_final = request.POST.get('rodada_final')

        if rodada_inicial and rodada_final:
            setar_rodada_atual_final_task.delay(rodada_inicial, rodada_final)
            print(f'Rodada inicial: {rodada_inicial} - Rodada Final: {rodada_final}')

        messages.success(request, f'Rodada inicial: {rodada_inicial} - Rodada Final: {rodada_final}, setadas com sucesso!')

    return redirect('configuracao')

@user_passes_test(lambda u: u.is_superuser)
def acoes_rodada(request):
    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'criar':
            criar_rodadas_campeonato_task.delay()
            messages.success(request, 'Todas as rodadas criada com sucesso.')
        elif acao == 'apagar':
            resetar_pontuacao_usuarios_task.delay()
            messages.success(request, f'Pontuações dos usuários resetadas.')
        elif acao == 'restaurar':
            messages.info(request, 'Rodada restaurada para o estado original.')

    return redirect('configuracao')

@user_passes_test(lambda u: u.is_superuser)
def atualizar_classificacao(request):
    if request.method == 'POST':
        acao = request.POST.get('acao')
        rodada_atualizar_classificacao = request.POST.get('atualizar_classificacao')
        rodada_original = request.POST.get('rodada_original')
        destaque_rodada = request.POST.get('destaque_rodada')
        rodada_false = request.POST.get('rodada_false')

        if rodada_atualizar_classificacao:
            calcular_pontuacao_usuario_task.delay(rodada_atualizar_classificacao)
            messages.success(request, 'Classificação Atualizada.')

        if rodada_original:
            salvar_rodada_original_task.delay(rodada_original)
            messages.success(request, f'Rodada {rodada_original} criada com sucesso!')

        if destaque_rodada:
            calcular_total_pontos_rodadas_usuarios_task.delay(destaque_rodada)
            messages.success(request, f'Destaque da {destaque_rodada}ª rodada criado com sucesso!')

        if rodada_false:
            resetar_rodadas_task.delay(rodada_false)
            messages.success(request, f'Rodada {rodada_false} criada false com sucesso!')

    return redirect('configuracao')

@user_passes_test(lambda u: u.is_superuser)
def controle_partidas(request):
    if request.method == 'POST':
        acao = request.POST.get('acao')

        if acao == 'bloquear_todas':
            bloquear_rodadas_task.delay()
            messages.warning(request, 'Todas as partidas foram bloqueadas.')
        elif acao == 'desbloquear_todas':
            desbloquear_rodadas_task.delay()
            messages.success(request, 'Todas as partidas foram desbloqueadas.')

    return redirect('configuracao')

def termos(request):
    return render(request,"termos/termos.html")

def privacidade(request):
    return render(request,"termos/privacidade.html")
