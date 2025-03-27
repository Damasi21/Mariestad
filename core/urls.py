
from django.urls import path
from . import views  # Importa as views

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
    path('cadastro_clientes/', views.cadastro_clientes, name='cadastro_clientes'),  # Página de cadastro de clientes
    path('cadastro_tags/', views.cadastro_tags, name='cadastro_tags'),
    path('cadastro_status/', views.cadastro_status, name='cadastro_status'),
    path('cadastro_obras/', views.cadastro_obras, name='cadastro_obras'),
    path('cadastro_contatos/', views.cadastro_contatos, name='cadastro_contatos'),


    path('salvar_status/', views.salvar_status, name='salvar_status'),  # Adicione esta linha
    path("editar_status/<int:id>/", views.editar_status, name="editar_status"),
    path("excluir_status/<int:id>/", views.excluir_status, name="excluir_status"),

    path('salvar_tags/', views.salvar_tags, name='salvar_tags'),  # Adicione esta linha
    path("editar_tags/<int:id>/", views.editar_tags, name="editar_tags"),
    path("excluir_tags/<int:id>/", views.excluir_tags, name="excluir_tags"),

    path('cadastro_produto/', views.cadastro_produto, name='cadastro_produto'),
    path('excluir_produto/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),

    path('excluir_obra/<int:id>/', views.excluir_obra, name='excluir_obra'),

    path('editar_contato/<int:id>/', views.editar_contato, name='editar_contato'),
    path('excluir_contato/<int:id>/', views.excluir_contato, name='excluir_contato'),



    path('buscar_dados_empresa/', views.buscar_dados_empresa, name='buscar_dados_empresa'),
]

    
