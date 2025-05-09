from django.urls import path

from .views import *

urlpatterns = [
    path('', loja, name='loja'),
    path('api/lojas/<int:pk>/', loja_api_detail, name='loja-api-detail'),
]
