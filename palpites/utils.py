import re
import datetime
import pytz
import pandas as pd
import time
from django.core.mail import send_mail

from premios.conquistas import verificar_conquistas
from .models import *
from usuarios.models import *
from .api_brasileirao import *
from usuarios.models import  Rodada as rodada_usuario
from .signals import classificacao_finalizada
from palpites.models import *



def validar_senha(senha, confirmar_senha):
  """Valida se a senha atende aos critérios de segurança e se as senhas coincidem.
      A senha deve ter pelo menos 8 caracteres, uma letra maiúscula e um número.

  Args:
    senha: A senha digitada pelo usuário.
    confirmar_senha: A confirmação da senha.

  Returns:
    True se a senha for válida e as senhas coincidirem, False caso contrário.
  """

  # Expressão regular para verificar a complexidade da senha
  regex = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'

  # Verifica se a senha corresponde à expressão regular e se as senhas coincidem
  return re.match(regex, senha) is not None and senha == confirmar_senha

def criar_rodadas_campeonato():

  contador = 1
  while contador <= 38:
    time.sleep(2)
    data = get_api_data(contador)
    time_casa = []
    img_casa = []
    time_visitante = []
    img_visitante = []
    rodada = []
    datas_api = []
    datas_jogos = []
    fuso_brasil = pytz.timezone('America/Sao_Paulo')

    for jogo in data["matches"]:
      time_casa.append(jogo['homeTeam']['shortName'])
      img_casa.append(jogo['homeTeam']['crest'])
      time_visitante.append(jogo['awayTeam']['shortName'])
      img_visitante.append(jogo['awayTeam']['crest'])
      rodada.append(jogo['matchday'])
      datas_api.append(jogo["utcDate"])

    for data_str in datas_api:
        dt_utc = datetime.datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
        dt_brasil = dt_utc.astimezone(fuso_brasil)
        datas_jogos.append(dt_brasil.strftime("%d/%m/%Y %H:%M"))

    resultado_tabela = {
      "time_casa": time_casa,
      "img_casa": img_casa,
      "img_visitante": img_visitante,
      "time_visitante": time_visitante,
      "datas_jogos": datas_jogos,
      "rodada": rodada,
      }

    df_tabela = pd.DataFrame(resultado_tabela)
    for _, row in df_tabela.iterrows():
      jogos_rodada_criado  = Rodada.objects.create(
        time_casa=row['time_casa'],
        imagem_casa=row['img_casa'],
        time_visitante=row['time_visitante'],
        imagem_fora=row['img_visitante'],
        data_jogo= row['datas_jogos'],
        rodada_atual= row['rodada'],
          )
    print(f'Rodada {contador} criada!')
    contador += 1  # Incrementa o contador em 1 a cada iteração
    time.sleep(5)

def calcular_pontuacao(user):
  '''
    Args:
      Receber como argumento o usuario para fazer o filtro da tabela Palpite "score" "winner" "fullTime
  '''
  usuario = user
  rodadas = Palpite.objects.filter(finalizado=False, usuario=usuario)
  pontuacao_usuario = Classificacao.objects.get(usuario__usuario=user)


  try:
    for rodada in rodadas:
      print("Rodadas vitorias")
      rodada.vitorias += 2
      print(rodada.vitorias)
      try:
        resultado_original = RodadaOriginal.objects.get(rodada_atual=rodada.rodada_atual, time_casa=rodada.time_casa,time_visitante=rodada.time_visitante)


        # Verifica se os placares coincidem
        if (rodada.vencedor == resultado_original.vencedor):
          pontuacao_usuario.pontos += 2
          pontuacao_usuario.vitorias += 1
          rodada.vitorias += 2
          rodada.tipo_class = "sucesso"
          rodada.finalizado = True
          pontuacao_usuario.save()
        else:
          rodada.tipo_class = "erro"
          rodada.finalizado = True


        # verifica os placares exatos
        if (rodada.placar_casa == resultado_original.placar_casa and
            rodada.placar_visitante == resultado_original.placar_visitante):
          pontuacao_usuario.pontos += 3
          pontuacao_usuario.placar_exato += 1
          rodada.placar_exato += 3
          rodada.finalizado = True
          pontuacao_usuario.save()

        else:
          print("Resultados não exatos")  # Atribui 0 se os resultados não forem iguais
          rodada.finalizado = True

        # Verificando quais os jogos que não foram realizados
        if resultado_original.placar_casa == 9999 and resultado_original.placar_visitante == 9999:
          rodada.finalizado = False
          rodada.tipo_class = "none"
          rodada.save()
          print(f'Jogo para ser realizado: {rodada.time_casa} x {rodada.time_visitante}')

        rodada.save()
        pontuacao_usuario.save()
      except :
        continue
  except:
    print('tabela pontuação não encontrada')

def calcular_pontuacao_usuario(rodada_atualizada):
  todos_usuarios = UserProfile.objects.filter(pagamento=True)

  try:
    for usuario in todos_usuarios:
      participante = UserProfile.objects.get(user=usuario.user)
      rodadas = Palpite.objects.filter(finalizado=False, usuario=usuario.user, rodada_atual=rodada_atualizada)
      pontuacao_usuario = Classificacao.objects.get(usuario=usuario.user)

      for rodada in rodadas:
        try:
          resultado_original = RodadaOriginal.objects.get(rodada_atual=rodada.rodada_atual, time_casa=rodada.time_casa,time_visitante=rodada.time_visitante)

          if rodada.vencedor == "empate" and resultado_original.vencedor == 'empate':
            pontuacao_usuario.empates += 1
            pontuacao_usuario.vitorias -= 1
            participante.xp += 50
            participante.moedas += 30
            participante.save()
            pontuacao_usuario.save()

          # Verifica se os placares coincidem
          if (rodada.vencedor == resultado_original.vencedor):
            pontuacao_usuario.pontos += 2
            pontuacao_usuario.vitorias += 1
            rodada.vitorias = 2
            rodada.tipo_class = "result-correct"
            rodada.finalizado = True
            participante.xp += 50
            participante.moedas += 30
            participante.save()
            pontuacao_usuario.save()
          else:
            rodada.tipo_class = "result-wrong"
            rodada.finalizado = True

          # verifica os placares exatos
          if (rodada.placar_casa == resultado_original.placar_casa and
              rodada.placar_visitante == resultado_original.placar_visitante):
            pontuacao_usuario.pontos += 3
            pontuacao_usuario.placar_exato += 1
            rodada.placar_exato = 3
            rodada.tipo_class = "exact-correct"
            rodada.finalizado = True
            participante.xp += 100
            participante.moedas += 50
            participante.save()
            pontuacao_usuario.save()
          else:
            print("Resultados não exatos")  # Atribui 0 se os resultados não forem iguais
            rodada.finalizado = True
          # Verificando quais os jogos que não foram realizados
          if resultado_original.placar_casa == 9999 and resultado_original.placar_visitante == 9999:
            rodada.finalizado = False
            rodada.tipo_class = "none"
            rodada.save()

          rodada.save()
          pontuacao_usuario.save()
        except :
          continue

    usuarios_pagantes = UserProfile.objects.filter(pagamento=True).values_list('user_id', flat=True)
    classificacao = (
        Classificacao.objects
        .filter(usuario__in=usuarios_pagantes)
        .select_related('usuario')
        .order_by('-pontos', '-placar_exato', '-vitorias', '-empates')
    )
    for index, item in enumerate(classificacao, start=1):
      item.posicao_anterior = item.posicao_atual
      item.posicao_atual = index
      if item.posicao_anterior is not None:
        item.posicao_variacao = item.posicao_anterior - item.posicao_atual
      else:
        item.posicao_variacao = 0  # Nenhuma variação se não há posição anterior
      item.save()
    print("Classificação atualizada de forma normal")
  except:
    print('tabela pontuação não encontrada')


def resetar_pontuacao_usuarios():
  '''
  Filtrar todos os usuários com o tipo aposta "normal", colocar o pagamento de todos os usuários em "False" e zera todos os pontos da classificação.
  '''
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

def bloquear_rodadas():
  bloquear_partidas = BloquearPartida.objects.all()
  for partidas in bloquear_partidas:
    partidas.rodada_bloqueada = True
    partidas.save()

def desbloquear_rodadas():
  bloquear_partidas = BloquearPartida.objects.all()
  for partidas in bloquear_partidas:
    partidas.rodada_bloqueada = False
    partidas.save()

def resetar_pagamento():
  usuarios = Usuario.objects.all()
  for usuario in usuarios:
    usuario.pagamento = False
    usuario.save()

def salvar_rodada_original(rodada_original):
  dados = get_api_data(rodada_original)
  time_casa = []
  placar_casa = []
  time_visitante = []
  placar_visitante = []
  rodada = []

  for jogo in dados["matches"]:
    if jogo['score']['fullTime']['home'] == None:
      placar_casa.append(9999)
      placar_visitante.append(9999)
    else:
      placar_casa.append(jogo['score']['fullTime']['home'])
      placar_visitante.append(jogo['score']['fullTime']['away'])
    time_casa.append(jogo['homeTeam']['shortName'])
    time_visitante.append(jogo['awayTeam']['shortName'])
    rodada.append(jogo['matchday'])
  resultado_tabela = {
      "time_casa": time_casa,
      "placar_casa": placar_casa,
      "placar_visitante": placar_visitante,
      "time_visitante": time_visitante,
      "rodada": rodada
      }

  df_tabela = pd.DataFrame(resultado_tabela)
  for _, row in df_tabela.iterrows():
    jogos_rodada_criado  = RodadaOriginal.objects.create(
        time_casa=row['time_casa'],
        placar_casa=row['placar_casa'],
        time_visitante=row['time_visitante'],
        placar_visitante=row['placar_visitante'],
        rodada_atual= row['rodada'],
          )
  print(f'Rodada criada!')

def setar_rodadaAtual_rodadaFinal(rodada_atual, rodada_final):
  '''
    Retorna todos os dados dos usuarios atualizado para rodada atual e rodada final.

    Args:
      1º argumento: Qual a rodada inicial
      2º argumento: Qual a rodada final
  '''
  usuarios = Usuario.objects.all()
  for usuario in usuarios:
    bloquear = BloquearPartida.objects.filter(usuario=usuario)
    for partida in bloquear:
        partida.partida_atual = rodada_atual
        partida.partida_final = rodada_final
        partida.save()

def rodadas_false(rodada):
  palpites = Palpite.objects.filter(rodada_atual=rodada)
  for palpite in palpites:
    palpite.finalizado = False
    palpite.tipo_class = 'none'
    palpite.save()

def remover_repetidos(lista):
    nova_lista = []
    for elemento in lista:
        if elemento not in nova_lista:
            nova_lista.append(elemento)
    nova_lista.sort()
    return nova_lista

def enviar_email(email):
  destinatario = email
  assunto = f"Inscrição realizada com sucesso!"
  corpo = f"""Parabéns! Sua inscrição no bolão virtual foi realizada com sucesso.
  Agora você pode criar seus palpites e ver seu progresso no ranking geral.
  """
  remetente = "hiaguinhospencer@gmail.com"
  send_mail(assunto,corpo,remetente,[destinatario])
