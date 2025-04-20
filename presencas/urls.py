from django.urls import path
from . import views

app_name = "presencas"

urlpatterns = [
    path("", views.listar_presencas, name="listar_presencas"),
    path(
        "<int:presenca_id>/", views.detalhar_presenca, name="detalhar_presenca"
    ),
    path("criar/", views.criar_presenca, name="criar_presenca"),
    path(
        "<int:presenca_id>/editar/",
        views.editar_presenca,
        name="editar_presenca",
    ),
    path(
        "<int:presenca_id>/excluir/",
        views.excluir_presenca,
        name="excluir_presenca",
    ),
    path("relatorio/", views.relatorio_presencas, name="relatorio_presencas"),
]
