from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from palpites.models import Classificacao
from usuarios.models import Usuario, UserProfile
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
    return render(request,"outros/configuracoes.html")

def termos(request):
    return render(request,"termos/termos.html")

def privacidade(request):
    return render(request,"termos/privacidade.html")
