from django.urls import path
from . import views_api
from .views_ext.relatorios import (
    relatorio_atividades,
    relatorio_atividades_curso_turma,
    relatorio_participacao_atividades,
    ajax_turmas_por_curso_relatorio,
    ajax_atividades_filtradas_relatorio,
    ajax_relatorio_participacao_tabela,
    exportar_atividades,
    exportar_relatorio_participacao,
    relatorio_frequencia_turmas,
    relatorio_cronograma_curso_turmas,
    exportar_relatorio_cronograma,
    relatorio_historico_aluno,
    exportar_relatorio_historico_aluno,
    ajax_relatorio_historico_tabela,
    ajax_relatorio_historico_opcoes,
    relatorio_carga_instrutores,
    exportar_relatorio_carga_instrutores,
    ajax_relatorio_carga_instrutores_tabela,
    exportar_relatorio_frequencia,
    ajax_relatorio_frequencia_tabela,
    ajax_relatorio_frequencia_opcoes,
    ajax_relatorio_cronograma_tabela,
    ajax_relatorio_cronograma_opcoes,
)
from .views_ext import importacao
from .views_ext.dashboard import (
    dashboard_atividades,
    ajax_turmas_por_curso_dashboard,
    ajax_dashboard_conteudo,
)
from .views_ext.calendario import calendario_atividades
from .views_ext.academicas import (
    listar_atividades_academicas,
    criar_atividade_academica,
    editar_atividade_academica,
    detalhar_atividade_academica,
    excluir_atividade_academica,
    copiar_atividade_academica,
    api_get_turmas_por_curso,
    ajax_atividades_filtradas,
)
# Atividades ritualísticas foram removidas no refatoramento

app_name = "atividades"

urlpatterns = [
    # Atividades (principal)
    path("", listar_atividades_academicas, name="listar_atividades"),
    path("listar/", listar_atividades_academicas, name="listar_atividades_academicas"),
    path("criar/", criar_atividade_academica, name="criar_atividade"),
    path("criar/", criar_atividade_academica, name="criar_atividade_academica"),
    path("<int:id>/editar/", editar_atividade_academica, name="editar_atividade"),
    path(
        "<int:id>/editar/",
        editar_atividade_academica,
        name="editar_atividade_academica",
    ),
    path("<int:id>/detalhes/", detalhar_atividade_academica, name="detalhar_atividade"),
    path(
        "<int:id>/detalhes/",
        detalhar_atividade_academica,
        name="detalhar_atividade_academica",
    ),
    path("<int:id>/excluir/", excluir_atividade_academica, name="excluir_atividade"),
    path(
        "<int:id>/excluir/",
        excluir_atividade_academica,
        name="excluir_atividade_academica",
    ),
    path("<int:id>/copiar/", copiar_atividade_academica, name="copiar_atividade"),
    path(
        "<int:id>/copiar/",
        copiar_atividade_academica,
        name="copiar_atividade_academica",
    ),
    # AJAX: turmas por curso (listagem)
    path(
        "ajax/turmas-por-curso/", api_get_turmas_por_curso, name="ajax_turmas_por_curso"
    ),
    # AJAX: atividades filtradas (listagem)
    path(
        "ajax/atividades-filtradas/",
        ajax_atividades_filtradas,
        name="ajax_atividades_filtradas",
    ),
    # Relatório de atividades por curso/turma
    path(
        "relatorio/curso-turma/",
        relatorio_atividades_curso_turma,
        name="relatorio_atividades",
    ),
    # Relatório de atividades
    path("relatorio/", relatorio_atividades, name="relatorio_atividades"),
    path(
        "relatorio/exportar/<str:formato>/",
        exportar_atividades,
        name="exportar_atividades",
    ),
    path(
        "relatorio/participacao/",
        relatorio_participacao_atividades,
        name="relatorio_participacao_atividades",
    ),
    path(
        "relatorio/participacao/exportar/<str:formato>/",
        exportar_relatorio_participacao,
        name="exportar_relatorio_participacao",
    ),
    path(
        "relatorio/carga-instrutores/",
        relatorio_carga_instrutores,
        name="relatorio_carga_instrutores",
    ),
    path(
        "relatorio/carga-instrutores/exportar/<str:formato>/",
        exportar_relatorio_carga_instrutores,
        name="exportar_relatorio_carga_instrutores",
    ),
    # AJAX: turmas por curso (relatório)
    path(
        "ajax/relatorio/turmas-por-curso/",
        ajax_turmas_por_curso_relatorio,
        name="ajax_turmas_por_curso_relatorio",
    ),
    # AJAX: atividades filtradas (relatório)
    path(
        "ajax/relatorio/atividades-filtradas/",
        ajax_atividades_filtradas_relatorio,
        name="ajax_atividades_filtradas_relatorio",
    ),
    path(
        "ajax/relatorio/participacao/tabela/",
        ajax_relatorio_participacao_tabela,
        name="ajax_relatorio_participacao_tabela",
    ),
    path(
        "ajax/relatorio/carga-instrutores/tabela/",
        ajax_relatorio_carga_instrutores_tabela,
        name="ajax_relatorio_carga_instrutores_tabela",
    ),
    # Relatório de Frequência por Turma
    path(
        "relatorio/frequencia/",
        relatorio_frequencia_turmas,
        name="relatorio_frequencia_turmas",
    ),
    path(
        "relatorio/frequencia/exportar/<str:formato>/",
        exportar_relatorio_frequencia,
        name="exportar_relatorio_frequencia",
    ),
    path(
        "ajax/relatorio/frequencia/tabela/",
        ajax_relatorio_frequencia_tabela,
        name="ajax_relatorio_frequencia_tabela",
    ),
    path(
        "ajax/relatorio/frequencia/opcoes/",
        ajax_relatorio_frequencia_opcoes,
        name="ajax_relatorio_frequencia_opcoes",
    ),
    # Relatório Cronograma Curso x Turmas
    path(
        "relatorio/cronograma/",
        relatorio_cronograma_curso_turmas,
        name="relatorio_cronograma_curso_turmas",
    ),
    path(
        "relatorio/cronograma/exportar/<str:formato>/",
        exportar_relatorio_cronograma,
        name="exportar_relatorio_cronograma",
    ),
    path(
        "ajax/relatorio/cronograma/tabela/",
        ajax_relatorio_cronograma_tabela,
        name="ajax_relatorio_cronograma_tabela",
    ),
    path(
        "ajax/relatorio/cronograma/opcoes/",
        ajax_relatorio_cronograma_opcoes,
        name="ajax_relatorio_cronograma_opcoes",
    ),
    # Relatório Histórico do Aluno
    path(
        "relatorio/historico-aluno/",
        relatorio_historico_aluno,
        name="relatorio_historico_aluno",
    ),
    path(
        "relatorio/historico-aluno/exportar/<str:formato>/",
        exportar_relatorio_historico_aluno,
        name="exportar_relatorio_historico_aluno",
    ),
    path(
        "ajax/relatorio/historico/tabela/",
        ajax_relatorio_historico_tabela,
        name="ajax_relatorio_historico_tabela",
    ),
    path(
        "ajax/relatorio/historico/opcoes/",
        ajax_relatorio_historico_opcoes,
        name="ajax_relatorio_historico_opcoes",
    ),
    # Dashboard de atividades
    path("dashboard/", dashboard_atividades, name="dashboard_atividades"),
    # AJAX: turmas por curso (dashboard)
    path(
        "ajax/dashboard/turmas-por-curso/",
        ajax_turmas_por_curso_dashboard,
        name="ajax_turmas_por_curso_dashboard",
    ),
    # AJAX: dashboard filtrado
    path(
        "ajax/dashboard/conteudo/",
        ajax_dashboard_conteudo,
        name="ajax_dashboard_conteudo",
    ),
    # Calendário de Atividades
    path("calendario_atividades/", calendario_atividades, name="calendario_atividades"),
    # API
    path(
        "api/filtrar-atividades/",
        views_api.api_filtrar_atividades,
        name="api_filtrar_atividades",
    ),
    # Importação de Atividades
    path(
        "importar/",
        importacao.importar_atividades_academicas,
        name="importar_atividades_academicas",
    ),
]
