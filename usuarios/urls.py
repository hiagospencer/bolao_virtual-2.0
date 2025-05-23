from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('login/', login_bolao, name='login_bolao'),
    path('cadastro/', cadastro, name='cadastro'),
    path('logout/', fazer_logout, name='fazer_logout'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='autenticacao/registration/password_reset.html',
             email_template_name='autenticacao/registration/password_reset_email.html',
             subject_template_name='autenticacao/registration/password_reset_subject.txt'
         ),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='autenticacao/registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='autenticacao/registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='autenticacao/registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
