from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView  # Importe TemplateView
from .forms import *
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('atualizar-perfil-aluno/', AlunoProfileUpdateView.as_view(), name='atualizar_perfil_aluno'),
    path('atualizar-perfil-empresa/', AnuncianteProfileUpdateView.as_view(), name='atualizar_perfil_empresa'),
    path('selecionar-tipo/', ProfileTypeView.as_view(), name='registrar'),
    path('registrar-aluno/', RegistrarAlunoView.as_view(), name='registrar_aluno'),
    path('registrar-empresa/', RegistrarAnuncianteView.as_view(), name='registrar_anunciante'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='usuarios/password_change_done.html'), name='password_change_done'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('email-verification-sent/', TemplateView.as_view(template_name="usuarios/email_verification_sent.html"), name='email_verification_sent'),

    # URLs para o fluxo de redefinição de senha
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='usuarios/password_reset/password_reset.html',
             form_class=CustomPasswordResetForm  # Use o formulário customizado aqui
         ),
         name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='usuarios/password_reset/password_reset_confirm.html',
             form_class=CustomSetPasswordForm  # Use o formulário customizado aqui
         ),
         name='password_reset_confirm'),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset/password_reset_done.html'), 
         name='password_reset_done'),

    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset/password_reset_complete.html'), 
         name='password_reset_complete'),
]

