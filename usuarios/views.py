from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import *
from .forms import *

class CustomLoginView(FormView):
    form_class = CustomLoginForm
    template_name = 'usuarios/login.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            form.add_error(None, 'Usuário ou senha inválidos')
            return self.form_invalid(form)


def custom_logout_view(request):
    logout(request)
    return redirect('login')


class ProfileTypeView(FormView):
    template_name = 'usuarios/selecionar_tipo_perfil.html'
    form_class = ProfileTypeForm

    def form_valid(self, form):
        profile_type = form.cleaned_data['profile_type']
        if profile_type == 'aluno':
            return redirect('registrar_aluno')
        elif profile_type == 'anunciante':
            return redirect('registrar_anunciante')
        return super().form_valid(form)




#class RegistrarAnuncianteView(CreateView):
#    model = User
#    form_class = CustomUserCreationForm
#    second_form_class = AnuncianteProfileForm
#    template_name = 'usuarios/registrar_empresa.html'
#    success_url = reverse_lazy('homepage')
#
#    def get_context_data(self, **kwargs):
#        context = super(RegistrarAnuncianteView, self).get_context_data(**kwargs)
#        if 'empresa_form' not in context:
#            context['empresa_form'] = self.second_form_class(self.request.POST or None)
#        return context
#
#    def post(self, request, *args, **kwargs):
#        self.object = None
#        user_form = self.get_form(self.form_class)
#        empresa_form = AnuncianteProfileForm(self.request.POST)
#
#        if user_form.is_valid() and empresa_form.is_valid():
#            user = user_form.save()
#            empresa_profile = empresa_form.save(commit=False)
#            empresa_profile.user = user  # Associa o perfil de empresa ao usuário criado
#            empresa_profile.save()
#            return self.form_valid(user_form)
#        else:
#            return self.form_invalid(user_form)
#


class AnuncianteProfileUpdateView(UpdateView):
    model = AnuncianteProfile
    template_name = 'usuarios/atualizar_perfil_empresa.html'
    success_url = reverse_lazy('homepage')
    form_class = AnuncianteProfileUpdateForm  # Formulário de perfil de empresa

    def get_object(self):
        # Obtendo o objeto do perfil da empresa associado ao usuário
        return get_object_or_404(AnuncianteProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        # Adicionando os formulários de usuário e empresa ao contexto
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['empresa_form'] = AnuncianteProfileUpdateForm(instance=self.get_object())  # Formulário de empresa
        user_type = None
        if hasattr(self.request.user, 'alunoprofile'):
            user_type = 'aluno'
        elif hasattr(self.request.user, 'anuncianteprofile'):
            user_type = 'anunciante'

        context['user_type'] = user_type  # Passando o tipo de usuário para o contexto

        return context

    def post(self, request, *args, **kwargs):
        # Manipulando os formulários no método POST
        self.object = self.get_object()
        user_form = UserUpdateForm(request.POST, instance=request.user)
        empresa_form = AnuncianteProfileUpdateForm(request.POST, instance=self.object)

        # Validando os dois formulários
        if user_form.is_valid() and empresa_form.is_valid():
            user_form.save()
            empresa_form.save()
            return self.form_valid(user_form)
        else:
            return self.form_invalid(user_form)


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'usuarios/password_change.html'
    success_url = reverse_lazy('password_change_done')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_type = None
        if hasattr(self.request.user, 'alunoprofile'):
            user_type = 'aluno'
        elif hasattr(self.request.user, 'anuncianteprofile'):
            user_type = 'anunciante'

        context['user_type'] = user_type  # Passando o tipo de usuário para o contexto

        return context


#
#class RegistrarAlunoView(CreateView):
#    model = User
#    form_class = CustomUserCreationForm
#    second_form_class = AlunoProfileForm
#    template_name = 'usuarios/registrar_aluno.html'
#    success_url = reverse_lazy('homepage')
#
#    def get_context_data(self, **kwargs):
#        context = super(RegistrarAlunoView, self).get_context_data(**kwargs)
#        if 'aluno_form' not in context:
#            context['aluno_form'] = self.second_form_class(self.request.POST or None)
#        return context
#
#    def post(self, request, *args, **kwargs):
#        self.object = None
#        user_form = self.get_form(self.form_class)
#        aluno_form = AlunoProfileForm(self.request.POST)
#
#        if user_form.is_valid() and aluno_form.is_valid():
#            user = user_form.save()
#            aluno_profile = aluno_form.save(commit=False)
#            aluno_profile.user = user  # Associa o perfil de aluno ao usuário criado
#            aluno_profile.save()
#            return self.form_valid(user_form)
#        else:
#            return self.form_invalid(user_form)

class AlunoProfileUpdateView(UpdateView):
    model = AlunoProfile
    template_name = 'usuarios/atualizar_perfil_aluno.html'
    success_url = reverse_lazy('homepage')
    form_class = AlunoProfileUpdateForm  # Formulário de perfil de aluno

    def get_object(self):
        # Obtendo o objeto do perfil de aluno associado ao usuário
        return get_object_or_404(AlunoProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        # Adicionando os formulários de usuário e aluno ao contexto
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['aluno_form'] = AlunoProfileUpdateForm(instance=self.get_object())  # Formulário de aluno

        user_type = None
        if hasattr(self.request.user, 'alunoprofile'):
            user_type = 'aluno'
        elif hasattr(self.request.user, 'anuncianteprofile'):
            user_type = 'anunciante'

        context['user_type'] = user_type  # Passando o tipo de usuário para o contexto

        return context


    def post(self, request, *args, **kwargs):
        # Manipulando os formulários no método POST
        self.object = self.get_object()
        user_form = UserUpdateForm(request.POST, instance=request.user)
        aluno_form = AlunoProfileUpdateForm(request.POST, instance=self.object)

        # Validando os dois formulários
        if user_form.is_valid() and aluno_form.is_valid():
            user_form.save()
            aluno_form.save()
            return self.form_valid(user_form)
        else:
            return self.form_invalid(user_form)



from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, AlunoProfileForm

class RegistrarAlunoView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    second_form_class = AlunoProfileForm
    template_name = 'usuarios/registrar_aluno.html'
    success_url = reverse_lazy('homepage')  # Sucesso padrão, mas não será usado no redirecionamento do e-mail

    def get_context_data(self, **kwargs):
        context = super(RegistrarAlunoView, self).get_context_data(**kwargs)
        if 'aluno_form' not in context:
            context['aluno_form'] = self.second_form_class(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        user_form = self.get_form(self.form_class)
        aluno_form = AlunoProfileForm(self.request.POST)

        if user_form.is_valid() and aluno_form.is_valid():
            # Salva o usuário como inativo
            user = user_form.save(commit=False)
            user.is_active = False  # Desativa o usuário até a ativação
            user.save()

            # Cria o perfil do aluno
            aluno_profile = aluno_form.save(commit=False)
            aluno_profile.user = user  # Associa o perfil de aluno ao usuário criado
            aluno_profile.save()

            # Enviar e-mail de ativação
            current_site = get_current_site(request)
            subject = 'Ativação da sua conta'
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activate_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            activate_url = f'http://{current_site.domain}{activate_url}'

            message = render_to_string('usuarios/activation_email.html', {
                'user': user,
                'activate_url': activate_url,
            })

            config_loader = ConfigLoader()
            email = config_loader.get("EMAIL")

            send_mail(subject, message, email, [user.email])

            # Redireciona para a página de confirmação de envio de e-mail
            return redirect('email_verification_sent')
        else:
            return self.form_invalid(user_form)

import json
from pathlib import Path

class ConfigLoader:
    def __init__(self, config_path="/Users/joaocarlosmartinsdealmeida/Desktop/django/config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self):
        """Carrega o arquivo de configuração JSON."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as config_file:
            return json.load(config_file)

    def get(self, key, default=None):
        """Retorna um valor do JSON, se existir."""
        return self.config.get(key, default)
    

class RegistrarAnuncianteView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    second_form_class = AnuncianteProfileForm
    template_name = 'usuarios/registrar_empresa.html'
    success_url = reverse_lazy('homepage')

    def get_context_data(self, **kwargs):
        context = super(RegistrarAnuncianteView, self).get_context_data(**kwargs)
        if 'empresa_form' not in context:
            context['empresa_form'] = self.second_form_class(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        user_form = self.get_form(self.form_class)
        empresa_form = AnuncianteProfileForm(self.request.POST)

        if user_form.is_valid() and empresa_form.is_valid():
            # Salva o usuário como inativo
            user = user_form.save(commit=False)
            user.is_active = False  # Desativa o usuário até a ativação
            user.save()

            # Cria o perfil da empresa
            empresa_profile = empresa_form.save(commit=False)
            empresa_profile.user = user  # Associa o perfil de empresa ao usuário criado
            empresa_profile.save()

            # Enviar e-mail de ativação
            current_site = get_current_site(request)
            subject = 'Ativação da sua conta'
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activate_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            activate_url = f'http://{current_site.domain}{activate_url}'

            message = render_to_string('usuarios/activation_email.html', {
                'user': user,
                'activate_url': activate_url,
            })

            config_loader = ConfigLoader()
            email = config_loader.get("EMAIL")

            send_mail(subject, message, email, [user.email])

            # Redireciona para a página de confirmação de envio de e-mail
            return redirect('email_verification_sent')
        else:
            return self.form_invalid(user_form)


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Sua conta foi ativada com sucesso!')
        return redirect('login')
    else:
        messages.error(request, 'O link de ativação é inválido.')
        return redirect('homepage')

# Create your views here.
