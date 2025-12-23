"""
Módulo de views para o aplicativo presencas.

Estrutura de views reorganizada (Fase 2):
- listagem.py: Listagem, visualização e CRUD básico
- consolidado.py: Tabela consolidada com edição inline
- registro_rapido.py: Registro rápido para professores
- exportacao_simplificada.py: Exportação em múltiplos formatos
- painel.py: Painel com dashboards
"""

# Importar views do módulo listagem (consolidado de views_main.py)
from .listagem import (
    listar_presencas_academicas,
    registrar_presenca_academica,
    editar_presenca_academica,
    excluir_presenca_academica,
    detalhar_presenca_academica,
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
    registrar_presenca_convocados,
    registrar_presenca_convocados_ajax,
    toggle_convocacao_ajax,
    editar_presencas_lote,
    editar_lote_dados_basicos,
    editar_lote_totais_atividades,
    editar_lote_dias_atividades,
    editar_lote_dias_atividades_ajax,
    editar_presenca_dados_basicos,
    editar_presenca_totais_atividades,
    editar_presenca_dias_atividades,
    editar_presenca_alunos,
    detalhar_presenca_dados_basicos,
    detalhar_presenca_totais_atividades,
    detalhar_presenca_dias_atividades,
    detalhar_presenca_alunos,
    exportar_presencas_academicas,
    importar_presencas_academicas,
    listar_observacoes_presenca,
)

__all__ = [
    "listar_presencas_academicas",
    "registrar_presenca_academica",
    "editar_presenca_academica",
    "excluir_presenca_academica",
    "detalhar_presenca_academica",
    "registrar_presenca_dados_basicos",
    "registrar_presenca_dados_basicos_ajax",
    "registrar_presenca_totais_atividades",
    "registrar_presenca_totais_atividades_ajax",
    "registrar_presenca_dias_atividades",
    "registrar_presenca_dias_atividades_ajax",
    "registrar_presenca_alunos",
    "registrar_presenca_alunos_ajax",
    "registrar_presenca_confirmar",
    "registrar_presenca_confirmar_ajax",
    "registrar_presenca_convocados",
    "registrar_presenca_convocados_ajax",
    "toggle_convocacao_ajax",
    "editar_presencas_lote",
    "editar_lote_dados_basicos",
    "editar_lote_totais_atividades",
    "editar_lote_dias_atividades",
    "editar_lote_dias_atividades_ajax",
    "editar_presenca_dados_basicos",
    "editar_presenca_totais_atividades",
    "editar_presenca_dias_atividades",
    "editar_presenca_alunos",
    "detalhar_presenca_dados_basicos",
    "detalhar_presenca_totais_atividades",
    "detalhar_presenca_dias_atividades",
    "detalhar_presenca_alunos",
    "exportar_presencas_academicas",
    "importar_presencas_academicas",
    "listar_observacoes_presenca",
]
