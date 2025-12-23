"""
URLs para detalhamento/visualização de presenças.
Endpoints para consulta e análise (sem edição).
"""

from django.urls import path
from .views import (
    detalhar_presenca_dados_basicos,
    detalhar_presenca_totais_atividades,
    detalhar_presenca_dias_atividades,
    detalhar_presenca_alunos,
    detalhar_presenca_academica,
)

urlpatterns = [
    path("<int:pk>/dados-basicos/", detalhar_presenca_dados_basicos, name="detalhar_presenca_dados_basicos"),
    path("<int:pk>/totais-atividades/", detalhar_presenca_totais_atividades, name="detalhar_presenca_totais_atividades"),
    path("<int:pk>/dias-atividades/", detalhar_presenca_dias_atividades, name="detalhar_presenca_dias_atividades"),
    path("<int:pk>/alunos/", detalhar_presenca_alunos, name="detalhar_presenca_alunos"),
    path("<int:pk>/", detalhar_presenca_academica, name="detalhar_presenca_academica"),
]
