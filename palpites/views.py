from django.shortcuts import render

def criar_palpites(request):
    return render(request, "palpites/palpites.html")

def meus_palpites(request):
    return render(request, "palpites/meus_palpites.html")
