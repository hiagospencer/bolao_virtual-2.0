from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login_bolao, name='login_bolao'),
    path('cadastro/', cadastro, name='cadastro'),
    path('logout/', fazer_logout, name='fazer_logout'),
]
