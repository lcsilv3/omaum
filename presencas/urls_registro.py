"""
URLs para fluxo guiado de registro de presenças (wizard).
Endpoints para as 5 etapas do registro.
"""

from django.urls import path
from .views import (
    registrar_presenca_academica,
    registrar_presenca_dados_basicos,
    registrar_presenca_dados_basicos_ajax,
    registrar_presenca_totais_atividades,
    registrar_presenca_totais_atividades_ajax,
    registrar_presenca_dias_atividades,
    registrar_presenca_dias_atividades_ajax,
    registrar_presenca_alunos,
    registrar_presenca_alunos_ajax,
    registrar_presenca_confirmar,
    registrar_presenca_confirmar_ajax,
    registrar_presenca_convocados,
    registrar_presenca_convocados_ajax,
    toggle_convocacao_ajax,
)
from .views_ext import registro_presenca as views_registro_presenca

urlpatterns = [
    path("", registrar_presenca_academica, name="registrar_presenca_academica"),
    path("dados-basicos/", registrar_presenca_dados_basicos, name="registrar_presenca_dados_basicos"),
    path("dados-basicos/ajax/", registrar_presenca_dados_basicos_ajax, name="registrar_presenca_dados_basicos_ajax"),
    path("totais-atividades/", registrar_presenca_totais_atividades, name="registrar_presenca_totais_atividades"),
    path("totais-atividades/ajax/", registrar_presenca_totais_atividades_ajax, name="registrar_presenca_totais_atividades_ajax"),
    path("dias-atividades/", registrar_presenca_dias_atividades, name="registrar_presenca_dias_atividades"),
    path("dias-atividades/ajax/", registrar_presenca_dias_atividades_ajax, name="registrar_presenca_dias_atividades_ajax"),
    path("alunos/", registrar_presenca_alunos, name="registrar_presenca_alunos"),
    path("alunos/ajax/", registrar_presenca_alunos_ajax, name="registrar_presenca_alunos_ajax"),
    path("confirmar/", registrar_presenca_confirmar, name="registrar_presenca_confirmar"),
    path("confirmar/ajax/", registrar_presenca_confirmar_ajax, name="registrar_presenca_confirmar_ajax"),
    path("convocados/", registrar_presenca_convocados, name="registrar_presenca_convocados"),
    path("convocados/ajax/", registrar_presenca_convocados_ajax, name="registrar_presenca_convocados_ajax"),
    path("convocados/toggle/", toggle_convocacao_ajax, name="toggle_convocacao_ajax"),
    path("atividades-por-turma/", views_registro_presenca.atividades_por_turma_ajax, name="atividades_por_turma_ajax"),
]
