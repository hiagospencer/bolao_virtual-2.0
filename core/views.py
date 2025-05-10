from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.db.models import Prefetch

from usuarios.models import Usuario, UserProfile, DestaqueDaSemana,Rodada
from premios.models import *
from core.models import PremiacaoBolao
from palpites.models import Classificacao,PontuacaoRodada, Palpite
from palpites.utils import *


def homepage(request):
    usuarios_pagantes = UserProfile.objects.filter(pagamento=True).values_list('user_id', flat=True)
    destaque = DestaqueDaSemana.objects.order_by('-rodada__numero').first()

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

    titulo_ativo_destaque = None
    if destaque:
        titulo_ativo_destaque = TituloAtivo.objects.select_related('titulo__premio').filter(usuario=destaque.usuario).first()

    pontuacao_rodada = None
    if PontuacaoRodada.objects.all().exists():
        pontuacao_rodada = PontuacaoRodada.objects.filter(usuario=destaque.usuario).first()

    context = {'classificacao': classificacao, "premiacoes":premiacoes, "usuario": usuario, 'destaque': destaque, 'titulo_ativo_destaque': titulo_ativo_destaque,"pontuacao_rodada":pontuacao_rodada}
    return render(request, 'index.html', context)

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

def configuracao(request):
    return render(request,"outros/configuracoes.html",{'faixa_rodadas': range(1, 38)},)

def configurar_rodadas(request):
    if request.method == 'POST':
        rodada_inicial = request.POST.get('rodada_inicial')
        rodada_final = request.POST.get('rodada_final')

        if rodada_inicial and rodada_final:
            setar_rodadaAtual_rodadaFinal(rodada_inicial, rodada_final)
            print(f'Rodada inicial: {rodada_inicial} - Rodada Final: {rodada_final}')

        messages.success(request, 'Rodadas configuradas com sucesso.')

    return redirect('configuracao')


def acoes_rodada(request):
    if request.method == 'POST':
        acao = request.POST.get('acao')
        if acao == 'criar':
            criar_rodadas_campeonato()
            messages.success(request, 'Todas as rodadas criada com sucesso.')
        elif acao == 'apagar':
            resetar_pontuacao_usuarios()
            messages.success(request, f'Pontuações dos usuários resetadas.')
        elif acao == 'restaurar':
            messages.info(request, 'Rodada restaurada para o estado original.')

    return redirect('configuracao')

def atualizar_classificacao(request):
    if request.method == 'POST':
        acao = request.POST.get('acao')
        rodada_atualizar_classificacao = request.POST.get('atualizar_classificacao')
        rodada_original = request.POST.get('rodada_original')
        rodada_false = request.POST.get('rodada_false')

        if rodada_atualizar_classificacao:
            calcular_pontuacao_usuario(rodada_atualizar_classificacao)
            messages.success(request, 'Classificação Atualizada.')
        if rodada_original:
            salvar_rodada_original(rodada_original)
            messages.warning(request, f'Rodada {rodada_original} criada com sucesso!')
        if rodada_false:
            rodadas_false(rodada_false)
            messages.warning(request, f'Rodada {rodada_false} criada false com sucesso!')

    return redirect('configuracao')

def controle_partidas(request):
    if request.method == 'POST':
        acao = request.POST.get('acao')

        if acao == 'bloquear_todas':
            bloquear_rodadas()
            messages.warning(request, 'Todas as partidas foram bloqueadas.')
        elif acao == 'desbloquear_todas':
            desbloquear_rodadas()
            messages.success(request, 'Todas as partidas foram desbloqueadas.')

    return redirect('configuracao')

def termos(request):
    return render(request,"termos/termos.html")

def privacidade(request):
    return render(request,"termos/privacidade.html")
