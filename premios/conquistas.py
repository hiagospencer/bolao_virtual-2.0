from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from premios.models import MetaConquista, ConquistaUsuario, HistoricoConquista, TipoTrofeu
from palpites.models import Classificacao
from usuarios.models import Usuario


# Relaciona tipo de meta com o campo da Classificacao (para metas simples)
TIPOS_META_CAMPO = {
    'placar_exato': 'placar_exato',
    'pontos_totais': 'pontos',
    'vitorias': 'vitorias',
    'empates': 'empates',
    'posicao_atual': 'posicao_atual',
}

# Metas compostas com lógica personalizada
METAS_COMPOSTAS = {
    'sequencia': {
        'condicao': lambda c: (c.vitorias or 0) >= 15 and (c.placar_exato or 0) >= 7,
        'descricao': 'Troféu para táticos impecáveis com +15 vitórias e +7 placares exatos',
    },
}

def verificar_conquistas(participante, request=None):

    try:
        classificacao = Classificacao.objects.get(usuario=participante.user)
    except Classificacao.DoesNotExist:
        return

    # Verificar metas simples
    for tipo, campo in TIPOS_META_CAMPO.items():
        progresso = getattr(classificacao, campo, 0) or 0
        meta = MetaConquista.objects.filter(tipo__codigo=tipo).first()
        if not meta:
            continue
        if progresso >= meta.valor_requerido:
            conquista, created = ConquistaUsuario.objects.get_or_create(
                usuario=participante.user,
                meta=meta,
                defaults={"progresso_atual": progresso, "concluida": True}
            )
            if created:
                level_up, moedas = participante.adicionar_xp(meta.xp_recompensa)
                participante.moedas += meta.moedas_recompensa
                participante.save()

                HistoricoConquista.objects.create(
                    usuario=participante.user,
                    meta=meta,
                    xp_ganho=meta.xp_recompensa,
                    moedas_ganhas=meta.moedas_recompensa
                )

                if request and level_up:
                    messages.success(request, f"Level up! Agora você é nível {participante.level}")
                if request:
                    messages.success(request, f"Conquista desbloqueada: {meta.nome}")

    # Verificar metas compostas
    for tipo, dados in METAS_COMPOSTAS.items():
        if dados['condicao'](classificacao):
            meta = MetaConquista.objects.filter(tipo__codigo=tipo).first()
            if not meta:
                continue
            conquista, created = ConquistaUsuario.objects.get_or_create(
                usuario=participante.user,
                meta=meta,
                defaults={"progresso_atual": 100, "concluida": True}
            )
            if created:
                level_up, moedas = participante.adicionar_xp(meta.xp_recompensa)
                participante.moedas += meta.moedas_recompensa
                participante.save()

                HistoricoConquista.objects.create(
                    usuario=participante.user,
                    meta=meta,
                    xp_ganho=meta.xp_recompensa,
                    moedas_ganhas=meta.moedas_recompensa
                )

                if request and level_up:
                    messages.success(request, f"Level up! Agora você é nível {participante.level}")
                if request:
                    messages.success(request, f"Conquista desbloqueada: {meta.nome}")

    # Verificar meta "colecionador"
    meta_colecionador = MetaConquista.objects.filter(tipo__codigo="colecionador").first()
    if meta_colecionador:
        total_metas = MetaConquista.objects.exclude(tipo__codigo="colecionador").count()
        total_conquistadas = ConquistaUsuario.objects.filter(
            usuario=participante.user, concluida=True
        ).exclude(meta__tipo__codigo="colecionador").count()

        if total_conquistadas >= total_metas:
            conquista, created = ConquistaUsuario.objects.get_or_create(
                usuario=participante.user,
                meta=meta_colecionador,
                defaults={"progresso_atual": 1, "concluida": True}
            )
            if created:
                level_up, moedas = participante.adicionar_xp(meta_colecionador.xp_recompensa)
                participante.moedas += meta_colecionador.moedas_recompensa
                participante.save()

                HistoricoConquista.objects.create(
                    usuario=participante.user,
                    meta=meta_colecionador,
                    xp_ganho=meta_colecionador.xp_recompensa,
                    moedas_ganhas=meta_colecionador.moedas_recompensa
                )

                if request and level_up:
                    messages.success(request, f"Level up! Agora você é nível {participante.level}")
                if request:
                    messages.success(request, f"Conquista desbloqueada: {meta_colecionador.nome}")
