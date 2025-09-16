from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import datetime

from .models import TopicoForum, ComentarioForum, Enquete, OpcaoEnquete, VotoEnquete

@login_required
def comunidades(request):
    topicos = TopicoForum.objects.all().order_by('-data_criacao')
    enquetes = Enquete.objects.all().order_by('-data_criacao')

    # Adiciona o usuário a cada enquete para os métodos
    for enquete in enquetes:
        enquete._request_user = request.user

    context = {
        'topicos': topicos,
        'enquetes': enquetes,
    }
    return render(request,"outros/comunidade.html", context)

@login_required
def criar_topico(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')

        TopicoForum.objects.create(
            titulo=titulo,
            conteudo=conteudo,
            autor=request.user
        )
        messages.success(request, 'Tópico criado com sucesso!')
        return redirect('comunidade')
    return redirect('comunidade')

@login_required
def criar_comentario(request):
    if request.method == 'POST':
        topico_id = request.POST.get('topico_id')
        parent_id = request.POST.get('parent_id')
        conteudo = request.POST.get('conteudo')

        try:
            topico = TopicoForum.objects.get(id=topico_id)
            parent = ComentarioForum.objects.get(id=parent_id) if parent_id else None

            ComentarioForum.objects.create(
                topico=topico,
                autor=request.user,
                conteudo=conteudo,
                parent=parent
            )
            messages.success(request, 'Resposta publicada com sucesso!')
        except TopicoForum.DoesNotExist:
            messages.error(request, 'Post não encontrado!')
        except ComentarioForum.DoesNotExist:
            messages.error(request, 'Comentário pai não encontrado!')

        return redirect('comunidade')
    return redirect('comunidade')

@login_required
@require_POST
def excluir_post(request, post_id):
    try:
        post = TopicoForum.objects.get(id=post_id, autor=request.user)
        post.delete()
        return JsonResponse({'success': True})
    except TopicoForum.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Post não encontrado'}, status=404)

@login_required
@require_POST
def editar_post(request):
    post_id = request.POST.get('post_id')
    titulo = request.POST.get('titulo')
    conteudo = request.POST.get('conteudo')

    try:
        post = TopicoForum.objects.get(id=post_id, autor=request.user)
        post.titulo = titulo
        post.conteudo = conteudo
        post.save()
        return JsonResponse({'success': True})
    except TopicoForum.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Post não encontrado'}, status=404)

@login_required
@require_POST
def excluir_comentario(request, comment_id):
    try:
        comment = ComentarioForum.objects.get(id=comment_id, autor=request.user)
        comment.delete()
        return JsonResponse({'success': True})
    except ComentarioForum.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Comentário não encontrado'}, status=404)


@login_required
@require_POST
def editar_comentario(request, comment_id):
    try:
        comment = ComentarioForum.objects.get(id=comment_id, autor=request.user)
        comment.conteudo = request.POST.get('conteudo')
        comment.save()
        return JsonResponse({'success': True})
    except ComentarioForum.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Comentário não encontrado'}, status=404)

@login_required
def criar_enquete(request):
    if request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        data_encerramento = request.POST.get('data_encerramento')
        opcoes = request.POST.getlist('opcoes[]')

        try:
            enquete = Enquete.objects.create(
                pergunta=pergunta,
                criador=request.user,
                data_encerramento=datetime.strptime(data_encerramento, '%Y-%m-%dT%H:%M')
            )

            for opcao in opcoes:
                if opcao.strip():  # Ignora opções vazias
                    OpcaoEnquete.objects.create(
                        enquete=enquete,
                        texto=opcao.strip()
                    )

            messages.success(request, 'Enquete criada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao criar enquete: {str(e)}')

        return redirect('comunidade')
    return redirect('comunidade')

import logging
logger = logging.getLogger(__name__)

@login_required
@require_POST
def votar_enquete(request, enquete_id, opcao_id):
    logger.info(f"Tentativa de voto - Enquete: {enquete_id}, Opção: {opcao_id}, Usuário: {request.user.id}")
    try:
        enquete = Enquete.objects.get(id=enquete_id)
        opcao = OpcaoEnquete.objects.get(id=opcao_id, enquete=enquete)

        # Verifica se usuário já votou
        if VotoEnquete.objects.filter(enquete=enquete, usuario=request.user).exists():
            return JsonResponse({'success': False, 'message': 'Você já votou nesta enquete'}, status=400)

        # Registra o voto
        VotoEnquete.objects.create(
            usuario=request.user,
            enquete=enquete,
            opcao=opcao
        )

        # Atualiza a contagem de votos
        opcao.votos += 1
        opcao.save()

        # Prepara os resultados para retorno
        opcoes = enquete.opcoes.all()
        total_votos = sum(op.votos for op in opcoes)
        resultados = [{
            'id': op.id,
            'percent': round((op.votos / total_votos) * 100) if total_votos > 0 else 0
        } for op in opcoes]

        return JsonResponse({
            'success': True,
            'results': resultados,
            'total_votos': total_votos
        })

    except (Enquete.DoesNotExist, OpcaoEnquete.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'Enquete ou opção não encontrada'}, status=404)

    except OpcaoEnquete.DoesNotExist:
        logger.error(f"Opção {opcao_id} não encontrada para enquete {enquete_id}")
        return JsonResponse({
            'success': False,
            'message': 'Opção inválida'
        }, status=400)

    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Erro interno no servidor'
        }, status=500)

def noticias(request):
    return render(request,"outros/noticias.html")
