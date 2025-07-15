import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import CodigoConvite, UserProfile, Usuario, Convite
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
    codigo_convite = request.GET.get('convite') or request.POST.get('convite')
    print(codigo_convite)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        telefone = request.POST.get('telefone', '').strip()
        senha = request.POST.get('password', '').strip()
        senha2 = request.POST.get('confirm_password', '').strip()
        chave_pix = request.POST.get('chave_pix', '').strip()
        convite_codigo = request.POST.get('convite', '').strip()
        print(f'Codigo de dentro do post {convite_codigo}')
         # Verifica campos obrigatórios
        if not username or not email or not telefone or not senha or not senha2:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, "autenticacao/cadastro.html", {'convite': convite_codigo})

        # Verifica se senhas coincidem
        if senha != senha2:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, "autenticacao/cadastro.html", {'convite': convite_codigo})

        # Verifica se usuário já existe
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já está em uso.')
            return render(request, "autenticacao/cadastro.html", {'convite': convite_codigo})

        # Verifica se email já existe
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
            return render(request, "autenticacao/cadastro.html", {'convite': convite_codigo})

        if UserProfile.objects.filter(telefone=telefone).exists():
            messages.error(request, 'Telefone já cadastrado.')
            return render(request, "autenticacao/cadastro.html", {'convite': convite_codigo})

        # Cria usuário
        user = Usuario.objects.create_user(username=username, email=email, password=senha)
        user.save()
        CodigoConvite.objects.get_or_create(usuario=user)
        # Cria perfil adicional
        UserProfile.objects.create(user=user, telefone=telefone, chave_pix=chave_pix)
        Classificacao.objects.create(usuario=user)
        BloquearPartida.objects.create(usuario=user)

        # Associar convite
        if convite_codigo:
            try:
                codigo_uuid = uuid.UUID(convite_codigo)  # CONVERTE aqui
                codigo_obj = CodigoConvite.objects.get(codigo=codigo_uuid)
                Convite.objects.create(
                    codigo=codigo_obj,
                    convidado=user
                )
            except CodigoConvite.DoesNotExist:
                print("Codigo invalido")
                pass

        mensagem = template_cadastro(username, email, telefone)
        send_telegram_message(mensagem)
        messages.success(request, 'Conta criada com sucesso! Faça login.')
        return redirect('login_bolao')
    return render(request,"autenticacao/cadastro.html", {'convite': codigo_convite})

def fazer_logout(request):
    logout(request)
    return redirect('login_bolao')
