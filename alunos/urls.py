from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views
from .views.localidade_api import (
    search_paises,
    search_estados,
    search_cidades,
    get_cidades_por_estado,
    search_bairros,
    get_bairros_por_cidade,
)

app_name = "alunos"

router = DefaultRouter()
router.register(r"", api_views.AlunoViewSet, basename="aluno")

urlpatterns = [
    # Sistema completo como padrão
    path("", views.listar_alunos_view, name="listar_alunos"),
    # CRUD de Tipos e Códigos
    path("tipos-codigos/", include("alunos.urls_codigos")),
    path("criar/", views.criar_aluno, name="criar_aluno"),
    # Autocomplete AJAX (django-select2)
    path("autocomplete/", include("alunos.urls_autocomplete")),
    # URLs principais - sistema completo (ATIVO)
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
    # APIs de localidade (devem vir antes do include do router para evitar shadowing)
    path("api/paises/", search_paises, name="api_search_paises"),
    path("api/estados/", search_estados, name="api_search_estados"),
    path("api/cidades/", search_cidades, name="api_search_cidades"),
    path(
        "api/cidades/estado/<int:estado_id>/",
        get_cidades_por_estado,
        name="api_cidades_por_estado",
    ),
    path("api/bairros/", search_bairros, name="api_search_bairros"),
    path(
        "api/bairros/cidade/<int:cidade_id>/",
        get_bairros_por_cidade,
        name="api_bairros_por_cidade",
    ),
    # APIs para filtros dinâmicos - Dados Iniciáticos (devem vir antes do include(router.urls))
    path(
        "api/tipos-codigos/", views.listar_tipos_codigos_ajax, name="api_tipos_codigos"
    ),
    path(
        "api/codigos-por-tipo/",
        views.listar_codigos_por_tipo_ajax,
        name="api_codigos_por_tipo",
    ),
    # Rotas da API base (ViewSet Aluno) - manter após endpoints específicos
    path("api/", include(router.urls)),
]