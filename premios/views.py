# apps/premios/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from premios.models import TipoTrofeu, MetaConquista, ConquistaUsuario, HistoricoConquista
from usuarios.models import Usuario, UserProfile
from premios.conquistas import verificar_conquistas


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


@login_required
def trofeus(request):
    usuario = request.user
    total_trofeus = MetaConquista.objects.count()
    conquistados = ConquistaUsuario.objects.filter(usuario=usuario, concluida=True).count()
    participante = UserProfile.objects.get(user=usuario)
    participante.corrigir_nivel()
    verificar_conquistas(participante)
    conquistas_usuario = ConquistaUsuario.objects.filter(usuario=usuario).select_related('meta__tipo_trofeu')
    historico = HistoricoConquista.objects.filter(usuario=usuario).order_by('-data_conquista')[:10]
    progresso = int((participante.xp / participante.xp_para_proximo_level) * 100)
    max_level = participante.nivel_maximo

    if total_trofeus > 0:
        porcentagem = round((conquistados / total_trofeus) * 100, 2)
    else:
        porcentagem = 0

    conquistas_concluidas = conquistas_usuario.filter(concluida=True)
    conquistas_em_progresso = conquistas_usuario.filter(concluida=False)


    todos_trofeus = MetaConquista.objects.all()

    context = {
        'conquistas_concluidas': conquistas_concluidas,
        'conquistas_em_progresso': conquistas_em_progresso,
        'historico_conquistas': historico,
        'todos_trofeus': todos_trofeus,
        'usuario': usuario,
        "participante":participante,
        'total_trofeus': total_trofeus,
        'conquistados': conquistados,
        'porcentagem': porcentagem,
        'participante': {
            'xp': participante.xp,
            'level': participante.level,
            'max_level': max_level,
            'xp_necessario': 0 if participante.level == max_level else participante.xp_para_proximo_level,
            'progresso': 0 if participante.level == max_level else int((participante.xp / participante.xp_para_proximo_level) * 100),
            'nivel_maximo_atingido': participante.level == max_level
        },
    }

    return render(request, "outros/trofeus.html", context)
