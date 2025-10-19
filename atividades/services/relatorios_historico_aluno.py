"""Serviços para relatório histórico de participação do aluno (timeline)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class HistoricoFiltros:
    aluno_id: Optional[int] = None
    curso_id: Optional[int] = None
    periodo_inicio: Optional[date] = None
    periodo_fim: Optional[date] = None


@dataclass
class EventoHistorico:
    data: date
    tipo: str
    descricao: str


@dataclass
class RelatorioHistoricoAluno:
    filtros: HistoricoFiltros
    eventos: List[EventoHistorico]


def normalizar_filtros_historico(dados: dict) -> HistoricoFiltros:
    return HistoricoFiltros()


def gerar_relatorio_historico_aluno(
    filtros: HistoricoFiltros,
) -> RelatorioHistoricoAluno:
    return RelatorioHistoricoAluno(filtros=filtros, eventos=[])


__all__ = [
    "HistoricoFiltros",
    "EventoHistorico",
    "RelatorioHistoricoAluno",
    "normalizar_filtros_historico",
    "gerar_relatorio_historico_aluno",
]
