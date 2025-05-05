from django.urls import path

from .views import *

urlpatterns = [
    path('comunidade/', comunidades, name='comunidade'),
    path('criar-topico/', criar_topico, name='criar_topico'),
    path('criar-comentario/', criar_comentario, name='criar_comentario'),
    path('excluir-post/<int:post_id>/', excluir_post, name='excluir_post'),
    path('editar-post/', editar_post, name='editar_post'),
    path('excluir-comentario/<int:comment_id>/', excluir_comentario, name='excluir_comentario'),
    path('editar-comentario/<int:comment_id>/', editar_comentario, name='editar_comentario'),

    path('criar-enquete/', criar_enquete, name='criar_enquete'),
     path('votar-enquete/<int:enquete_id>/<int:opcao_id>/', votar_enquete, name='votar_enquete'),
    path('noticias/', noticias, name='noticias'),
]
