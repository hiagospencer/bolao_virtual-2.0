from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import datetime

from .models import TopicoForum, ComentarioForum, Enquete, OpcaoEnquete


def comunidades(request):
    topicos = TopicoForum.objects.all().order_by('-data_criacao')
    enquetes = Enquete.objects.all().order_by('-data_criacao')

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
        conteudo = request.POST.get('conteudo')

        try:
            topico = TopicoForum.objects.get(id=topico_id)
            ComentarioForum.objects.create(
                topico=topico,
                conteudo=conteudo,
                autor=request.user
            )
            messages.success(request, 'Resposta publicada com sucesso!')
        except TopicoForum.DoesNotExist:
            messages.error(request, 'Tópico não encontrado!')

        return redirect('comunidade')
    return redirect('comunidade')

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

@require_POST
def votar_enquete(request, enquete_id, opcao_id):
    try:
        opcao = OpcaoEnquete.objects.get(id=opcao_id, enquete_id=enquete_id)
        opcao.votos += 1
        opcao.save()

        return JsonResponse({
            'success': True,
            'percent': enquete.porcentagem_votos(opcao)
        })
    except OpcaoEnquete.DoesNotExist:
        return JsonResponse({'success': False}, status=404)
    
def noticias(request):
    return render(request,"outros/noticias.html")
