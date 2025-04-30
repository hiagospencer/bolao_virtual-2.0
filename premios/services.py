# apps/premios/services.py
from django.utils import timezone
from .models import MetaConquista, ConquistaUsuario
from palpites.models import Palpite
from usuarios.models import Usuario

class VerificadorConquistas:
    @classmethod
    def verificar_todos_usuarios(cls):
        usuarios = Usuario.objects.all()
        for usuario in usuarios:
            cls.verificar_usuario(usuario)

    @classmethod
    def verificar_usuario(cls, usuario):
        metas = MetaConquista.objects.all()
        for meta in metas:
            cls.verificar_meta_usuario(usuario, meta)

    @classmethod
    def verificar_meta_usuario(cls, usuario, meta):
        conquista, created = ConquistaUsuario.objects.get_or_create(
            usuario=usuario,
            meta=meta,
            defaults={'progresso_atual': 0, 'concluida': False}
        )

        if conquista.concluida:
            return

        progresso = 0

        if meta.tipo == 'placar_exato':
            progresso = Palpite.objects.filter(
                usuario=usuario,
                pontos_ganhos=5  # Assumindo que 5 pontos é placar exato
            ).count()

        elif meta.tipo == 'pontos_rodada':
            # Aqui precisaríamos de um model Rodada para agrupar por rodada
            # Esta é uma implementação simplificada
            pass

        elif meta.tipo == 'sequencia':
            # Verificar maior sequência de palpites corretos
            pass

        elif meta.tipo == 'participacao':
            progresso = Palpite.objects.filter(
                usuario=usuario
            ).values('partida__rodada').distinct().count()

        elif meta.tipo == 'top_ranking':
            # Depende da sua implementação de ranking
            pass

        # Atualizar progresso
        conquista.progresso_atual = progresso

        # Verificar se a meta foi atingida
        if progresso >= meta.valor_requerido:
            conquista.concluida = True
            cls.recompensar_usuario(usuario, meta)

        conquista.save()

    @classmethod
    def recompensar_usuario(cls, usuario, meta):
        # Adicionar XP
        usuario.xp += meta.xp_recompensa

        # Adicionar moedas virtuais
        usuario.moedas_virtuais += meta.moedas_recompensa

        # Verificar level up
        cls.verificar_level_up(usuario)

        usuario.save()

    @classmethod
    def verificar_level_up(cls, usuario):
        xp_necessario = usuario.level * 1000  # Exemplo simples
        if usuario.xp >= xp_necessario:
            usuario.level += 1
            usuario.xp -= xp_necessario
            return True
        return False
