from django.urls import path

from .views import *

urlpatterns = [
    path('comunidade/', comunidades, name='comunidade'),
    path('noticias/', noticias, name='noticias'),
]
