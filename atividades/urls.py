from django.urls import path
from . import views_ext
from . import views_api
from .views_ext.relatorios_academicos import relatorio_atividades_academicas
from .views_ext.relatorios_ritualisticos import relatorio_atividades_ritualisticas
from .views_ext import importacao

app_name = "atividades"

urlpatterns = [
    # Atividades Acadêmicas
    path("academicas/", views_ext.academicas.listar_atividades_academicas, name="listar_atividades_academicas"),
    path("academicas/criar/", views_ext.academicas.criar_atividade_academica, name="criar_atividade_academica"),
    path("academicas/<int:id>/editar/", views_ext.academicas.editar_atividade_academica, name="editar_atividade_academica"),
    path("academicas/<int:id>/detalhes/", views_ext.academicas.detalhar_atividade_academica, name="detalhar_atividade_academica"),
    path("academicas/<int:id>/excluir/", views_ext.academicas.excluir_atividade_academica, name="excluir_atividade_academica"),
    path("academicas/<int:id>/copiar/", views_ext.academicas.copiar_atividade_academica, name="copiar_atividade_academica"),

    # AJAX: turmas por curso (listagem)
    path("ajax/turmas-por-curso/", views_ext.academicas.ajax_turmas_por_curso, name="ajax_turmas_por_curso"),
    # AJAX: atividades filtradas (listagem)
    path("ajax/atividades-filtradas/", views_ext.academicas.ajax_atividades_filtradas, name="ajax_atividades_filtradas"),

    # Relatório de atividades por curso/turma
    path(
        "relatorio/curso-turma/",
        views_ext.relatorios.relatorio_atividades_curso_turma,
        name="relatorio_atividades"
    ),
    # Relatório de atividades acadêmicas
    path(
        "relatorio/academicas/",
        relatorio_atividades_academicas,
        name="relatorio_atividades_academicas"
    ),
    # Relatório de atividades ritualísticas
    path(
        "relatorio/ritualisticas/",
        relatorio_atividades_ritualisticas,
        name="relatorio_atividades_ritualisticas"
    ),
    # AJAX: turmas por curso (relatório)
    path("ajax/relatorio/turmas-por-curso/", views_ext.relatorios.ajax_turmas_por_curso_relatorio, name="ajax_turmas_por_curso_relatorio"),
    # AJAX: atividades filtradas (relatório)
    path("ajax/relatorio/atividades-filtradas/", views_ext.relatorios.ajax_atividades_filtradas_relatorio, name="ajax_atividades_filtradas_relatorio"),

    # Dashboard de atividades
    path("dashboard/", views_ext.dashboard.dashboard_atividades, name="dashboard_atividades"),
    # AJAX: turmas por curso (dashboard)
    path("ajax/dashboard/turmas-por-curso/", views_ext.dashboard.ajax_turmas_por_curso_dashboard, name="ajax_turmas_por_curso_dashboard"),
    # AJAX: dashboard filtrado
    path("ajax/dashboard/conteudo/", views_ext.dashboard.ajax_dashboard_conteudo, name="ajax_dashboard_conteudo"),

    # Atividades Ritualísticas
    path("ritualisticas/", views_ext.ritualisticas.listar_atividades_ritualisticas, name="listar_atividades_ritualisticas"),
    path("ritualisticas/criar/", views_ext.ritualisticas.criar_atividade_ritualistica, name="criar_atividade_ritualistica"),
    path("ritualisticas/<int:id>/editar/", views_ext.ritualisticas.editar_atividade_ritualistica, name="editar_atividade_ritualistica"),
    path("ritualisticas/<int:id>/detalhes/", views_ext.ritualisticas.detalhar_atividade_ritualistica, name="detalhar_atividade_ritualistica"),
    path("ritualisticas/<int:id>/excluir/", views_ext.ritualisticas.excluir_atividade_ritualistica, name="excluir_atividade_ritualistica"),
    path("ritualisticas/<int:id>/copiar/", views_ext.ritualisticas.copiar_atividade_ritualistica, name="copiar_atividade_ritualistica"),

    # Calendário de Atividades
    path("calendario_atividades/", views_ext.calendario.calendario_atividades, name="calendario_atividades"),

    # API
    path("api/filtrar-atividades/", views_api.api_filtrar_atividades, name="api_filtrar_atividades"),

    # Importação de Atividades
    path(
        "academicas/importar/",
        importacao.importar_atividades_academicas,
        name="importar_atividades_academicas"
    ),
    path(
        "ritualisticas/importar/",
        importacao.importar_atividades_ritualisticas,
        name="importar_atividades_ritualisticas"
    ),
]