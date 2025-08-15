"""
URLs para API do sistema de presenças.
"""

from django.urls import path
from . import views
from . import inline_views

app_name = "presencas_api"

urlpatterns = [
    # Endpoints principais
    path("atualizar-presencas/", views.atualizar_presencas, name="atualizar_presencas"),
    path(
        "calcular-estatisticas/",
        views.calcular_estatisticas,
        name="calcular_estatisticas",
    ),
    path("buscar-alunos/", views.buscar_alunos, name="buscar_alunos"),
    path("validar-dados/", views.validar_dados, name="validar_dados"),
    path("atividades-turma/", views.atividades_turma, name="atividades_turma"),
    path(
        "configuracao-presenca/",
        views.configuracao_presenca,
        name="configuracao_presenca",
    ),
    # Endpoints para views baseadas em classe (URLs alternativas)
    path(
        "v2/atualizar-presencas/",
        views.AtualizarPresencasView.as_view(),
        name="atualizar_presencas_v2",
    ),
    path(
        "v2/calcular-estatisticas/",
        views.CalcularEstatisticasView.as_view(),
        name="calcular_estatisticas_v2",
    ),
    path(
        "v2/buscar-alunos/", views.BuscarAlunosView.as_view(), name="buscar_alunos_v2"
    ),
    path(
        "v2/validar-dados/", views.ValidarDadosView.as_view(), name="validar_dados_v2"
    ),
    path(
        "v2/atividades-turma/",
        views.AtividadesTurmaView.as_view(),
        name="atividades_turma_v2",
    ),
    path(
        "v2/configuracao-presenca/",
        views.ConfiguracaoPresencaView.as_view(),
        name="configuracao_presenca_v2",
    ),
]

# Adicionar endpoints DRF se disponível
try:
    from . import views

    if hasattr(views, "presencas_resumo"):
        urlpatterns.append(
            path("resumo/", views.presencas_resumo, name="presencas_resumo")
        )
except ImportError:
    pass

# Endpoints de edição inline (PATCH/DELETE)
urlpatterns += [
    path(
        "inline/presencas/<int:pk>/patch/",
        inline_views.presenca_patch,
        name="inline_presenca_patch",
    ),
    path(
        "inline/presencas/<int:pk>/delete/",
        inline_views.presenca_delete,
        name="inline_presenca_delete",
    ),
]
