from django.urls import path, include
from django.shortcuts import redirect
from .views_ext.multiplas import (
    registrar_presencas_multiplas,
    formulario_presencas_multiplas,
)
from . import views as views_module  # Importar o arquivo views.py
# Import direto do arquivo views_main.py
from . import views_main as presencas_views
from .views_ext.academicas import listar_presencas_academicas
from .views_ext.registro_presenca import (
    registrar_presenca_dados_basicos,
    registrar_presenca_dados_basicos_ajax,
    registrar_presenca_totais_atividades,
    registrar_presenca_totais_atividades_ajax,
    registrar_presenca_dias_atividades,
    registrar_presenca_dias_atividades_ajax,
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
    toggle_convocacao_ajax,
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

# Funções de redirect para URLs antigas
def redirect_to_multi_step_register(request):
    """Redirect de URLs antigas para o sistema multi-etapas"""
    return redirect('presencas:registrar_presenca_dados_basicos')

def redirect_to_multi_step_edit(request, pk):
    """Redirect de URLs antigas de edição para o sistema multi-etapas"""
    return redirect('presencas:editar_presenca_dados_basicos', pk=pk)

def redirect_to_multi_step_detail(request, pk):
    """Redirect de URLs antigas de detalhamento para o sistema multi-etapas"""
    return redirect('presencas:detalhar_presenca_dados_basicos', pk=pk)

urlpatterns = [
    # ===== SISTEMA PRINCIPAL DE PRESENÇAS =====
    # Listagem principal
    path("", listar_presencas_academicas, name="listar_presencas"),
    path("listar/", listar_presencas_academicas, name="listar_presencas_academicas"),
    
    # ===== REDIRECTS PARA COMPATIBILIDADE =====
    # URLs antigas redirecionam para sistema multi-etapas
    path("registrar/", redirect_to_multi_step_register, name="registrar_presenca_academica"),
    path("editar/<int:pk>/", redirect_to_multi_step_edit, name="editar_presenca_academica"), 
    path("detalhar/<int:pk>/", redirect_to_multi_step_detail, name="detalhar_presenca_academica"),
    
    # Placeholders temporários (serão removidos na Fase 2)
    path("excluir/<int:pk>/", presencas_views.excluir_presenca_academica, name="excluir_presenca_academica"),
    path("exportar/", presencas_views.exportar_presencas_academicas, name="exportar_presencas_academicas"),
    path("importar/", presencas_views.importar_presencas_academicas, name="importar_presencas_academicas"),
    # Observações de presença
    path("observacoes/", presencas_views.listar_observacoes_presenca, name="listar_observacoes_presenca"),
    
    # ===== SISTEMA MULTI-ETAPAS (PRINCIPAL) =====
    # Registro de presença - 4 etapas
    path('registrar-presenca/dados-basicos/', registrar_presenca_dados_basicos, name='registrar_presenca_dados_basicos'),
    path('registrar-presenca/dados-basicos/ajax/', registrar_presenca_dados_basicos_ajax, name='registrar_presenca_dados_basicos_ajax'),
    
    path('registrar-presenca/totais-atividades/', registrar_presenca_totais_atividades, name='registrar_presenca_totais_atividades'),
    path('registrar-presenca/totais-atividades/ajax/', registrar_presenca_totais_atividades_ajax, name='registrar_presenca_totais_atividades_ajax'),
    
    path('registrar-presenca/dias-atividades/', registrar_presenca_dias_atividades, name='registrar_presenca_dias_atividades'),
    path('registrar-presenca/dias-atividades/ajax/', registrar_presenca_dias_atividades_ajax, name='registrar_presenca_dias_atividades_ajax'),
    
    path('registrar-presenca/confirmar/', registrar_presenca_confirmar, name='registrar_presenca_confirmar'),
    path('registrar-presenca/confirmar/ajax/', registrar_presenca_confirmar_ajax, name='registrar_presenca_confirmar_ajax'),
    
    # ===== EDIÇÃO MULTI-ETAPAS =====
    path('editar-presenca/dados-basicos/<int:pk>/', editar_presenca_dados_basicos, name='editar_presenca_dados_basicos'),
    path('editar-presenca/totais-atividades/<int:pk>/', editar_presenca_totais_atividades, name='editar_presenca_totais_atividades'),
    path('editar-presenca/dias-atividades/<int:pk>/', editar_presenca_dias_atividades, name='editar_presenca_dias_atividades'),
    path('editar-presenca/alunos/<int:pk>/', editar_presenca_alunos, name='editar_presenca_alunos'),
    
    # ===== DETALHAMENTO MULTI-ETAPAS =====
    path('detalhar-presenca/dados-basicos/<int:pk>/', detalhar_presenca_dados_basicos, name='detalhar_presenca_dados_basicos'),
    path('detalhar-presenca/totais-atividades/<int:pk>/', detalhar_presenca_totais_atividades, name='detalhar_presenca_totais_atividades'),
    path('detalhar-presenca/dias-atividades/<int:pk>/', detalhar_presenca_dias_atividades, name='detalhar_presenca_dias_atividades'),
    path('detalhar-presenca/alunos/<int:pk>/', detalhar_presenca_alunos, name='detalhar_presenca_alunos'),
    
    # ===== AJAX HELPERS =====
    path('registrar-presenca/turmas-por-curso/', turmas_por_curso_ajax, name='turmas_por_curso_ajax'),
    path('registrar-presenca/atividades-por-turma/', atividades_por_turma_ajax, name='atividades_por_turma_ajax'),
    path('registrar-presenca/limites-calendario/', obter_limites_calendario_ajax, name='registrar_presenca_limites_calendario_ajax'),
    path('ajax/toggle-convocacao/', toggle_convocacao_ajax, name='toggle_convocacao_ajax'),
    
    # ===== SISTEMAS ALTERNATIVOS =====
    # Sistema de múltiplas presenças  
    path("multiplas/", registrar_presencas_multiplas, name="registrar_presencas_multiplas"),
    path("multiplas/formulario/", formulario_presencas_multiplas, name="formulario_presencas_multiplas"),
    
    # Registro Rápido Otimizado (sistema alternativo)
    path('registro-rapido/', registro_rapido_otimizado, name='registro_rapido_otimizado'),
    path('ajax/buscar-alunos/', buscar_alunos_ajax, name='buscar_alunos_ajax'),
    path('ajax/alunos-turma/', obter_alunos_turma_ajax, name='obter_alunos_turma_ajax'),
    path('ajax/salvar-lote/', salvar_presencas_lote_ajax, name='salvar_presencas_lote_ajax'),
    path('ajax/validar-presenca/', validar_presenca_ajax, name='validar_presenca_ajax'),
    path('ajax/atualizar-convocacao/', atualizar_convocacao_ajax, name='atualizar_convocacao_ajax'),
    
    # ===== RELATÓRIOS E ANÁLISES =====
    # Consolidado de presenças
    path('consolidado/', ConsolidadoPresencasView.as_view(), name='consolidado'),
    path('consolidado/filtros/', FiltroConsolidadoView.as_view(), name='filtros_consolidado'),
    path('consolidado/exportar/', ExportarConsolidadoView.as_view(), name='exportar_consolidado'),
    
    # Painel de Estatísticas
    path('painel/', PainelEstatisticasView.as_view(), name='painel_estatisticas'),
    path('painel/dados-ajax/', PainelDadosAjaxView.as_view(), name='painel_dados_ajax'),
    path('painel/exportar/', ExportarRelatorioView.as_view(), name='exportar_relatorio_painel'),
    
    # Exportação Avançada
    path('exportacao/', ExportacaoAvancadaView.as_view(), name='exportacao_avancada'),
    path('exportacao/processar/', ProcessarExportacaoView.as_view(), name='processar_exportacao'),
    path('exportacao/agendamentos/', GerenciarAgendamentosView.as_view(), name='gerenciar_agendamentos'),
    path('exportacao/agendamento-form/', agendamento_form_ajax, name='agendamento_form'),
    
    # ===== API ENDPOINTS =====
    path('api/', include('presencas.api.urls')),
]
