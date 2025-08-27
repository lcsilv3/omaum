from django.urls import path
from . import views_codigos

urlpatterns = [
    path("tipos/", views_codigos.listar_tipocodigos, name="listar_tipocodigos"),
    path("tipos/criar/", views_codigos.criar_tipocodigo, name="criar_tipocodigo"),
    path(
        "tipos/<int:pk>/editar/",
        views_codigos.editar_tipocodigo,
        name="editar_tipocodigo",
    ),
    path(
        "tipos/<int:pk>/excluir/",
        views_codigos.excluir_tipocodigo,
        name="excluir_tipocodigo",
    ),
    path("codigos/", views_codigos.listar_codigos, name="listar_codigos"),
    path("codigos/criar/", views_codigos.criar_codigo, name="criar_codigo"),
    path("codigos/<int:pk>/editar/", views_codigos.editar_codigo, name="editar_codigo"),
    path(
        "codigos/<int:pk>/excluir/", views_codigos.excluir_codigo, name="excluir_codigo"
    ),
]
