
from django.urls import path
from . import views  # Importa as views

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial

    # Produtos
    path('produtos/', views.cadastro_produto, name='cadastro_produto'),
    path('produtos/excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),

    # Configurações
    path('configuracoes/', views.configuracoes, name='configuracoes'),

    # Novo: rotas de telas separadas
    path('configuracoes/status/', views.cadastro_status, name='cadastro_status'),
    path('configuracoes/tags/', views.cadastro_tags, name='cadastro_tags'),
    path('configuracoes/status-cliente/', views.cadastro_status_cliente, name='cadastro_status_cliente'),

    path('status-obra/excluir/<int:id>/', views.excluir_status, name='excluir_status'),
    path('tags/excluir/<int:id>/', views.excluir_tag, name='excluir_tag'),
    path('status-cliente/excluir/<int:id>/', views.excluir_status_cliente, name='excluir_status_cliente'),

    # Contatos
    path('contatos/', views.cadastro_contatos, name='cadastro_contatos'),


    # Obras
    path('obras/', views.cadastro_obras, name='cadastro_obras'),
    path('obras/excluir/<int:id>/', views.excluir_obra, name='excluir_obra'),
    path('obras/anexar/', views.anexar_arquivos, name='anexar_arquivos'),
    path('obras/listar-anexos/<int:obra_id>/', views.listar_anexos, name='listar_anexos'),
    path('obras/excluir-anexo/', views.excluir_anexo, name='excluir_anexo'),



    # Clientes
    path("clientes/", views.cadastro_clientes, name="cadastro_clientes"),
    path('buscar_dados_empresa/', views.buscar_dados_empresa, name='buscar_dados_empresa'),
    path('clientes/contatos/', views.listar_contatos_cliente, name='listar_contatos_cliente'),
    path('clientes/salvar-contato/', views.salvar_contato, name='salvar_contato'),
    path('clientes/excluir-contato/<int:id>/', views.excluir_contato, name='excluir_contato'),
    path('clientes/contato/<int:id>/', views.contato_por_id, name='contato_por_id'),
    path('clientes/editar-contato/<int:id>/', views.editar_contato, name='editar_contato'), 

     # Mapas
    path('clientes/mapa/', views.mapa_clientes, name='mapa_clientes'),
    path('clientes/mapa/json/', views.clientes_mapa_json, name='clientes_mapa_json'),


]
