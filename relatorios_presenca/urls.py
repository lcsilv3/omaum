from django.urls import path
from . import views

app_name = "relatorios_presenca"

urlpatterns = [
    path("dashboard/", views.dashboard_relatorios, name="dashboard_relatorios"),
    path(
        "frequencia-por-atividade/",
        views.frequencia_por_atividade,
        name="frequencia_por_atividade",
    ),
    path("relatorio-faltas/", views.relatorio_faltas, name="relatorio_faltas"),
    path("alunos-com-carencia/", views.alunos_com_carencia, name="alunos_com_carencia"),
    path("", views.relatorio_form, name="relatorio_form"),
    path(
        "exportar/consolidado/",
        views.exportar_relatorio_consolidado,
        name="exportar_relatorio_consolidado",
    ),
    # AJAX Endpoints
    path(
        "ajax/turmas-por-curso/",
        views.turmas_por_curso_json,
        name="turmas_por_curso_json",
    ),
    path(
        "ajax/alunos-por-turma/",
        views.alunos_por_turma_json,
        name="alunos_por_turma_json",
    ),
    path(
        "ajax/consolidado-tabela/",
        views.consolidado_tabela_ajax,
        name="consolidado_tabela_ajax",
    ),
    # Boletim de Frequência do Aluno
    path(
        "boletim/aluno/",
        views.boletim_frequencia_aluno,
        name="boletim_frequencia_aluno",
    ),
]
