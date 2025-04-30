# apps/premios/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from premios.models import TipoTrofeu, MetaConquista, ConquistaUsuario, HistoricoConquista

@login_required
def minhas_conquistas(request):
    conquistas = ConquistaUsuario.objects.filter(
        usuario=request.user
    ).select_related('meta')

    # Separar conquistas concluídas e em progresso
    concluidas = conquistas.filter(concluida=True)
    em_progresso = conquistas.filter(concluida=False)

    # Metas não iniciadas
    metas_nao_iniciadas = MetaConquista.objects.exclude(
        id__in=conquistas.values_list('meta_id', flat=True)
    )

    return render(request, 'premios/conquistas.html', {
        'concluidas': concluidas,
        'em_progresso': em_progresso,
        'metas_nao_iniciadas': metas_nao_iniciadas,
    })

@login_required
def meus_premios(request):
    premios = PremioUsuario.objects.filter(
        usuario=request.user
    ).select_related('premio').order_by('-data_premiacao')

    return render(request, 'premios/premios.html', {
        'premios': premios,
    })


def trofeus(request):
    usuario = request.user

    # Buscar todas as conquistas do usuário (comcluídas e em progresso)
    conquistas_usuario = ConquistaUsuario.objects.filter(usuario=usuario).select_related('meta__tipo_trofeu')
    historico = HistoricoConquista.objects.filter(usuario=usuario).order_by('-data_conquista')[:10]
    # Separar conquistas concluídas e em progresso
    conquistas_concluidas = conquistas_usuario.filter(concluida=True)
    conquistas_em_progresso = conquistas_usuario.filter(concluida=False)

    # Buscar todos os troféus disponíveis (para a seção "Troféus")
    todos_trofeus = TipoTrofeu.objects.all()

    context = {
        'conquistas_concluidas': conquistas_concluidas,
        'conquistas_em_progresso': conquistas_em_progresso,
        'historico_conquistas': historico,
        'todos_trofeus': todos_trofeus,
        'usuario': usuario,
    }

    return render(request, "outros/trofeus.html", context)
