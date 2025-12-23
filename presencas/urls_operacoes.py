"""
URLs para operações CRUD básicas e auxiliares.
Endpoints para exclusão, importação, exportação e observações.
"""

from django.urls import path
from .views import (
    excluir_presenca_academica,
    exportar_presencas_academicas,
    importar_presencas_academicas,
    listar_observacoes_presenca,
    toggle_convocacao_ajax,
)

urlpatterns = [
    path("excluir/<int:pk>/", excluir_presenca_academica, name="excluir_presenca_academica"),
    path("exportar/", exportar_presencas_academicas, name="exportar_presencas_academicas"),
    path("importar/", importar_presencas_academicas, name="importar_presencas_academicas"),
    path("observacoes/", listar_observacoes_presenca, name="listar_observacoes_presenca"),
    path("ajax/toggle-convocacao/", toggle_convocacao_ajax, name="toggle_convocacao_ajax"),
]
