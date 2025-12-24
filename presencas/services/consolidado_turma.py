"""
Serviço de cálculos consolidados por turma.
Extraído de calculadora_estatisticas.py para melhor organização.
"""

import logging
from decimal import Decimal
from datetime import date
from typing import Dict, Any, List, Optional

from django.db.models import Sum, Count
from django.core.exceptions import ValidationError
from django.utils import timezone

from ..models import PresencaDetalhada

logger = logging.getLogger(__name__)


class ConsolidadoTurma:
    """
    Calculadora de estatísticas consolidadas por turma.
    
    Responsabilidades:
    - Calcular estatísticas gerais da turma
    - Agregar dados por atividade
    - Agregar dados por aluno
    - Calcular distribuição de carências
    """

    @staticmethod
    def calcular(
        turma_id: int,
        periodo_inicio: Optional[date] = None,
        periodo_fim: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Calcula estatísticas consolidadas de uma turma.

        Args:
            turma_id: ID da turma
            periodo_inicio: Data início do período (opcional)
            periodo_fim: Data fim do período (opcional)

        Returns:
            Dict com estatísticas da turma:
            - turma: Informações da turma
            - periodo: Período analisado
            - totais: Agregações totais
            - percentuais: Percentuais médios
            - por_atividade: Lista de estatísticas por atividade
            - por_aluno: Lista de estatísticas por aluno
            - distribuicao_carencias: Distribuição de carências
            - data_calculo: Timestamp do cálculo
        """
        try:
            # Filtros
            filtros = {"turma_id": turma_id}
            if periodo_inicio:
                filtros["periodo__gte"] = periodo_inicio
            if periodo_fim:
                filtros["periodo__lte"] = periodo_fim

            # Query otimizada
            presencas = PresencaDetalhada.objects.filter(**filtros).select_related(
                "aluno", "turma", "atividade"
            )

            if not presencas.exists():
                return ConsolidadoTurma._criar_vazio(turma_id)

            # Agregações gerais
            agregacoes = presencas.aggregate(
                total_convocacoes=Sum("convocacoes"),
                total_presencas=Sum("presencas"),
                total_faltas=Sum("faltas"),
                total_voluntario_extra=Sum("voluntario_extra"),
                total_voluntario_simples=Sum("voluntario_simples"),
                total_carencias=Sum("carencias"),
                alunos_distintos=Count("aluno", distinct=True),
                atividades_distintas=Count("atividade", distinct=True),
            )

            # Percentual médio da turma
            percentual_medio = Decimal("0.00")
            if agregacoes["total_convocacoes"] and agregacoes["total_convocacoes"] > 0:
                percentual_medio = round(
                    (
                        Decimal(agregacoes["total_presencas"])
                        / Decimal(agregacoes["total_convocacoes"])
                    )
                    * Decimal("100"),
                    2,
                )

            # Estatísticas por atividade
            estatisticas_atividades = ConsolidadoTurma._calcular_por_atividade(
                presencas
            )

            # Estatísticas por aluno
            estatisticas_alunos = ConsolidadoTurma._calcular_por_aluno(presencas)

            # Distribuição de carências
            distribuicao_carencias = (
                ConsolidadoTurma._calcular_distribuicao_carencias(presencas)
            )

            # Informações da turma
            turma_info = None
            if presencas.exists():
                primeira_presenca = presencas.first()
                turma_info = {
                    "id": primeira_presenca.turma.id,
                    "nome": primeira_presenca.turma.nome,
                    "perc_presenca_minima": getattr(
                        primeira_presenca.turma,
                        "perc_presenca_minima",
                        getattr(primeira_presenca.turma, "perc_carencia", None),
                    ),
                }

            estatisticas = {
                "turma": turma_info,
                "periodo": {"inicio": periodo_inicio, "fim": periodo_fim},
                "totais": {
                    "convocacoes": agregacoes["total_convocacoes"] or 0,
                    "presencas": agregacoes["total_presencas"] or 0,
                    "faltas": agregacoes["total_faltas"] or 0,
                    "voluntario_extra": agregacoes["total_voluntario_extra"] or 0,
                    "voluntario_simples": agregacoes["total_voluntario_simples"] or 0,
                    "total_voluntarios": (agregacoes["total_voluntario_extra"] or 0)
                    + (agregacoes["total_voluntario_simples"] or 0),
                    "carencias": agregacoes["total_carencias"] or 0,
                    "alunos": agregacoes["alunos_distintos"] or 0,
                    "atividades": agregacoes["atividades_distintas"] or 0,
                },
                "percentuais": {
                    "presenca_media": float(percentual_medio),
                    "faltas_media": float(
                        round(
                            (
                                Decimal(agregacoes["total_faltas"] or 0)
                                / Decimal(agregacoes["total_convocacoes"] or 1)
                            )
                            * Decimal("100"),
                            2,
                        )
                    ),
                },
                "por_atividade": estatisticas_atividades,
                "por_aluno": estatisticas_alunos,
                "distribuicao_carencias": distribuicao_carencias,
                "data_calculo": timezone.now(),
            }

            logger.info(
                f"Estatísticas da turma {turma_id}: {agregacoes['alunos_distintos']} alunos, "
                f"{percentual_medio}% presença média"
            )

            return estatisticas

        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas da turma {turma_id}: {str(e)}")
            raise ValidationError(f"Erro no cálculo das estatísticas: {str(e)}")

    @staticmethod
    def _criar_vazio(turma_id: int) -> Dict[str, Any]:
        """
        Cria um dicionário de estatísticas vazio para turma sem registros.

        Args:
            turma_id: ID da turma

        Returns:
            Dict com valores zerados
        """
        return {
            "turma": {"id": turma_id, "nome": "Sem registros", "perc_presenca_minima": None},
            "periodo": {"inicio": None, "fim": None},
            "totais": {
                "convocacoes": 0,
                "presencas": 0,
                "faltas": 0,
                "voluntario_extra": 0,
                "voluntario_simples": 0,
                "total_voluntarios": 0,
                "carencias": 0,
                "alunos": 0,
                "atividades": 0,
            },
            "percentuais": {"presenca_media": 0.0, "faltas_media": 0.0},
            "por_atividade": [],
            "por_aluno": [],
            "distribuicao_carencias": {},
            "data_calculo": timezone.now(),
        }

    @staticmethod
    def _calcular_por_atividade(presencas_queryset) -> List[Dict[str, Any]]:
        """
        Calcula estatísticas agrupadas por atividade.

        Args:
            presencas_queryset: QuerySet de PresencaDetalhada

        Returns:
            Lista de dicts com estatísticas por atividade
        """
        atividades = {}

        for presenca in presencas_queryset:
            atividade_id = presenca.atividade.id

            if atividade_id not in atividades:
                atividades[atividade_id] = {
                    "id": atividade_id,
                    "nome": presenca.atividade.nome,
                    "convocacoes": 0,
                    "presencas": 0,
                    "faltas": 0,
                    "voluntario_extra": 0,
                    "voluntario_simples": 0,
                    "carencias": 0,
                    "alunos": set(),
                }

            atividade = atividades[atividade_id]
            atividade["convocacoes"] += presenca.convocacoes
            atividade["presencas"] += presenca.presencas
            atividade["faltas"] += presenca.faltas
            atividade["voluntario_extra"] += presenca.voluntario_extra
            atividade["voluntario_simples"] += presenca.voluntario_simples
            atividade["carencias"] += presenca.carencias
            atividade["alunos"].add(presenca.aluno.id)

        # Calcular percentuais e finalizar
        resultado = []
        for atividade_data in atividades.values():
            percentual = Decimal("0.00")
            if atividade_data["convocacoes"] > 0:
                percentual = round(
                    (
                        Decimal(atividade_data["presencas"])
                        / Decimal(atividade_data["convocacoes"])
                    )
                    * Decimal("100"),
                    2,
                )

            resultado.append(
                {
                    "id": atividade_data["id"],
                    "nome": atividade_data["nome"],
                    "convocacoes": atividade_data["convocacoes"],
                    "presencas": atividade_data["presencas"],
                    "faltas": atividade_data["faltas"],
                    "voluntario_extra": atividade_data["voluntario_extra"],
                    "voluntario_simples": atividade_data["voluntario_simples"],
                    "carencias": atividade_data["carencias"],
                    "total_alunos": len(atividade_data["alunos"]),
                    "percentual_presenca": float(percentual),
                }
            )

        # Ordenar por data (ID da atividade como proxy)
        return sorted(resultado, key=lambda x: x["id"])

    @staticmethod
    def _calcular_por_aluno(presencas_queryset) -> List[Dict[str, Any]]:
        """
        Calcula estatísticas agrupadas por aluno.

        Args:
            presencas_queryset: QuerySet de PresencaDetalhada

        Returns:
            Lista de dicts com estatísticas por aluno
        """
        alunos = {}

        for presenca in presencas_queryset:
            aluno_id = presenca.aluno.id

            if aluno_id not in alunos:
                alunos[aluno_id] = {
                    "id": aluno_id,
                    "nome": presenca.aluno.nome,
                    "convocacoes": 0,
                    "presencas": 0,
                    "faltas": 0,
                    "voluntario_extra": 0,
                    "voluntario_simples": 0,
                    "carencias": 0,
                }

            aluno = alunos[aluno_id]
            aluno["convocacoes"] += presenca.convocacoes
            aluno["presencas"] += presenca.presencas
            aluno["faltas"] += presenca.faltas
            aluno["voluntario_extra"] += presenca.voluntario_extra
            aluno["voluntario_simples"] += presenca.voluntario_simples
            aluno["carencias"] += presenca.carencias

        # Calcular percentuais e finalizar
        resultado = []
        for aluno_data in alunos.values():
            percentual = Decimal("0.00")
            if aluno_data["convocacoes"] > 0:
                percentual = round(
                    (
                        Decimal(aluno_data["presencas"])
                        / Decimal(aluno_data["convocacoes"])
                    )
                    * Decimal("100"),
                    2,
                )

            resultado.append(
                {
                    "id": aluno_data["id"],
                    "nome": aluno_data["nome"],
                    "convocacoes": aluno_data["convocacoes"],
                    "presencas": aluno_data["presencas"],
                    "faltas": aluno_data["faltas"],
                    "voluntario_extra": aluno_data["voluntario_extra"],
                    "voluntario_simples": aluno_data["voluntario_simples"],
                    "carencias": aluno_data["carencias"],
                    "percentual_presenca": float(percentual),
                }
            )

        # Ordenar por nome
        return sorted(resultado, key=lambda x: x["nome"])

    @staticmethod
    def _calcular_distribuicao_carencias(presencas_queryset) -> Dict[str, int]:
        """
        Calcula distribuição de alunos por faixa de carências.

        Args:
            presencas_queryset: QuerySet de PresencaDetalhada

        Returns:
            Dict com contagem por faixa: sem_carencias, ate_3, ate_6, mais_de_6
        """
        # Agregar carências por aluno
        carencias_por_aluno = {}
        for presenca in presencas_queryset:
            aluno_id = presenca.aluno.id
            if aluno_id not in carencias_por_aluno:
                carencias_por_aluno[aluno_id] = 0
            carencias_por_aluno[aluno_id] += presenca.carencias

        # Distribuir em faixas
        distribuicao = {
            "sem_carencias": 0,
            "ate_3": 0,
            "ate_6": 0,
            "mais_de_6": 0,
        }

        for carencias in carencias_por_aluno.values():
            if carencias == 0:
                distribuicao["sem_carencias"] += 1
            elif carencias <= 3:
                distribuicao["ate_3"] += 1
            elif carencias <= 6:
                distribuicao["ate_6"] += 1
            else:
                distribuicao["mais_de_6"] += 1

        return distribuicao
