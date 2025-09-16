"""
URLs para o app relatorios_presenca.
Segue padrão de nomenclatura estabelecido nas premissas.
"""

from django.urls import path
from . import views

app_name = "relatorios_presenca"

urlpatterns = [
    # URLs principais seguindo padrão: ação_recurso
    path("", views.listar_relatorios, name="listar_relatorios"),
    path("gerar/", views.gerar_relatorio, name="gerar_relatorio"),
    path(
        "detalhar/<int:relatorio_id>/",
        views.detalhar_relatorio,
        name="detalhar_relatorio",
    ),
    path(
        "excluir/<int:relatorio_id>/", views.excluir_relatorio, name="excluir_relatorio"
    ),
    # URLs AJAX para filtros dinâmicos
    path(
        "ajax/atividades-turma/",
        views.ajax_obter_atividades_turma,
        name="ajax_obter_atividades_turma",
    ),
    path(
        "ajax/periodos-turma/",
        views.ajax_obter_periodos_turma,
        name="ajax_obter_periodos_turma",
    ),
    path(
        "ajax/validar-parametros/",
        views.ajax_validar_parametros,
        name="ajax_validar_parametros",
    ),
]
