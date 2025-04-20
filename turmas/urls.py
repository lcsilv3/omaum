from django.urls import path
from . import views

app_name = "turmas"

urlpatterns = [
    path("", views.listar_turmas, name="listar_turmas"),
    path("criar/", views.criar_turma, name="criar_turma"),
    path("<int:id>/", views.detalhar_turma, name="detalhar_turma"),
    path("<int:id>/editar/", views.editar_turma, name="editar_turma"),
    path("<int:id>/excluir/", views.excluir_turma, name="excluir_turma"),
    path(
        "<int:id>/alunos/",
        views.listar_alunos_matriculados,
        name="listar_alunos_matriculados",
    ),
    path(
        "<int:turma_id>/matricular/",
        views.matricular_aluno,
        name="matricular_aluno",
    ),
    path(
        "<int:turma_id>/cancelar-matricula/<str:aluno_cpf>/",
        views.cancelar_matricula,
        name="cancelar_matricula",
    ),
]
