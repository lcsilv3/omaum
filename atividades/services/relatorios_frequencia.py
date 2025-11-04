"""Serviços para o relatório de carências e frequência por turma."""

from __future__ import annotations

from calendar import monthrange
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from importlib import import_module
from typing import Dict, Iterable, List, Optional, Tuple

from django.db.models import Count

PERCENTUAL_MINIMO_PADRAO = 75


def _get_model(app_label: str, model_name: str):
    """Obtém um modelo dinamicamente, evitando importações circulares."""

    module = import_module(f"{app_label}.models")
    return getattr(module, model_name)


@dataclass
class FrequenciaFiltros:
    """Conjunto de filtros aplicáveis ao relatório de frequência."""

    curso_id: Optional[int] = None
    turma_id: Optional[int] = None
    mes: Optional[int] = None
    ano: Optional[int] = None
    status_carencia: Optional[str] = None


@dataclass
class LinhaFrequencia:
    """Linha detalhada da frequência de um aluno em uma turma."""

    aluno_id: int
    aluno_nome: str
    curso_nome: str
    turma_nome: str
    total_atividades: int
    presentes: int
    faltas: int
    percentual_presenca: float
    numero_carencias: int
    liberado: bool
    status_carencia: Optional[str]
    frequencia_id: Optional[int] = None


@dataclass
class ResumoRelatorioFrequencia:
    """Resumo consolidado do relatório de frequência."""

    total_alunos: int
    alunos_liberados: int
    alunos_com_carencia: int
    total_presencas: int
    total_faltas: int
    total_atividades: int
    percentual_presenca_medio: float


@dataclass
class RelatorioFrequencia:
    filtros: FrequenciaFiltros
    linhas: List[LinhaFrequencia]
    resumo: ResumoRelatorioFrequencia


def normalizar_filtros_frequencia(dados: Dict[str, str]) -> FrequenciaFiltros:
    """Normaliza os valores recebidos da camada de apresentação."""

    def _to_int(valor: Optional[str]) -> Optional[int]:
        try:
            return int(valor) if valor else None
        except (TypeError, ValueError):
            return None

    status_carencia = dados.get("status_carencia") or dados.get("status")

    return FrequenciaFiltros(
        curso_id=_to_int(dados.get("curso")),
        turma_id=_to_int(dados.get("turma")),
        mes=_to_int(dados.get("mes")),
        ano=_to_int(dados.get("ano")),
        status_carencia=status_carencia or None,
    )


def gerar_relatorio_frequencia(filtros: FrequenciaFiltros) -> RelatorioFrequencia:
    """Gera o relatório de carências e frequência considerando os filtros."""

    frequencias = _buscar_frequencias_mensais(filtros)

    if frequencias:
        linhas = _gerar_linhas_a_partir_de_carencias(frequencias, filtros)
    else:
        linhas = _gerar_linhas_por_registros(filtros)

    resumo = _montar_resumo(linhas)
    return RelatorioFrequencia(filtros=filtros, linhas=linhas, resumo=resumo)


def obter_opcoes_filtros_frequencia(
    curso_id: Optional[int] = None,
    ano: Optional[int] = None,
) -> Dict[str, List[Dict[str, str]]]:
    """Retorna as opções dos filtros dinâmicos para o relatório."""

    Curso = _get_model("cursos", "Curso")
    Turma = _get_model("turmas", "Turma")
    FrequenciaMensal = _get_model("frequencias", "FrequenciaMensal")
    Carencia = _get_model("frequencias", "Carencia")

    cursos = list(
        Curso.objects.filter(ativo=True).order_by("nome").values("id", "nome")
    )

    turmas_qs = Turma.objects.select_related("curso").filter(status="A", ativo=True)
    if curso_id:
        turmas_qs = turmas_qs.filter(curso_id=curso_id)

    turmas = list(turmas_qs.order_by("nome").values("id", "nome"))

    anos_disponiveis = (
        FrequenciaMensal.objects.order_by("-ano")
        .values_list("ano", flat=True)
        .distinct()
    )
    anos = [
        {"value": str(valor), "label": str(valor)} for valor in anos_disponiveis
    ] or [{"value": str(date.today().year), "label": str(date.today().year)}]

    meses = [
        {"value": str(valor), "label": nome}
        for valor, nome in FrequenciaMensal.MES_CHOICES
    ]

    status = [
        {"value": valor, "label": rotulo} for valor, rotulo in Carencia.STATUS_CHOICES
    ]

    return {
        "cursos": cursos,
        "turmas": turmas,
        "meses": meses,
        "anos": anos,
        "status": status,
    }


def _buscar_frequencias_mensais(
    filtros: FrequenciaFiltros,
) -> List["FrequenciaMensal"]:
    """Localiza frequências mensais conforme os filtros informados."""

    FrequenciaMensal = _get_model("frequencias", "FrequenciaMensal")

    qs = FrequenciaMensal.objects.select_related("turma__curso").prefetch_related(
        "carencia_set__aluno"
    )

    if filtros.curso_id:
        qs = qs.filter(turma__curso_id=filtros.curso_id)
    if filtros.turma_id:
        qs = qs.filter(turma_id=filtros.turma_id)
    if filtros.mes:
        qs = qs.filter(mes=filtros.mes)
    if filtros.ano:
        qs = qs.filter(ano=filtros.ano)

    return list(qs.order_by("-ano", "-mes", "turma__nome"))


def _gerar_linhas_a_partir_de_carencias(
    frequencias: Iterable["FrequenciaMensal"],
    filtros: FrequenciaFiltros,
) -> List[LinhaFrequencia]:
    """Monta as linhas do relatório a partir das carências persistidas."""

    linhas: List[LinhaFrequencia] = []

    for frequencia in frequencias:
        carencias_qs = frequencia.carencia_set.select_related("aluno")

        if filtros.status_carencia:
            if filtros.status_carencia == "RESOLVIDO":
                carencias_qs = carencias_qs.filter(status="RESOLVIDO")
            elif filtros.status_carencia == "PENDENTE":
                carencias_qs = carencias_qs.filter(status="PENDENTE")
            elif filtros.status_carencia == "EM_ACOMPANHAMENTO":
                carencias_qs = carencias_qs.filter(status="EM_ACOMPANHAMENTO")
            else:
                # Quando o filtro não corresponde a um status conhecido,
                # nenhum registro será retornado.
                carencias_qs = carencias_qs.none()

        for carencia in carencias_qs:
            presentes = int(carencia.total_presencas or 0)
            total_atividades = int(carencia.total_atividades or 0)
            faltas = max(total_atividades - presentes, 0)
            percentual = float(carencia.percentual_presenca or 0)
            numero_carencias = int(carencia.numero_carencias or faltas)
            status_carencia = carencia.status or (
                "RESOLVIDO" if carencia.liberado else "PENDENTE"
            )

            linhas.append(
                LinhaFrequencia(
                    aluno_id=carencia.aluno_id,
                    aluno_nome=carencia.aluno.nome,
                    curso_nome=frequencia.turma.curso.nome
                    if frequencia.turma and frequencia.turma.curso
                    else "-",
                    turma_nome=frequencia.turma.nome if frequencia.turma else "-",
                    total_atividades=total_atividades,
                    presentes=presentes,
                    faltas=faltas,
                    percentual_presenca=round(percentual, 2),
                    numero_carencias=numero_carencias,
                    liberado=bool(carencia.liberado),
                    status_carencia=status_carencia,
                    frequencia_id=frequencia.id,
                )
            )

    return linhas


def _gerar_linhas_por_registros(
    filtros: FrequenciaFiltros,
) -> List[LinhaFrequencia]:
    """Constrói as linhas a partir de matrículas e registros de presença."""

    if filtros.mes is None or filtros.ano is None:
        return []

    Turma = _get_model("turmas", "Turma")
    Matricula = _get_model("matriculas", "Matricula")
    RegistroPresenca = _get_model("presencas", "RegistroPresenca")

    turmas_qs = Turma.objects.select_related("curso").filter(status="A", ativo=True)
    if filtros.curso_id:
        turmas_qs = turmas_qs.filter(curso_id=filtros.curso_id)
    if filtros.turma_id:
        turmas_qs = turmas_qs.filter(id=filtros.turma_id)

    turmas = list(turmas_qs)
    if not turmas:
        return []

    turma_por_id = {turma.id: turma for turma in turmas}
    turma_ids = list(turma_por_id.keys())

    matriculas_qs = Matricula.objects.filter(
        turma_id__in=turma_ids, status="A"
    ).select_related("aluno", "turma__curso")

    matriculas = list(matriculas_qs)
    if not matriculas:
        return []

    matricula_por_chave = {
        (matricula.turma_id, matricula.aluno_id): matricula for matricula in matriculas
    }

    ultimo_dia = monthrange(filtros.ano, filtros.mes)[1]
    periodo_inicio = date(filtros.ano, filtros.mes, 1)
    periodo_fim = date(filtros.ano, filtros.mes, ultimo_dia)

    registros_qs = RegistroPresenca.objects.filter(
        turma_id__in=turma_ids,
        data__gte=periodo_inicio,
        data__lte=periodo_fim,
    )

    dados_registros: Dict[Tuple[int, int], Dict[str, int]] = defaultdict(
        lambda: {
            "convocados": 0,
            "presentes": 0,
            "faltas": 0,
            "faltas_justificadas": 0,
        }
    )

    for registro in registros_qs.values("turma_id", "aluno_id", "status").annotate(
        total=Count("id")
    ):
        chave = (registro["turma_id"], registro["aluno_id"])
        total = int(registro.get("total") or 0)
        dados_registros[chave]["convocados"] += total

        status = registro.get("status")
        if status in {"P", "V1", "V2"}:
            dados_registros[chave]["presentes"] += total
        elif status == "F":
            dados_registros[chave]["faltas"] += total
        elif status == "J":
            dados_registros[chave]["faltas_justificadas"] += total

    linhas: List[LinhaFrequencia] = []

    for chave, matricula in matricula_por_chave.items():
        turma_id, aluno_id = chave
        turma = turma_por_id.get(turma_id)
        if not turma:
            continue

        dados = dados_registros[chave]
        total_atividades = dados["convocados"]
        presentes = dados["presentes"]
        faltas_totais = dados["faltas"] + dados["faltas_justificadas"]
        if total_atividades <= 0:
            faltas_totais = 0

        percentual_minimo = (
            float(turma.perc_presenca_minima)
            if turma.perc_presenca_minima is not None
            else PERCENTUAL_MINIMO_PADRAO
        )

        percentual = (
            round((presentes / total_atividades) * 100, 2) if total_atividades else 0.0
        )
        numero_carencias = max(total_atividades - presentes, 0)
        liberado = percentual >= percentual_minimo
        status_carencia = "RESOLVIDO" if liberado else "PENDENTE"

        if filtros.status_carencia == "RESOLVIDO" and not liberado:
            continue
        if filtros.status_carencia == "PENDENTE" and liberado:
            continue
        if filtros.status_carencia == "EM_ACOMPANHAMENTO":
            continue

        linhas.append(
            LinhaFrequencia(
                aluno_id=aluno_id,
                aluno_nome=matricula.aluno.nome,
                curso_nome=turma.curso.nome if turma.curso else "-",
                turma_nome=turma.nome,
                total_atividades=total_atividades,
                presentes=presentes,
                faltas=faltas_totais,
                percentual_presenca=percentual,
                numero_carencias=numero_carencias,
                liberado=liberado,
                status_carencia=status_carencia,
            )
        )

    return linhas


def _montar_resumo(linhas: List[LinhaFrequencia]) -> ResumoRelatorioFrequencia:
    """Calcula os agregados gerais do relatório."""

    total_alunos = len(linhas)
    total_presencas = sum(linha.presentes for linha in linhas)
    total_faltas = sum(linha.faltas for linha in linhas)
    total_atividades = sum(linha.total_atividades for linha in linhas)
    alunos_liberados = sum(1 for linha in linhas if linha.liberado)
    alunos_com_carencia = total_alunos - alunos_liberados
    percentual_medio = (
        round(
            sum(linha.percentual_presenca for linha in linhas) / total_alunos,
            2,
        )
        if total_alunos
        else 0.0
    )

    return ResumoRelatorioFrequencia(
        total_alunos=total_alunos,
        alunos_liberados=alunos_liberados,
        alunos_com_carencia=alunos_com_carencia,
        total_presencas=total_presencas,
        total_faltas=total_faltas,
        total_atividades=total_atividades,
        percentual_presenca_medio=percentual_medio,
    )


__all__ = [
    "FrequenciaFiltros",
    "LinhaFrequencia",
    "RelatorioFrequencia",
    "ResumoRelatorioFrequencia",
    "normalizar_filtros_frequencia",
    "gerar_relatorio_frequencia",
    "obter_opcoes_filtros_frequencia",
]
