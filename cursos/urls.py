from django.urls import path
from . import views

app_name = "cursos"

urlpatterns = [
    path("", views.listar_cursos, name="listar_cursos"),
    path("criar/", views.criar_curso, name="criar_curso"),
    path("<int:codigo_curso>/", views.detalhar_curso, name="detalhar_curso"),
    path(
        "<int:codigo_curso>/editar/", views.editar_curso, name="editar_curso"
    ),
    path(
        "<int:codigo_curso>/excluir/",
        views.excluir_curso,
        name="excluir_curso",
    ),
    path("exportar/", views.exportar_cursos, name="exportar_cursos"),
    path("importar/", views.importar_cursos, name="importar_cursos"),
]
