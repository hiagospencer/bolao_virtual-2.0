# apps/premios/services.py
from django.utils import timezone
from .models import MetaConquista, ConquistaUsuario
from palpites.models import Palpite
from usuarios.models import Usuario

class VerificadorConquistas:
    @classmethod
    def verificar_meta_usuario(cls, usuario, meta):
        conquista, created = ConquistaUsuario.objects.get_or_create(
            usuario=usuario,
            meta=meta,
            defaults={'progresso_atual': 0, 'concluida': False}
        )

        if conquista.concluida:
            return

        progresso = cls._calcular_progresso(usuario, meta)

        conquista.progresso_atual = progresso
        if progresso >= meta.valor_requerido:
            conquista.concluida = True
            conquista.data_conquista = timezone.now()
            cls._recompensar_usuario(usuario, meta)
        conquista.save()

    @classmethod
    def _calcular_progresso(cls, usuario, meta):
        if meta.tipo == 'placar_exato':
            return Palpite.objects.filter(
                usuario=usuario,
                placar_exato=True  # Assumindo campo booleano no Palpite
            ).count()

        elif meta.tipo == 'pontos_rodada':
            from palpites.models import Rodada  # Supondo que existe
            return Rodada.objects.filter(
                palpites__usuario=usuario,
                palpites__pontos__gte=meta.valor_requerido
            ).distinct().count()

        elif meta.tipo == 'sequencia':
            # Implementar lógica de sequência (ex: maior streak de acertos)
            pass

        elif meta.tipo == 'top_ranking':
            from ranking.models import PosicaoRanking  # Modelo hipotético
            return PosicaoRanking.objects.filter(
                usuario=usuario,
                posicao__lte=meta.valor_requerido
            ).count()

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
