from django.urls import path
from . import views

app_name = "turmas"

urlpatterns = [
    path("", views.listar_turmas, name="listar_turmas"),
    path("criar/", views.criar_turma, name="criar_turma"),
    path("<int:turma_id>/", views.detalhar_turma, name="detalhar_turma"),
    path("<int:turma_id>/editar/", views.editar_turma, name="editar_turma"),
    path("<int:turma_id>/excluir/", views.excluir_turma, name="excluir_turma"),
    path("<int:turma_id>/alunos/", views.listar_alunos_matriculados, name="listar_alunos_matriculados"),
    path("<int:turma_id>/matricular/", views.matricular_aluno, name="matricular_aluno"),
    path("<int:turma_id>/cancelar-matricula/<str:aluno_cpf>/", views.cancelar_matricula, name="cancelar_matricula"),
    path("exportar/", views.exportar_turmas, name="exportar_turmas"),
    path("relatorio/", views.relatorio_turmas, name="relatorio_turmas"),
    path("dashboard/", views.dashboard_turmas, name="dashboard"),
]
