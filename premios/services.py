# apps/premios/services.py
from django.utils import timezone
from .models import MetaConquista, ConquistaUsuario
from palpites.models import Palpite
from usuarios.models import Usuario


class VerificadorConquistas:
    @classmethod
    def verificar_meta_usuario(cls, usuario, filtro_func):
        metas = MetaConquista.objects.all()
        for meta in metas:
            if not filtro_func(meta):
                continue

            conquista, created = ConquistaUsuario.objects.get_or_create(
                usuario=usuario,
                meta=meta,
                defaults={'progresso_atual': 0, 'concluida': False}
            )

            if conquista.concluida:
                continue

            progresso = cls._calcular_progresso(usuario, meta)

            conquista.progresso_atual = progresso
            if progresso >= meta.valor_requerido:
                conquista.concluida = True
                conquista.data_conquista = timezone.now()
                cls._recompensar_usuario(usuario, meta)
            conquista.save()

    @classmethod
    def _calcular_progresso(cls, usuario, meta):
        classificacao = Classificacao.objects.get(usuario=usuario)

        if meta.tipo == 'total_conquistas':
            # Verifica se o usuário completou TODAS as metas (exceto esta)
            total_metas = MetaConquista.objects.exclude(id=meta.id).count()
            conquistas_completas = ConquistaUsuario.objects.filter(
                usuario=usuario,
                concluida=True
            ).count()
            return 1 if conquistas_completas >= total_metas else 0

        elif meta.tipo == 'sequencia_vitorias':
            # Maior sequência de vitórias em uma rodada (exemplo simplificado)
            palpites = Palpite.objects.filter(
                usuario=usuario,
                rodada_atual=Rodada.objects.latest('id'),  # Última rodada
                vitorias__gt=0  # Palpites corretos
            ).order_by('id')
            streak = 0
            max_streak = 0
            for palpite in palpites:
                streak = streak + 1 if palpite.vitorias > 0 else 0
                max_streak = max(max_streak, streak)
            return 1 if max_streak >= meta.valor_requerido else 0

        elif meta.tipo == 'melhor_rodada':
            # Verifica se o usuário já foi 1º em alguma rodada (usar histórico)
            return 1 if HistoricoRanking.objects.filter(
                usuario=usuario,
                posicao=1
            ).exists() else 0

        elif meta.tipo == 'pontos_totais':
            return 1 if classificacao.pontos >= meta.valor_requerido else 0

        elif meta.tipo == 'combinada':
            # 15 vitórias E 10 placares exatos
            return 1 if (
                classificacao.vitorias >= 15 and
                classificacao.placar_exato >= 10
            ) else 0

        elif meta.tipo == 'vitorias':
            return classificacao.vitorias

        return 0


    @classmethod
    def _recompensar_usuario(cls, usuario, meta):
        usuario.xp += meta.xp_recompensa
        usuario.moedas += meta.moedas_recompensa
        usuario.save()

        # Registrar no histórico
        HistoricoConquista.objects.create(
            usuario=usuario,
            meta=meta,
            xp_ganho=meta.xp_recompensa,
            moedas_ganhas=meta.moedas_recompensa
        )

        # Verificar level up (opcional)
        cls._verificar_level_up(usuario)

    @classmethod
    def _verificar_level_up(cls, usuario):
        niveis = {1: 1000, 2: 2500, 3: 5000}  # Exemplo customizável
        for level, xp_necessario in niveis.items():
            if usuario.xp >= xp_necessario and usuario.level < level:
                usuario.level = level
                usuario.save()
                break
