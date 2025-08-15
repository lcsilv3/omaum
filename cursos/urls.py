from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = "cursos"

# Roteador para a API
router = DefaultRouter()
router.register(r"api", api_views.CursoViewSet, basename="curso-api")

# URLs da aplicação web e da API
urlpatterns = [
    # URLs da Aplicação Web
    path("", views.listar_cursos, name="listar_cursos"),
    path("relatorio/", views.relatorio_cursos, name="relatorio_cursos"),
    path("relatorio/pdf/", views.gerar_relatorio_pdf, name="gerar_relatorio_pdf"),
    path("criar/", views.criar_curso, name="criar_curso"),
    path("<int:id>/", views.detalhar_curso, name="detalhar_curso"),
    path("<int:id>/editar/", views.editar_curso, name="editar_curso"),
    path("<int:id>/excluir/", views.excluir_curso, name="excluir_curso"),
    path("exportar/", views.exportar_cursos, name="exportar_cursos"),
    path("importar/", views.importar_cursos, name="importar_cursos"),
    # URLs da API
    path("", include(router.urls)),
]
