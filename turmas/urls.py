from django.urls import path
from . import views

app_name = 'turmas'

urlpatterns = [
    # URLs para Turmas
    path('', views.listar_turmas, name='listar_turmas'),
    path('criar/', views.criar_turma, name='criar_turma'),
    path('<int:id>/', views.detalhar_turma, name='detalhar_turma'),
    path('<int:id>/editar/', views.editar_turma, name='editar_turma'),
    path('<int:id>/excluir/', views.excluir_turma, name='excluir_turma'),
    
    # URLs para Matrículas
    path('<int:turma_id>/matricular/', views.matricular_aluno, name='matricular_aluno'),
    path('matricula/<int:matricula_id>/cancelar/', views.cancelar_matricula, name='cancelar_matricula'),
    
    # URLs para Cursos (mantidas para compatibilidade)
    path('cursos/', views.listar_cursos, name='listar_cursos'),
    path('cursos/criar/', views.criar_curso, name='criar_curso'),
    path('cursos/<int:id>/editar/', views.editar_curso, name='editar_curso'),
    path('cursos/<int:id>/excluir/', views.excluir_curso, name='excluir_curso'),
    path('cursos/<int:id>/', views.detalhar_curso, name='detalhar_curso'),
]
