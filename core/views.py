from django.shortcuts import render

def homepage(request):
    return render(request, 'index.html')

def perfil(request):
    return render(request, "perfil.html")

def regras(request):
    return render(request,"regras.html")

def configuracao(request):
    return render(request,"outros/configuracoes.html")
