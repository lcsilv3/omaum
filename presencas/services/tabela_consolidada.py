"""
Serviço de geração de tabelas consolidadas.
Extraído de calculadora_estatisticas.py para melhor organização.
"""

import logging
from decimal import Decimal
from datetime import date
from typing import Dict, Any, List, Optional

from django.core.exceptions import ValidationError
from django.utils import timezone

from ..models import PresencaDetalhada

logger = logging.getLogger(__name__)


class TabelaConsolidada:
    """
    Gerador de tabelas consolidadas replicando funcionalidade Excel.
    
    Responsabilidades:
    - Gerar tabela consolidada por aluno/turma/atividade/período
    - Calcular percentuais e estatísticas gerais
    - Ordenar e formatar dados
    """

    @staticmethod
    def gerar(
        turma_id: Optional[int] = None,
        atividade_id: Optional[int] = None,
        periodo_inicio: Optional[date] = None,
        periodo_fim: Optional[date] = None,
        ordenar_por: str = "nome",
    ) -> Dict[str, Any]:
        """
        Gera tabela consolidada completa (replicando Excel).

        Args:
            turma_id: ID da turma (opcional)
            atividade_id: ID da atividade (opcional)
            periodo_inicio: Data início do período (opcional)
            periodo_fim: Data fim do período (opcional)
            ordenar_por: Campo para ordenação ('nome', 'percentual', 'carencias')

        Returns:
            Dict com tabela consolidada:
            - linhas: Lista de dicts com dados por aluno
            - estatisticas_gerais: Médias e totais gerais
            - filtros_aplicados: Filtros usados
            - total_alunos: Quantidade de alunos
            - data_geracao: Timestamp
        """
        try:
            # Filtros
            filtros = {}
            if turma_id:
                filtros["turma_id"] = turma_id
            if atividade_id:
                filtros["atividade_id"] = atividade_id
            if periodo_inicio:
                filtros["periodo__gte"] = periodo_inicio
            if periodo_fim:
                filtros["periodo__lte"] = periodo_fim

            # Query otimizada
            presencas = (
                PresencaDetalhada.objects.filter(**filtros)
                .select_related("aluno", "turma", "atividade")
                .prefetch_related("turma__configuracoes_presenca")
            )

            if not presencas.exists():
                return TabelaConsolidada._criar_vazia()

            # Agrupar por aluno
            dados_por_aluno = {}
            for presenca in presencas:
                aluno_id = presenca.aluno.id

                if aluno_id not in dados_por_aluno:
                    dados_por_aluno[aluno_id] = {
                        "aluno": {
                            "id": presenca.aluno.id,
                            "nome": presenca.aluno.nome,
                            "cpf": presenca.aluno.cpf,
                        },
                        "turma": {
                            "id": presenca.turma.id,
                            "nome": presenca.turma.nome,
                        }
                        if presenca.turma
                        else None,
                        "totais": {
                            "convocacoes": 0,
                            "presencas": 0,
                            "faltas": 0,
                            "voluntario_extra": 0,
                            "voluntario_simples": 0,
                            "carencias": 0,
                        },
                        "atividades": {},
                    }

                # Somar totais
                dados_por_aluno[aluno_id]["totais"]["convocacoes"] += (
                    presenca.convocacoes
                )
                dados_por_aluno[aluno_id]["totais"]["presencas"] += presenca.presencas
                dados_por_aluno[aluno_id]["totais"]["faltas"] += presenca.faltas
                dados_por_aluno[aluno_id]["totais"]["voluntario_extra"] += (
                    presenca.voluntario_extra
                )
                dados_por_aluno[aluno_id]["totais"]["voluntario_simples"] += (
                    presenca.voluntario_simples
                )
                dados_por_aluno[aluno_id]["totais"]["carencias"] += presenca.carencias

                # Detalhar por atividade
                atividade_key = f"{presenca.atividade.id}_{presenca.atividade.nome}"
                if atividade_key not in dados_por_aluno[aluno_id]["atividades"]:
                    dados_por_aluno[aluno_id]["atividades"][atividade_key] = {
                        "id": presenca.atividade.id,
                        "nome": presenca.atividade.nome,
                        "convocacoes": 0,
                        "presencas": 0,
                        "faltas": 0,
                        "voluntario_extra": 0,
                        "voluntario_simples": 0,
                        "carencias": 0,
                        "percentual": Decimal("0.00"),
                    }

                atividade_data = dados_por_aluno[aluno_id]["atividades"][atividade_key]
                atividade_data["convocacoes"] += presenca.convocacoes
                atividade_data["presencas"] += presenca.presencas
                atividade_data["faltas"] += presenca.faltas
                atividade_data["voluntario_extra"] += presenca.voluntario_extra
                atividade_data["voluntario_simples"] += presenca.voluntario_simples
                atividade_data["carencias"] += presenca.carencias

            # Calcular percentuais e processar dados
            linhas_tabela = []
            for aluno_id, dados in dados_por_aluno.items():
                totais = dados["totais"]

                # Calcular percentual geral
                percentual_geral = Decimal("0.00")
                if totais["convocacoes"] > 0:
                    percentual_geral = round(
                        (Decimal(totais["presencas"]) / Decimal(totais["convocacoes"]))
                        * Decimal("100"),
                        2,
                    )

                # Calcular percentuais por atividade
                for atividade_key, atividade_data in dados["atividades"].items():
                    if atividade_data["convocacoes"] > 0:
                        atividade_data["percentual"] = round(
                            (
                                Decimal(atividade_data["presencas"])
                                / Decimal(atividade_data["convocacoes"])
                            )
                            * Decimal("100"),
                            2,
                        )

                # Determinar status
                status = TabelaConsolidada._determinar_status_aluno(
                    percentual_geral, totais["carencias"]
                )

                linha = {
                    "aluno": dados["aluno"],
                    "turma": dados["turma"],
                    "totais": totais,
                    "percentual_geral": float(percentual_geral),
                    "total_voluntarios": totais["voluntario_extra"]
                    + totais["voluntario_simples"],
                    "status": status,
                    "atividades": list(dados["atividades"].values()),
                }

                linhas_tabela.append(linha)

            # Ordenar
            linhas_tabela = TabelaConsolidada._ordenar_tabela(
                linhas_tabela, ordenar_por
            )

            # Estatísticas gerais
            estatisticas_gerais = TabelaConsolidada._calcular_estatisticas_gerais(
                linhas_tabela
            )

            tabela_consolidada = {
                "linhas": linhas_tabela,
                "estatisticas_gerais": estatisticas_gerais,
                "filtros_aplicados": {
                    "turma_id": turma_id,
                    "atividade_id": atividade_id,
                    "periodo_inicio": periodo_inicio,
                    "periodo_fim": periodo_fim,
                    "ordenar_por": ordenar_por,
                },
                "total_alunos": len(linhas_tabela),
                "data_geracao": timezone.now(),
            }

            logger.info(
                f"Tabela consolidada gerada: {len(linhas_tabela)} alunos, "
                f"turma_id={turma_id}, atividade_id={atividade_id}"
            )

            return tabela_consolidada

        except Exception as e:
            logger.error(f"Erro ao gerar tabela consolidada: {str(e)}")
            raise ValidationError(f"Erro na geração da tabela: {str(e)}")

    @staticmethod
    def _criar_vazia() -> Dict[str, Any]:
        """
        Cria uma tabela consolidada vazia.

        Returns:
            Dict com estrutura vazia
        """
        return {
            "linhas": [],
            "estatisticas_gerais": {
                "total_alunos": 0,
                "percentual_medio": 0.0,
                "total_presencas": 0,
                "total_faltas": 0,
                "total_carencias": 0,
                "alunos_ok": 0,
                "alunos_carentes": 0,
                "alunos_reprovados": 0,
            },
            "filtros_aplicados": {},
            "total_alunos": 0,
            "data_geracao": timezone.now(),
        }

    @staticmethod
    def _determinar_status_aluno(percentual: Decimal, carencias: int) -> str:
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

    @staticmethod
    def _ordenar_tabela(linhas: List[Dict], ordenar_por: str) -> List[Dict]:
        """
        Ordena linhas da tabela pelo critério especificado.

        Args:
            linhas: Lista de linhas da tabela
            ordenar_por: Critério de ordenação ('nome', 'percentual', 'carencias')

        Returns:
            Lista ordenada
        """
        if ordenar_por == "percentual":
            return sorted(linhas, key=lambda x: x["percentual_geral"], reverse=True)
        elif ordenar_por == "carencias":
            return sorted(linhas, key=lambda x: x["totais"]["carencias"], reverse=True)
        else:  # nome (padrão)
            return sorted(linhas, key=lambda x: x["aluno"]["nome"])

    @staticmethod
    def _calcular_estatisticas_gerais(linhas: List[Dict]) -> Dict[str, Any]:
        """
        Calcula estatísticas gerais da tabela.

        Args:
            linhas: Lista de linhas da tabela

        Returns:
            Dict com estatísticas gerais
        """
        if not linhas:
            return {
                "total_alunos": 0,
                "percentual_medio": 0.0,
                "total_presencas": 0,
                "total_faltas": 0,
                "total_carencias": 0,
                "alunos_ok": 0,
                "alunos_carentes": 0,
                "alunos_reprovados": 0,
            }

        total_alunos = len(linhas)
        soma_percentual = sum(linha["percentual_geral"] for linha in linhas)
        percentual_medio = soma_percentual / total_alunos if total_alunos > 0 else 0.0

        total_presencas = sum(linha["totais"]["presencas"] for linha in linhas)
        total_faltas = sum(linha["totais"]["faltas"] for linha in linhas)
        total_carencias = sum(linha["totais"]["carencias"] for linha in linhas)

        # Contadores por status
        alunos_ok = sum(1 for linha in linhas if linha["status"] == "OK")
        alunos_carentes = sum(1 for linha in linhas if linha["status"] == "CARENTE")
        alunos_reprovados = sum(1 for linha in linhas if linha["status"] == "REPROVADO")

        return {
            "total_alunos": total_alunos,
            "percentual_medio": round(percentual_medio, 2),
            "total_presencas": total_presencas,
            "total_faltas": total_faltas,
            "total_carencias": total_carencias,
            "alunos_ok": alunos_ok,
            "alunos_carentes": alunos_carentes,
            "alunos_reprovados": alunos_reprovados,
        }
