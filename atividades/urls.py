from django.urls import path
from . import views_api
from .views_ext.relatorios import (
    relatorio_atividades,
    relatorio_atividades_curso_turma,
    ajax_turmas_por_curso_relatorio,
    ajax_atividades_filtradas_relatorio,
)
from .views_ext import importacao
from .views_ext.dashboard import (
    dashboard_atividades,
    ajax_turmas_por_curso_dashboard,
    ajax_dashboard_conteudo,
)
from .views_ext.calendario import calendario_atividades
from .views_ext.academicas import (
    listar_atividades_academicas,
    criar_atividade_academica,
    editar_atividade_academica,
    detalhar_atividade_academica,
    excluir_atividade_academica,
    copiar_atividade_academica,
    api_get_turmas_por_curso,
    ajax_atividades_filtradas,
)
# Atividades ritualísticas foram removidas no refatoramento

app_name = "atividades"

urlpatterns = [
    # Atividades (principal)
    path("", listar_atividades_academicas, name="listar_atividades"),
    path("listar/", listar_atividades_academicas, name="listar_atividades_academicas"),
    path("criar/", criar_atividade_academica, name="criar_atividade"),
    path("criar/", criar_atividade_academica, name="criar_atividade_academica"),
    path("<int:id>/editar/", editar_atividade_academica, name="editar_atividade"),
    path("<int:id>/editar/", editar_atividade_academica, name="editar_atividade_academica"),
    path("<int:id>/detalhes/", detalhar_atividade_academica, name="detalhar_atividade"),
    path("<int:id>/detalhes/", detalhar_atividade_academica, name="detalhar_atividade_academica"),
    path("<int:id>/excluir/", excluir_atividade_academica, name="excluir_atividade"),
    path("<int:id>/excluir/", excluir_atividade_academica, name="excluir_atividade_academica"),
    path("<int:id>/copiar/", copiar_atividade_academica, name="copiar_atividade"),
    path("<int:id>/copiar/", copiar_atividade_academica, name="copiar_atividade_academica"),

    # AJAX: turmas por curso (listagem)
    path("ajax/turmas-por-curso/", api_get_turmas_por_curso, name="ajax_turmas_por_curso"),
    # AJAX: atividades filtradas (listagem)
    path("ajax/atividades-filtradas/", ajax_atividades_filtradas, name="ajax_atividades_filtradas"),

    # Relatório de atividades por curso/turma
    path(
        "relatorio/curso-turma/",
        relatorio_atividades_curso_turma,
        name="relatorio_atividades"
    ),
    # Relatório de atividades
    path(
        "relatorio/",
        relatorio_atividades,
        name="relatorio_atividades"
    ),
    # AJAX: turmas por curso (relatório)
    path("ajax/relatorio/turmas-por-curso/", ajax_turmas_por_curso_relatorio, name="ajax_turmas_por_curso_relatorio"),
    # AJAX: atividades filtradas (relatório)
    path("ajax/relatorio/atividades-filtradas/", ajax_atividades_filtradas_relatorio, name="ajax_atividades_filtradas_relatorio"),

    # Dashboard de atividades
    path("dashboard/", dashboard_atividades, name="dashboard_atividades"),
    # AJAX: turmas por curso (dashboard)
    path("ajax/dashboard/turmas-por-curso/", ajax_turmas_por_curso_dashboard, name="ajax_turmas_por_curso_dashboard"),
    # AJAX: dashboard filtrado
    path("ajax/dashboard/conteudo/", ajax_dashboard_conteudo, name="ajax_dashboard_conteudo"),

    # Calendário de Atividades
    path("calendario_atividades/", calendario_atividades, name="calendario_atividades"),

    # API
    path("api/filtrar-atividades/", views_api.api_filtrar_atividades, name="api_filtrar_atividades"),

    # Importação de Atividades
    path(
        "importar/",
        importacao.importar_atividades_academicas,
        name="importar_atividades"
    ),
]