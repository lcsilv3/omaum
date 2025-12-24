"""
Serviço de cálculos estatísticos para o sistema de presenças.
Replica a funcionalidade das planilhas Excel com lógica de negócios otimizada.

Este módulo atua como facade para os serviços especializados:
- consolidado_aluno: Estatísticas por aluno
- consolidado_turma: Estatísticas por turma
- carencias: Cálculo e recálculo de carências
- tabela_consolidada: Geração de tabelas consolidadas

Mantém API pública para retrocompatibilidade.
"""

import logging
from decimal import Decimal
from datetime import date
from typing import Dict, List, Optional, Any

# Importar serviços especializados
from .consolidado_aluno import ConsolidadoAluno
from .consolidado_turma import ConsolidadoTurma
from .carencias import CalculadoraCarencias
from .tabela_consolidada import TabelaConsolidada

logger = logging.getLogger(__name__)


class CalculadoraEstatisticas:
    """
    Calculadora de estatísticas de presença (Facade Pattern).
    
    Principais responsabilidades:
    - Delegar cálculos para serviços especializados
    - Manter API pública retrocompatível
    - Fornecer ponto único de acesso aos cálculos
    
    Módulos especializados:
    - ConsolidadoAluno: Estatísticas por aluno individual
    - ConsolidadoTurma: Estatísticas agregadas por turma
    - CalculadoraCarencias: Cálculo e recálculo de carências
    - TabelaConsolidada: Geração de tabelas tipo Excel
    """

    # ========== Métodos Públicos (Facade) ==========

    @staticmethod
    def calcular_totais_consolidado(presencas):
        """
        Exemplo de implementação: retorna um dicionário vazio se não houver presenças.
        
        Args:
            presencas: Lista ou queryset de presenças
            
        Returns:
            Dict com totais consolidados
        """
        if not presencas:
            return {}
        # Adapte conforme a lógica real
        return {"total": len(presencas)}

    @staticmethod
    def calcular_consolidado_aluno(
        aluno_id: int,
        turma_id: Optional[int] = None,
        atividade_id: Optional[int] = None,
        periodo_inicio: Optional[date] = None,
        periodo_fim: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Calcula dados consolidados de um aluno específico.
        
        Delega para: ConsolidadoAluno.calcular()

        Args:
            aluno_id: ID do aluno
            turma_id: ID da turma (opcional)
            atividade_id: ID da atividade (opcional)
            periodo_inicio: Data início do período (opcional)
            periodo_fim: Data fim do período (opcional)

        Returns:
            Dict com estatísticas consolidadas do aluno
        """
        return ConsolidadoAluno.calcular(
            aluno_id=aluno_id,
            turma_id=turma_id,
            atividade_id=atividade_id,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
        )

    @staticmethod
    def gerar_tabela_consolidada(
        turma_id: Optional[int] = None,
        atividade_id: Optional[int] = None,
        periodo_inicio: Optional[date] = None,
        periodo_fim: Optional[date] = None,
        ordenar_por: str = "nome",
    ) -> Dict[str, Any]:
        """
        Gera tabela consolidada completa (replicando Excel).
        
        Delega para: TabelaConsolidada.gerar()

        Args:
            turma_id: ID da turma (opcional)
            atividade_id: ID da atividade (opcional)
            periodo_inicio: Data início do período (opcional)
            periodo_fim: Data fim do período (opcional)
            ordenar_por: Campo para ordenação ('nome', 'percentual', 'carencias')

        Returns:
            Dict com tabela consolidada e estatísticas gerais
        """
        return TabelaConsolidada.gerar(
            turma_id=turma_id,
            atividade_id=atividade_id,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
            ordenar_por=ordenar_por,
        )

    @staticmethod
    def calcular_estatisticas_turma(
        turma_id: int,
        periodo_inicio: Optional[date] = None,
        periodo_fim: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Calcula estatísticas consolidadas de uma turma.
        
        Delega para: ConsolidadoTurma.calcular()

        Args:
            turma_id: ID da turma
            periodo_inicio: Data início do período (opcional)
            periodo_fim: Data fim do período (opcional)

        Returns:
            Dict com estatísticas da turma
        """
        return ConsolidadoTurma.calcular(
            turma_id=turma_id,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
        )

    @staticmethod
    def calcular_carencias(
        presenca_detalhada_id: int, forcar_recalculo: bool = False
    ) -> Dict[str, Any]:
        """
        Calcula carências para uma presença detalhada específica.
        
        Delega para: CalculadoraCarencias.calcular()

        Args:
            presenca_detalhada_id: ID da presença detalhada
            forcar_recalculo: Se True, força recálculo mesmo que já calculado

        Returns:
            Dict com informações das carências calculadas
        """
        return CalculadoraCarencias.calcular(
            presenca_detalhada_id=presenca_detalhada_id,
            forcar_recalculo=forcar_recalculo,
        )

    @staticmethod
    def recalcular_todas_carencias(
        turma_id: Optional[int] = None,
        atividade_id: Optional[int] = None,
        periodo_inicio: Optional[date] = None,
        periodo_fim: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Recalcula todas as carências para um conjunto de presenças.
        
        Delega para: CalculadoraCarencias.recalcular_todas()

        Args:
            turma_id: ID da turma (opcional)
            atividade_id: ID da atividade (opcional)
            periodo_inicio: Data início (opcional)
            periodo_fim: Data fim (opcional)

        Returns:
            Dict com resultado do recálculo
        """
        return CalculadoraCarencias.recalcular_todas(
            turma_id=turma_id,
            atividade_id=atividade_id,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
        )

    # ========== Métodos Privados (Helpers Legados) ==========
    # Mantidos para retrocompatibilidade, mas delegam para módulos especializados

    @staticmethod
    def _criar_consolidado_vazio(aluno_id: int) -> Dict[str, Any]:
        """
        Cria um dicionário de consolidado vazio para aluno sem registros.
        
        Delega para: ConsolidadoAluno._criar_vazio()
        """
        return ConsolidadoAluno._criar_vazio(aluno_id)

    @staticmethod
    def _criar_tabela_vazia() -> Dict[str, Any]:
        """
        Cria uma tabela consolidada vazia.
        
        Delega para: TabelaConsolidada._criar_vazia()
        """
        return TabelaConsolidada._criar_vazia()

    @staticmethod
    def _criar_estatisticas_turma_vazia(turma_id: int) -> Dict[str, Any]:
        """
        Cria um dicionário de estatísticas vazio para turma sem registros.
        
        Delega para: ConsolidadoTurma._criar_vazio()
        """
        return ConsolidadoTurma._criar_vazio(turma_id)

    @staticmethod
    def _calcular_por_atividade(presencas_queryset) -> List[Dict[str, Any]]:
        """
        Calcula estatísticas agrupadas por atividade.
        
        Delega para: ConsolidadoTurma._calcular_por_atividade()
        """
        return ConsolidadoTurma._calcular_por_atividade(presencas_queryset)

    @staticmethod
    def _calcular_por_aluno(presencas_queryset) -> List[Dict[str, Any]]:
        """
        Calcula estatísticas agrupadas por aluno.
        
        Delega para: ConsolidadoTurma._calcular_por_aluno()
        """
        return ConsolidadoTurma._calcular_por_aluno(presencas_queryset)

    @staticmethod
    def _calcular_distribuicao_carencias(presencas_queryset) -> Dict[str, int]:
        """
        Calcula distribuição de alunos por faixa de carências.
        
        Delega para: ConsolidadoTurma._calcular_distribuicao_carencias()
        """
        return ConsolidadoTurma._calcular_distribuicao_carencias(presencas_queryset)

    @staticmethod
    def _determinar_status_aluno(percentual: Decimal, carencias: int) -> str:
        """
        Determina status do aluno baseado em percentual e carências.
        
        Delega para: TabelaConsolidada._determinar_status_aluno()
        """
        return TabelaConsolidada._determinar_status_aluno(percentual, carencias)

    @staticmethod
    def _ordenar_tabela(linhas: List[Dict], ordenar_por: str) -> List[Dict]:
        """
        Ordena linhas da tabela pelo critério especificado.
        
        Delega para: TabelaConsolidada._ordenar_tabela()
        """
        return TabelaConsolidada._ordenar_tabela(linhas, ordenar_por)

    @staticmethod
    def _calcular_estatisticas_gerais(linhas: List[Dict]) -> Dict[str, Any]:
        """
        Calcula estatísticas gerais da tabela.
        
        Delega para: TabelaConsolidada._calcular_estatisticas_gerais()
        """
        return TabelaConsolidada._calcular_estatisticas_gerais(linhas)
