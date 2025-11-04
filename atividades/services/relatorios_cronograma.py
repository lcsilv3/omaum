"""Serviços para o relatório Cronograma Curso × Turmas."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from importlib import import_module
from typing import Dict, Iterable, List, Optional


def _get_model(app_label: str, model_name: str):
    """Obtém modelo dinamicamente, evitando importações circulares."""

    module = import_module(f"{app_label}.models")
    return getattr(module, model_name)


@dataclass
class CronogramaFiltros:
    """Filtros disponíveis para o relatório de cronograma."""

    curso_id: Optional[int] = None
    turma_id: Optional[int] = None
    responsavel: Optional[str] = None
    status: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None


@dataclass
class LinhaCronograma:
    """Representa uma linha do relatório Cronograma Curso × Turmas."""

    atividade_id: int
    atividade_nome: str
    curso_nome: str
    turmas: List[str]
    data_prevista: Optional[date]
    data_prevista_fim: Optional[date]
    data_realizada: Optional[date]
    status: str
    responsavel: Optional[str]
    atraso_dias: Optional[int]
    adiantamento_dias: Optional[int]


@dataclass
class ResumoCronograma:
    """Resumo consolidado do cronograma."""

    total_atividades: int
    atividades_por_status: Dict[str, int]
    atividades_atrasadas: int
    atividades_adiantadas: int
    atividades_no_prazo: int


@dataclass
class RelatorioCronograma:
    filtros: CronogramaFiltros
    linhas: List[LinhaCronograma]
    resumo: ResumoCronograma


def normalizar_filtros_cronograma(dados: Dict[str, str]) -> CronogramaFiltros:
    """Normaliza filtros recebidos da camada de apresentação."""

    from django.utils.dateparse import parse_date

    def _to_int(valor: Optional[str]) -> Optional[int]:
        try:
            return int(valor) if valor else None
        except (TypeError, ValueError):
            return None

    data_inicio = (
        parse_date(dados.get("data_inicio")) if dados.get("data_inicio") else None
    )
    data_fim = parse_date(dados.get("data_fim")) if dados.get("data_fim") else None
    responsavel = dados.get("responsavel") or None
    status = dados.get("status") or None

    return CronogramaFiltros(
        curso_id=_to_int(dados.get("curso")),
        turma_id=_to_int(dados.get("turma")),
        responsavel=responsavel.strip() if responsavel else None,
        status=status,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


def gerar_relatorio_cronograma(filtros: CronogramaFiltros) -> RelatorioCronograma:
    """Gera relatório agrupando atividades por curso e turma."""

    atividades = _buscar_atividades(filtros)
    linhas = _montar_linhas(atividades)
    resumo = _gerar_resumo(linhas)
    return RelatorioCronograma(filtros=filtros, linhas=linhas, resumo=resumo)


def obter_opcoes_filtros_cronograma(
    curso_id: Optional[int] = None,
) -> Dict[str, List[Dict[str, str]]]:
    """Retorna opções para os filtros de curso, turma, status e responsável."""

    Curso = _get_model("cursos", "Curso")
    Turma = _get_model("turmas", "Turma")
    Atividade = _get_model("atividades", "Atividade")

    cursos = list(
        Curso.objects.filter(ativo=True).order_by("nome").values("id", "nome")
    )

    turmas_qs = Turma.objects.select_related("curso").filter(status="A", ativo=True)
    if curso_id:
        turmas_qs = turmas_qs.filter(curso_id=curso_id)

    turmas = list(turmas_qs.order_by("nome").values("id", "nome"))

    status = [
        {"value": valor, "label": label}
        for valor, label in getattr(Atividade, "STATUS_CHOICES", [])
    ]

    responsaveis = (
        Atividade.objects.exclude(responsavel__isnull=True)
        .exclude(responsavel__exact="")
        .order_by("responsavel")
        .values_list("responsavel", flat=True)
        .distinct()
    )
    responsaveis_opcoes = [
        {"value": valor, "label": valor} for valor in responsaveis if valor
    ]

    return {
        "cursos": cursos,
        "turmas": turmas,
        "status": status,
        "responsaveis": responsaveis_opcoes,
    }


def _buscar_atividades(filtros: CronogramaFiltros):
    """Recupera atividades aplicando os filtros informados."""

    Atividade = _get_model("atividades", "Atividade")

    qs = (
        Atividade.objects.select_related("curso")
        .prefetch_related("turmas")
        .filter(ativo=True)
    )

    if filtros.curso_id:
        qs = qs.filter(curso_id=filtros.curso_id)
    if filtros.turma_id:
        qs = qs.filter(turmas__id=filtros.turma_id)
    if filtros.status:
        qs = qs.filter(status=filtros.status)
    if filtros.responsavel:
        qs = qs.filter(responsavel__iexact=filtros.responsavel)
    if filtros.data_inicio:
        qs = qs.filter(data_inicio__gte=filtros.data_inicio)
    if filtros.data_fim:
        qs = qs.filter(data_inicio__lte=filtros.data_fim)

    return list(qs.distinct().order_by("data_inicio", "hora_inicio", "nome"))


def _montar_linhas(atividades: Iterable) -> List[LinhaCronograma]:
    """Transforma atividades em linhas prontas para exibição/exportação."""

    linhas: List[LinhaCronograma] = []
    hoje = date.today()

    for atividade in atividades:
        data_prevista = getattr(atividade, "data_inicio", None)
        data_prevista_fim = getattr(atividade, "data_fim", None)

        # Considera data de término como data realizada caso a atividade esteja marcada como realizada
        data_realizada = data_prevista_fim if atividade.status == "REALIZADA" else None

        atraso_dias: Optional[int] = None
        adiantamento_dias: Optional[int] = None

        if atividade.status == "REALIZADA" and data_prevista and data_prevista_fim:
            delta = (data_prevista_fim - data_prevista).days
            if delta > 0:
                atraso_dias = delta
            elif delta < 0:
                adiantamento_dias = abs(delta)
        elif atividade.status in {"PENDENTE", "CONFIRMADA"} and data_prevista:
            delta = (hoje - data_prevista).days
            if delta > 0:
                atraso_dias = delta

        turmas_list = []
        turmas_rel = getattr(atividade, "turmas", None)
        if turmas_rel is not None and hasattr(turmas_rel, "all"):
            turmas_list = [turma.nome for turma in turmas_rel.all()]

        linhas.append(
            LinhaCronograma(
                atividade_id=atividade.id,
                atividade_nome=atividade.nome,
                curso_nome=atividade.curso.nome if atividade.curso else "-",
                turmas=turmas_list,
                data_prevista=data_prevista,
                data_prevista_fim=data_prevista_fim,
                data_realizada=data_realizada,
                status=atividade.get_status_display()
                if hasattr(atividade, "get_status_display")
                else atividade.status,
                responsavel=atividade.responsavel,
                atraso_dias=atraso_dias,
                adiantamento_dias=adiantamento_dias,
            )
        )

    return linhas


def _gerar_resumo(linhas: Iterable[LinhaCronograma]) -> ResumoCronograma:
    """Resumir dados para exibição de cards e exportações."""

    total = 0
    por_status: Dict[str, int] = {}
    atrasadas = 0
    adiantadas = 0
    no_prazo = 0

    for linha in linhas:
        total += 1
        por_status[linha.status] = por_status.get(linha.status, 0) + 1

        if linha.atraso_dias:
            atrasadas += 1
        elif linha.adiantamento_dias:
            adiantadas += 1
        else:
            no_prazo += 1

    return ResumoCronograma(
        total_atividades=total,
        atividades_por_status=dict(sorted(por_status.items())),
        atividades_atrasadas=atrasadas,
        atividades_adiantadas=adiantadas,
        atividades_no_prazo=no_prazo,
    )


__all__ = [
    "CronogramaFiltros",
    "LinhaCronograma",
    "RelatorioCronograma",
    "ResumoCronograma",
    "normalizar_filtros_cronograma",
    "gerar_relatorio_cronograma",
    "obter_opcoes_filtros_cronograma",
]
