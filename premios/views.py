# apps/premios/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
import secrets
import string

from usuarios.models import Usuario, UserProfile
from premios.models import *
from premios.conquistas import verificar_conquistas

from .utils import show_alert, json_alert

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
def lista_premios(request):
    usuario = UserProfile.objects.get(user=request.user)
    categorias_premios = CategoriaPremio.objects.all()
    categoria_id = request.GET.get('categoria')

    is_htmx = request.headers.get('HX-Request') == 'true'

    # Filtra prêmios disponíveis (estoque > 0 ou ilimitado)
    premios_disponiveis = Premio.objects.filter(
        disponivel=True
    ).exclude(
        estoque=0
    ).exclude(
        id__in=PedidoPremio.objects.filter(usuario=request.user).values_list('premio_id', flat=True)
    ).order_by('-data_criacao')

    # Aplicar filtro de categoria se existir
    if categoria_id and categoria_id != 'todos':
        premios_disponiveis = premios_disponiveis.filter(categoria_id=categoria_id).order_by('-data_criacao')


    # Prêmios já adquiridos pelo usuário
    premios_adquiridos = Premio.objects.filter(
        pedidopremio__usuario=request.user
    ).distinct()

    if is_htmx:
        return render(request, 'premios/partials/premios_lista.html', {
            'premios_disponiveis': premios_disponiveis
        })

    context = {
        'premios_disponiveis': premios_disponiveis,
        'premios_adquiridos': premios_adquiridos,
        'usuario': usuario,
        "categorias_premios":categorias_premios,
        'categoria_selecionada': categoria_id,
    }
    return render(request, 'premios/conquistas_premios.html', context)


@login_required
def meus_premios(request):
    titulos_adquiridos = PedidoPremio.objects.filter(
        usuario=request.user,
    ).select_related('premio')

    # Título ativo atual
    titulo_ativo = None
    if TituloAtivo.objects.filter(usuario=request.user).exists():
        titulo_ativo = TituloAtivo.objects.get(usuario=request.user).titulo.premio

    context = {
        'titulos_adquiridos': titulos_adquiridos,
        'titulo_ativo': titulo_ativo,
    }
    return render(request, 'premios/meus_premios.html', context)

@login_required
def comprar_premio(request, premio_id):
    usuario = request.user
    premio = get_object_or_404(Premio, id=premio_id, disponivel=True)
    usuario_bolao = UserProfile.objects.get(user=request.user)
    error = None
    success = None
    # Verifica se o usuário já possui o prêmio (exceto para itens sem estoque)
    if PedidoPremio.objects.filter(usuario=usuario, premio=premio).exists() and premio.estoque != -1:
        messages.error(request, "Você já adquiriu este prêmio!")
        return redirect('lista_premios')

    # Verifica moedas e estoque
    if usuario_bolao.moedas < premio.preco_moedas:
        messages.error(request, "Moedas insuficientes!")
        return redirect('lista_premios')

    if premio.estoque == 0:
        messages.error(request, "Prêmio esgotado!")
        return redirect('lista_premios')

    # Realiza a compra
    PedidoPremio.objects.create(usuario=usuario, premio=premio)
    usuario_bolao.moedas -= premio.preco_moedas
    usuario_bolao.save()

    # Atualiza estoque (se não for ilimitado)
    if premio.estoque > 0:
        premio.estoque -= 1
        premio.save()

    messages.success(request, f"Prêmio {premio.nome} adquirido com sucesso!")
    return redirect('meus_premios')

@login_required
def ativar_titulo(request, pedido_id):
    pedido = get_object_or_404(PedidoPremio, id=pedido_id, usuario=request.user)

    # Remove título ativo anterior (se existir)
    TituloAtivo.objects.filter(usuario=request.user).delete()

    # Ativa o novo título
    TituloAtivo.objects.create(usuario=request.user, titulo=pedido)

    messages.success(request, f"Título {pedido.premio.nome} ativado!")
    return redirect('meus_premios')

@login_required
def resgatar_voucher(request, pedido_id):
    pedido = get_object_or_404(
        PedidoPremio,
        id=pedido_id,
        usuario=request.user,
        premio__tipo='voucher'
    )

    if pedido.utilizado:
        messages.error(request, "Este voucher já foi resgatado!")
        return redirect('meus_premios')

    # Gera código único se ainda não existir
    if not pedido.codigo_voucher:
        alphabet = string.ascii_uppercase + string.digits
        codigo = f"BOL{secrets.choice(alphabet)}{secrets.choice(alphabet)}{secrets.choice(string.digits)}"
        pedido.codigo_voucher = codigo
        pedido.data_resgate = timezone.now()
        pedido.save()

    # Verifica validade
    valido = True
    if pedido.premio.data_expiracao and pedido.premio.data_expiracao < timezone.now().date():
        valido = False

    context = {
        'pedido': pedido,
        'valido': valido,
        'whatsapp_link': pedido.premio.whatsapp_loja if pedido.premio.whatsapp_loja else None,
    }
    return render(request, 'premios/resgate_voucher.html', context)

@login_required
def marcar_como_utilizado(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(PedidoPremio, id=pedido_id, usuario=request.user)
        pedido.utilizado = True
        pedido.data_utilizacao = timezone.now()
        pedido.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


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
    conquistas_ids = conquistas_concluidas.values_list('meta_id', flat=True)

    todos_trofeus = MetaConquista.objects.all()

    context = {
        'conquistas_concluidas': conquistas_concluidas,
        'conquistas_em_progresso': conquistas_em_progresso,
        'conquistas_ids': list(conquistas_ids),
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
