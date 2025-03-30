from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    path('', views.listar_alunos, name='listar_alunos'),
    path('buscar/', views.buscar_alunos, name='buscar_alunos'),
    path('cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('editar/<str:cpf>/', views.editar_aluno, name='editar_aluno'),
    path('excluir/<str:cpf>/', views.excluir_aluno, name='excluir_aluno'),
    path('detalhes/<str:cpf>/', views.detalhes_aluno, name='detalhar_aluno'),
    path('exportar/', views.exportar_alunos, name='exportar_alunos'),
    path('importar/', views.importar_alunos, name='importar_alunos'),
    path('relatorio/', views.relatorio_alunos, name='relatorio_alunos'),
    path('dashboard/', views.dashboard, name='dashboard_alunos'),
]
