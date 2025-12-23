"""
URLs para as views de estatísticas de presença.
"""

from django.urls import path
from . import views_estatisticas

urlpatterns = [
    path("dashboard/", views_estatisticas.dashboard_presencas, name="dashboard"),
    path("consolidado/aluno/<int:aluno_id>/", views_estatisticas.consolidado_aluno, name="consolidado_aluno"),
    path("consolidado/tabela/", views_estatisticas.tabela_consolidada, name="tabela_consolidada"),
    path("estatisticas/turma/<int:turma_id>/", views_estatisticas.estatisticas_turma, name="estatisticas_turma"),
    path("recalcular-carencias/", views_estatisticas.recalcular_carencias, name="recalcular_carencias"),
    path("exportar/consolidado/", views_estatisticas.exportar_consolidado, name="exportar_consolidado"),
]
