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
    path('turmas/create/', views.turma_create, name='cadastrar_turma'),
    path('turmas/<int:pk>/', views.turma_detail, name='detalhes_turma'),
    path('turmas/<int:pk>/update/', views.turma_update, name='editar_turma'),
    path('turmas/<int:pk>/delete/', views.turma_delete, name='excluir_turma'),
    path('registro/', views.registro, name='registro'),
]