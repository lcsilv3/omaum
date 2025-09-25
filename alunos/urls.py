from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alunos.views import (
    listar_alunos_view,
    criar_aluno,
    detalhar_aluno,
    editar_aluno,
    excluir_aluno,
    search_alunos,
    painel,
    exportar_alunos,
    importar_alunos,
    relatorio_alunos,
    confirmar_remocao_instrutoria,
    diagnostico_instrutores,
    listar_tipos_codigos_ajax,
    listar_codigos_por_tipo_ajax,
)
from . import api_views
from . import views_novo

app_name = "alunos"

from .views.localidade_api import (
    search_paises,
    search_estados,
    search_cidades,
    get_cidades_por_estado,
    search_bairros,
    get_bairros_por_cidade,
)

# Rotas simples removidas definitivamente
router = DefaultRouter()

urlpatterns = [
    path("criar/", criar_aluno, name="criar_aluno"),
    path("listar/", listar_alunos_view, name="listar_alunos"),
    # Alias global para compatibilidade com {% url 'listar_alunos' %}
    path("listar/", listar_alunos_view, name="listar_alunos"),
    # Autocomplete AJAX (django-select2)
    path("autocomplete/", include("alunos.urls_autocomplete")),
    # Rotas de tipos/códigos iniciáticos
    path("codigos/", include("alunos.urls_codigos")),
    # URLs principais - sistema completo (ATIVO)
    path("<int:aluno_id>/detalhes/", detalhar_aluno, name="detalhar_aluno"),
    path("<int:aluno_id>/editar/", editar_aluno, name="editar_aluno"),
    path("<int:aluno_id>/excluir/", excluir_aluno, name="excluir_aluno"),
    path("painel/", painel, name="painel"),
    # APIs do painel (corrigido para views_novo)
    path("api/painel/kpis/", views_novo.painel_kpis_api, name="painel_kpis_api"),
    path(
        "api/painel/graficos/",
        views_novo.painel_graficos_api,
        name="painel_graficos_api",
    ),
    path("api/painel/tabela/", views_novo.painel_tabela_api, name="painel_tabela_api"),
    path("exportar/", exportar_alunos, name="exportar_alunos"),
    path("importar/", importar_alunos, name="importar_alunos"),
    path("relatorio/", relatorio_alunos, name="relatorio_alunos"),
    path(
        "relatorio/ficha-cadastral/",
        views_novo.relatorio_ficha_cadastral,
        name="relatorio_ficha_cadastral",
    ),
    path(
        "relatorio/dados-iniciaticos/",
        views_novo.relatorio_dados_iniciaticos,
        name="relatorio_dados_iniciaticos",
    ),
    path(
        "relatorio/historico/",
        views_novo.relatorio_historico_aluno,
        name="relatorio_historico_aluno",
    ),
    path(
        "relatorio/auditoria/",
        views_novo.relatorio_auditoria_dados,
        name="relatorio_auditoria_dados",
    ),
    path(
        "relatorio/demografico/",
        views_novo.relatorio_demografico,
        name="relatorio_demografico",
    ),
    path(
        "relatorio/aniversariantes/",
        views_novo.relatorio_aniversariantes,
        name="relatorio_aniversariantes",
    ),
    path("search/", search_alunos, name="search_alunos"),
    path(
        "<str:cpf>/confirmar-remocao-instrutoria/<str:nova_situacao>/",
        confirmar_remocao_instrutoria,
        name="confirmar_remocao_instrutoria",
    ),
    path(
        "api/verificar-elegibilidade/<str:cpf>/",
        api_views.verificar_elegibilidade_endpoint,
        name="verificar_elegibilidade_instrutor",
    ),
    path(
        "diagnostico-instrutores/",
        diagnostico_instrutores,
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
    path("api/tipos-codigos/", listar_tipos_codigos_ajax, name="api_tipos_codigos"),
    path(
        "api/codigos-por-tipo/",
        listar_codigos_por_tipo_ajax,
        name="api_codigos_por_tipo",
    ),
    path(
        "api/<int:aluno_id>/historico/",
        api_views.listar_historico_aluno_api,
        name="api_historico_aluno",
    ),
    # Rotas da API base (ViewSet Aluno) - manter após endpoints específicos
    path("api/", include(router.urls)),
]
