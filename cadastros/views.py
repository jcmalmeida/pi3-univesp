from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.views import View
from .models import *
from .forms import *


#class PainelAnuncianteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
#    template_name = 'cadastros/painel_anunciante.html'
#    def test_func(self):
#        return hasattr(self.request.user, 'anuncianteprofile')

#class PainelAnuncianteView(LoginRequiredMixin, ListView):
#    model = Vaga
#    template_name = 'cadastros/painel_anunciante.html'
#    context_object_name = 'vagas'
#
#    def get_queryset(self):
#        # Filtra as vagas criadas pelo anunciante logado
#        return Vaga.objects.filter(usuario=self.request.user)


class EditarVagaView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'cadastros/form_vaga.html'
    success_url = reverse_lazy('minhas_vagas')

    def test_func(self):
        # Verifica se o usuário é o criador da vaga (ou pode ser feito com base no perfil de anunciante)
        vaga = self.get_object()
        return vaga.usuario == self.request.user or hasattr(self.request.user, 'anuncianteprofile')

    def form_valid(self, form):
        # Mantém o usuário que criou a vaga inicialmente
        form.instance.usuario = self.request.user
        return super().form_valid(form)






###############################################################################
###############################################################################
###############################################################################
###############################################################################
class CriarEmpresaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'cadastros/form_empresa.html'
    success_url = reverse_lazy('minhas_vagas')

    def test_func(self):
        return hasattr(self.request.user, 'anuncianteprofile')

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

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Vaga, Empresa, Curso
from .forms import VagaForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Vaga, Empresa
from .forms import VagaForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class CriarVagaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'cadastros/form_vaga.html'
    success_url = reverse_lazy('minhas_vagas')

    def test_func(self):
        # Somente usuários com perfil 'anunciante' podem acessar esta view
        return hasattr(self.request.user, 'anuncianteprofile')

    def get_initial(self):
        # Passa a empresa específica ao formulário para pré-selecioná-la
        initial = super().get_initial()
        empresa_id = self.kwargs.get('empresa_id')
        if empresa_id:
            initial['empresa'] = empresa_id
        return initial

    def form_valid(self, form):
        # Define o usuário que está criando a vaga
        form.instance.usuario = self.request.user

        # Se um `empresa_id` for passado, associa a empresa ao objeto de vaga
        empresa_id = self.kwargs.get('empresa_id')
        if empresa_id:
            form.instance.empresa = get_object_or_404(Empresa, pk=empresa_id)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Adiciona informações adicionais ao contexto do template
        context = super().get_context_data(**kwargs)

        # Define o tipo de usuário no contexto, se necessário
        user_type = None
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'alunoprofile'):
                user_type = 'aluno'
            elif hasattr(self.request.user, 'anuncianteprofile'):
                user_type = 'anunciante'
        context['user_type'] = user_type

        # Passa `empresa_id` no contexto para verificar no template
        context['empresa_id'] = self.kwargs.get('empresa_id')
        return context


from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Vaga, Empresa
import pandas as pd

class CriarMultiplasVagasView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'cadastros/form_multiplas_vagas.html'

    def test_func(self):
        return hasattr(self.request.user, 'anuncianteprofile')

    def get(self, request, empresa_id=None):
        context = {
            'empresa_id': empresa_id,
            'user_type': 'anunciante' if hasattr(request.user, 'anuncianteprofile') else None,
        }
        return render(request, self.template_name, context)

    def post(self, request, empresa_id=None):
        arquivo = request.FILES.get('arquivo')

        if not arquivo or not arquivo.name.endswith('.xlsx'):
            messages.error(request, "Por favor, envie um arquivo .xlsx válido e baseado no modelo de planilha de vaga.")
            return redirect(request.path)

        try:
            criadas_ativas = 0
            criadas_inativas = 0

            df = pd.read_excel(arquivo, sheet_name='Planilha1')

            if (pd.notna(df.iloc[4, 2])):
                print(f'Empresa: {df.iloc[4, 2]}')

            empresa = Empresa.objects.get(nome = df.iloc[4, 2])

            linha_inicial_atual = 7
            coluna_atual = 2

            for i in range(1, 11):                
                # Verifica se a vaga não foi preenchida
                if not pd.notna(df.iloc[linha_inicial_atual, coluna_atual]):
                    break

                vaga = Vaga(
                    nome = df.iloc[linha_inicial_atual, coluna_atual],
                    descricao = df.iloc[linha_inicial_atual + 1, coluna_atual],
                    empresa = empresa,
                    link = df.iloc[linha_inicial_atual + 2, coluna_atual],
                    inativa = False if df.iloc[linha_inicial_atual + 3, coluna_atual] == 'Ativa' else True,
                    usuario = request.user,
                )
                vaga.save()

                linha_inicial_atual += 6

                if (vaga.inativa):
                    criadas_inativas += 1
                else:
                    criadas_ativas += 1
            
            if (criadas_ativas == 0 and criadas_inativas == 0):
                raise Exception("Nenhuma vaga foi criada. Verifique o modelo de arquivo utilizado e tente novamente.")

            messages.success(request, f"A partir do upload da planilha preenchida, {criadas_ativas} vaga(s) ativa(s) e {criadas_inativas} vaga(s) inativa(s) foram criadas com sucesso.")
            return redirect('criar_multiplas_vagas')

        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao processar o arquivo: {e}")
            return redirect(request.path)



###############################################################################
###############################################################################
###############################################################################
###############################################################################
class ListaTodasVagasView(ListView):
    model = Vaga
    template_name = 'cadastros/lista_todas_vagas.html'
    context_object_name = 'vagas'

    def get_queryset(self):
        # Retorna todas as vagas, apenas as que não estão inativas
        return Vaga.objects.filter(inativa=False)

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


class ListaVagasView(LoginRequiredMixin, ListView):
    model = Vaga
    template_name = 'cadastros/minhas_vagas.html'
    context_object_name = 'vagas'

    def get_queryset(self):
        # Retorna apenas as vagas criadas pelo usuário logado (anunciante)
        return Vaga.objects.filter(usuario=self.request.user)

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



###############################################################################
###############################################################################
###############################################################################
###############################################################################


class ExcluirVagaView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vaga
    template_name = 'cadastros/confirmar_exclusao_vaga.html'
    success_url = reverse_lazy('minhas_vagas')

    def test_func(self):
        vaga = self.get_object()
        return vaga.usuario == self.request.user




class ListarEmpresasView(ListView):
    model = Empresa
    template_name = 'cadastros/lista_empresas.html'  # O template que será usado
    context_object_name = 'empresas'
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

class ListarVagasPorEmpresaView(ListView):
    model = Vaga
    template_name = 'cadastros/listar_vagas_empresa.html'
    context_object_name = 'vagas'

    def get_queryset(self):
        self.empresa = Empresa.objects.get(pk=self.kwargs['pk'])
        return Vaga.objects.filter(empresa=self.empresa)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa'] = self.empresa  # Adiciona a empresa ao contexto
        user_type = None
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'alunoprofile'):
                user_type = 'aluno'
            elif hasattr(self.request.user, 'anuncianteprofile'):
                user_type = 'anunciante'

        context['user_type'] = user_type
        return context

        return context

    def test_func(self):
        return hasattr(self.request.user, 'anuncianteprofile')



from django.views.generic.detail import DetailView

class VagaDetailView(DetailView):
    model = Vaga
    template_name = 'cadastros/vaga_detail.html'  # Template que exibe os detalhes da vaga
    context_object_name = 'vaga'        # Nome da variável no template
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



from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Curso
from .forms import CursoForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class CriarCursoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cadastros/form_curso.html'
    success_url = reverse_lazy('meus_cursos')

    def test_func(self):
        # Somente usuários com perfil 'anunciante' podem acessar esta view
        return hasattr(self.request.user, 'anuncianteprofile')

    def get_initial(self):
        # Passa a empresa específica ao formulário para pré-selecioná-la
        initial = super().get_initial()
        
        return initial

    def form_valid(self, form):
        # Define o usuário que está criando o curso
        form.instance.usuario = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Adiciona informações adicionais ao contexto do template
        context = super().get_context_data(**kwargs)

        # Define o tipo de usuário no contexto, se necessário
        user_type = None
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'alunoprofile'):
                user_type = 'aluno'
            elif hasattr(self.request.user, 'anuncianteprofile'):
                user_type = 'anunciante'
        context['user_type'] = user_type

        return context


from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Curso
import pandas as pd

class CriarMultiplosCursosView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'cadastros/form_multiplos_cursos.html'

    def test_func(self):
        return hasattr(self.request.user, 'anuncianteprofile')

    def get(self, request, empresa_id=None):
        context = {
            'user_type': 'anunciante' if hasattr(request.user, 'anuncianteprofile') else None,
        }
        return render(request, self.template_name, context)

    def post(self, request, empresa_id=None):
        arquivo = request.FILES.get('arquivo')

        if not arquivo or not arquivo.name.endswith('.xlsx'):
            messages.error(request, "Por favor, envie um arquivo .xlsx válido e baseado no modelo de planilha de curso.")
            return redirect(request.path)

        try:
            criados_ativos = 0
            criados_inativos = 0

            df = pd.read_excel(arquivo, sheet_name='Planilha1')

            linha_inicial_atual = 5
            coluna_atual = 2

            for i in range(1, 11):                
                # Verifica se o curso não foi preenchido
                if not pd.notna(df.iloc[linha_inicial_atual, coluna_atual]):
                    break

                curso = Curso(
                    nome = df.iloc[linha_inicial_atual, coluna_atual],
                    descricao = df.iloc[linha_inicial_atual + 1, coluna_atual],
                    link = df.iloc[linha_inicial_atual + 2, coluna_atual],
                    inativo = False if df.iloc[linha_inicial_atual + 3, coluna_atual] == 'Ativo' else True,
                    usuario = request.user,
                )
                
                curso.save()

                linha_inicial_atual += 6

                if (curso.inativo):
                    criados_inativos += 1
                else:
                    criados_ativos += 1

            if (criados_ativos == 0 and criados_inativos == 0):
                raise Exception("Nenhum curso foi criado. Verifique o modelo de arquivo utilizado e tente novamente.")

            messages.success(request, f"A partir do upload da planilha preenchida, {criados_ativos} curso(s) ativo(s) e {criados_inativos} curso(s) inativo(s) foram criados com sucesso.")
            return redirect('criar_multiplos_cursos')

        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao processar o arquivo: {e}")
            return redirect(request.path)


class EditarCursoView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cadastros/form_curso.html'
    success_url = reverse_lazy('meus_cursos')

    def test_func(self):
        # Verifica se o usuário é o criador do curso (ou pode ser feito com base no perfil de anunciante)
        curso = self.get_object()
        return curso.usuario == self.request.user or hasattr(self.request.user, 'anuncianteprofile')

    def form_valid(self, form):
        # Mantém o usuário que criou o curso inicialmente
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ExcluirCursoView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Curso
    template_name = 'cadastros/confirmar_exclusao_curso.html'
    success_url = reverse_lazy('meus_cursos')

    def test_func(self):
        curso = self.get_object()
        return curso.usuario == self.request.user


from django.views.generic.detail import DetailView

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'cadastros/curso_detail.html'  # Template que exibe os detalhes do curso
    context_object_name = 'curso'        # Nome da variável no template
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


###############################################################################
###############################################################################
###############################################################################
###############################################################################
class ListaTodosCursosView(ListView):
    model = Curso
    template_name = 'cadastros/lista_todos_cursos.html'
    context_object_name = 'cursos'

    def get_queryset(self):
        # Retorna todas os cursos, apenas os que não estão inativos
        return Curso.objects.filter(inativo=False)

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


class ListaCursosView(LoginRequiredMixin, ListView):
    model = Curso
    template_name = 'cadastros/meus_cursos.html'
    context_object_name = 'cursos'

    def get_queryset(self):
        # Retorna apenas os cursos criados pelo usuário logado (anunciante)
        return Curso.objects.filter(usuario=self.request.user)

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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UploadArquivoSerializer
from .models import Curso
import pandas as pd

class IncluirMultiplosCursosAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if (not hasattr(self.request.user, 'anuncianteprofile')):
            return Response({"erro": "Usuário não autorizado."}, status=403)

        serializer = UploadArquivoSerializer(data=request.data)
        if serializer.is_valid():
            arquivo = serializer.validated_data['arquivo']
            
            if not arquivo.name.endswith('.xlsx'):
                return Response({"erro": "Por favor, envie um arquivo .xlsx válido e baseado no modelo de planilha de curso."}, status=400)
            
            response = self.criarMultiplosCursosAPI(arquivo, self.request.user)

            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def criarMultiplosCursosAPI(self, arquivo, user):
        try:
            criados_ativos = 0
            criados_inativos = 0

            df = pd.read_excel(arquivo, sheet_name='Planilha1')

            linha_inicial_atual = 5
            coluna_atual = 2

            for i in range(1, 11):                
                # Verifica se o curso não foi preenchido
                if not pd.notna(df.iloc[linha_inicial_atual, coluna_atual]):
                    break

                curso = Curso(
                    nome = df.iloc[linha_inicial_atual, coluna_atual],
                    descricao = df.iloc[linha_inicial_atual + 1, coluna_atual],
                    link = df.iloc[linha_inicial_atual + 2, coluna_atual],
                    inativo = False if df.iloc[linha_inicial_atual + 3, coluna_atual] == 'Ativo' else True,
                    usuario = user,
                )
                
                curso.save()

                linha_inicial_atual += 6

                if (curso.inativo):
                    criados_inativos += 1
                else:
                    criados_ativos += 1

            if (criados_ativos == 0 and criados_inativos == 0):
                raise Exception("Nenhum curso foi criado. Verifique o modelo de arquivo utilizado e tente novamente.")

            return Response({
                "mensagem":
                    f"A partir do upload da planilha preenchida, {criados_ativos} curso(s) ativo(s) e {criados_inativos} curso(s) inativo(s) foram criados com sucesso."},
                status=201)


        except Exception as e:
            return Response({
                "mensagem": f"Ocorreu um erro ao processar o arquivo: {e}"
            }, status=400)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UploadArquivoSerializer
from .models import Vaga, Empresa
import pandas as pd

class IncluirMultiplasVagasAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if (not hasattr(self.request.user, 'anuncianteprofile')):
            return Response({"erro": "Usuário não autorizado."}, status=403)

        serializer = UploadArquivoSerializer(data=request.data)
        if serializer.is_valid():
            arquivo = serializer.validated_data['arquivo']
            
            if not arquivo.name.endswith('.xlsx'):
                return Response({"erro": "Por favor, envie um arquivo .xlsx válido e baseado no modelo de planilha de vaga."}, status=400)
            
            response = self.criarMultiplasVagasAPI(arquivo, self.request.user)

            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def criarMultiplasVagasAPI(self, arquivo, user):
        try:
            criadas_ativas = 0
            criadas_inativas = 0

            df = pd.read_excel(arquivo, sheet_name='Planilha1')

            if (pd.notna(df.iloc[4, 2])):
                print(f'Empresa: {df.iloc[4, 2]}')

            empresa = Empresa.objects.get(nome = df.iloc[4, 2])

            linha_inicial_atual = 7
            coluna_atual = 2

            for i in range(1, 11):                
                # Verifica se a vaga não foi preenchida
                if not pd.notna(df.iloc[linha_inicial_atual, coluna_atual]):
                    break

                vaga = Vaga(
                    nome = df.iloc[linha_inicial_atual, coluna_atual],
                    descricao = df.iloc[linha_inicial_atual + 1, coluna_atual],
                    empresa = empresa,
                    link = df.iloc[linha_inicial_atual + 2, coluna_atual],
                    inativa = False if df.iloc[linha_inicial_atual + 3, coluna_atual] == 'Ativa' else True,
                    usuario = user,
                )
                vaga.save()

                linha_inicial_atual += 6

                if (vaga.inativa):
                    criadas_inativas += 1
                else:
                    criadas_ativas += 1
            
            if (criadas_ativas == 0 and criadas_inativas == 0):
                raise Exception("Nenhuma vaga foi criada. Verifique o modelo de arquivo utilizado e tente novamente.")

            return Response({
                "mensagem":
                    f"A partir do upload da planilha preenchida, {criadas_ativas} vaga(s) ativa(s) e {criadas_inativas} vaga(s) inativa(s) foram criadas com sucesso."},
                status=201)

        except Exception as e:
            return Response({
                "mensagem": f"Ocorreu um erro ao processar o arquivo: {e}"
            }, status=400)

