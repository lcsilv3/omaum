"""Serviços para relatório de carências e frequência por turma.

Implementação mínima para permitir chamadas das views; lógica será
completada posteriormente conforme dados de `frequencias`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class FrequenciaFiltros:
    curso_id: Optional[int] = None
    turma_id: Optional[int] = None
    mes: Optional[int] = None
    ano: Optional[int] = None


@dataclass
class LinhaFrequencia:
    aluno_id: int
    aluno_nome: str
    total_atividades: int
    presentes: int
    faltas: int
    percentual_presenca: float


@dataclass
class RelatorioFrequencia:
    filtros: FrequenciaFiltros
    linhas: List[LinhaFrequencia]


def normalizar_filtros_frequencia(dados: Dict[str, str]) -> FrequenciaFiltros:
    def _to_int(v):
        try:
            return int(v)
        except Exception:
            return None

    return FrequenciaFiltros(
        curso_id=_to_int(dados.get("curso")),
        turma_id=_to_int(dados.get("turma")),
        mes=_to_int(dados.get("mes")),
        ano=_to_int(dados.get("ano")),
    )


def gerar_relatorio_frequencia(filtros: FrequenciaFiltros) -> RelatorioFrequencia:
    return RelatorioFrequencia(filtros=filtros, linhas=[])


__all__ = [
    "FrequenciaFiltros",
    "LinhaFrequencia",
    "RelatorioFrequencia",
    "normalizar_filtros_frequencia",
    "gerar_relatorio_frequencia",
]
