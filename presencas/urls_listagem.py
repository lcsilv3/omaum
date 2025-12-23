"""
URLs para listagem de presenças.
Endpoints para visualização e filtros.
"""

from django.urls import path
from .views import listar_presencas_academicas

urlpatterns = [
    path("", listar_presencas_academicas, name="listar_presencas_academicas"),
]
