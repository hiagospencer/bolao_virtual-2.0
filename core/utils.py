from usuarios.models import UserProfile,DestaqueDaSemana
from palpites.models import Palpite, PontuacaoRodada


def calcular_total_pontos_rodadas_usuarios(rodada):
    usuarios = UserProfile.objects.filter(pagamento=True)

    for usuario in usuarios:
        palpites = Palpite.objects.filter(usuario=usuario.user, rodada_atual=rodada)

        total_vitoria_rodada = 0
        total_placar_exato = 0

        for palpite in palpites:
            total_vitoria_rodada += palpite.vitorias
            total_placar_exato += palpite.placar_exato

        total_pontos = total_vitoria_rodada + total_placar_exato

        # Cria ou atualiza a pontuação da rodada
        PontuacaoRodada.objects.update_or_create(
            usuario=usuario.user,
            rodada=rodada,
            defaults={'pontos': total_pontos}
        )
    definir_destaque_da_semana(rodada)


def definir_destaque_da_semana(rodada):
    # Busca quem fez mais pontos na rodada
    destaque = PontuacaoRodada.objects.filter(rodada=rodada).order_by('-pontos').first()

    if destaque:
        usuario = destaque.usuario
        acertos = Palpite.objects.filter(usuario=usuario,rodada_atual=rodada,tipo_class__in=['result-correct', 'exact-correct']).count()
        total_jogos = Palpite.objects.filter(rodada_atual=rodada, usuario=usuario).count()

        # Cria o registro do destaque (evita duplicado com get_or_create)
        DestaqueDaSemana.objects.update_or_create(
            usuario=usuario,
            rodada=rodada,
            defaults={
                'acertos': acertos,
                'total_jogos': total_jogos,
                'dica_do_mestre': ''  # ou algo como 'Excelente desempenho!'
            }
        )
