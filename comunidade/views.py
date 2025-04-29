from django.shortcuts import render

# Create your views here.
def comunidades(request):
    return render(request,"outros/comunidade.html")

def noticias(request):
    return render(request,"outros/noticias.html")

def trofeus(request):
    return render(request,"outros/trofeus.html")
