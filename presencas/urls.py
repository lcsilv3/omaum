from django.urls import path
from .views_main import listar_presencas_academicas

app_name = "presencas"

urlpatterns = [
    path("listar/", listar_presencas_academicas, name="listar_presencas"),
]
