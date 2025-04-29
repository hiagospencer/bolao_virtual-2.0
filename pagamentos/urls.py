from django.urls import path

from .views import *

urlpatterns = [
    path('', pagamento, name='pagamento'),
]
