
from django.urls import path
from . import views  # Importa as views

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
      # Página de cadastro de clientes
    

    path('produtos/', views.cadastro_produto, name='cadastro_produto'),
    path('produtos/excluir/<int:id>/', views.excluir_produto, name='excluir_produto'),
    
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('status-obra/excluir/<int:id>/', views.excluir_status, name='excluir_status'),
    path('tags/excluir/<int:id>/', views.excluir_tag, name='excluir_tag'),
    path('status-cliente/excluir/<int:id>/', views.excluir_status_cliente, name='excluir_status_cliente'),


    path('contatos/', views.cadastro_contatos, name='cadastro_contatos'),
    path('contatos/excluir/<int:id>/', views.excluir_contato, name='excluir_contato'),

    path('obras/', views.cadastro_obras, name='cadastro_obras'),
    path('obras/excluir/<int:id>/', views.excluir_obra, name='excluir_obra'),
    path('obras/anexar/', views.anexar_arquivos, name='anexar_arquivos'),
    path('obras/listar-anexos/<int:obra_id>/', views.listar_anexos, name='listar_anexos'),
    path('obras/excluir-anexo/', views.excluir_anexo, name='excluir_anexo'),





]


    
