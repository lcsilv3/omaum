from django.urls import path
from . import views

app_name = "punicoes"

urlpatterns = [
    path("", views.listar_punicoes, name="listar_punicoes"),
    path("nova/", views.criar_punicao, name="criar_punicao"),
    path("<int:id>/editar/", views.editar_punicao, name="editar_punicao"),
    path("<int:id>/excluir/", views.excluir_punicao, name="excluir_punicao"),
    path(
        "<int:id>/detalhes/", views.detalhar_punicao, name="detalhar_punicao"
    ),
    path("tipos/", views.listar_tipos_punicao, name="listar_tipos_punicao"),
    path("tipos/novo/", views.criar_tipo_punicao, name="criar_tipo_punicao"),
    path(
        "tipos/<int:id>/editar/",
        views.editar_tipo_punicao,
        name="editar_tipo_punicao",
    ),
    path(
        "tipos/<int:id>/excluir/",
        views.excluir_tipo_punicao,
        name="excluir_tipo_punicao",
    ),
]
