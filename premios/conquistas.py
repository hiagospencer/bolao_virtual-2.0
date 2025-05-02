# apps/premios/conquistas.py

from django.utils import timezone
from premios.models import MetaConquista, ConquistaUsuario, HistoricoConquista, TipoTrofeu
from palpites.models import Classificacao
# from ranking.models import PosicaoRanking
from usuarios.models import Usuario


class GerenciadorConquistas:
    def __init__(self, usuario):
        self.usuario = usuario
        self.classificacao = Classificacao.objects.get(usuario=usuario)
        self.criar_metas_padrao()

    def criar_metas_padrao(self):
        metas = [
            {
                "tipo": "placar_exato",
                "nome": "Mestre do Placar Exato",
                "descricao": "Acertou 10 placares exatos.",
                "valor_requerido": 10,
                "xp": 100,
                "moedas": 50
            },
            {
                "tipo": "vitorias",
                "nome": "Senhor das Vitórias",
                "descricao": "Acertou o vencedor de 20 jogos.",
                "valor_requerido": 20,
                "xp": 200,
                "moedas": 50
            },
            {
                "tipo": "pontos_totais",
                "nome": "Acumulador de Pontos",
                "descricao": "Acumulou 100 pontos totais.",
                "valor_requerido": 100,
                "xp": 300,
                "moedas": 70
            },
            {
                "tipo": "participacao",
                "nome": "Presença Constante",
                "descricao": "Participou de 10 rodadas.",
                "valor_requerido": 10,
                "xp": 150,
                "moedas": 40
            },
            {
                "tipo": "total_conquistas",
                "nome": "Colecionador de Conquistas",
                "descricao": "Conquistou 5 metas diferentes.",
                "valor_requerido": 5,
                "xp": 250,
                "moedas": 60
            },
        ]

        tipo_trofeu_padrao, _ = TipoTrofeu.objects.get_or_create(
            nome="Troféu Padrão",
            defaults={"descricao": "Troféu padrão", "icone": "fa-trophy", "nivel": 1}
        )

        for meta in metas:
            MetaConquista.objects.get_or_create(
                tipo=meta["tipo"],
                valor_requerido=meta["valor_requerido"],
                defaults={
                    "tipo_trofeu": tipo_trofeu_padrao,
                    "nome": meta["nome"],
                    "descricao": meta["descricao"],
                    "xp_recompensa": meta["xp"],
                    "moedas_recompensa": meta["moedas"],
                }
            )

    def verificar_conquistas(self):
        print("Verificar Conquista")
        metas = MetaConquista.objects.all()

        for meta in metas:
            progresso = self.calcular_progresso(meta.tipo)

            conquista, created = ConquistaUsuario.objects.get_or_create(
                usuario=self.usuario,
                meta=meta,
                defaults={
                    "progresso_atual": progresso,
                    "concluida": progresso >= meta.valor_requerido
                }
            )

            if progresso >= meta.valor_requerido and not conquista.concluida:
                conquista.progresso_atual = progresso
                conquista.concluida = True
                conquista.save()

                # Adiciona ao histórico (somente se ainda não existe)
                HistoricoConquista.objects.get_or_create(
                    usuario=self.usuario,
                    meta=meta,
                    defaults={
                        "xp_ganho": meta.xp_recompensa,
                        "moedas_ganhas": meta.moedas_recompensa,
                        "data_conquista": timezone.now()
                    }
                )

                # Adiciona XP e moedas ao usuário
                self.usuario.xp += meta.xp_recompensa
                self.usuario.moedas += meta.moedas_recompensa
                self.usuario.save()

            elif not conquista.concluida:
                conquista.progresso_atual = progresso
                conquista.save()

    def calcular_progresso(self, tipo):
        if tipo == 'placar_exato':
            return self.classificacao.placar_exato
        elif tipo == 'vitorias':
            return self.classificacao.vitorias
        elif tipo == 'pontos_totais':
            return self.classificacao.total_pontos
        elif tipo == 'participacao':
            return self.classificacao.total_rodadas
        elif tipo == 'total_conquistas':
            return ConquistaUsuario.objects.filter(usuario=self.usuario, concluida=True).count()
        else:
            return 0  # para metas não implementadas ainda

    def _recompensar_usuario(self, meta):
        self.usuario.xp += meta.xp_recompensa
        self.usuario.moedas += meta.moedas_recompensa
        self.usuario.save()

        HistoricoConquista.objects.create(
            usuario=self.usuario,
            meta=meta,
            xp_ganho=meta.xp_recompensa,
            moedas_ganhas=meta.moedas_recompensa
        )

        self._verificar_level_up()

    def _verificar_level_up(self):
        niveis = {1: 1000, 2: 2500, 3: 5000}
        for level, xp_necessario in niveis.items():
            if self.usuario.xp >= xp_necessario and self.usuario.level < level:
                self.usuario.level = level
                self.usuario.save()
                break
