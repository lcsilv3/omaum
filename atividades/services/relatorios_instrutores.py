"""Serviços para o relatório de carga de instrutores."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from importlib import import_module
from typing import Any, Dict, List, Optional, Set, Tuple

from django.db.models import Prefetch, Q
from django.utils.dateparse import parse_date

PAPEL_INSTRUTOR = "instrutor"
PAPEL_INSTRUTOR_AUX = "instrutor_auxiliar"
PAPEL_AUX_INSTRUCAO = "auxiliar_instrucao"

PAPEIS_DISPLAY = {
    PAPEL_INSTRUTOR: "Instrutor Principal",
    PAPEL_INSTRUTOR_AUX: "Instrutor Auxiliar",
    PAPEL_AUX_INSTRUCAO: "Auxiliar de Instrução",
}


def _get_model(model_name: str, app_label: str):
    module = import_module(f"{app_label}.models")
    return getattr(module, model_name)


@dataclass
class CargaInstrutorFiltros:
    """Filtros aplicáveis ao relatório de carga de instrutores."""

    instrutor_id: Optional[int] = None
    curso_id: Optional[int] = None
    status_turma: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None

    def as_query_params(self) -> Dict[str, str]:
        return {
            "instrutor": str(self.instrutor_id) if self.instrutor_id else "",
            "curso": str(self.curso_id) if self.curso_id else "",
            "status_turma": self.status_turma or "",
            "data_inicio": self.data_inicio.isoformat() if self.data_inicio else "",
            "data_fim": self.data_fim.isoformat() if self.data_fim else "",
        }


@dataclass
class LinhaCargaInstrutor:
    """Linha consolidada do relatório de carga por instrutor e papel."""

    instrutor_id: int
    instrutor_nome: str
    papel: str
    cursos: List[str]
    turmas: List[str]
    total_atividades: int
    total_horas: float
    atividades_por_status: Dict[str, int]

    @property
    def papel_display(self) -> str:
        return PAPEIS_DISPLAY.get(self.papel, self.papel.title())


@dataclass
class ResumoCargaInstrutores:
    """Resumo geral do relatório."""

    total_instrutores: int
    total_atividades: int
    total_horas: float
    atividades_por_status: Dict[str, int]


@dataclass
class RelatorioCargaInstrutores:
    filtros: CargaInstrutorFiltros
    linhas: List[LinhaCargaInstrutor]
    resumo: ResumoCargaInstrutores


def normalizar_filtros_instrutores(dados: Dict[str, str]) -> CargaInstrutorFiltros:
    """Normaliza filtros recebidos da camada de view."""

    def _to_int(value: Optional[str]) -> Optional[int]:
        if not value:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    data_inicio_val = dados.get("data_inicio")
    data_fim_val = dados.get("data_fim")

    data_inicio_parsed = (
        parse_date(data_inicio_val)
        if isinstance(data_inicio_val, str) and data_inicio_val
        else None
    )
    data_fim_parsed = (
        parse_date(data_fim_val)
        if isinstance(data_fim_val, str) and data_fim_val
        else None
    )

    return CargaInstrutorFiltros(
        instrutor_id=_to_int(dados.get("instrutor")),
        curso_id=_to_int(dados.get("curso")),
        status_turma=dados.get("status_turma") or dados.get("status") or None,
        data_inicio=data_inicio_parsed,
        data_fim=data_fim_parsed,
    )


def gerar_relatorio_carga_instrutores(
    filtros: CargaInstrutorFiltros,
) -> RelatorioCargaInstrutores:
    """Constrói o relatório de carga de instrutores com base nos filtros."""

    Atividade = _get_model("Atividade", "atividades")
    Turma = _get_model("Turma", "turmas")
    aluno_fields = ["instrutor", "instrutor_auxiliar", "auxiliar_instrucao"]

    atividades_qs = (
        Atividade.objects.all()
        .select_related("curso")
        .prefetch_related(
            Prefetch(
                "turmas",
                queryset=Turma.objects.select_related(
                    "curso",
                    "instrutor",
                    "instrutor_auxiliar",
                    "auxiliar_instrucao",
                ),
            )
        )
        .order_by("data_inicio", "hora_inicio", "id")
    )

    if filtros.curso_id:
        atividades_qs = atividades_qs.filter(curso_id=filtros.curso_id)
    if filtros.data_inicio:
        atividades_qs = atividades_qs.filter(data_inicio__gte=filtros.data_inicio)
    if filtros.data_fim:
        atividades_qs = atividades_qs.filter(data_inicio__lte=filtros.data_fim)

    if filtros.status_turma:
        atividades_qs = atividades_qs.filter(turmas__status=filtros.status_turma)

    if filtros.instrutor_id:
        instrutor_filter = Q(turmas__instrutor_id=filtros.instrutor_id)
        instrutor_filter |= Q(turmas__instrutor_auxiliar_id=filtros.instrutor_id)
        instrutor_filter |= Q(turmas__auxiliar_instrucao_id=filtros.instrutor_id)
        atividades_qs = atividades_qs.filter(instrutor_filter)

    linhas_map: Dict[Tuple[int, str], Dict[str, Any]] = {}
    resumo_status = defaultdict(int)

    for atividade in atividades_qs.distinct():
        duracao = _calcular_duracao_horas(atividade.hora_inicio, atividade.hora_fim)
        status_atividade = atividade.get_status_display() or atividade.status

        for turma in atividade.turmas.all():
            if filtros.curso_id and turma.curso_id != filtros.curso_id:
                continue
            if filtros.status_turma and turma.status != filtros.status_turma:
                continue

            for campo in aluno_fields:
                instrutor = getattr(turma, campo)
                if not instrutor:
                    continue

                if filtros.instrutor_id and instrutor.id != filtros.instrutor_id:
                    continue

                chave = (instrutor.id, campo)
                registro = linhas_map.setdefault(
                    chave,
                    {
                        "instrutor": instrutor,
                        "cursos": set(),
                        "turmas": set(),
                        "total_atividades": 0,
                        "total_horas": 0.0,
                        # usar defaultdict(int) evita setdefault/checagens repetidas
                        "atividades_por_status": defaultdict(int),
                    },
                )

                registro["cursos"].add(turma.curso.nome if turma.curso else "-")
                registro["turmas"].add(turma.nome)
                registro["total_atividades"] += 1
                registro["total_horas"] += duracao
                registro["atividades_por_status"].setdefault(status_atividade, 0)
                registro["atividades_por_status"][status_atividade] += 1
                resumo_status[status_atividade] += 1

    linhas: List[LinhaCargaInstrutor] = []
    total_atividades = 0
    total_horas = 0.0

    for (instrutor_id, papel), dados in linhas_map.items():
        total_atividades += dados["total_atividades"]
        total_horas += dados["total_horas"]

        linhas.append(
            LinhaCargaInstrutor(
                instrutor_id=instrutor_id,
                instrutor_nome=dados["instrutor"].nome,
                papel=papel,
                cursos=sorted(dados["cursos"]),
                turmas=sorted(dados["turmas"]),
                total_atividades=dados["total_atividades"],
                total_horas=round(dados["total_horas"], 2),
                atividades_por_status=dict(
                    sorted(dados["atividades_por_status"].items())
                ),
            )
        )

    linhas.sort(key=lambda linha: (linha.instrutor_nome.lower(), linha.papel))

    resumo = ResumoCargaInstrutores(
        total_instrutores=len({linha.instrutor_id for linha in linhas}),
        total_atividades=total_atividades,
        total_horas=round(total_horas, 2),
        atividades_por_status=dict(sorted(resumo_status.items())),
    )

    return RelatorioCargaInstrutores(filtros=filtros, linhas=linhas, resumo=resumo)


def obter_opcoes_filtros_instrutores(
    curso_id: Optional[int] = None,
) -> Dict[str, List]:
    """Retorna opções para montagem do formulário de filtros."""

    Curso = _get_model("Curso", "cursos")
    Turma = _get_model("Turma", "turmas")
    Aluno = _get_model("Aluno", "alunos")

    cursos = list(
        Curso.objects.filter(ativo=True).order_by("nome").values("id", "nome")
    )

    instrutor_ids: Set[int] = set()
    campos = ["instrutor", "instrutor_auxiliar", "auxiliar_instrucao"]
    turmas_qs = Turma.objects.select_related(*campos)
    if curso_id:
        turmas_qs = turmas_qs.filter(curso_id=curso_id)

    for turma in turmas_qs:
        for campo in campos:
            instrutor = getattr(turma, campo)
            if instrutor:
                instrutor_ids.add(instrutor.id)

    instrutores = list(
        Aluno.objects.filter(id__in=instrutor_ids).order_by("nome").values("id", "nome")
    )

    status_choices = [
        {"value": value, "label": label}
        for value, label in getattr(Turma, "STATUS_CHOICES", [])
    ]

    return {"cursos": cursos, "instrutores": instrutores, "status": status_choices}


def _calcular_duracao_horas(hora_inicio, hora_fim) -> float:
    """Calcula a duração em horas entre dois horários."""

    if not hora_inicio or not hora_fim:
        return 0.0

    hoje = date.today()
    inicio = datetime.combine(hoje, hora_inicio)
    fim = datetime.combine(hoje, hora_fim)
    if fim <= inicio:
        return 0.0

    delta: timedelta = fim - inicio
    return round(delta.total_seconds() / 3600, 2)


__all__ = [
    "CargaInstrutorFiltros",
    "LinhaCargaInstrutor",
    "RelatorioCargaInstrutores",
    "ResumoCargaInstrutores",
    "gerar_relatorio_carga_instrutores",
    "normalizar_filtros_instrutores",
    "obter_opcoes_filtros_instrutores",
]
