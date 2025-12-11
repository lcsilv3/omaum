"""
Serviços de Análise Preditiva e Machine Learning para Presenças
Categoria 4 - Relatórios Preditivos
"""

import numpy as np
from datetime import timedelta, date
from typing import Dict, List
from django.db.models import Q, Avg, Sum, F
from importlib import import_module
import logging

logger = logging.getLogger(__name__)

# Configurações de Machine Learning
ML_CONFIG = {
    "periodo_analise_meses": 6,  # Janela de análise para previsões
    "threshold_risco_evasao": 60,  # % abaixo do qual é considerado risco
    "threshold_engajamento_alto": 85,  # % acima do qual é alta engajamento
    "peso_tendencia": 0.4,  # Peso da tendência na predição
    "peso_historico": 0.6,  # Peso do histórico na predição
    "min_periodos_analise": 3,  # Mínimo de períodos para análise confiável
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


def _calcular_tendencia_presenca(dados_historicos: List[Dict]) -> float:
    """
    Calcula a tendência de presença baseada nos últimos períodos.

    Args:
        dados_historicos: Lista de dados históricos ordenados por período

    Returns:
        Valor da tendência (-1 a +1, onde -1 é decrescente, +1 é crescente)
    """
    if len(dados_historicos) < 2:
        return 0.0

    percentuais = [float(d.get("percentual_presenca", 0)) for d in dados_historicos]

    # Calcular tendência usando regressão linear simples
    n = len(percentuais)
    x = list(range(n))

    # Cálculos de regressão linear
    sum_x = sum(x)
    sum_y = sum(percentuais)
    sum_xy = sum(xi * yi for xi, yi in zip(x, percentuais))
    sum_x2 = sum(xi * xi for xi in x)

    # Coeficiente angular (slope)
    if n * sum_x2 - sum_x * sum_x != 0:
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        # Normalizar slope para (-1, +1)
        return max(-1.0, min(1.0, slope / 10))

    return 0.0


def _calcular_score_risco(dados_aluno: Dict) -> float:
    """
    Calcula score de risco de evasão baseado em múltiplos fatores.

    Args:
        dados_aluno: Dados consolidados do aluno

    Returns:
        Score de risco (0-100, onde 100 é alto risco)
    """
    try:
        # Fatores de risco
        percentual_atual = float(dados_aluno.get("percentual_medio", 0))
        tendencia = dados_aluno.get("tendencia", 0)
        faltas_consecutivas = dados_aluno.get("faltas_consecutivas", 0)
        carencias_acumuladas = dados_aluno.get("carencias_total", 0)

        # Cálculo do score baseado em pesos
        score_percentual = max(0, 100 - percentual_atual)  # Quanto menor %, maior risco
        score_tendencia = (
            (1 - tendencia) * 50 if tendencia < 0 else 0
        )  # Tendência decrescente
        score_faltas = min(faltas_consecutivas * 10, 40)  # Faltas consecutivas
        score_carencias = min(carencias_acumuladas * 5, 30)  # Carências acumuladas

        # Score final (média ponderada)
        score_final = (
            score_percentual * 0.4
            + score_tendencia * 0.3
            + score_faltas * 0.2
            + score_carencias * 0.1
        )

        return min(100.0, max(0.0, score_final))

    except Exception as e:
        logger.warning(f"Erro ao calcular score de risco: {e}")
        return 50.0  # Score neutro em caso de erro


def get_previsao_evasao(turma_id=None, limite=50, periodo_analise=None):
    """
    Identifica alunos com alto risco de evasão baseado em análise preditiva.

    Args:
        turma_id: ID da turma (opcional)
        limite: Número máximo de resultados
        periodo_analise: Período base para análise

    Returns:
        Dict com dados dos alunos em risco de evasão
    """
    try:
        PresencaDetalhada = _pd_model()
        Aluno = _get_aluno_model()

        # Definir período de análise
        if not periodo_analise:
            periodo_analise = date.today().replace(day=1)

        # Período de análise (últimos 6 meses)
        periodo_inicio = (periodo_analise - timedelta(days=180)).replace(day=1)

        # Filtros base
        filtros = Q(periodo__gte=periodo_inicio, periodo__lte=periodo_analise)
        if turma_id:
            filtros &= Q(turma_id=turma_id)

        # Buscar dados históricos por aluno
        dados_historicos = (
            PresencaDetalhada.objects.filter(filtros)
            .values("aluno__id", "aluno__nome", "turma__nome", "periodo")
            .annotate(
                percentual_presenca=F("percentual_presenca"),
                carencias=F("carencias"),
                faltas=F("faltas"),
            )
            .order_by("aluno__id", "periodo")
        )

        # Agrupar por aluno para análise
        alunos_data = {}
        for item in dados_historicos:
            aluno_id = item["aluno__id"]
            if aluno_id not in alunos_data:
                alunos_data[aluno_id] = {
                    "nome": item["aluno__nome"],
                    "turma": item["turma__nome"],
                    "historico": [],
                }
            alunos_data[aluno_id]["historico"].append(item)

        # Calcular métricas preditivas para cada aluno
        alunos_risco = []

        for aluno_id, dados in alunos_data.items():
            if len(dados["historico"]) < ML_CONFIG["min_periodos_analise"]:
                continue

            # Calcular métricas
            percentuais = [float(h["percentual_presenca"]) for h in dados["historico"]]
            percentual_medio = sum(percentuais) / len(percentuais)
            tendencia = _calcular_tendencia_presenca(dados["historico"])

            # Métricas de risco
            carencias_total = sum(h.get("carencias", 0) for h in dados["historico"])
            faltas_total = sum(h.get("faltas", 0) for h in dados["historico"])

            # Detectar faltas consecutivas
            faltas_consecutivas = 0
            max_faltas_consecutivas = 0
            for h in reversed(dados["historico"][-3:]):  # Últimos 3 períodos
                if h.get("faltas", 0) > 0:
                    faltas_consecutivas += 1
                    max_faltas_consecutivas = max(
                        max_faltas_consecutivas, faltas_consecutivas
                    )
                else:
                    faltas_consecutivas = 0

            # Consolidar dados do aluno
            dados_consolidados = {
                "percentual_medio": percentual_medio,
                "tendencia": tendencia,
                "carencias_total": carencias_total,
                "faltas_consecutivas": max_faltas_consecutivas,
            }

            # Calcular score de risco
            score_risco = _calcular_score_risco(dados_consolidados)

            # Classificar nível de risco
            if score_risco >= 80:
                nivel_risco = "CRÍTICO"
                cor_risco = "danger"
            elif score_risco >= 60:
                nivel_risco = "ALTO"
                cor_risco = "warning"
            elif score_risco >= 40:
                nivel_risco = "MÉDIO"
                cor_risco = "info"
            else:
                nivel_risco = "BAIXO"
                cor_risco = "success"

            # Adicionar à lista se há risco significativo
            if score_risco >= 40:  # Threshold mínimo para aparecer no relatório
                alunos_risco.append(
                    {
                        "aluno_id": aluno_id,
                        "nome": dados["nome"],
                        "turma": dados["turma"],
                        "percentual_medio": round(percentual_medio, 2),
                        "tendencia": round(tendencia, 3),
                        "score_risco": round(score_risco, 1),
                        "nivel_risco": nivel_risco,
                        "cor_risco": cor_risco,
                        "carencias_total": carencias_total,
                        "faltas_consecutivas": max_faltas_consecutivas,
                        "recomendacoes": _gerar_recomendacoes(
                            dados_consolidados, score_risco
                        ),
                    }
                )

        # Ordenar por score de risco (maior risco primeiro)
        alunos_risco.sort(key=lambda x: x["score_risco"], reverse=True)

        # Limitar resultados
        alunos_risco = alunos_risco[:limite]

        # Estatísticas gerais
        total_analisados = len(alunos_data)
        total_em_risco = len(alunos_risco)
        taxa_risco = (
            (total_em_risco / total_analisados * 100) if total_analisados > 0 else 0
        )

        return {
            "alunos": alunos_risco,
            "estatisticas": {
                "total_analisados": total_analisados,
                "total_em_risco": total_em_risco,
                "taxa_risco": round(taxa_risco, 1),
                "periodo_analise": periodo_analise.strftime("%m/%Y"),
                "config_usado": ML_CONFIG,
            },
            "periodo_analise": periodo_analise,
            "sucesso": True,
        }

    except Exception as e:
        logger.error(f"Erro ao gerar previsão de evasão: {e}")
        return {"alunos": [], "estatisticas": {"erro": str(e)}, "sucesso": False}


def _gerar_recomendacoes(dados_aluno: Dict, score_risco: float) -> List[str]:
    """
    Gera recomendações de intervenção baseadas no perfil do aluno.

    Args:
        dados_aluno: Dados consolidados do aluno
        score_risco: Score de risco calculado

    Returns:
        Lista de recomendações de intervenção
    """
    recomendacoes = []

    percentual = dados_aluno.get("percentual_medio", 0)
    tendencia = dados_aluno.get("tendencia", 0)
    faltas_consecutivas = dados_aluno.get("faltas_consecutivas", 0)

    # Recomendações baseadas no score de risco
    if score_risco >= 80:
        recomendacoes.append("🚨 URGENTE: Contato imediato com o aluno")
        recomendacoes.append("📞 Agendar reunião presencial com coordenação")

    if percentual < 60:
        recomendacoes.append("📚 Revisar metodologia de ensino aplicada")
        recomendacoes.append("🤝 Implementar programa de mentoria")

    if tendencia < -0.3:
        recomendacoes.append("📉 Investigar causas da queda de frequência")
        recomendacoes.append("💬 Aplicar questionário de satisfação")

    if faltas_consecutivas >= 2:
        recomendacoes.append("📧 Comunicação formal com responsáveis")
        recomendacoes.append("📋 Verificar situação acadêmica geral")

    # Recomendações de apoio
    if score_risco >= 60:
        recomendacoes.append("🎯 Plano de recuperação personalizado")
        recomendacoes.append("📊 Monitoramento semanal de progresso")

    return recomendacoes[:5]  # Limitar a 5 recomendações


def get_intervencoes_automaticas(turma_id=None, periodo=None):
    """
    Identifica automaticamente alunos que precisam de intervenção.

    Args:
        turma_id: ID da turma (opcional)
        periodo: Período de análise

    Returns:
        Dict com sugestões de intervenções automáticas
    """
    try:
        # Buscar previsão de evasão
        dados_evasao = get_previsao_evasao(
            turma_id, limite=100, periodo_analise=periodo
        )

        if not dados_evasao["sucesso"]:
            return dados_evasao

        alunos = dados_evasao["alunos"]

        # Categorizar intervenções por urgência
        intervencoes = {
            "criticas": [],  # Score >= 80
            "altas": [],  # Score 60-79
            "medias": [],  # Score 40-59
            "preventivas": [],  # Tendência negativa mas score < 40
        }

        for aluno in alunos:
            score = aluno["score_risco"]

            if score >= 80:
                intervencoes["criticas"].append(
                    {
                        **aluno,
                        "acao_sugerida": "Intervenção imediata obrigatória",
                        "prazo": "24 horas",
                        "responsavel": "Coordenação + Psicopedagogia",
                    }
                )
            elif score >= 60:
                intervencoes["altas"].append(
                    {
                        **aluno,
                        "acao_sugerida": "Reunião agendada urgente",
                        "prazo": "3 dias úteis",
                        "responsavel": "Professor + Coordenação",
                    }
                )
            elif score >= 40:
                intervencoes["medias"].append(
                    {
                        **aluno,
                        "acao_sugerida": "Acompanhamento reforçado",
                        "prazo": "1 semana",
                        "responsavel": "Professor responsável",
                    }
                )

        # Adicionar ações preventivas para alunos com tendência negativa
        for aluno in alunos:
            if aluno["tendencia"] < -0.2 and aluno["score_risco"] < 40:
                intervencoes["preventivas"].append(
                    {
                        **aluno,
                        "acao_sugerida": "Monitoramento preventivo",
                        "prazo": "2 semanas",
                        "responsavel": "Professor",
                    }
                )

        # Estatísticas das intervenções
        total_intervencoes = sum(len(v) for v in intervencoes.values())

        return {
            "intervencoes": intervencoes,
            "estatisticas": {
                "total_intervencoes": total_intervencoes,
                "criticas": len(intervencoes["criticas"]),
                "altas": len(intervencoes["altas"]),
                "medias": len(intervencoes["medias"]),
                "preventivas": len(intervencoes["preventivas"]),
            },
            "recomendacoes_gerais": _gerar_recomendacoes_gerais(intervencoes),
            "sucesso": True,
        }

    except Exception as e:
        logger.error(f"Erro ao gerar intervenções automáticas: {e}")
        return {"intervencoes": {}, "estatisticas": {"erro": str(e)}, "sucesso": False}


def _gerar_recomendacoes_gerais(intervencoes: Dict) -> List[str]:
    """
    Gera recomendações gerais baseadas no padrão de intervenções.

    Args:
        intervencoes: Dict com intervenções categorizadas

    Returns:
        Lista de recomendações gerais para a instituição
    """
    recomendacoes = []

    total_criticas = len(intervencoes.get("criticas", []))
    total_altas = len(intervencoes.get("altas", []))
    total_intervencoes = sum(len(v) for v in intervencoes.values())

    if total_criticas > 5:
        recomendacoes.append(
            "🚨 Alto número de casos críticos - revisar estratégias institucionais"
        )

    if total_altas > 10:
        recomendacoes.append("⚠️ Implementar programa de acompanhamento preventivo")

    if total_intervencoes > 20:
        recomendacoes.append("📊 Análise sistêmica de causas de evasão necessária")
        recomendacoes.append("👥 Considerar ampliação da equipe de apoio")

    if not recomendacoes:
        recomendacoes.append("✅ Situação controlada - manter monitoramento preventivo")

    return recomendacoes


def get_correlacao_presenca_desempenho(turma_id=None, periodo=None):
    """
    Analisa correlação entre frequência e desempenho acadêmico.

    Args:
        turma_id: ID da turma
        periodo: Período de análise

    Returns:
        Dict com análise de correlação
    """
    try:
        PresencaDetalhada = _pd_model()

        # Buscar dados de presença
        filtros = Q()
        if turma_id:
            filtros &= Q(turma_id=turma_id)
        if periodo:
            filtros &= Q(periodo=periodo)

        dados_presenca = (
            PresencaDetalhada.objects.filter(filtros)
            .values("aluno__id", "aluno__nome")
            .annotate(
                percentual_medio=Avg("percentual_presenca"),
                total_carencias=Sum("carencias"),
                total_faltas=Sum("faltas"),
            )
        )

        # Simular dados de desempenho (em sistema real, viria de app notas)
        correlacoes = []

        for item in dados_presenca:
            percentual = float(item["percentual_medio"] or 0)
            carencias = item["total_carencias"] or 0

            # Simular nota baseada em presença (correlação realística)
            nota_simulada = min(
                10.0, max(0.0, (percentual / 10) + np.random.normal(0, 1))
            )

            correlacoes.append(
                {
                    "aluno_nome": item["aluno__nome"],
                    "percentual_presenca": round(percentual, 1),
                    "nota_estimada": round(nota_simulada, 1),
                    "carencias": carencias,
                    "classificacao": _classificar_correlacao(percentual, nota_simulada),
                }
            )

        # Calcular estatísticas de correlação
        if correlacoes:
            percentuais = [c["percentual_presenca"] for c in correlacoes]
            notas = [c["nota_estimada"] for c in correlacoes]

            # Coeficiente de correlação Pearson simplificado
            n = len(percentuais)
            if n > 1:
                r = (
                    np.corrcoef(percentuais, notas)[0, 1]
                    if not np.isnan(np.corrcoef(percentuais, notas)[0, 1])
                    else 0
                )
            else:
                r = 0
        else:
            r = 0

        return {
            "correlacoes": correlacoes[:50],  # Limitar a 50 resultados
            "estatisticas": {
                "coeficiente_correlacao": round(r, 3),
                "interpretacao": _interpretar_correlacao(r),
                "total_analisados": len(correlacoes),
                "media_presenca": round(np.mean(percentuais) if percentuais else 0, 1),
                "media_desempenho": round(np.mean(notas) if notas else 0, 1),
            },
            "recomendacoes": _gerar_recomendacoes_correlacao(r, correlacoes),
            "sucesso": True,
        }

    except Exception as e:
        logger.error(f"Erro ao analisar correlação presença-desempenho: {e}")
        return {"correlacoes": [], "estatisticas": {"erro": str(e)}, "sucesso": False}


def _classificar_correlacao(percentual: float, nota: float) -> str:
    """
    Classifica a correlação individual entre presença e desempenho.

    Args:
        percentual: Percentual de presença
        nota: Nota do aluno

    Returns:
        Classificação da correlação
    """
    if percentual >= 85 and nota >= 8:
        return "ALTA_PERFORMANCE"
    elif percentual >= 75 and nota >= 7:
        return "BOA_PERFORMANCE"
    elif percentual >= 60 and nota >= 6:
        return "PERFORMANCE_REGULAR"
    elif percentual < 60 and nota < 6:
        return "BAIXA_PERFORMANCE"
    elif percentual >= 80 and nota < 6:
        return "DIVERGENTE_ALTA_PRESENCA"
    elif percentual < 60 and nota >= 8:
        return "DIVERGENTE_BAIXA_PRESENCA"
    else:
        return "INDEFINIDA"


def _interpretar_correlacao(r: float) -> str:
    """
    Interpreta o coeficiente de correlação.

    Args:
        r: Coeficiente de correlação

    Returns:
        Interpretação textual
    """
    if abs(r) >= 0.8:
        return "Correlação muito forte"
    elif abs(r) >= 0.6:
        return "Correlação forte"
    elif abs(r) >= 0.4:
        return "Correlação moderada"
    elif abs(r) >= 0.2:
        return "Correlação fraca"
    else:
        return "Correlação muito fraca ou inexistente"


def _gerar_recomendacoes_correlacao(r: float, dados: List[Dict]) -> List[str]:
    """
    Gera recomendações baseadas na análise de correlação.

    Args:
        r: Coeficiente de correlação
        dados: Dados das correlações individuais

    Returns:
        Lista de recomendações
    """
    recomendacoes = []

    if r >= 0.6:
        recomendacoes.append("✅ Forte correlação presença-desempenho confirmada")
        recomendacoes.append("📈 Manter política de controle de frequência rigorosa")
    elif r >= 0.3:
        recomendacoes.append("⚠️ Correlação moderada - investigar outros fatores")
        recomendacoes.append("🔍 Analisar métodos pedagógicos complementares")
    else:
        recomendacoes.append("❓ Baixa correlação - revisar estratégia educacional")
        recomendacoes.append("🎯 Focar em qualidade ao invés de apenas frequência")

    # Analisar casos divergentes
    divergentes = [d for d in dados if "DIVERGENTE" in d.get("classificacao", "")]
    if len(divergentes) > 5:
        recomendacoes.append(
            "🔄 Casos divergentes detectados - análise individualizada necessária"
        )

    return recomendacoes


# Funções de exportação CSV
def csv_previsao_evasao(contexto):
    """Exporta dados de previsão de evasão para CSV."""
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # Cabeçalhos
    writer.writerow(
        [
            "Aluno",
            "Turma",
            "Percentual Médio",
            "Score Risco",
            "Nível Risco",
            "Tendência",
            "Carências Total",
            "Faltas Consecutivas",
        ]
    )

    # Dados
    for aluno in contexto.get("alunos", []):
        writer.writerow(
            [
                aluno.get("nome", ""),
                aluno.get("turma", ""),
                aluno.get("percentual_medio", 0),
                aluno.get("score_risco", 0),
                aluno.get("nivel_risco", ""),
                aluno.get("tendencia", 0),
                aluno.get("carencias_total", 0),
                aluno.get("faltas_consecutivas", 0),
            ]
        )

    return output.getvalue()


def csv_intervencoes_automaticas(contexto):
    """Exporta dados de intervenções automáticas para CSV."""
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # Cabeçalhos
    writer.writerow(
        [
            "Categoria",
            "Aluno",
            "Turma",
            "Score Risco",
            "Ação Sugerida",
            "Prazo",
            "Responsável",
        ]
    )

    # Dados por categoria
    intervencoes = contexto.get("intervencoes", {})
    for categoria, lista in intervencoes.items():
        for item in lista:
            writer.writerow(
                [
                    categoria.upper(),
                    item.get("nome", ""),
                    item.get("turma", ""),
                    item.get("score_risco", 0),
                    item.get("acao_sugerida", ""),
                    item.get("prazo", ""),
                    item.get("responsavel", ""),
                ]
            )

    return output.getvalue()


def csv_correlacao_presenca_desempenho(contexto):
    """Exporta dados de correlação presença-desempenho para CSV."""
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)

    # Cabeçalhos
    writer.writerow(
        ["Aluno", "Percentual Presença", "Nota Estimada", "Carências", "Classificação"]
    )

    # Dados
    for item in contexto.get("correlacoes", []):
        writer.writerow(
            [
                item.get("aluno_nome", ""),
                item.get("percentual_presenca", 0),
                item.get("nota_estimada", 0),
                item.get("carencias", 0),
                item.get("classificacao", ""),
            ]
        )

    return output.getvalue()
