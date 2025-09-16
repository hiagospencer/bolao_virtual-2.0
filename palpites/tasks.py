from django.db.models import Sum
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from usuarios.models import UserProfile, DestaqueDaSemana, Usuario
from palpites.models import Palpite, Classificacao, RodadaOriginal, BloquearPartida, Rodada, PontuacaoRodada
from .api_brasileirao import get_api_data
from django.contrib import messages

import time
import pandas as pd
import datetime
import pytz


@shared_task(bind=True, max_retries=3)
def calcular_pontuacao_usuario_task(self, rodada_atualizada):
    try:
        usuarios = UserProfile.objects.filter(pagamento=True).select_related('user')
        resultados = RodadaOriginal.objects.filter(rodada_atual=rodada_atualizada)

        resultados_dict = {
            (r.time_casa, r.time_visitante): r for r in resultados
        }

        # Listas para armazenar objetos que precisam ser atualizados
        palpites_para_atualizar = []
        usuarios_para_atualizar = []
        classificacoes_para_atualizar = []

        for usuario in usuarios:
            participante = usuario
            pontuacao_usuario, _ = Classificacao.objects.get_or_create(usuario=usuario.user)

            rodadas = Palpite.objects.filter(
                finalizado=False,
                usuario=usuario.user,
                rodada_atual=rodada_atualizada
            )

            for rodada in rodadas:
                resultado_key = (rodada.time_casa, rodada.time_visitante)
                resultado_original = resultados_dict.get(resultado_key)

                if not resultado_original:
                    continue

                # Verifica se o jogo foi realizado
                if resultado_original.placar_casa == 9999 and resultado_original.placar_visitante == 9999:
                    rodada.finalizado = False
                    rodada.tipo_class = "none"
                    palpites_para_atualizar.append(rodada)
                    continue

                pontos_ganhos = 0
                xp_ganhos = 0
                moedas_ganhas = 0

                # Empate correto
                if rodada.vencedor == "empate" and resultado_original.vencedor == "empate":
                    pontuacao_usuario.empates += 1
                    pontuacao_usuario.vitorias -= 1
                    xp_ganhos += 50
                    moedas_ganhas += 30

                # Acertou vencedor
                if rodada.vencedor == resultado_original.vencedor:
                    pontuacao_usuario.pontos += 2
                    pontuacao_usuario.vitorias += 1
                    rodada.vitorias = 2
                    rodada.tipo_class = "result-correct"
                    pontos_ganhos += 2
                    xp_ganhos += 50
                    moedas_ganhas += 30
                else:
                    rodada.tipo_class = "result-wrong"

                # Acertou placar exato
                if (rodada.placar_casa == resultado_original.placar_casa and
                    rodada.placar_visitante == resultado_original.placar_visitante):
                    pontuacao_usuario.pontos += 3
                    pontuacao_usuario.placar_exato += 1
                    rodada.placar_exato = 3
                    rodada.tipo_class = "exact-correct"
                    pontos_ganhos += 3
                    xp_ganhos += 100
                    moedas_ganhas += 50

                rodada.finalizado = True
                palpites_para_atualizar.append(rodada)

                participante.xp += xp_ganhos
                participante.moedas += moedas_ganhas
                if participante not in usuarios_para_atualizar:
                    usuarios_para_atualizar.append(participante)

                if pontuacao_usuario not in classificacoes_para_atualizar:
                    classificacoes_para_atualizar.append(pontuacao_usuario)

        # Atualizando classificação geral
        usuarios_ids = usuarios.values_list('user_id', flat=True)
        classificacao = (
            Classificacao.objects
            .filter(usuario__in=usuarios_ids)
            .select_related('usuario')
            .order_by('-pontos', '-placar_exato', '-vitorias', '-empates')
        )

        for index, item in enumerate(classificacao, start=1):
            item.posicao_anterior = item.posicao_atual
            item.posicao_atual = index
            item.posicao_variacao = (item.posicao_anterior - index) if item.posicao_anterior else 0
            if item not in classificacoes_para_atualizar:
                classificacoes_para_atualizar.append(item)

        # 🚀 Executa todos os updates de uma vez
        Palpite.objects.bulk_update(
            palpites_para_atualizar,
            ['finalizado', 'vitorias', 'placar_exato', 'tipo_class']
        )
        UserProfile.objects.bulk_update(
            usuarios_para_atualizar,
            ['xp', 'moedas']
        )
        Classificacao.objects.bulk_update(
            classificacoes_para_atualizar,
            ['pontos', 'vitorias', 'empates', 'placar_exato', 'posicao_atual', 'posicao_anterior', 'posicao_variacao']
        )

        print("✅ Pontuações calculadas com sucesso usando bulk_update!")
        return "Pontuações calculadas com sucesso!"

    except Exception as e:
        print(f"🔥 Erro na task: {e}")
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def resetar_pontuacao_usuarios_task(self):
    """
    Task para resetar a pontuação de todos os usuários
    """
    try:
        # Resetar pontuações
        pontuacoes = Classificacao.objects.all()
        for pontuacao in pontuacoes:
            pontuacao.pontos = 0
            pontuacao.placar_exato = 0
            pontuacao.vitorias = 0
            pontuacao.empates = 0
            pontuacao.posicao_atual = None
            pontuacao.posicao_anterior = None
            pontuacao.posicao_variacao = None
            pontuacao.save()
        return "Pontuações resetadas com sucesso!"

    except Exception as e:
        self.retry(exc=e, countdown=60)

@shared_task(bind=True, max_retries=3)
def bloquear_rodadas_task(self):
    """
    Task para bloquear todas as rodadas
    """
    try:
        BloquearPartida.objects.all().update(rodada_bloqueada=True)
        return "Rodadas bloqueadas com sucesso!"
    except Exception as e:
        self.retry(exc=e, countdown=60)

@shared_task(bind=True, max_retries=3)
def desbloquear_rodadas_task(self):
    """
    Task para desbloquear todas as rodadas
    """
    try:
        BloquearPartida.objects.all().update(rodada_bloqueada=False)
        return "Rodadas desbloqueadas com sucesso!"
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3, time_limit=600)
def setar_rodada_atual_final_task(self, rodada_atual, rodada_final):
    """
    Atualiza a rodada atual e final para todos os usuários
    """
    try:
        usuarios = Usuario.objects.all()
        for usuario in usuarios:
            BloquearPartida.objects.filter(usuario=usuario).update(
                partida_atual=rodada_atual,
                partida_final=rodada_final
            )

        return f"Rodadas atualizadas: Atual={rodada_atual}, Final={rodada_final}"
    except Exception as e:
        self.retry(exc=e, countdown=60)

@shared_task(bind=True, max_retries=3)
def resetar_rodadas_task(self, rodada):
    """
    Reseta o status dos palpites de uma rodada específica
    """
    try:
        updated = Palpite.objects.filter(rodada_atual=rodada).update(
            finalizado=False,
            tipo_class='none'
        )

        return f"{updated} palpites resetados para a rodada {rodada}"
    except Exception as e:
        self.retry(exc=e, countdown=60)

@shared_task(bind=True, max_retries=3, time_limit=300)
def salvar_rodada_original_task(self, rodada_original):
    """
    Salva os dados originais de uma rodada a partir da API
    """
    try:
        dados = get_api_data(rodada_original)

        # Limpa rodadas existentes para evitar duplicação
        RodadaOriginal.objects.filter(rodada_atual=rodada_original).delete()

        batch = []
        for jogo in dados["matches"]:
            home_goals = 9999 if jogo['score']['fullTime']['home'] is None else jogo['score']['fullTime']['home']
            away_goals = 9999 if jogo['score']['fullTime']['away'] is None else jogo['score']['fullTime']['away']

            batch.append(RodadaOriginal(
                time_casa=jogo['homeTeam']['shortName'],
                placar_casa=home_goals,
                time_visitante=jogo['awayTeam']['shortName'],
                placar_visitante=away_goals,
                rodada_atual=jogo['matchday']
            ))

        RodadaOriginal.objects.bulk_create(batch)
        return f"Rodada {rodada_original} salva com {len(batch)} jogos"
    except Exception as e:
        self.retry(exc=e, countdown=120)

@shared_task(bind=True, max_retries=3, time_limit=1800)
def criar_rodadas_campeonato_task(self):
    """
    Cria todas as rodadas do campeonato (1 a 38) a partir da API
    """
    try:
        fuso_brasil = pytz.timezone('America/Sao_Paulo')
        total_created = 0

        for contador in range(1, 39):
            try:
                print(f"🔄 Buscando dados da rodada {contador}")
                data = get_api_data(contador)

                if not data or "matches" not in data:
                    raise ValueError(f"❌ Dados inválidos ou vazios para a rodada {contador}")

                batch = []

                for jogo in data["matches"]:
                    dt_utc = datetime.datetime.strptime(
                        jogo["utcDate"], "%Y-%m-%dT%H:%M:%SZ"
                    ).replace(tzinfo=pytz.UTC)

                    dt_brasil = dt_utc.astimezone(fuso_brasil)

                    batch.append(Rodada(
                        time_casa=jogo['homeTeam']['shortName'],
                        imagem_casa=jogo['homeTeam']['crest'],
                        time_visitante=jogo['awayTeam']['shortName'],
                        imagem_fora=jogo['awayTeam']['crest'],
                        data_jogo=dt_brasil.strftime("%d/%m/%Y %H:%M"),
                        rodada_atual=jogo['matchday']
                    ))

                # Deleta rodada existente e cria nova
                Rodada.objects.filter(rodada_atual=contador).delete()
                Rodada.objects.bulk_create(batch)
                total_created += len(batch)

                print(f"✅ Rodada {contador} criada com {len(batch)} jogos.")
                time.sleep(9)  # Respeitar limite de requisição

            except Exception as e:
                print(f"⚠️ Erro na rodada {contador}: {e}")
                self.retry(exc=e, countdown=120)
                continue
        return f"🏆 Campeonato criado com {total_created} jogos em 38 rodadas."

    except Exception as e:
        print(f"🔥 Erro geral na criação das rodadas: {e}")
        self.retry(exc=e, countdown=300)


@shared_task(bind=True, max_retries=3, time_limit=300)
def calcular_total_pontos_rodadas_usuarios_task(self, rodada):
    """
    Calcula o total de pontos dos usuários em uma rodada específica
    e atualiza a tabela de pontuação por rodada
    """
    try:
        usuarios = UserProfile.objects.filter(pagamento=True).select_related('user')

        for usuario in usuarios:
            try:
                # Calcula totais usando aggregate para melhor performance
                totais = Palpite.objects.filter(
                    usuario=usuario.user,
                    rodada_atual=rodada
                ).aggregate(
                    total_vitorias=Sum('vitorias'),
                    total_placares=Sum('placar_exato')
                )

                total_pontos = (totais['total_vitorias'] or 0) + (totais['total_placares'] or 0)

                # Atualiza ou cria o registro de pontuação
                PontuacaoRodada.objects.update_or_create(
                    usuario=usuario.user,
                    rodada=rodada,
                    defaults={'pontos': total_pontos}
                )

            except Exception as e:
                self.retry(exc=e, countdown=60)
                continue

        # Chama a task de definir destaque como subtask
        definir_destaque_da_semana_task.delay(rodada)

        return f"Pontuações calculadas para rodada {rodada}"

    except Exception as e:
        self.retry(exc=e, countdown=120)

@shared_task(bind=True, max_retries=3)
def definir_destaque_da_semana_task(self, rodada):
    """
    Define o destaque da semana baseado na pontuação mais alta da rodada
    """
    try:
        # Busca o destaque com maior pontuação
        destaque = PontuacaoRodada.objects.filter(
            rodada=rodada
        ).select_related('usuario').order_by('-pontos').first()

        if not destaque:
            return "Nenhum destaque encontrado para a rodada"

        # Calcula estatísticas
        acertos = Palpite.objects.filter(
            usuario=destaque.usuario,
            rodada_atual=rodada,
            tipo_class__in=['result-correct', 'exact-correct']
        ).count()

        total_jogos = Palpite.objects.filter(
            rodada_atual=rodada,
            usuario=destaque.usuario
        ).count()

        # Cria/atualiza o registro de destaque
        DestaqueDaSemana.objects.update_or_create(
            usuario=destaque.usuario,
            rodada=rodada,
            defaults={
                'acertos': acertos,
                'total_jogos': total_jogos,
                'dica_do_mestre': f'Parabéns pelos {destaque.pontos} pontos!'
            }
        )

        return f"Destaque da semana definido: {destaque.usuario.username}"

    except Exception as e:
        self.retry(exc=e, countdown=60)
