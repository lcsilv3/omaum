from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alunos.views import (
    main as main_views,
    relatorio_views,
    api_views,
    listar_tipos_codigos_ajax,
    listar_codigos_por_tipo_ajax,
    localidade_api,
)
from alunos.api.viewsets import AlunoViewSet

app_name = "alunos"

router = DefaultRouter()
router.register(r"api/alunos", AlunoViewSet, basename="aluno")

urlpatterns = [
    # Views principais
    path("", main_views.listar_alunos_view, name="listar_alunos"),
    path("criar/", main_views.criar_aluno, name="criar_aluno"),
    path("<int:aluno_id>/detalhes/", main_views.detalhar_aluno, name="detalhar_aluno"),
    path("<int:aluno_id>/editar/", main_views.editar_aluno, name="editar_aluno"),
    path("<int:aluno_id>/excluir/", main_views.excluir_aluno, name="excluir_aluno"),
    path("search/", main_views.search_alunos, name="search_alunos"),
    # Painel e Relatórios
    path("painel/", relatorio_views.painel, name="painel"),
    path(
        "relatorios/ficha-cadastral/",
        relatorio_views.relatorio_ficha_cadastral,
        name="relatorio_ficha_cadastral",
    ),
    # Adicionar outras URLs de relatório aqui quando forem implementadas
    # Relatórios complementares
    path(
        "relatorios/dados-iniciaticos/",
        relatorio_views.relatorio_dados_iniciaticos,
        name="relatorio_dados_iniciaticos",
    ),
    path(
        "relatorios/historico-aluno/",
        relatorio_views.relatorio_historico_aluno,
        name="relatorio_historico_aluno",
    ),
    path(
        "relatorios/auditoria-dados/",
        relatorio_views.relatorio_auditoria_dados,
        name="relatorio_auditoria_dados",
    ),
    path(
        "relatorios/demografico/",
        relatorio_views.relatorio_demografico,
        name="relatorio_demografico",
    ),
    path(
        "relatorios/aniversariantes/",
        relatorio_views.relatorio_aniversariantes,
        name="relatorio_aniversariantes",
    ),
    # Tipos e Códigos Iniciáticos
    path("", include("alunos.urls_codigos")),
    # API
    path("api/search/", api_views.search_alunos, name="api_search_alunos"),
    path(
        "api/instrutores/", api_views.search_instrutores, name="api_search_instrutores"
    ),
    path("api/alunos/<str:cpf>/", api_views.get_aluno, name="api_get_aluno"),
    path(
        "api/alunos/<str:cpf>/elegibilidade/",
        api_views.verificar_elegibilidade_endpoint,
        name="api_verificar_elegibilidade",
    ),
    path(
        "api/alunos/<str:cpf>/detalhes/",
        api_views.get_aluno_detalhes,
        name="api_get_aluno_detalhes",
    ),
    path(
        "api/alunos/<int:aluno_id>/historico/",
        api_views.listar_historico_aluno_api,
        name="api_historico_aluno",
    ),
    path(
        "api/alunos/<int:aluno_id>/historico/criar/",
        api_views.criar_historico_aluno_api,
        name="api_criar_historico_aluno",
    ),
    path(
        "api/alunos/<int:aluno_id>/historico/<int:registro_id>/desativar/",
        api_views.desativar_historico_aluno_api,
        name="api_desativar_historico_aluno",
    ),
    path(
        "api/alunos/<int:aluno_id>/historico/<int:registro_id>/reativar/",
        api_views.reativar_historico_aluno_api,
        name="api_reativar_historico_aluno",
    ),
    path(
        "api/tipos-codigos/",
        listar_tipos_codigos_ajax,
        name="api_tipos_codigos",
    ),
    path(
        "api/codigos-por-tipo/",
        listar_codigos_por_tipo_ajax,
        name="api_codigos_por_tipo",
    ),
    path(
        "api/painel/kpis/",
        api_views.painel_kpis_api,
        name="api_painel_kpis",
    ),
    path(
        "api/painel/graficos/",
        api_views.painel_graficos_api,
        name="api_painel_graficos",
    ),
    path(
        "api/painel/tabela/",
        api_views.painel_tabela_api,
        name="api_painel_tabela",
    ),
    # APIs de Localidade (Estados e Cidades)
    path(
        "api/localidade/paises/",
        localidade_api.search_paises,
        name="api_search_paises",
    ),
    path(
        "api/localidade/estados/",
        localidade_api.search_estados,
        name="api_search_estados",
    ),
    path(
        "api/localidade/cidades/",
        localidade_api.search_cidades,
        name="api_search_cidades",
    ),
    path(
        "api/localidade/estados/<int:estado_id>/cidades/",
        localidade_api.get_cidades_por_estado,
        name="api_cidades_por_estado",
    ),
    path(
        "api/localidade/bairros/",
        localidade_api.search_bairros,
        name="api_search_bairros",
    ),
    path(
        "api/localidade/cidades/<int:cidade_id>/bairros/",
        localidade_api.get_bairros_por_cidade,
        name="api_bairros_por_cidade",
    ),
    # API de busca de foto por número iniciático
    path(
        "api/buscar-foto/<str:numero_iniciatico>/",
        api_views.buscar_foto_por_numero_iniciatico,
        name="api_buscar_foto_numero_iniciatico",
    ),
    # API para servir fotos de diretórios externos
    path(
        "api/servir-foto/<str:numero_iniciatico>/",
        api_views.servir_foto_externa,
        name="api_servir_foto_externa",
    ),
    path("", include(router.urls)),
]
