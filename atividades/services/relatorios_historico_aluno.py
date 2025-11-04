"""Serviços para o relatório histórico de participação do aluno."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date
from importlib import import_module
from typing import Dict, List, Optional

from django.db.models import Q
from django.utils.dateparse import parse_date


def _get_model(model_name: str, app_label: str):
    module = import_module(f"{app_label}.models")
    return getattr(module, model_name)


PAPEL_PARTICIPANTE = "participante"
PAPEL_VOLUNTARIO = "voluntario"
PAPEL_VOLUNTARIO_EXTRA = "voluntario_extra"
PAPEL_VOLUNTARIO_SIMPLES = "voluntario_simples"
PAPEL_INSTRUTOR = "instrutor"
PAPEL_INSTRUTOR_AUX = "instrutor_auxiliar"
PAPEL_AUX_INSTRUCAO = "auxiliar_instrucao"

PAPEIS_LABELS = {
    PAPEL_PARTICIPANTE: "Participante",
    PAPEL_VOLUNTARIO: "Voluntário",
    PAPEL_VOLUNTARIO_EXTRA: "Voluntário Extra",
    PAPEL_VOLUNTARIO_SIMPLES: "Voluntário Simples",
    PAPEL_INSTRUTOR: "Instrutor Principal",
    PAPEL_INSTRUTOR_AUX: "Instrutor Auxiliar",
    PAPEL_AUX_INSTRUCAO: "Auxiliar de Instrução",
}

STATUS_PARA_PAPEL = {
    "P": PAPEL_PARTICIPANTE,
    "F": PAPEL_PARTICIPANTE,
    "J": PAPEL_PARTICIPANTE,
    "V1": PAPEL_VOLUNTARIO_EXTRA,
    "V2": PAPEL_VOLUNTARIO_SIMPLES,
}

PAPEIS_VOLUNTARIO = {PAPEL_VOLUNTARIO_EXTRA, PAPEL_VOLUNTARIO_SIMPLES}
PAPEIS_INSTRUCAO = {
    PAPEL_INSTRUTOR,
    PAPEL_INSTRUTOR_AUX,
    PAPEL_AUX_INSTRUCAO,
}


@dataclass
class HistoricoFiltros:
    aluno_id: Optional[int] = None
    curso_id: Optional[int] = None
    papel: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None


@dataclass
class EventoHistorico:
    data: date
    papel: str
    papel_display: str
    descricao: str
    atividade_nome: str
    curso_nome: Optional[str]
    turma_nome: Optional[str]
    status_presenca: Optional[str]
    status_atividade: Optional[str]
    tipo_atividade: Optional[str]


@dataclass
class ResumoHistorico:
    total_eventos: int
    total_participacoes: int
    total_presencas: int
    total_faltas: int
    total_justificadas: int
    total_voluntarios: int
    total_instrucao: int
    eventos_por_papel: Dict[str, int]


@dataclass
class RelatorioHistoricoAluno:
    filtros: HistoricoFiltros
    eventos: List[EventoHistorico]
    resumo: ResumoHistorico


def normalizar_filtros_historico(dados: Dict[str, str]) -> HistoricoFiltros:
    """Converte parâmetros de consulta em tipos adequados."""

    def _to_int(value: Optional[str]) -> Optional[int]:
        if not value:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    data_inicio = (
        parse_date(dados.get("data_inicio")) if dados.get("data_inicio") else None
    )
    data_fim = parse_date(dados.get("data_fim")) if dados.get("data_fim") else None

    papel = dados.get("papel") or None
    if papel and papel not in PAPEIS_LABELS:
        # Permite alias "voluntario" para os dois tipos específicos
        if papel != PAPEL_VOLUNTARIO:
            papel = None

    return HistoricoFiltros(
        aluno_id=_to_int(dados.get("aluno")),
        curso_id=_to_int(dados.get("curso")),
        papel=papel,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


def gerar_relatorio_historico_aluno(
    filtros: HistoricoFiltros,
) -> RelatorioHistoricoAluno:
    """Gera timeline consolidada com participações e atuações do aluno."""

    if not filtros.aluno_id:
        resumo_vazio = ResumoHistorico(0, 0, 0, 0, 0, 0, 0, {})
        return RelatorioHistoricoAluno(filtros=filtros, eventos=[], resumo=resumo_vazio)

    Registro = _get_model("RegistroPresenca", "presencas")
    Atividade = _get_model("Atividade", "atividades")

    eventos: List[EventoHistorico] = []
    contagem_por_papel: Counter[str] = Counter()
    total_participacoes = 0
    total_presencas = 0
    total_faltas = 0
    total_justificadas = 0
    total_voluntarios = 0
    total_instrucao = 0

    registros_qs = (
        Registro.objects.select_related("atividade", "atividade__curso", "turma")
        .filter(aluno_id=filtros.aluno_id)
        .order_by("-data", "atividade__nome")
    )

    if filtros.curso_id:
        registros_qs = registros_qs.filter(atividade__curso_id=filtros.curso_id)
    if filtros.data_inicio:
        registros_qs = registros_qs.filter(data__gte=filtros.data_inicio)
    if filtros.data_fim:
        registros_qs = registros_qs.filter(data__lte=filtros.data_fim)

    for registro in registros_qs:
        papel_evento = STATUS_PARA_PAPEL.get(registro.status, PAPEL_PARTICIPANTE)
        if not _papel_corresponde(papel_evento, filtros.papel):
            continue

        atividade = registro.atividade
        turma = registro.turma
        curso = getattr(atividade, "curso", None)

        status_presenca = registro.get_status_display()
        descricao = f"{PAPEIS_LABELS.get(papel_evento, papel_evento.title())} na atividade {getattr(atividade, 'nome', '')}"
        if status_presenca:
            descricao = f"{descricao} ({status_presenca})"

        tipo_atividade = (
            atividade.get_tipo_atividade_display()
            if hasattr(atividade, "get_tipo_atividade_display")
            else getattr(atividade, "tipo_atividade", None)
        )

        status_atividade = (
            atividade.get_status_display()
            if hasattr(atividade, "get_status_display")
            else getattr(atividade, "status", None)
        )

        eventos.append(
            EventoHistorico(
                data=registro.data,
                papel=papel_evento,
                papel_display=PAPEIS_LABELS.get(papel_evento, papel_evento.title()),
                descricao=descricao,
                atividade_nome=getattr(atividade, "nome", ""),
                curso_nome=getattr(curso, "nome", None),
                turma_nome=getattr(turma, "nome", None),
                status_presenca=status_presenca,
                status_atividade=status_atividade,
                tipo_atividade=tipo_atividade,
            )
        )

        contagem_por_papel[PAPEIS_LABELS.get(papel_evento, papel_evento.title())] += 1
        total_participacoes += 1
        if registro.status == "P":
            total_presencas += 1
        elif registro.status == "F":
            total_faltas += 1
        elif registro.status == "J":
            total_justificadas += 1
        if registro.status in {"V1", "V2"}:
            total_voluntarios += 1

    atividades_instrucao = (
        Atividade.objects.select_related("curso")
        .prefetch_related("turmas")
        .filter(
            Q(turmas__instrutor_id=filtros.aluno_id)
            | Q(turmas__instrutor_auxiliar_id=filtros.aluno_id)
            | Q(turmas__auxiliar_instrucao_id=filtros.aluno_id)
        )
        .order_by("-data_inicio", "nome")
    )

    if filtros.curso_id:
        atividades_instrucao = atividades_instrucao.filter(curso_id=filtros.curso_id)
    if filtros.data_inicio:
        atividades_instrucao = atividades_instrucao.filter(
            Q(data_inicio__gte=filtros.data_inicio)
            | Q(turmas__data_inicio_ativ__gte=filtros.data_inicio)
        )
    if filtros.data_fim:
        atividades_instrucao = atividades_instrucao.filter(
            Q(data_inicio__lte=filtros.data_fim)
            | Q(turmas__data_inicio_ativ__lte=filtros.data_fim)
        )

    seen_papel_por_turma = set()

    for atividade in atividades_instrucao.distinct():
        for turma in atividade.turmas.all():
            papel_evento: Optional[str] = None
            if turma.instrutor_id == filtros.aluno_id:
                papel_evento = PAPEL_INSTRUTOR
            elif turma.instrutor_auxiliar_id == filtros.aluno_id:
                papel_evento = PAPEL_INSTRUTOR_AUX
            elif turma.auxiliar_instrucao_id == filtros.aluno_id:
                papel_evento = PAPEL_AUX_INSTRUCAO

            if not papel_evento:
                continue

            if (turma.id, papel_evento) in seen_papel_por_turma:
                continue
            seen_papel_por_turma.add((turma.id, papel_evento))

            if not _papel_corresponde(papel_evento, filtros.papel):
                continue

            data_evento = (
                getattr(atividade, "data_inicio", None)
                or getattr(turma, "data_inicio_ativ", None)
                or filtros.data_inicio
                or date.today()
            )

            descricao = f"{PAPEIS_LABELS.get(papel_evento, papel_evento.title())} na turma {getattr(turma, 'nome', '')}"

            tipo_atividade = (
                atividade.get_tipo_atividade_display()
                if hasattr(atividade, "get_tipo_atividade_display")
                else getattr(atividade, "tipo_atividade", None)
            )
            status_atividade = (
                atividade.get_status_display()
                if hasattr(atividade, "get_status_display")
                else getattr(atividade, "status", None)
            )

            eventos.append(
                EventoHistorico(
                    data=data_evento,
                    papel=papel_evento,
                    papel_display=PAPEIS_LABELS.get(papel_evento, papel_evento.title()),
                    descricao=descricao,
                    atividade_nome=getattr(atividade, "nome", ""),
                    curso_nome=getattr(getattr(atividade, "curso", None), "nome", None),
                    turma_nome=getattr(turma, "nome", None),
                    status_presenca=None,
                    status_atividade=status_atividade,
                    tipo_atividade=tipo_atividade,
                )
            )

            contagem_por_papel[
                PAPEIS_LABELS.get(papel_evento, papel_evento.title())
            ] += 1
            total_instrucao += 1

    eventos.sort(
        key=lambda evento: (evento.data, evento.papel_display.lower()), reverse=True
    )

    resumo = ResumoHistorico(
        total_eventos=len(eventos),
        total_participacoes=total_participacoes,
        total_presencas=total_presencas,
        total_faltas=total_faltas,
        total_justificadas=total_justificadas,
        total_voluntarios=total_voluntarios,
        total_instrucao=total_instrucao,
        eventos_por_papel=dict(
            sorted(contagem_por_papel.items(), key=lambda item: item[0])
        ),
    )

    return RelatorioHistoricoAluno(filtros=filtros, eventos=eventos, resumo=resumo)


def obter_opcoes_filtros_historico(
    aluno_id: Optional[int] = None, curso_id: Optional[int] = None
) -> Dict[str, List[Dict[str, str]]]:
    """Retorna opções para montagem dos filtros dinâmicos do relatório."""

    Aluno = _get_model("Aluno", "alunos")
    Curso = _get_model("Curso", "cursos")

    alunos_qs = Aluno.objects.filter(ativo=True)
    if curso_id:
        alunos_qs = alunos_qs.filter(
            Q(registros_de_presenca__atividade__curso_id=curso_id)
            | Q(turmas_como_instrutor__curso_id=curso_id)
            | Q(turmas_como_instrutor_auxiliar__curso_id=curso_id)
            | Q(turmas_como_auxiliar_instrucao__curso_id=curso_id)
        )
    alunos_qs = alunos_qs.distinct().order_by("nome")

    alunos = [
        {
            "id": aluno.id,
            "nome": aluno_display(aluno),
        }
        for aluno in alunos_qs
    ]

    if aluno_id and not any(item["id"] == aluno_id for item in alunos):
        try:
            aluno = Aluno.objects.get(id=aluno_id)
            alunos.append({"id": aluno.id, "nome": aluno_display(aluno)})
        except Aluno.DoesNotExist:  # pragma: no cover - sincronização defensiva
            pass

    cursos = list(
        Curso.objects.filter(ativo=True).order_by("nome").values("id", "nome")
    )

    papeis = [
        {"value": PAPEL_PARTICIPANTE, "label": PAPEIS_LABELS[PAPEL_PARTICIPANTE]},
        {"value": PAPEL_VOLUNTARIO, "label": PAPEIS_LABELS[PAPEL_VOLUNTARIO]},
        {
            "value": PAPEL_VOLUNTARIO_EXTRA,
            "label": PAPEIS_LABELS[PAPEL_VOLUNTARIO_EXTRA],
        },
        {
            "value": PAPEL_VOLUNTARIO_SIMPLES,
            "label": PAPEIS_LABELS[PAPEL_VOLUNTARIO_SIMPLES],
        },
        {"value": PAPEL_INSTRUTOR, "label": PAPEIS_LABELS[PAPEL_INSTRUTOR]},
        {"value": PAPEL_INSTRUTOR_AUX, "label": PAPEIS_LABELS[PAPEL_INSTRUTOR_AUX]},
        {"value": PAPEL_AUX_INSTRUCAO, "label": PAPEIS_LABELS[PAPEL_AUX_INSTRUCAO]},
    ]

    return {
        "alunos": sorted(alunos, key=lambda item: item["nome"].lower()),
        "cursos": cursos,
        "papeis": papeis,
    }


def aluno_display(aluno) -> str:
    """Retorna representação curta do aluno (nome + número iniciático)."""

    numero = getattr(aluno, "numero_iniciatico", "") or ""
    return f"{aluno.nome} ({numero})" if numero else aluno.nome


def _papel_corresponde(papel_evento: str, filtro: Optional[str]) -> bool:
    if not filtro:
        return True
    if filtro == PAPEL_VOLUNTARIO:
        return papel_evento in PAPEIS_VOLUNTARIO
    return papel_evento == filtro


__all__ = [
    "HistoricoFiltros",
    "EventoHistorico",
    "ResumoHistorico",
    "RelatorioHistoricoAluno",
    "normalizar_filtros_historico",
    "gerar_relatorio_historico_aluno",
    "obter_opcoes_filtros_historico",
    "aluno_display",
]
