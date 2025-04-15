from django.urls import path
from . import views

app_name = "iniciacoes"

urlpatterns = [
    path("", views.listar_iniciacoes, name="listar_iniciacoes"),
    path("nova/", views.criar_iniciacao, name="criar_iniciacao"),
    path("<int:id>/editar/", views.editar_iniciacao, name="editar_iniciacao"),
    path(
        "<int:id>/excluir/", views.excluir_iniciacao, name="excluir_iniciacao"
    ),
    path(
        "<int:id>/detalhes/",
        views.detalhar_iniciacao,
        name="detalhar_iniciacao",
    ),
    path("graus/", views.listar_graus, name="listar_graus"),
    path("graus/novo/", views.criar_grau, name="criar_grau"),
    path("graus/<int:id>/editar/", views.editar_grau, name="editar_grau"),
    path("graus/<int:id>/excluir/", views.excluir_grau, name="excluir_grau"),
]
