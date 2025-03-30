from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import *
from cadastros.models import *
#from cadastros.models import *
# Create your views here.
#class IndexView(TemplateView):
#    template_name = 'paginas/index.html'
#    form_class = ProfileTypeForm2  # A classe do formulário está aqui
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['form'] = self.form_class()  # Instancia e passa o formulário para o template
#        user_type = None
#        # Verificando se o usuário tem um perfil de aluno ou empresa
#        if hasattr(self.request.user, 'alunoprofile'):
#            user_type = 'aluno'
#        elif hasattr(self.request.user, 'anuncianteprofile'):
#            user_type = 'anunciante'
#        # Passando o tipo de usuário para o contexto
#        context['user_type'] = user_type
#        # Adicionando as vagas do usuário logado, se for um anunciante
#        if user_type == 'anunciante':
#            context['vagas'] = Vaga.objects.filter(usuario=self.request.user)
#        return context
from django.views.generic import TemplateView
#from cadastros.models import Empresa, Vaga

class IndexView(TemplateView):
    model = Vaga
    template_name = 'paginas/index.html'
    form_class = ProfileTypeForm2  # A classe do formulário está aqui
    context_object_name = 'vagas'

    def get_queryset(self):
        # Retorna todas as vagas, apenas as que não estão inativas
        return Vaga.objects.filter(inativa=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Instancia e passa o formulário para o template

        # Definir o tipo de usuário
        user_type = None
        if hasattr(self.request.user, 'alunoprofile'):
            user_type = 'aluno'
        elif hasattr(self.request.user, 'anuncianteprofile'):
            user_type = 'anunciante'

        context['user_type'] = user_type  # Passando o tipo de usuário para o contexto

        # Adicionando as vagas ao contexto explicitamente
        context['vagas'] = Vaga.objects.filter(inativa=False)  # Certifique-se de que inativa=False está correto

        return context




class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_type = None
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'alunoprofile'):
                user_type = 'aluno'
            elif hasattr(self.request.user, 'anuncianteprofile'):
                user_type = 'anunciante'

        context['user_type'] = user_type
        return context

class ContatoView(TemplateView):
    template_name = 'paginas/contato.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_type = None
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'alunoprofile'):
                user_type = 'aluno'
            elif hasattr(self.request.user, 'anuncianteprofile'):
                user_type = 'anunciante'

        context['user_type'] = user_type
        return context
