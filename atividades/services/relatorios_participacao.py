"""Serviços para relatório de participação por atividade.

Versão única e consolidada: normaliza filtros, agrega registros por
atividade e fornece opções de filtros para UI.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from importlib import import_module
from typing import Dict, List, Optional

from django.db.models import Count
from django.utils.dateparse import parse_date


def _get_model(model_name: str, app_label: str):
    module = import_module(f"{app_label}.models")
    return getattr(module, model_name)


@dataclass
class ParticipacaoFiltros:
    curso_id: Optional[int] = None
    turma_id: Optional[int] = None
    tipo_atividade: Optional[str] = None
    status_atividade: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None


@dataclass
class LinhaRelatorioParticipacao:
    atividade_id: int
    atividade_nome: str
    curso_nome: Optional[str]
    turmas: List[str]
    data_inicio: Optional[date]
    data_fim: Optional[date]
    tipo_atividade: str
    status_atividade: str
    total_convocados: int
    total_presentes: int
    total_faltas: int
    total_faltas_justificadas: int
    total_voluntario_extra: int
    total_voluntario_simples: int
    percentual_presenca: float


@dataclass
class ResumoRelatorioParticipacao:
    total_atividades: int
    total_convocados: int
    total_presentes: int
    total_faltas: int
    total_faltas_justificadas: int
    total_voluntario_extra: int
    total_voluntario_simples: int
    percentual_presenca_medio: float


@dataclass
class RelatorioParticipacao:
    filtros: ParticipacaoFiltros
    linhas: List[LinhaRelatorioParticipacao]
    resumo: ResumoRelatorioParticipacao


def normalizar_filtros(dados: Dict[str, str]) -> ParticipacaoFiltros:
    def _to_int(v: Optional[str]) -> Optional[int]:
        if not v:
            return None
        try:
            return int(v)
        except Exception:
            return None

    inicio = parse_date(dados.get("data_inicio")) if dados.get("data_inicio") else None
    fim = parse_date(dados.get("data_fim")) if dados.get("data_fim") else None

    return ParticipacaoFiltros(
        curso_id=_to_int(dados.get("curso")),
        turma_id=_to_int(dados.get("turma")),
        tipo_atividade=dados.get("tipo_atividade") or None,
        status_atividade=dados.get("status") or None,
        data_inicio=inicio,
        data_fim=fim,
    )


def gerar_relatorio_participacao(filtros: ParticipacaoFiltros) -> RelatorioParticipacao:
    Atividade = _get_model("Atividade", "atividades")
    Registro = _get_model("RegistroPresenca", "presencas")

    qs = (
        Atividade.objects.select_related("curso")
        .prefetch_related("turmas")
        .order_by("data_inicio", "id")
    )
    if filtros.curso_id:
        qs = qs.filter(curso_id=filtros.curso_id)
    if filtros.turma_id:
        qs = qs.filter(turmas__id=filtros.turma_id)
    if filtros.tipo_atividade:
        qs = qs.filter(tipo_atividade=filtros.tipo_atividade)
    if filtros.status_atividade:
        qs = qs.filter(status=filtros.status_atividade)
    if filtros.data_inicio:
        qs = qs.filter(data_inicio__gte=filtros.data_inicio)
    if filtros.data_fim:
        qs = qs.filter(data_inicio__lte=filtros.data_fim)

    atividades = list(qs.distinct())
    if not atividades:
        resumo = ResumoRelatorioParticipacao(0, 0, 0, 0, 0, 0, 0, 0.0)
        return RelatorioParticipacao(filtros=filtros, linhas=[], resumo=resumo)

    ids = [int(getattr(a, "id", 0)) for a in atividades]
    registros = Registro.objects.filter(atividade_id__in=ids)
    agreg = registros.values("atividade_id", "status").annotate(total=Count("id"))

    mapa: Dict[int, Dict[str, int]] = {i: {} for i in ids}
    for ag in agreg:
        aid = int(ag.get("atividade_id") or 0)
        st = ag.get("status") or ""
        total = int(ag.get("total") or 0)
        mapa.setdefault(aid, {})[str(st)] = total

    linhas: List[LinhaRelatorioParticipacao] = []
    totais = {
        "convocados": 0,
        "presentes": 0,
        "faltas": 0,
        "justificadas": 0,
        "vextra": 0,
        "vsimples": 0,
    }
    percentuais: List[float] = []

    for atividade in atividades:
        aid = int(getattr(atividade, "id", 0))
        ag = mapa.get(aid, {})
        convocados = sum(ag.values()) if ag else 0
        presentes = int(ag.get("P", 0))
        faltas = int(ag.get("F", 0))
        justificadas = int(ag.get("J", 0))
        vextra = int(ag.get("V1", 0))
        vsimples = int(ag.get("V2", 0))

        percentual = round((presentes / convocados) * 100, 2) if convocados > 0 else 0.0
        if convocados > 0:
            percentuais.append(percentual)

        totais["convocados"] += convocados
        totais["presentes"] += presentes
        totais["faltas"] += faltas
        totais["justificadas"] += justificadas
        totais["vextra"] += vextra
        totais["vsimples"] += vsimples

        turmas_list: List[str] = []
        turmas_rel = getattr(atividade, "turmas", None)
        try:
            if turmas_rel is not None and hasattr(turmas_rel, "all"):
                turmas_list = [getattr(t, "nome", "") for t in turmas_rel.all()]
        except Exception:
            turmas_list = []

        linhas.append(
            LinhaRelatorioParticipacao(
                atividade_id=aid,
                atividade_nome=getattr(atividade, "nome", ""),
                curso_nome=getattr(getattr(atividade, "curso", None), "nome", None),
                turmas=turmas_list,
                data_inicio=getattr(atividade, "data_inicio", None),
                data_fim=getattr(atividade, "data_fim", None),
                tipo_atividade=str(getattr(atividade, "tipo_atividade", "") or ""),
                status_atividade=str(getattr(atividade, "status", "") or ""),
                total_convocados=convocados,
                total_presentes=presentes,
                total_faltas=faltas,
                total_faltas_justificadas=justificadas,
                total_voluntario_extra=vextra,
                total_voluntario_simples=vsimples,
                percentual_presenca=percentual,
            )
        )

    linhas.sort(
        key=lambda it: (
            it.data_inicio or date.min,
            -it.percentual_presenca,
            it.atividade_nome.lower(),
        )
    )

    percentual_medio = (
        round(sum(percentuais) / len(percentuais), 2) if percentuais else 0.0
    )

    resumo = ResumoRelatorioParticipacao(
        total_atividades=len(linhas),
        total_convocados=totais["convocados"],
        total_presentes=totais["presentes"],
        total_faltas=totais["faltas"],
        total_faltas_justificadas=totais["justificadas"],
        total_voluntario_extra=totais["vextra"],
        total_voluntario_simples=totais["vsimples"],
        percentual_presenca_medio=percentual_medio,
    )

    return RelatorioParticipacao(filtros=filtros, linhas=linhas, resumo=resumo)


def obter_opcoes_filtros_participacao(
    curso_id: Optional[int] = None,
) -> Dict[str, List]:
    Curso = _get_model("Curso", "cursos")
    Turma = _get_model("Turma", "turmas")
    Atividade = _get_model("Atividade", "atividades")

    cursos = list(
        Curso.objects.filter(ativo=True).order_by("nome").values("id", "nome")
    )
    turmas_qs = Turma.objects.filter(ativo=True).order_by("nome")
    if curso_id:
        turmas_qs = turmas_qs.filter(curso_id=curso_id)
    turmas = list(turmas_qs.values("id", "nome"))

    tipos = [
        {"value": v, "label": label}
        for v, label in getattr(Atividade, "TIPO_CHOICES", [])
    ]

    status = [
        {"value": v, "label": label}
        for v, label in getattr(Atividade, "STATUS_CHOICES", [])
    ]

    return {
        "cursos": cursos,
        "turmas": turmas,
        "tipos": tipos,
        "status": status,
    }


__all__ = [
    "ParticipacaoFiltros",
    "LinhaRelatorioParticipacao",
    "ResumoRelatorioParticipacao",
    "RelatorioParticipacao",
    "normalizar_filtros",
    "gerar_relatorio_participacao",
    "obter_opcoes_filtros_participacao",
]
