from django.urls import path
from .views import *

urlpatterns = [
#    path('painel/', PainelAnuncianteView.as_view(), name='painel_anunciante'),
    path('criar-vaga/', CriarVagaView.as_view(), name='criar_vaga'),
    path('criar-vaga/<int:empresa_id>/', CriarVagaView.as_view(), name='criar_vaga_empresa'),  # Com empresa específica
    path('criar-empresa/', CriarEmpresaView.as_view(), name='criar_empresa'),
#    path('empresa/<int:pk>/vagas/', ListarVagasPorEmpresaView.as_view(), name='listar_vagas_empresa'),
    path('editar-vaga/<int:pk>/', EditarVagaView.as_view(), name='editar_vaga'),

    path('todas-vagas/', ListaTodasVagasView.as_view(), name='todas_vagas'),
    path('minhas-vagas/', ListaVagasView.as_view(), name='minhas_vagas'),
    path('editar-vaga/<int:pk>/', EditarVagaView.as_view(), name='editar_vaga'),
    path('excluir-vaga/<int:pk>/', ExcluirVagaView.as_view(), name='excluir_vaga'),

    #    path('cadastrar/empresa', EmpresaCreate.as_view(), name='cadastrar-empresa'),
    #    path('cadastrar/vaga', VagaCreate.as_view(), name='cadastrar-vaga'),
    #
    #
#        path('editar/empresa/<int:pk>/', EmpresaUpdate.as_view(), name='editar-empresa'),
#        path('editar/vaga/<int:pk>/', VagaUpdate.as_view(), name='editar-vaga'),
    #    #
    #    path('excluir/empresa/<int:pk>/', EmpresaDelete.as_view(), name='excluir-empresa'),
    #    path('excluir/vaga/<int:pk>/', VagaDelete.as_view(), name='excluir-vaga'),
    #
    #    path('listar/empresas/', EmpresaList.as_view(), name='listar-empresas'),
#        path('listar/vagas/', VagaList.as_view(), name = 'listar-vagas'),
    #
    #    path('listar/mural/', AlunoList.as_view(), name = 'mural'),
    #
    #    path('listar/vaga/<int:pk>', AnuncioList.as_view(), name= 'anuncio'),
#    path('empresas/', ListaEmpresasView.as_view(), name='listar_empresas'),
#    path('empresa/<int:pk>/', EmpresaDetailView.as_view(), name='detalhe_empresa'),
    path('empresas/', ListarEmpresasView.as_view(), name='listar_empresas'),
    path('empresas/<int:pk>/vagas/', ListarVagasPorEmpresaView.as_view(), name='listar_vagas_empresa'),
    path('vaga/<int:pk>/', VagaDetailView.as_view(), name='vaga_detail'),
]




