import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import UserProfile, Usuario
from palpites.models import *

from .utils import *
from .templates_mensagens import *


User = get_user_model()

# Create your views here.
def login_bolao(request):
    if request.method == 'POST':
        username_or_email = request.POST['username'].strip()
        password = request.POST['password'].strip()

        # Verifica se o login é por e-mail
        try:
            user_obj = User.objects.get(email=username_or_email)
            username = user_obj.username
        except User.DoesNotExist:
            username = username_or_email

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request,"autenticacao/login_bolao.html")

def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        telefone = request.POST.get('telefone', '').strip()
        senha = request.POST.get('password', '').strip()
        senha2 = request.POST.get('confirm_password', '').strip()
        chave_pix = request.POST.get('chave_pix', '').strip()

         # Verifica campos obrigatórios
        if not username or not email or not telefone or not senha or not senha2:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, "autenticacao/cadastro.html")

        # Verifica se senhas coincidem
        if senha != senha2:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, "autenticacao/cadastro.html")

        # Verifica se usuário já existe
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já está em uso.')
            return render(request, "autenticacao/cadastro.html")

        # Verifica se email já existe
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
            return render(request, "autenticacao/cadastro.html")

        if UserProfile.objects.filter(telefone=telefone).exists():
            messages.error(request, 'Telefone já cadastrado.')
            return render(request, "autenticacao/cadastro.html")

        # Cria usuário
        user = Usuario.objects.create_user(username=username, email=email, password=senha)
        user.save()
        # Cria perfil adicional
        UserProfile.objects.create(user=user, telefone=telefone, chave_pix=chave_pix)
        Classificacao.objects.create(usuario=user)
        BloquearPartida.objects.create(usuario=user)

        mensagem = template_cadastro(username, email, telefone)
        send_telegram_message(mensagem)
        messages.success(request, 'Conta criada com sucesso! Faça login.')
        return redirect('login_bolao')
    return render(request,"autenticacao/cadastro.html")

def fazer_logout(request):
    logout(request)
    return redirect('login_bolao')
