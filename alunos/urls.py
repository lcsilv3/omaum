from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views
from .views.localidade_api import (
    search_paises,
    search_estados,
    search_cidades,
    get_cidades_por_estado,
)

app_name = "alunos"

router = DefaultRouter()
router.register(r"", api_views.AlunoViewSet, basename="aluno")

urlpatterns = [
    path("", views.listar_alunos, name="listar_alunos"),
    path("criar/", views.criar_aluno, name="criar_aluno"),
    path("<str:cpf>/detalhes/", views.detalhar_aluno, name="detalhar_aluno"),
    path("<str:cpf>/editar/", views.editar_aluno, name="editar_aluno"),
    path("<str:cpf>/excluir/", views.excluir_aluno, name="excluir_aluno"),
    path("painel/", views.painel, name="painel"),
    path("exportar/", views.exportar_alunos, name="exportar_alunos"),
    path("importar/", views.importar_alunos, name="importar_alunos"),
    path("relatorio/", views.relatorio_alunos, name="relatorio_alunos"),
    path("search/", views.search_alunos, name="search_alunos"),
    path(
        "<str:cpf>/confirmar-remocao-instrutoria/<str:nova_situacao>/",
        views.confirmar_remocao_instrutoria,
        name="confirmar_remocao_instrutoria",
    ),
    path(
        "api/verificar-elegibilidade/<str:cpf>/",
        api_views.verificar_elegibilidade_endpoint,
        name="verificar_elegibilidade_instrutor",
    ),
    path(
        "diagnostico-instrutores/",
        views.diagnostico_instrutores,
        name="diagnostico_instrutores",
    ),
    # Rotas da API
    path("api/", include(router.urls)),
    # APIs de localidade
    path("api/paises/", search_paises, name="api_search_paises"),
    path("api/estados/", search_estados, name="api_search_estados"),
    path("api/cidades/", search_cidades, name="api_search_cidades"),
    path(
        "api/cidades/estado/<int:estado_id>/",
        get_cidades_por_estado,
        name="api_cidades_por_estado",
    ),
]
