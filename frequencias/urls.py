from django.urls import path
from .views import (
    listar_frequencias,
    criar_frequencia_mensal,
    editar_frequencia_mensal,
    excluir_frequencia_mensal,
    detalhar_frequencia_mensal,
    recalcular_carencias,
    editar_carencia,
    resolver_carencia,
    detalhar_carencia,
    iniciar_acompanhamento,
    listar_notificacoes_carencia,
    criar_notificacao,
    detalhar_notificacao,
    editar_notificacao,
    enviar_notificacao,
    reenviar_notificacao,
    responder_aluno,
    relatorio_frequencias,
    exportar_frequencia_csv,
    historico_frequencia,
    exportar_historico,
    dashboard,
    painel_frequencias,
    visualizar_painel_frequencias,
    exportar_frequencias,
    importar_frequencias,
)
from .views import api_views

app_name = "frequencias"

urlpatterns = [
    # Views principais seguindo o padrão do contrato
    path("", listar_frequencias, name="listar_frequencias"),
    path("criar/", criar_frequencia_mensal, name="criar_frequencia"),
    path("criar-mensal/", criar_frequencia_mensal, name="criar_frequencia_mensal"),
    path(
        "<int:frequencia_id>/editar/",
        editar_frequencia_mensal,
        name="editar_frequencia",
    ),
    path(
        "<int:frequencia_id>/excluir/",
        excluir_frequencia_mensal,
        name="excluir_frequencia",
    ),
    path(
        "<int:frequencia_id>/", detalhar_frequencia_mensal, name="detalhar_frequencia"
    ),
    path(
        "<int:frequencia_id>/recalcular/",
        recalcular_carencias,
        name="recalcular_carencias",
    ),
    # Carências
    path(
        "carencias/<int:carencia_id>/editar/", editar_carencia, name="editar_carencia"
    ),
    path(
        "carencias/<int:carencia_id>/resolver/",
        resolver_carencia,
        name="resolver_carencia",
    ),
    path("carencias/<int:carencia_id>/", detalhar_carencia, name="detalhar_carencia"),
    path(
        "carencias/<int:carencia_id>/iniciar-acompanhamento/",
        iniciar_acompanhamento,
        name="iniciar_acompanhamento",
    ),
    # Notificações
    path("notificacoes/", listar_notificacoes_carencia, name="listar_notificacoes"),
    path(
        "notificacoes/criar/<int:carencia_id>/",
        criar_notificacao,
        name="criar_notificacao",
    ),
    path(
        "notificacoes/<int:notificacao_id>/",
        detalhar_notificacao,
        name="detalhar_notificacao",
    ),
    path(
        "notificacoes/<int:notificacao_id>/editar/",
        editar_notificacao,
        name="editar_notificacao",
    ),
    path(
        "notificacoes/<int:notificacao_id>/enviar/",
        enviar_notificacao,
        name="enviar_notificacao",
    ),
    path(
        "notificacoes/<int:notificacao_id>/reenviar/",
        reenviar_notificacao,
        name="reenviar_notificacao",
    ),
    path(
        "notificacoes/<int:notificacao_id>/responder/",
        responder_aluno,
        name="responder_aluno",
    ),
    # Exportação e relatórios
    path(
        "<int:frequencia_id>/exportar/",
        exportar_frequencia_csv,
        name="exportar_frequencia_csv",
    ),
    path("painel/", painel_frequencias, name="painel_frequencias"),
    path(
        "painel/visualizar/<int:turma_id>/<int:mes_inicio>/"
        "<int:ano_inicio>/<int:mes_fim>/<int:ano_fim>/",
        visualizar_painel_frequencias,
        name="visualizar_painel_frequencias",
    ),
    path("relatorio/", relatorio_frequencias, name="relatorio_frequencias"),
    path(
        "historico/<str:aluno_cpf>/", historico_frequencia, name="historico_frequencia"
    ),
    path(
        "historico/<str:aluno_cpf>/exportar/",
        exportar_historico,
        name="exportar_historico",
    ),
    path("exportar/", exportar_frequencias, name="exportar_frequencias"),
    path("importar/", importar_frequencias, name="importar_frequencias"),
    # Dashboard
    path("dashboard/", dashboard, name="dashboard"),
    # APIs
    path(
        "api/dados-frequencia/<int:frequencia_id>/",
        api_views.obter_dados_frequencia,
        name="api_obter_dados_frequencia",
    ),
    path(
        "api/dados-painel-frequencias/",
        api_views.obter_dados_painel_frequencias,
        name="api_obter_dados_painel_frequencias",
    ),
]
