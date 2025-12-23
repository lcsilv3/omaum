"""
URLs para edição de presenças (lote e individual).
Endpoints para modificação de dados de presença após registro.
"""

from django.urls import path
from .views import (
    editar_presencas_lote,
    editar_lote_dados_basicos,
    editar_lote_totais_atividades,
    editar_lote_dias_atividades,
    editar_lote_dias_atividades_ajax,
    editar_presenca_dados_basicos,
    editar_presenca_totais_atividades,
    editar_presenca_dias_atividades,
    editar_presenca_alunos,
    editar_presenca_academica,
)

urlpatterns = [
    path("lote/", editar_presencas_lote, name="editar_presencas_lote"),
    path("lote/dados-basicos/", editar_lote_dados_basicos, name="editar_lote_dados_basicos"),
    path("lote/totais-atividades/", editar_lote_totais_atividades, name="editar_lote_totais_atividades"),
    path("lote/dias-atividades/", editar_lote_dias_atividades, name="editar_lote_dias_atividades"),
    path("lote/dias-atividades/ajax/", editar_lote_dias_atividades_ajax, name="editar_lote_dias_atividades_ajax"),
    path("<int:pk>/dados-basicos/", editar_presenca_dados_basicos, name="editar_presenca_dados_basicos"),
    path("<int:pk>/totais-atividades/", editar_presenca_totais_atividades, name="editar_presenca_totais_atividades"),
    path("<int:pk>/dias-atividades/", editar_presenca_dias_atividades, name="editar_presenca_dias_atividades"),
    path("<int:pk>/alunos/", editar_presenca_alunos, name="editar_presenca_alunos"),
    path("<int:pk>/", editar_presenca_academica, name="editar_presenca"),
]
