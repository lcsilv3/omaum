"""
Serviço de cálculos consolidados por aluno.
Extraído de calculadora_estatisticas.py para melhor organização.
"""

import logging
from decimal import Decimal
from datetime import date
from typing import Dict, Any, Optional

from django.db.models import Sum, Count

from ..models import PresencaDetalhada

logger = logging.getLogger(__name__)


class ConsolidadoAluno:
    """
    Calculadora de estatísticas consolidadas por aluno.
    
    Responsabilidades:
    - Calcular dados consolidados de um aluno específico
    - Agregar presenças, faltas, carências e voluntários
    - Calcular percentuais de presença
    """

    @staticmethod
    def calcular(
        aluno_id: int,
        turma_id: Optional[int] = None,
        atividade_id: Optional[int] = None,
        periodo_inicio: Optional[date] = None,
        periodo_fim: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Calcula dados consolidados de um aluno específico.

        Args:
            aluno_id: ID do aluno
            turma_id: ID da turma (opcional)
            atividade_id: ID da atividade (opcional)
            periodo_inicio: Data início do período (opcional)
            periodo_fim: Data fim do período (opcional)

        Returns:
            Dict com estatísticas consolidadas do aluno:
            - aluno_id: ID do aluno
            - aluno_nome: Nome do aluno
            - total_convocacoes: Total de convocações
            - total_presencas: Total de presenças
            - total_faltas: Total de faltas
            - total_voluntarios: Total de participações voluntárias
            - total_carencias: Total de carências
            - percentual_presenca: Percentual de presença
            - status: Status do aluno (OK/CARENTE/REPROVADO)
            - registros_count: Total de registros
        """
        try:
            # Filtros base
            filtros = {"aluno_id": aluno_id}

            if turma_id:
                filtros["turma_id"] = turma_id
            if atividade_id:
                filtros["atividade_id"] = atividade_id
            if periodo_inicio:
                filtros["periodo__gte"] = periodo_inicio
            if periodo_fim:
                filtros["periodo__lte"] = periodo_fim

            # Query otimizada com select_related
            presencas = PresencaDetalhada.objects.filter(**filtros).select_related(
                "aluno", "turma", "atividade"
            )

            if not presencas.exists():
                return ConsolidadoAluno._criar_vazio(aluno_id)

            # Agregações
            agregacoes = presencas.aggregate(
                total_convocacoes=Sum("convocacoes"),
                total_presencas=Sum("presencas"),
                total_faltas=Sum("faltas"),
                total_voluntario_extra=Sum("voluntario_extra"),
                total_voluntario_simples=Sum("voluntario_simples"),
                total_carencias=Sum("carencias"),
                total_registros=Count("id"),
            )

            # Cálculos
            total_convocacoes = agregacoes["total_convocacoes"] or 0
            total_presencas = agregacoes["total_presencas"] or 0
            total_faltas = agregacoes["total_faltas"] or 0
            total_voluntarios = (agregacoes["total_voluntario_extra"] or 0) + (
                agregacoes["total_voluntario_simples"] or 0
            )
            total_carencias = agregacoes["total_carencias"] or 0

            # Percentual de presença
            if total_convocacoes > 0:
                percentual = (Decimal(total_presencas) / Decimal(total_convocacoes)) * 100
            else:
                percentual = Decimal("0.00")

            # Status do aluno
            status = ConsolidadoAluno._determinar_status(percentual, total_carencias)

            # Dados do aluno
            primeiro_registro = presencas.first()
            aluno_nome = (
                primeiro_registro.aluno.nome if primeiro_registro else "Desconhecido"
            )

            return {
                "aluno_id": aluno_id,
                "aluno_nome": aluno_nome,
                "total_convocacoes": total_convocacoes,
                "total_presencas": total_presencas,
                "total_faltas": total_faltas,
                "total_voluntarios": total_voluntarios,
                "total_carencias": total_carencias,
                "percentual_presenca": round(percentual, 2),
                "status": status,
                "registros_count": agregacoes["total_registros"],
            }

        except Exception as e:
            logger.error(
                f"Erro ao calcular consolidado do aluno {aluno_id}: {str(e)}",
                exc_info=True,
            )
            return ConsolidadoAluno._criar_vazio(aluno_id)

    @staticmethod
    def _criar_vazio(aluno_id: int) -> Dict[str, Any]:
        """
        Cria um dicionário de consolidado vazio para aluno sem registros.

        Args:
            aluno_id: ID do aluno

        Returns:
            Dict com valores zerados
        """
        return {
            "aluno_id": aluno_id,
            "aluno_nome": "Sem registros",
            "total_convocacoes": 0,
            "total_presencas": 0,
            "total_faltas": 0,
            "total_voluntarios": 0,
            "total_carencias": 0,
            "percentual_presenca": Decimal("0.00"),
            "status": "SEM_DADOS",
            "registros_count": 0,
        }

    @staticmethod
    def _determinar_status(percentual: Decimal, carencias: int) -> str:
        """
        Determina status do aluno baseado em percentual e carências.

        Regras:
        - REPROVADO: < 75% de presença
        - CARENTE: >= 75% mas com carências > 0
        - OK: >= 75% e sem carências

        Args:
            percentual: Percentual de presença
            carencias: Número de carências

        Returns:
            Status: OK, CARENTE ou REPROVADO
        """
        if percentual < Decimal("75.00"):
            return "REPROVADO"
        elif carencias > 0:
            return "CARENTE"
        else:
            return "OK"
