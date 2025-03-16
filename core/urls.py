from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('alunos/', views.aluno_list, name='listar_alunos'),
    path('alunos/create/', views.aluno_create, name='cadastrar_aluno'),
    path('alunos/<int:pk>/', views.aluno_detail, name='detalhes_aluno'),
    path('alunos/<int:pk>/update/', views.aluno_update, name='editar_aluno'),
    path('alunos/<int:pk>/delete/', views.aluno_delete, name='excluir_aluno'),
    path('turmas/', views.turma_list, name='listar_turmas'),
    path('turmas/create/', views.turma_create, name='cadastrar_turma'),  # Verify this is correct
    path('turmas/<int:pk>/', views.turma_detail, name='detalhes_turma'),
    path('turmas/<int:pk>/update/', views.turma_update, name='editar_turma'),
    path('turmas/<int:pk>/delete/', views.turma_delete, name='excluir_turma'),
    path('atividades_academicas/', views.atividade_academica_list, name='listar_atividades_academicas'),
    path('atividades_academicas/create/', views.atividade_academica_create, name='cadastrar_atividade_academica'),
    path('atividades_academicas/<int:pk>/', views.atividade_academica_detail, name='detalhes_atividade_academica'),
    path('atividades_academicas/<int:pk>/update/', views.atividade_academica_update, name='editar_atividade_academica'),
    path('atividades_academicas/<int:pk>/delete/', views.atividade_academica_delete, name='excluir_atividade_academica'),
    path('atividades_ritualisticas/', views.listar_atividades_ritualisticas, name='listar_atividades_ritualisticas'),
    path('presencas_academicas/', views.listar_presencas_academicas, name='listar_presencas_academicas'),
    path('cargos_administrativos/', views.listar_cargos_administrativos, name='listar_cargos_administrativos'),
    path('relatorios/alunos/', views.relatorio_alunos, name='relatorio_alunos'),
    path('punicoes/', views.listar_punicoes, name='listar_punicoes'),
    path('iniciacoes/', views.listar_iniciacoes, name='listar_iniciacoes'),
    path('registro/', views.registro, name='registro'),
]