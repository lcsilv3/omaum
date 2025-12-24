"""
Serviço de cálculo e recálculo de carências.
Extraído de calculadora_estatisticas.py para melhor organização.
"""

import logging
from datetime import date
from typing import Dict, Any, Optional

from django.core.exceptions import ValidationError
from django.utils import timezone

from ..models import PresencaDetalhada, ConfiguracaoPresenca

logger = logging.getLogger(__name__)


class CalculadoraCarencias:
    """
    Calculadora de carências para o sistema de presenças.
    
    Responsabilidades:
    - Calcular carências por presença detalhada
    - Recalcular carências em lote
    - Aplicar regras de configuração específica ou turma
    """

    @staticmethod
    def calcular(
        presenca_detalhada_id: int, forcar_recalculo: bool = False
    ) -> Dict[str, Any]:
        """
        Calcula carências para uma presença detalhada específica.

        Args:
            presenca_detalhada_id: ID da presença detalhada
            forcar_recalculo: Se True, força recálculo mesmo que já calculado

        Returns:
            Dict com informações das carências calculadas:
            - presenca_id: ID da presença
            - carencias_antigas: Valor anterior (se existir)
            - carencias_novas: Valor calculado
            - diferenca: Diferença entre novo e antigo
            - metodo_calculo: Método usado (configuracao_especifica/percentual_turma/sem_configuracao)
            - configuracao_usada: ID da configuração (se aplicável)
            - percentual_presenca: Percentual atual
            - recalculado: Se foi recalculado
            - data_calculo: Timestamp
        """
        try:
            presenca = PresencaDetalhada.objects.select_related(
                "aluno", "turma", "atividade"
            ).get(id=presenca_detalhada_id)

            # Verificar se precisa recalcular
            if (
                not forcar_recalculo
                and hasattr(presenca, "carencias")
                and presenca.carencias is not None
            ):
                logger.info(
                    f"Carência já calculada para presença {presenca_detalhada_id}"
                )
                return {
                    "presenca_id": presenca_detalhada_id,
                    "carencias_atuais": presenca.carencias,
                    "recalculado": False,
                    "data_calculo": presenca.data_atualizacao,
                }

            # Buscar configuração
            configuracao = None
            try:
                configuracao = ConfiguracaoPresenca.objects.get(
                    turma=presenca.turma, atividade=presenca.atividade, ativo=True
                )
            except ConfiguracaoPresenca.DoesNotExist:
                logger.warning(
                    f"Configuração não encontrada para turma {presenca.turma.id} "
                    f"e atividade {presenca.atividade.id}"
                )

            # Calcular carências
            carencias_antigas = presenca.carencias

            if configuracao:
                # Usar configuração específica
                percentual_atual = presenca.calcular_percentual()
                limite_carencia = configuracao.get_limite_carencia_por_percentual(
                    percentual_atual
                )

                # Aplicar peso
                carencia_permitida = int(
                    limite_carencia * float(configuracao.peso_calculo)
                )

                # Calcular carências necessárias
                if presenca.convocacoes > 0:
                    presencas_necessarias = presenca.convocacoes - carencia_permitida
                    carencias_calculadas = max(
                        0, presencas_necessarias - presenca.presencas
                    )
                else:
                    carencias_calculadas = 0

                metodo_calculo = "configuracao_especifica"
            else:
                # Usar lógica padrão da turma
                percentual_turma = getattr(
                    presenca.turma,
                    "perc_presenca_minima",
                    getattr(presenca.turma, "perc_carencia", None),
                )

                if percentual_turma:
                    percentual_atual = presenca.calcular_percentual()
                    percentual_minimo = percentual_turma

                    if percentual_atual < percentual_minimo:
                        presencas_necessarias = (
                            percentual_minimo * presenca.convocacoes
                        ) / 100
                        carencias_calculadas = int(
                            presencas_necessarias - presenca.presencas
                        )
                        carencias_calculadas = max(0, carencias_calculadas)
                    else:
                        carencias_calculadas = 0

                    metodo_calculo = "percentual_turma"
                else:
                    carencias_calculadas = 0
                    metodo_calculo = "sem_configuracao"

            # Atualizar presença
            presenca.carencias = carencias_calculadas
            presenca.save()

            resultado = {
                "presenca_id": presenca_detalhada_id,
                "carencias_antigas": carencias_antigas,
                "carencias_novas": carencias_calculadas,
                "diferenca": carencias_calculadas - (carencias_antigas or 0),
                "metodo_calculo": metodo_calculo,
                "configuracao_usada": configuracao.id if configuracao else None,
                "percentual_presenca": float(presenca.percentual_presenca),
                "recalculado": True,
                "data_calculo": timezone.now(),
            }

            logger.info(
                f"Carências calculadas para presença {presenca_detalhada_id}: "
                f"{carencias_antigas} -> {carencias_calculadas}"
            )

            return resultado

        except PresencaDetalhada.DoesNotExist:
            logger.error(f"Presença detalhada {presenca_detalhada_id} não encontrada")
            raise ValidationError("Presença detalhada não encontrada")
        except Exception as e:
            logger.error(
                f"Erro ao calcular carências para presença {presenca_detalhada_id}: {str(e)}"
            )
            raise ValidationError(f"Erro no cálculo de carências: {str(e)}")

    @staticmethod
    def recalcular_todas(
        turma_id: Optional[int] = None,
        atividade_id: Optional[int] = None,
        periodo_inicio: Optional[date] = None,
        periodo_fim: Optional[date] = None,
    ) -> Dict[str, Any]:
        """
        Recalcula todas as carências para um conjunto de presenças.

        Args:
            turma_id: ID da turma (opcional)
            atividade_id: ID da atividade (opcional)
            periodo_inicio: Data início (opcional)
            periodo_fim: Data fim (opcional)

        Returns:
            Dict com resultado do recálculo:
            - total_presencas: Total de presenças processadas
            - presencas_atualizadas: Total atualizado com sucesso
            - erros: Lista de erros encontrados
            - total_erros: Quantidade de erros
            - filtros_aplicados: Filtros usados
            - data_recalculo: Timestamp
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

            # Buscar presenças
            presencas = PresencaDetalhada.objects.filter(**filtros).select_related(
                "aluno", "turma", "atividade"
            )

            total_presencas = presencas.count()
            presencas_atualizadas = 0
            erros = []

            logger.info(f"Iniciando recálculo de {total_presencas} presenças")

            for presenca in presencas:
                try:
                    resultado = CalculadoraCarencias.calcular(
                        presenca.id, forcar_recalculo=True
                    )
                    if resultado["recalculado"]:
                        presencas_atualizadas += 1
                except Exception as e:
                    erros.append({"presenca_id": presenca.id, "erro": str(e)})

            resultado = {
                "total_presencas": total_presencas,
                "presencas_atualizadas": presencas_atualizadas,
                "erros": erros,
                "total_erros": len(erros),
                "filtros_aplicados": filtros,
                "data_recalculo": timezone.now(),
            }

            logger.info(
                f"Recálculo concluído: {presencas_atualizadas}/{total_presencas} atualizadas, "
                f"{len(erros)} erros"
            )

            return resultado

        except Exception as e:
            logger.error(f"Erro no recálculo geral de carências: {str(e)}")
            raise ValidationError(f"Erro no recálculo: {str(e)}")
