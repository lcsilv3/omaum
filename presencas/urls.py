from django.urls import path, include
from presencas.views_ext import registro_presenca
from .views_ext.multiplas import (
    registrar_presencas_multiplas,
    formulario_presencas_multiplas,
)
from . import views
from .views_ext.academicas import listar_presencas_academicas
from .views_ext.registro_presenca import (
    registrar_presenca_dados_basicos,
    registrar_presenca_dados_basicos_ajax,
    registrar_presenca_totais_atividades,
    registrar_presenca_totais_atividades_ajax,
    registrar_presenca_dias_atividades,
    registrar_presenca_dias_atividades_ajax,
    registrar_presenca_alunos,
    registrar_presenca_alunos_ajax,
    registrar_presenca_confirmar,
    registrar_presenca_confirmar_ajax,
    turmas_por_curso_ajax,
    atividades_por_turma_ajax,
    obter_limites_calendario_ajax,
    editar_presenca_dados_basicos,
    editar_presenca_totais_atividades,
    editar_presenca_dias_atividades,
    editar_presenca_alunos,
    detalhar_presenca_dados_basicos,
    detalhar_presenca_totais_atividades,
    detalhar_presenca_dias_atividades,
    detalhar_presenca_alunos,
)
from .views.consolidado import (
    ConsolidadoPresencasView,
    FiltroConsolidadoView,
    ExportarConsolidadoView,
)
from .views.registro_rapido import (
    registro_rapido_otimizado,
    buscar_alunos_ajax,
    obter_alunos_turma_ajax,
    salvar_presencas_lote_ajax,
    validar_presenca_ajax,
    atualizar_convocacao_ajax,
)
from .views.painel import (
    PainelEstatisticasView,
    PainelDadosAjaxView,
    ExportarRelatorioView,
)
from .views.exportacao_simplificada import (
    ExportacaoAvancadaView,
    ProcessarExportacaoView,
    GerenciarAgendamentosView,
    agendamento_form_ajax,
)

app_name = "presencas"

urlpatterns = [
    # Presenças (principal)
    path("", listar_presencas_academicas, name="listar_presencas"),
    path(
        "listar/", listar_presencas_academicas, name="listar_presencas_academicas"
    ),
    path("registrar/", views.registrar_presenca_academica, name="registrar_presenca"),
    path(
        "registrar/",
        views.registrar_presenca_academica,
        name="registrar_presenca_academica",
    ),
    path("editar/<int:pk>/", views.editar_presenca_academica, name="editar_presenca"),
    path(
        "editar/<int:pk>/",
        views.editar_presenca_academica,
        name="editar_presenca_academica",
    ),
    path(
        "excluir/<int:pk>/", views.excluir_presenca_academica, name="excluir_presenca"
    ),
    path(
        "excluir/<int:pk>/",
        views.excluir_presenca_academica,
        name="excluir_presenca_academica",
    ),
    path(
        "detalhar/<int:pk>/",
        views.detalhar_presenca_academica,
        name="detalhar_presenca",
    ),
    path(
        "detalhar/<int:pk>/",
        views.detalhar_presenca_academica,
        name="detalhar_presenca_academica",
    ),
    path("exportar/", views.exportar_presencas_academicas, name="exportar_presencas"),
    path(
        "exportar/",
        views.exportar_presencas_academicas,
        name="exportar_presencas_academicas",
    ),
    path("importar/", views.importar_presencas_academicas, name="importar_presencas"),
    path(
        "importar/",
        views.importar_presencas_academicas,
        name="importar_presencas_academicas",
    ),
    # Observações de presença
    path(
        "observacoes/",
        views.listar_observacoes_presenca,
        name="listar_observacoes_presenca",
    ),
    # Outras rotas dos submódulos, se necessário
    path(
        "multiplas/",
        registrar_presencas_multiplas,
        name="registrar_presencas_multiplas",
    ),
    path(
        "multiplas/formulario/",
        formulario_presencas_multiplas,
        name="formulario_presencas_multiplas",
    ),
    # Registro de presença - dados básicos
    path(
        'registrar-presenca/dados-basicos/',
        registrar_presenca_dados_basicos,
        name='registrar_presenca_dados_basicos',
    ),
    path(
        'registrar-presenca/dados-basicos/ajax/',
        registrar_presenca_dados_basicos_ajax,
        name='registrar_presenca_dados_basicos_ajax',
    ),
    # Registro de presença - totais por atividades
    path(
        'registrar-presenca/totais-atividades/',
        registrar_presenca_totais_atividades,
        name='registrar_presenca_totais_atividades',
    ),
    path(
        'registrar-presenca/totais-atividades/ajax/',
        registrar_presenca_totais_atividades_ajax,
        name='registrar_presenca_totais_atividades_ajax',
    ),
    # Registro de presença - dias/atividades (GET e POST)
    path(
        'registrar-presenca/dias-atividades/',
        registrar_presenca_dias_atividades,
        name='registrar_presenca_dias_atividades',
    ),
    path(
        'registrar-presenca/dias-atividades/ajax/',
        registrar_presenca_dias_atividades_ajax,
        name='registrar_presenca_dias_atividades_ajax',
    ),
    # Registro de presença - alunos (OBSOLETO - Funcionalidade integrada na etapa de dias)
    # path(
    #     'registrar-presenca/alunos/',
    #     registrar_presenca_alunos,
    #     name='registrar_presenca_alunos',
    # ),
    # path(
    #     'registrar-presenca/alunos/ajax/',
    #     registrar_presenca_alunos_ajax,
    #     name='registrar_presenca_alunos_ajax',
    # ),
    # Confirmação de registro de presença
    path(
        'registrar-presenca/confirmar/',
        registrar_presenca_confirmar,
        name='registrar_presenca_confirmar',
    ),
    path(
        'registrar-presenca/confirmar/ajax/',
        registrar_presenca_confirmar_ajax,
        name='registrar_presenca_confirmar_ajax',
    ),
    # Turmas por curso - AJAX
    path(
        'registrar-presenca/turmas-por-curso/',
        turmas_por_curso_ajax,
        name='turmas_por_curso_ajax',
    ),
    path(
        'registrar-presenca/atividades-por-turma/',
        atividades_por_turma_ajax,
        name='atividades_por_turma_ajax',
    ),
    # Limites do calendário - AJAX
    path(
        'registrar-presenca/limites-calendario/',
        obter_limites_calendario_ajax,
        name='registrar_presenca_limites_calendario_ajax',
    ),
    # Edição multi-etapas
    path(
        'editar-presenca/dados-basicos/<int:pk>/',
        editar_presenca_dados_basicos,
        name='editar_presenca_dados_basicos',
    ),
    path(
        'editar-presenca/totais-atividades/<int:pk>/',
        editar_presenca_totais_atividades,
        name='editar_presenca_totais_atividades',
    ),
    path(
        'editar-presenca/dias-atividades/<int:pk>/',
        editar_presenca_dias_atividades,
        name='editar_presenca_dias_atividades',
    ),
    path(
        'editar-presenca/alunos/<int:pk>/',
        editar_presenca_alunos,
        name='editar_presenca_alunos',
    ),
    # Detalhamento multi-etapas
    path(
        'detalhar-presenca/dados-basicos/<int:pk>/',
        detalhar_presenca_dados_basicos,
        name='detalhar_presenca_dados_basicos',
    ),
    path(
        'detalhar-presenca/totais-atividades/<int:pk>/',
        detalhar_presenca_totais_atividades,
        name='detalhar_presenca_totais_atividades',
    ),
    path(
        'detalhar-presenca/dias-atividades/<int:pk>/',
        detalhar_presenca_dias_atividades,
        name='detalhar_presenca_dias_atividades',
    ),
    path(
        'detalhar-presenca/alunos/<int:pk>/',
        detalhar_presenca_alunos,
        name='detalhar_presenca_alunos',
    ),
    # Consolidado de presenças
    path('consolidado/', ConsolidadoPresencasView.as_view(), name='consolidado'),
    path(
        'consolidado/filtros/',
        FiltroConsolidadoView.as_view(),
        name='filtros_consolidado',
    ),
    path(
        'consolidado/exportar/',
        ExportarConsolidadoView.as_view(),
        name='exportar_consolidado',
    ),
    # Painel de Estatísticas
    path('painel/', PainelEstatisticasView.as_view(), name='painel_estatisticas'),
    path('painel/dados-ajax/', PainelDadosAjaxView.as_view(), name='painel_dados_ajax'),
    path(
        'painel/exportar/',
        ExportarRelatorioView.as_view(),
        name='exportar_relatorio_painel',
    ),
    # API endpoints
    path('api/', include('presencas.api.urls')),
    # Registro Rápido Otimizado
    path(
        'registro-rapido/', registro_rapido_otimizado, name='registro_rapido_otimizado'
    ),
    path('ajax/buscar-alunos/', buscar_alunos_ajax, name='buscar_alunos_ajax'),
    path('ajax/alunos-turma/', obter_alunos_turma_ajax, name='obter_alunos_turma_ajax'),
    path(
        'ajax/salvar-lote/',
        salvar_presencas_lote_ajax,
        name='salvar_presencas_lote_ajax',
    ),
    path('ajax/validar-presenca/', validar_presenca_ajax, name='validar_presenca_ajax'),
    path('ajax/atualizar-convocacao/', atualizar_convocacao_ajax, name='atualizar_convocacao_ajax'),
    # Exportação Avançada
    path('exportacao/', ExportacaoAvancadaView.as_view(), name='exportacao_avancada'),
    path(
        'exportacao/processar/',
        ProcessarExportacaoView.as_view(),
        name='processar_exportacao',
    ),
    path(
        'exportacao/agendamentos/',
        GerenciarAgendamentosView.as_view(),
        name='gerenciar_agendamentos',
    ),
    path(
        'exportacao/agendamento-form/', agendamento_form_ajax, name='agendamento_form'
    ),
]

# Endpoint AJAX para alternância de convocação
urlpatterns.append(
    path('ajax/toggle-convocacao/', registro_presenca.toggle_convocacao_ajax, name='toggle_convocacao_ajax')
)
