from django.shortcuts import render

def loja(request):
    return render(request, "outros/shop.html")
