from django.urls import path
from . import views

app_name = "atividades"  # Definindo o namespace

urlpatterns = [
    path("", views.listar_atividades, name="listar_atividades"),
    # Atividades Acadêmicas
    path(
        "academicas/",
        views.listar_atividades_academicas,
        name="listar_atividades_academicas",
    ),
    path(
        "academicas/criar/",
        views.criar_atividade_academica,
        name="criar_atividade_academica",
    ),
    path(
        "academicas/editar/<int:pk>/",
        views.editar_atividade_academica,
        name="editar_atividade_academica",
    ),
    path(
        "academicas/excluir/<int:pk>/",
        views.excluir_atividade_academica,
        name="excluir_atividade_academica",
    ),
    path(
        "academicas/detalhar/<int:pk>/",
        views.detalhar_atividade_academica,
        name="detalhar_atividade_academica",
    ),
    path(
        "academicas/confirmar-exclusao/<int:pk>/",
        views.confirmar_exclusao_academica,
        name="confirmar_exclusao_academica",
    ),
    path(
        "academicas/<int:id>/copiar/",
        views.copiar_atividade_academica,
        name="copiar_atividade_academica",
    ),
    # Atividades Ritualísticas
    path(
        "ritualisticas/",
        views.listar_atividades_ritualisticas,
        name="listar_atividades_ritualisticas",
    ),
    path(
        "ritualisticas/criar/",
        views.criar_atividade_ritualistica,
        name="criar_atividade_ritualistica",
    ),
    path(
        "ritualisticas/editar/<int:pk>/",
        views.editar_atividade_ritualistica,
        name="editar_atividade_ritualistica",
    ),
    path(
        "ritualisticas/excluir/<int:pk>/",
        views.excluir_atividade_ritualistica,
        name="excluir_atividade_ritualistica",
    ),
    path(
        "ritualisticas/detalhar/<int:pk>/",
        views.detalhar_atividade_ritualistica,
        name="detalhar_atividade_ritualistica",
    ),
    path(
        "ritualisticas/confirmar-exclusao/<int:pk>/",
        views.confirmar_exclusao_ritualistica,
        name="confirmar_exclusao_ritualistica",
    ),
    path(
        "ritualisticas/<int:id>/copiar/",
        views.copiar_atividade_ritualistica,
        name="copiar_atividade_ritualistica",
    ),
    # Novas funcionalidades
    path("relatorio/", views.relatorio_atividades, name="relatorio_atividades"),
    path("exportar/<str:formato>/", views.exportar_atividades, name="exportar_atividades"),
    path("calendario/", views.calendario_atividades, name="calendario_atividades"),
    path("dashboard/", views.dashboard_atividades, name="dashboard_atividades"),
    # APIs
    path("api/eventos/", views.api_eventos_calendario, name="api_eventos_calendario"),
    path("api/evento/<int:evento_id>/", views.api_detalhe_evento, name="api_detalhe_evento"),
]
