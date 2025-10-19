# c:/projetos/omaum/presencas/services/administrative.py
"""
Serviços de Relatórios Administrativos para Gestão Institucional
Categoria 5 - Relatórios Administrativos
"""

from datetime import timedelta
from typing import Dict
from django.db.models import Q, Avg, Count, Sum, F, Case, When, Value
from django.utils import timezone
from importlib import import_module
import logging

logger = logging.getLogger(__name__)

# Configurações administrativas
ADMIN_CONFIG = {
    "metas_institucionais": {
        "percentual_presenca_minimo": 75,  # Meta institucional de presença
        "percentual_aprovacao_minimo": 80,  # Meta de aprovação
        "limite_evasao_maximo": 15,  # Limite máximo de evasão (%)
        "nota_media_institucional": 7.0,  # Nota média esperada
    },
    "niveis_alerta": {
        "critico": 60,  # Abaixo de 60% - crítico
        "atencao": 75,  # Entre 60-75% - atenção
        "bom": 85,  # Entre 75-85% - bom
        "excelente": 90,  # Acima de 90% - excelente
    },
    "periodos_analise": {"trimestre": 3, "semestre": 6, "ano": 12},
}


def _pd_model():
    """Obtém o modelo PresencaDetalhada dinamicamente."""
    try:
        mdl = import_module("presencas.models")
        return getattr(mdl, "PresencaDetalhada")
    except Exception as e:
        logger.error(f"Erro ao importar modelo PresencaDetalhada: {e}")
        raise


def _get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    try:
        mdl = import_module("alunos.models")
        return getattr(mdl, "Aluno")
    except Exception as e:
        logger.error(f"Erro ao importar modelo Aluno: {e}")
        raise


def _get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    try:
        mdl = import_module("turmas.models")
        return getattr(mdl, "Turma")
    except Exception as e:
        logger.error(f"Erro ao importar modelo Turma: {e}")
        raise


def _get_curso_model():
    """Obtém o modelo Curso dinamicamente."""
    try:
        mdl = import_module("cursos.models")
        return getattr(mdl, "Curso")
    except Exception as e:
        logger.error(f"Erro ao importar modelo Curso: {e}")
        raise


def _calcular_indice_performance_institucional(dados_gerais: Dict) -> Dict:
    """
    Calcula índices de performance institucional baseado em múltiplas métricas.

    Args:
        dados_gerais: Dados consolidados da instituição

    Returns:
        Dicionário com índices de performance
    """
    try:
        metas = ADMIN_CONFIG["metas_institucionais"]

        # Cálculo do Índice de Presença Institucional (IPI)
        presenca_media = dados_gerais.get("presenca_media", 0)
        ipi = min(100, (presenca_media / metas["percentual_presenca_minimo"]) * 100)

        # Cálculo do Índice de Qualidade Acadêmica (IQA)
        nota_media = dados_gerais.get("nota_media", 0)
        iqa = min(100, (nota_media / metas["nota_media_institucional"]) * 100)

        # Cálculo do Índice de Retenção (IR)
        taxa_evasao = dados_gerais.get("taxa_evasao", 0)
        ir = max(0, 100 - (taxa_evasao / metas["limite_evasao_maximo"]) * 100)

        # Índice Geral de Performance (IGP) - média ponderada
        igp = ipi * 0.4 + iqa * 0.35 + ir * 0.25

        return {
            "indice_presenca": round(ipi, 1),
            "indice_qualidade": round(iqa, 1),
            "indice_retencao": round(ir, 1),
            "indice_geral": round(igp, 1),
            "classificacao": _classificar_performance(igp),
        }
    except Exception as e:
        logger.error(f"Erro ao calcular índices de performance: {e}")
        return {
            "indice_presenca": 0,
            "indice_qualidade": 0,
            "indice_retencao": 0,
            "indice_geral": 0,
            "classificacao": "Sem dados",
        }


def _classificar_performance(indice: float) -> str:
    """Classifica a performance baseada no índice geral."""
    niveis = ADMIN_CONFIG["niveis_alerta"]

    if indice >= niveis["excelente"]:
        return "Excelente"
    elif indice >= niveis["bom"]:
        return "Bom"
    elif indice >= niveis["atencao"]:
        return "Atenção"
    else:
        return "Crítico"


def get_dashboard_coordenacao(turma_id=None, curso_id=None, periodo=None):
    """
    Gera dashboard executivo para coordenação acadêmica.

    Args:
        turma_id: ID da turma para filtrar
        curso_id: ID do curso para filtrar
        periodo: Período de análise (trimestre, semestre, ano)

    Returns:
        Contexto com dados do dashboard de coordenação
    """
    try:
        logger.info(
            f"Gerando dashboard de coordenação - Turma: {turma_id}, Curso: {curso_id}"
        )

        # Modelos
        PresencaDetalhada = _pd_model()
        Aluno = _get_aluno_model()
        Turma = _get_turma_model()

        # Filtros base
        filtros = Q()
        if turma_id:
            filtros &= Q(turma_id=turma_id)
        if curso_id:
            filtros &= Q(turma__curso_id=curso_id)

        # Período de análise
        meses_analise = ADMIN_CONFIG["periodos_analise"].get(periodo or "semestre", 6)
        data_inicio = timezone.now() - timedelta(days=meses_analise * 30)
        filtros &= Q(periodo__gte=data_inicio.date())

        # Dados de presença por turma
        dados_turmas = (
            PresencaDetalhada.objects.filter(filtros)
            .values("turma__nome", "turma__curso__nome")
            .annotate(
                total_alunos=Count("aluno", distinct=True),
                total_presencas=Sum("presencas"),
                total_faltas=Sum("faltas"),
                total_convocacoes=Sum("convocacoes"),
                percentual_presenca=Case(
                    When(total_convocacoes=0, then=Value(0)),
                    default=F("total_presencas") * 100.0 / F("total_convocacoes"),
                ),
                media_carencias=Avg("carencias"),
            )
            .order_by("-percentual_presenca")
        )

        # Estatísticas gerais da coordenação
        stats_gerais = PresencaDetalhada.objects.filter(filtros).aggregate(
            total_alunos=Count("aluno", distinct=True),
            total_turmas=Count("turma", distinct=True),
            presenca_media=Avg(
                Case(
                    When(convocacoes=0, then=Value(0)),
                    default=F("presencas") * 100.0 / F("convocacoes"),
                )
            ),
            carencias_media=Avg("carencias"),
            total_carencias=Sum("carencias"),
        )

        # Top 5 melhores e piores turmas
        melhores_turmas = list(dados_turmas[:5])
        piores_turmas = list(dados_turmas.order_by("percentual_presenca")[:5])

        # Alunos com mais carências (atenção da coordenação)
        alunos_atencao = (
            PresencaDetalhada.objects.filter(filtros)
            .values("aluno__nome", "turma__nome")
            .annotate(
                total_carencias=Sum("carencias"),
                percentual_presenca=Case(
                    When(total_convocacoes=0, then=Value(0)),
                    default=Sum("presencas") * 100.0 / Sum("convocacoes"),
                ),
                total_convocacoes=Sum("convocacoes"),
            )
            .filter(total_carencias__gte=5)
            .order_by("-total_carencias")[:10]
        )

        # Análise de tendências (comparação com período anterior)
        data_inicio_anterior = data_inicio - timedelta(days=meses_analise * 30)
        stats_anteriores = PresencaDetalhada.objects.filter(
            filtros,
            periodo__gte=data_inicio_anterior.date(),
            periodo__lt=data_inicio.date(),
        ).aggregate(
            presenca_media_anterior=Avg(
                Case(
                    When(convocacoes=0, then=Value(0)),
                    default=F("presencas") * 100.0 / F("convocacoes"),
                )
            )
        )

        presenca_atual = stats_gerais.get("presenca_media", 0) or 0
        presenca_anterior = stats_anteriores.get("presenca_media_anterior", 0) or 0
        tendencia_presenca = presenca_atual - presenca_anterior

        # Distribuição por níveis de performance
        distribuicao_performance = {
            "excelente": dados_turmas.filter(percentual_presenca__gte=90).count(),
            "bom": dados_turmas.filter(
                percentual_presenca__gte=75, percentual_presenca__lt=90
            ).count(),
            "atencao": dados_turmas.filter(
                percentual_presenca__gte=60, percentual_presenca__lt=75
            ).count(),
            "critico": dados_turmas.filter(percentual_presenca__lt=60).count(),
        }

        return {
            "sucesso": True,
            "dashboard_tipo": "coordenacao",
            "periodo_analise": periodo or "semestre",
            "estatisticas_gerais": {
                "total_alunos": stats_gerais.get("total_alunos", 0),
                "total_turmas": stats_gerais.get("total_turmas", 0),
                "presenca_media": round(presenca_atual, 1),
                "carencias_media": round(
                    stats_gerais.get("carencias_media", 0) or 0, 1
                ),
                "total_carencias": stats_gerais.get("total_carencias", 0),
                "tendencia_presenca": round(tendencia_presenca, 1),
            },
            "melhores_turmas": melhores_turmas,
            "piores_turmas": piores_turmas,
            "alunos_atencao": list(alunos_atencao),
            "distribuicao_performance": distribuicao_performance,
            "dados_turmas": list(dados_turmas),
            "metas_institucionais": ADMIN_CONFIG["metas_institucionais"],
        }

    except Exception as e:
        logger.error(f"Erro ao gerar dashboard de coordenação: {e}")
        return {
            "sucesso": False,
            "erro": str(e),
            "dashboard_tipo": "coordenacao",
            "estatisticas_gerais": {},
            "melhores_turmas": [],
            "piores_turmas": [],
            "alunos_atencao": [],
            "distribuicao_performance": {},
            "dados_turmas": [],
        }


def get_dashboard_direcao(curso_id=None, ano=None):
    """
    Gera dashboard executivo para direção institucional.

    Args:
        curso_id: ID do curso para filtrar
        ano: Ano para análise

    Returns:
        Contexto com dados do dashboard de direção
    """
    try:
        logger.info(f"Gerando dashboard de direção - Curso: {curso_id}, Ano: {ano}")

        # Modelos
        PresencaDetalhada = _pd_model()
        Curso = _get_curso_model()

        # Filtros base
        filtros = Q()
        if curso_id:
            filtros &= Q(turma__curso_id=curso_id)
        if ano:
            filtros &= Q(periodo__year=ano)
        else:
            # Último ano por padrão
            filtros &= Q(periodo__year=timezone.now().year)

        # Dados consolidados por curso
        dados_cursos = (
            PresencaDetalhada.objects.filter(filtros)
            .values("turma__curso__nome", "turma__curso__id")
            .annotate(
                total_alunos=Count("aluno", distinct=True),
                total_turmas=Count("turma", distinct=True),
                presenca_media=Avg(
                    Case(
                        When(convocacoes=0, then=Value(0)),
                        default=F("presencas") * 100.0 / F("convocacoes"),
                    )
                ),
                total_carencias=Sum("carencias"),
                taxa_carencias=Case(
                    When(total_alunos=0, then=Value(0)),
                    default=F("total_carencias") * 100.0 / F("total_alunos"),
                ),
            )
            .order_by("-presenca_media")
        )

        # Estatísticas institucionais
        stats_institucionais = PresencaDetalhada.objects.filter(filtros).aggregate(
            total_alunos_instituicao=Count("aluno", distinct=True),
            total_cursos=Count("turma__curso", distinct=True),
            total_turmas_instituicao=Count("turma", distinct=True),
            presenca_media_instituicao=Avg(
                Case(
                    When(convocacoes=0, then=Value(0)),
                    default=F("presencas") * 100.0 / F("convocacoes"),
                )
            ),
            total_carencias_instituicao=Sum("carencias"),
        )

        # Cálculo de indicadores de qualidade institucional
        presenca_media = stats_institucionais.get("presenca_media_instituicao", 0) or 0
        total_alunos = stats_institucionais.get("total_alunos_instituicao", 0) or 1
        total_carencias = (
            stats_institucionais.get("total_carencias_instituicao", 0) or 0
        )

        # Simular nota média (em um sistema real, viria de outro módulo)
        nota_media_estimada = (
            7.5 if presenca_media >= 80 else 6.5 if presenca_media >= 70 else 5.5
        )

        # Simular taxa de evasão baseada em carências
        taxa_evasao_estimada = min(25, (total_carencias / total_alunos) * 2)

        dados_performance = {
            "presenca_media": presenca_media,
            "nota_media": nota_media_estimada,
            "taxa_evasao": taxa_evasao_estimada,
        }

        # Calcular índices de performance institucional
        indices_performance = _calcular_indice_performance_institucional(
            dados_performance
        )

        # Evolução mensal (últimos 12 meses)
        data_12_meses = timezone.now() - timedelta(days=365)
        evolucao_mensal = (
            PresencaDetalhada.objects.filter(filtros, periodo__gte=data_12_meses.date())
            .extra(
                select={
                    "mes": "EXTRACT(month FROM periodo)",
                    "ano": "EXTRACT(year FROM periodo)",
                }
            )
            .values("mes", "ano")
            .annotate(
                presenca_media=Avg(
                    Case(
                        When(convocacoes=0, then=Value(0)),
                        default=F("presencas") * 100.0 / F("convocacoes"),
                    )
                ),
                total_alunos=Count("aluno", distinct=True),
            )
            .order_by("ano", "mes")
        )

        # Ranking de cursos por performance
        ranking_cursos = dados_cursos.annotate(
            score_performance=(
                F("presenca_media") * 0.6 + (100 - F("taxa_carencias")) * 0.4
            )
        ).order_by("-score_performance")

        # Alertas para direção
        alertas_direcao = []

        for curso in dados_cursos:
            if curso["presenca_media"] < 70:
                alertas_direcao.append(
                    {
                        "tipo": "critico",
                        "curso": curso["turma__curso__nome"],
                        "valor": curso["presenca_media"],
                        "mensagem": f"Presença crítica: {curso['presenca_media']:.1f}%",
                    }
                )
            elif curso["taxa_carencias"] > 20:
                alertas_direcao.append(
                    {
                        "tipo": "atencao",
                        "curso": curso["turma__curso__nome"],
                        "valor": curso["taxa_carencias"],
                        "mensagem": f"Alta taxa de carências: {curso['taxa_carencias']:.1f}%",
                    }
                )

        return {
            "sucesso": True,
            "dashboard_tipo": "direcao",
            "ano_analise": ano or timezone.now().year,
            "estatisticas_institucionais": {
                "total_alunos": stats_institucionais.get("total_alunos_instituicao", 0),
                "total_cursos": stats_institucionais.get("total_cursos", 0),
                "total_turmas": stats_institucionais.get("total_turmas_instituicao", 0),
                "presenca_media": round(presenca_media, 1),
                "nota_media_estimada": round(nota_media_estimada, 1),
                "taxa_evasao_estimada": round(taxa_evasao_estimada, 1),
                "total_carencias": total_carencias,
            },
            "indices_performance": indices_performance,
            "dados_cursos": list(dados_cursos),
            "ranking_cursos": list(ranking_cursos),
            "evolucao_mensal": list(evolucao_mensal),
            "alertas_direcao": alertas_direcao,
            "metas_institucionais": ADMIN_CONFIG["metas_institucionais"],
        }

    except Exception as e:
        logger.error(f"Erro ao gerar dashboard de direção: {e}")
        return {
            "sucesso": False,
            "erro": str(e),
            "dashboard_tipo": "direcao",
            "estatisticas_institucionais": {},
            "indices_performance": {},
            "dados_cursos": [],
            "ranking_cursos": [],
            "evolucao_mensal": [],
            "alertas_direcao": [],
        }


def get_metricas_professor(professor_id=None, disciplina=None, periodo=None):
    """
    Gera métricas por professor/disciplina.

    Args:
        professor_id: ID do professor
        disciplina: Nome da disciplina
        periodo: Período de análise

    Returns:
        Contexto com métricas do professor
    """
    try:
        logger.info(
            f"Gerando métricas de professor - ID: {professor_id}, Disciplina: {disciplina}"
        )

        # Modelos
        PresencaDetalhada = _pd_model()

        # Filtros base
        filtros = Q()

        # Simular filtro por professor (em um sistema real, haveria relação com User/Professor)
        if professor_id:
            # Filtrar por turmas que o professor leciona
            filtros &= Q(turma__id__in=[1, 2, 3])  # Simulação

        if disciplina:
            # Filtrar por disciplina (em um sistema real, haveria modelo Disciplina)
            filtros &= Q(turma__nome__icontains=disciplina)

        # Período de análise
        meses_analise = ADMIN_CONFIG["periodos_analise"].get(periodo or "trimestre", 3)
        data_inicio = timezone.now() - timedelta(days=meses_analise * 30)
        filtros &= Q(periodo__gte=data_inicio.date())

        # Dados por turma do professor
        dados_turmas_professor = (
            PresencaDetalhada.objects.filter(filtros)
            .values("turma__nome")
            .annotate(
                total_alunos=Count("aluno", distinct=True),
                presenca_media=Avg(
                    Case(
                        When(convocacoes=0, then=Value(0)),
                        default=F("presencas") * 100.0 / F("convocacoes"),
                    )
                ),
                total_carencias=Sum("carencias"),
                percentual_aprovacao=Value(85.0),  # Simulação - viria de outro módulo
            )
            .order_by("-presenca_media")
        )

        # Estatísticas do professor
        stats_professor = PresencaDetalhada.objects.filter(filtros).aggregate(
            total_alunos_professor=Count("aluno", distinct=True),
            total_turmas_professor=Count("turma", distinct=True),
            presenca_media_professor=Avg(
                Case(
                    When(convocacoes=0, then=Value(0)),
                    default=F("presencas") * 100.0 / F("convocacoes"),
                )
            ),
            total_carencias_professor=Sum("carencias"),
        )

        # Comparação com média institucional
        stats_institucionais = PresencaDetalhada.objects.filter(
            periodo__gte=data_inicio.date()
        ).aggregate(
            presenca_media_geral=Avg(
                Case(
                    When(convocacoes=0, then=Value(0)),
                    default=F("presencas") * 100.0 / F("convocacoes"),
                )
            )
        )

        presenca_professor = stats_professor.get("presenca_media_professor", 0) or 0
        presenca_geral = stats_institucionais.get("presenca_media_geral", 0) or 0
        diferenca_media = presenca_professor - presenca_geral

        # Ranking do professor
        posicao_ranking = (
            "Top 10%"
            if diferenca_media > 5
            else "Média"
            if abs(diferenca_media) <= 5
            else "Abaixo da média"
        )

        # Sugestões de melhoria
        sugestoes = []
        if presenca_professor < 75:
            sugestoes.append(
                "Implementar estratégias de engajamento para melhorar presença"
            )
        if stats_professor.get("total_carencias_professor", 0) > 10:
            sugestoes.append("Acompanhar mais de perto alunos com carências")
        if diferenca_media < -5:
            sugestoes.append("Buscar apoio pedagógico para melhoria dos indicadores")

        return {
            "sucesso": True,
            "professor_id": professor_id,
            "disciplina": disciplina,
            "periodo_analise": periodo or "trimestre",
            "estatisticas_professor": {
                "total_alunos": stats_professor.get("total_alunos_professor", 0),
                "total_turmas": stats_professor.get("total_turmas_professor", 0),
                "presenca_media": round(presenca_professor, 1),
                "total_carencias": stats_professor.get("total_carencias_professor", 0),
                "diferenca_media_institucional": round(diferenca_media, 1),
                "posicao_ranking": posicao_ranking,
            },
            "dados_turmas": list(dados_turmas_professor),
            "comparacao_institucional": {
                "presenca_media_geral": round(presenca_geral, 1),
                "performance_relativa": "Acima" if diferenca_media > 0 else "Abaixo",
            },
            "sugestoes_melhoria": sugestoes,
        }

    except Exception as e:
        logger.error(f"Erro ao gerar métricas de professor: {e}")
        return {
            "sucesso": False,
            "erro": str(e),
            "professor_id": professor_id,
            "estatisticas_professor": {},
            "dados_turmas": [],
            "comparacao_institucional": {},
            "sugestoes_melhoria": [],
        }


def get_indicadores_qualidade():
    """
    Gera relatório de indicadores de qualidade institucional.

    Returns:
        Contexto com indicadores de qualidade
    """
    try:
        logger.info("Gerando indicadores de qualidade institucional")

        # Modelos
        PresencaDetalhada = _pd_model()

        # Período dos últimos 12 meses
        data_12_meses = timezone.now() - timedelta(days=365)

        # Indicadores principais
        indicadores = PresencaDetalhada.objects.filter(
            periodo__gte=data_12_meses.date()
        ).aggregate(
            presenca_media_anual=Avg(
                Case(
                    When(convocacoes=0, then=Value(0)),
                    default=F("presencas") * 100.0 / F("convocacoes"),
                )
            ),
            total_alunos_anual=Count("aluno", distinct=True),
            total_carencias_anual=Sum("carencias"),
            taxa_carencias_media=Avg("carencias"),
        )

        # Distribuição de presença por faixas
        total_registros = PresencaDetalhada.objects.filter(
            periodo__gte=data_12_meses.date()
        ).count()

        if total_registros > 0:
            distribuicao_presenca = {
                "excelente": PresencaDetalhada.objects.filter(
                    periodo__gte=data_12_meses.date()
                )
                .extra(
                    where=[
                        "CASE WHEN convocacoes = 0 THEN 0 ELSE (presencas * 100.0 / convocacoes) END >= 90"
                    ]
                )
                .count()
                / total_registros
                * 100,
                "bom": PresencaDetalhada.objects.filter(
                    periodo__gte=data_12_meses.date()
                )
                .extra(
                    where=[
                        "CASE WHEN convocacoes = 0 THEN 0 ELSE (presencas * 100.0 / convocacoes) END >= 75 AND CASE WHEN convocacoes = 0 THEN 0 ELSE (presencas * 100.0 / convocacoes) END < 90"
                    ]
                )
                .count()
                / total_registros
                * 100,
                "regular": PresencaDetalhada.objects.filter(
                    periodo__gte=data_12_meses.date()
                )
                .extra(
                    where=[
                        "CASE WHEN convocacoes = 0 THEN 0 ELSE (presencas * 100.0 / convocacoes) END >= 60 AND CASE WHEN convocacoes = 0 THEN 0 ELSE (presencas * 100.0 / convocacoes) END < 75"
                    ]
                )
                .count()
                / total_registros
                * 100,
                "critico": PresencaDetalhada.objects.filter(
                    periodo__gte=data_12_meses.date()
                )
                .extra(
                    where=[
                        "CASE WHEN convocacoes = 0 THEN 0 ELSE (presencas * 100.0 / convocacoes) END < 60"
                    ]
                )
                .count()
                / total_registros
                * 100,
            }
        else:
            distribuicao_presenca = {
                "excelente": 0,
                "bom": 0,
                "regular": 0,
                "critico": 0,
            }

        # Evolução trimestral
        evolucao_trimestral = []
        for i in range(4):
            inicio_trimestre = timezone.now() - timedelta(days=(i + 1) * 90)
            fim_trimestre = timezone.now() - timedelta(days=i * 90)

            stats_trimestre = PresencaDetalhada.objects.filter(
                periodo__gte=inicio_trimestre.date(), periodo__lt=fim_trimestre.date()
            ).aggregate(
                presenca_media=Avg(
                    Case(
                        When(convocacoes=0, then=Value(0)),
                        default=F("presencas") * 100.0 / F("convocacoes"),
                    )
                )
            )

            evolucao_trimestral.append(
                {
                    "trimestre": f"T{4-i}",
                    "presenca_media": round(
                        stats_trimestre.get("presenca_media", 0) or 0, 1
                    ),
                }
            )

        evolucao_trimestral.reverse()

        # Calcular índices de qualidade
        presenca_media = indicadores.get("presenca_media_anual", 0) or 0
        taxa_carencias = indicadores.get("taxa_carencias_media", 0) or 0

        # Simular dados complementares
        dados_qualidade = {
            "presenca_media": presenca_media,
            "nota_media": 7.2,  # Simulação
            "taxa_evasao": min(
                20, taxa_carencias * 1.5
            ),  # Estimativa baseada em carências
        }

        indices_qualidade = _calcular_indice_performance_institucional(dados_qualidade)

        # Comparação com metas
        metas = ADMIN_CONFIG["metas_institucionais"]
        comparacao_metas = {
            "presenca": {
                "valor": presenca_media,
                "meta": metas["percentual_presenca_minimo"],
                "atingiu": presenca_media >= metas["percentual_presenca_minimo"],
            },
            "nota_media": {
                "valor": dados_qualidade["nota_media"],
                "meta": metas["nota_media_institucional"],
                "atingiu": dados_qualidade["nota_media"]
                >= metas["nota_media_institucional"],
            },
            "evasao": {
                "valor": dados_qualidade["taxa_evasao"],
                "meta": metas["limite_evasao_maximo"],
                "atingiu": dados_qualidade["taxa_evasao"]
                <= metas["limite_evasao_maximo"],
            },
        }

        return {
            "sucesso": True,
            "indicadores_principais": {
                "presenca_media_anual": round(presenca_media, 1),
                "total_alunos": indicadores.get("total_alunos_anual", 0),
                "total_carencias": indicadores.get("total_carencias_anual", 0),
                "taxa_carencias_media": round(taxa_carencias, 1),
            },
            "indices_qualidade": indices_qualidade,
            "distribuicao_presenca": {
                k: round(v, 1) for k, v in distribuicao_presenca.items()
            },
            "evolucao_trimestral": evolucao_trimestral,
            "comparacao_metas": comparacao_metas,
            "metas_institucionais": metas,
        }

    except Exception as e:
        logger.error(f"Erro ao gerar indicadores de qualidade: {e}")
        return {
            "sucesso": False,
            "erro": str(e),
            "indicadores_principais": {},
            "indices_qualidade": {},
            "distribuicao_presenca": {},
            "evolucao_trimestral": [],
            "comparacao_metas": {},
        }


# ===== FUNÇÕES DE EXPORTAÇÃO CSV =====


def csv_dashboard_coordenacao(contexto):
    """Exporta dados do dashboard de coordenação para CSV."""
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # Cabeçalhos
    writer.writerow(
        [
            "Turma",
            "Curso",
            "Total Alunos",
            "Percentual Presença",
            "Total Carências",
            "Classificação",
        ]
    )

    # Dados das turmas
    for turma in contexto.get("dados_turmas", []):
        percentual = turma.get("percentual_presenca", 0)
        classificacao = _classificar_performance(percentual)

        writer.writerow(
            [
                turma.get("turma__nome", ""),
                turma.get("turma__curso__nome", ""),
                turma.get("total_alunos", 0),
                f"{percentual:.1f}%",
                turma.get("total_carencias", 0),
                classificacao,
            ]
        )

    return output.getvalue()


def csv_dashboard_direcao(contexto):
    """Exporta dados do dashboard de direção para CSV."""
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # Cabeçalhos
    writer.writerow(
        [
            "Curso",
            "Total Alunos",
            "Total Turmas",
            "Presença Média",
            "Taxa Carências",
            "Score Performance",
        ]
    )

    # Dados dos cursos
    for curso in contexto.get("ranking_cursos", []):
        writer.writerow(
            [
                curso.get("turma__curso__nome", ""),
                curso.get("total_alunos", 0),
                curso.get("total_turmas", 0),
                f"{curso.get('presenca_media', 0):.1f}%",
                f"{curso.get('taxa_carencias', 0):.1f}%",
                f"{curso.get('score_performance', 0):.1f}",
            ]
        )

    return output.getvalue()


def csv_metricas_professor(contexto):
    """Exporta métricas de professor para CSV."""
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # Cabeçalhos
    writer.writerow(
        ["Turma", "Total Alunos", "Presença Média", "Total Carências", "% Aprovação"]
    )

    # Dados das turmas do professor
    for turma in contexto.get("dados_turmas", []):
        writer.writerow(
            [
                turma.get("turma__nome", ""),
                turma.get("total_alunos", 0),
                f"{turma.get('presenca_media', 0):.1f}%",
                turma.get("total_carencias", 0),
                f"{turma.get('percentual_aprovacao', 0):.1f}%",
            ]
        )

    return output.getvalue()


def csv_indicadores_qualidade(contexto):
    """Exporta indicadores de qualidade para CSV."""
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # Cabeçalhos
    writer.writerow(["Indicador", "Valor Atual", "Meta", "Status", "Classificação"])

    # Indicadores principais
    indices = contexto.get("indices_qualidade", {})
    metas = contexto.get("metas_institucionais", {})

    writer.writerow(
        [
            "Índice Geral de Performance",
            f"{indices.get('indice_geral', 0):.1f}%",
            "85%",
            "✅" if indices.get("indice_geral", 0) >= 85 else "❌",
            indices.get("classificacao", "N/A"),
        ]
    )

    writer.writerow(
        [
            "Índice de Presença",
            f"{indices.get('indice_presenca', 0):.1f}%",
            f"{metas.get('percentual_presenca_minimo', 75)}%",
            "✅" if indices.get("indice_presenca", 0) >= 75 else "❌",
            "Presença",
        ]
    )

    writer.writerow(
        [
            "Índice de Qualidade",
            f"{indices.get('indice_qualidade', 0):.1f}%",
            f"{metas.get('nota_media_institucional', 7) * 10:.0f}%",
            "✅" if indices.get("indice_qualidade", 0) >= 70 else "❌",
            "Acadêmica",
        ]
    )

    writer.writerow(
        [
            "Índice de Retenção",
            f"{indices.get('indice_retencao', 0):.1f}%",
            f"{100 - metas.get('limite_evasao_maximo', 15)}%",
            "✅" if indices.get("indice_retencao", 0) >= 85 else "❌",
            "Retenção",
        ]
    )

    return output.getvalue()
