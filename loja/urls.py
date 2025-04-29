from django.urls import path

from .views import *

urlpatterns = [
    path('', loja, name='loja'),
]
