from django.urls import path
from . import views
from . import views_api
from .views.relatorios_academicos import relatorio_atividades_academicas
from .views.relatorios_ritualisticos import relatorio_atividades_ritualisticas
from .views import importacao

app_name = "atividades"

urlpatterns = [
    # Atividades Acadêmicas
    path("academicas/", views.academicas.listar_atividades_academicas, name="listar_atividades_academicas"),
    path("academicas/criar/", views.academicas.criar_atividade_academica, name="criar_atividade_academica"),
    path("academicas/<int:id>/editar/", views.academicas.editar_atividade_academica, name="editar_atividade_academica"),
    path("academicas/<int:id>/detalhes/", views.academicas.detalhar_atividade_academica, name="detalhar_atividade_academica"),
    path("academicas/<int:id>/excluir/", views.academicas.excluir_atividade_academica, name="excluir_atividade_academica"),
    path("academicas/<int:id>/copiar/", views.academicas.copiar_atividade_academica, name="copiar_atividade_academica"),

    # AJAX: turmas por curso (listagem)
    path("ajax/turmas-por-curso/", views.academicas.ajax_turmas_por_curso, name="ajax_turmas_por_curso"),
    # AJAX: atividades filtradas (listagem)
    path("ajax/atividades-filtradas/", views.academicas.ajax_atividades_filtradas, name="ajax_atividades_filtradas"),

    # Relatório de atividades por curso/turma
    path(
        "relatorio/curso-turma/",
        views.relatorios.relatorio_atividades_curso_turma,
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
    path("ajax/relatorio/turmas-por-curso/", views.relatorios.ajax_turmas_por_curso_relatorio, name="ajax_turmas_por_curso_relatorio"),
    # AJAX: atividades filtradas (relatório)
    path("ajax/relatorio/atividades-filtradas/", views.relatorios.ajax_atividades_filtradas_relatorio, name="ajax_atividades_filtradas_relatorio"),

    # Dashboard de atividades
    path("dashboard/", views.dashboard.dashboard_atividades, name="dashboard_atividades"),
    # AJAX: turmas por curso (dashboard)
    path("ajax/dashboard/turmas-por-curso/", views.dashboard.ajax_turmas_por_curso_dashboard, name="ajax_turmas_por_curso_dashboard"),
    # AJAX: dashboard filtrado
    path("ajax/dashboard/conteudo/", views.dashboard.ajax_dashboard_conteudo, name="ajax_dashboard_conteudo"),

    # Atividades Ritualísticas
    path("ritualisticas/", views.ritualisticas.listar_atividades_ritualisticas, name="listar_atividades_ritualisticas"),
    path("ritualisticas/criar/", views.ritualisticas.criar_atividade_ritualistica, name="criar_atividade_ritualistica"),
    path("ritualisticas/<int:id>/editar/", views.ritualisticas.editar_atividade_ritualistica, name="editar_atividade_ritualistica"),
    path("ritualisticas/<int:id>/detalhes/", views.ritualisticas.detalhar_atividade_ritualistica, name="detalhar_atividade_ritualistica"),
    path("ritualisticas/<int:id>/excluir/", views.ritualisticas.excluir_atividade_ritualistica, name="excluir_atividade_ritualistica"),
    path("ritualisticas/<int:id>/copiar/", views.ritualisticas.copiar_atividade_ritualistica, name="copiar_atividade_ritualistica"),

    # Calendário de Atividades
    path("calendario_atividades/", views.calendario.calendario_atividades, name="calendario_atividades"),

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