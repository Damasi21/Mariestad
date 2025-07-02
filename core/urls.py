from django.urls import path
from . import views  # Importa as views
from django.contrib.auth.views import LoginView
from .views import gerar_pdf_exemplo




urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
   

    # Produtos
    path('produtos/', views.cadastro_produto, name='cadastro_produto'),
    path('produtos/excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),

    # Configurações
    path('configuracoes/', views.configuracoes, name='configuracoes'),

    path('configuracoes/status/', views.cadastro_status, name='cadastro_status'),
    path('configuracoes/tags/', views.cadastro_tags, name='cadastro_tags'),
    path('configuracoes/status-cliente/', views.cadastro_status_cliente, name='cadastro_status_cliente'),
    path('configuracoes/vendedores/', views.cadastro_vendedores, name='cadastro_vendedores'),
    
    path('configuracoes/usuarios/', views.cadastro_usuarios, name='cadastro_usuarios'),
    path('configuracoes/usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('configuracoes/usuarios/excluir/<int:user_id>/', views.excluir_usuario, name='excluir_usuario'),


    path('status-obra/excluir/<int:id>/', views.excluir_status, name='excluir_status'),
    path('tags/excluir/<int:id>/', views.excluir_tag, name='excluir_tag'),
    path('status-cliente/excluir/<int:id>/', views.excluir_status_cliente, name='excluir_status_cliente'),
    path('configuracoes/vendedores/excluir/<int:id>/', views.excluir_vendedor, name='excluir_vendedor'),

    # Contatos
    path('contatos/', views.cadastro_contatos, name='cadastro_contatos'),


    # Obras
    path('obras/', views.cadastro_obras, name='cadastro_obras'),
    path('obras/excluir/<int:id>/', views.excluir_obra, name='excluir_obra'),
    path('obras/anexar/', views.anexar_arquivos, name='anexar_arquivos'),
    path('obras/listar-anexos/<int:obra_id>/', views.listar_anexos, name='listar_anexos'),
    path('obras/excluir-anexo/', views.excluir_anexo, name='excluir_anexo'),
    path('obras/observacoes/<int:obra_id>/', views.observacoes_obra_ajax, name='observacoes_obra_ajax'),

    # Clientes
    path("clientes/", views.cadastro_clientes, name="cadastro_clientes"),
    path('buscar_dados_empresa/', views.buscar_dados_empresa, name='buscar_dados_empresa'),
    path('clientes/contatos/', views.listar_contatos_cliente, name='listar_contatos_cliente'),
    path('clientes/salvar-contato/', views.salvar_contato, name='salvar_contato'),
    path('clientes/excluir-contato/<int:id>/', views.excluir_contato, name='excluir_contato'),
    path('clientes/contato/<int:id>/', views.contato_por_id, name='contato_por_id'),
    path('clientes/editar-contato/<int:id>/', views.editar_contato, name='editar_contato'), 
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),


     # Mapas
    path('clientes/mapa/', views.mapa_clientes, name='mapa_clientes'),
    path('clientes/mapa/json/', views.clientes_mapa_json, name='clientes_mapa_json'),
    path('obras/mapa/json/', views.obras_mapa_json, name='obras_mapa_json'),

    
    # Propostas 
    path('propostas/', views.cadastro_propostas, name='cadastro_propostas'),
    path('propostas/obras/<int:cliente_id>/', views.carregar_obras_por_cliente, name='carregar_obras_por_cliente'),
    path('propostas/contatos/<int:cliente_id>/', views.carregar_contatos_por_cliente, name='carregar_contatos_por_cliente'),
    path('buscar-clientes', views.buscar_clientes_ajax, name='buscar_clientes'),
    path('buscar-obras', views.buscar_obras_ajax, name='buscar_obras'),
    path('buscar-transportadoras', views.buscar_transportadoras_ajax, name='buscar_transportadoras'),
    path('propostas/dados-cliente/', views.dados_cliente_ajax, name='dados_cliente_ajax'),
    path('propostas/produtos-json/', views.produtos_json, name='produtos_json'),
    path('propostas/carregar/<int:proposta_id>/', views.carregar_proposta, name='carregar_proposta'),
    path('propostas/excluir/<int:proposta_id>/', views.excluir_proposta, name='excluir_proposta'),
    path('propostas/observacoes-obra/<int:obra_id>/', views.observacoes_obra_ajax, name='observacoes_obra_ajax'),
    path("propostas/buscar/", views.buscar_propostas_ajax, name="buscar_propostas_ajax"),

    path("proposta/exemplo/", gerar_pdf_exemplo, name="proposta_pdf_exemplo"),
    path("proposta/<int:proposta_id>/pdf/", gerar_pdf_exemplo, name="proposta_pdf"), 


    

    # Login / logout 
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
 
]
