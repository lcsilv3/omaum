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
        "<int:id>/adicionar-aluno/",
        views.adicionar_aluno_turma,
        name="matricular_aluno",
    ),
    path(
        "<int:id>/matricular-aluno/",
        views.adicionar_aluno_turma,
        name="matricular_aluno",
    ),
    path(
        "<int:turma_id>/remover-aluno/<str:aluno_id>/",
        views.remover_aluno_turma,
        name="remover_aluno_turma",
    ),
    path("dashboard/", views.dashboard_turmas, name="dashboard"),
    path(
        "<int:id>/alunos/",
        views.listar_alunos_matriculados,
        name="listar_alunos_matriculados",
    ),
]
