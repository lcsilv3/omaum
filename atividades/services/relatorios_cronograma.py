"""Serviços para relatório Cronograma Curso x Turmas.

Implementação mínima para exposição nas views; ampliação futura necessária.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from datetime import date


@dataclass
class CronogramaFiltros:
    curso_id: Optional[int] = None
    turma_id: Optional[int] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None


@dataclass
class LinhaCronograma:
    atividade_id: int
    atividade_nome: str
    data_prevista: Optional[date]
    data_realizada: Optional[date]
    status: str


@dataclass
class RelatorioCronograma:
    filtros: CronogramaFiltros
    linhas: List[LinhaCronograma]


def normalizar_filtros_cronograma(dados: dict) -> CronogramaFiltros:
    return CronogramaFiltros()


def gerar_relatorio_cronograma(filtros: CronogramaFiltros) -> RelatorioCronograma:
    return RelatorioCronograma(filtros=filtros, linhas=[])


__all__ = [
    "CronogramaFiltros",
    "LinhaCronograma",
    "RelatorioCronograma",
    "normalizar_filtros_cronograma",
    "gerar_relatorio_cronograma",
]
