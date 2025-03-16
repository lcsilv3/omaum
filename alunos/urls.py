from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    path('', views.listar_alunos, name='listar'),
    path('buscar/', views.listar_alunos, name='buscar'),
    path('cadastrar/', views.cadastrar_aluno, name='cadastrar'),
    path('editar/<str:cpf>/', views.editar_aluno, name='editar'),
    path('excluir/<str:cpf>/', views.excluir_aluno, name='excluir'),
    path('detalhes/<str:cpf>/', views.detalhes_aluno, name='detalhes'),
]

