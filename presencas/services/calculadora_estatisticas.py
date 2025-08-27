"""
Serviço de cálculos estatísticos para o sistema de presenças.
Replica a funcionalidade das planilhas Excel com lógica de negócios otimizada.
"""

import logging
from decimal import Decimal
from datetime import date
from typing import Dict, List, Optional, Any
from django.db.models import Sum, Count
from django.core.exceptions import ValidationError
from django.utils import timezone

from ..models import PresencaDetalhada, ConfiguracaoPresenca

logger = logging.getLogger(__name__)


class CalculadoraEstatisticas:
    @staticmethod
    def calcular_totais_consolidado(presencas):
        """Exemplo de implementação: retorna um dicionário vazio se não houver presenças."""
        if not presencas:
            return {}
        # Adapte conforme a lógica real
        return {"total": len(presencas)}

    """
    Calculadora de estatísticas de presença que replica funcionalidade Excel.
    
    Principais responsabilidades:
    - Calcular estatísticas consolidadas por aluno
    - Gerar tabelas consolidadas (replicando Excel)
    - Calcular carências e percentuais
    - Otimizar queries para performance
    """

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

        Args:
            aluno_id: ID do aluno
            turma_id: ID da turma (opcional)
            atividade_id: ID da atividade (opcional)
            periodo_inicio: Data início do período (opcional)
            periodo_fim: Data fim do período (opcional)

        Returns:
            Dict com estatísticas consolidadas do aluno
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
                return CalculadoraEstatisticas._criar_consolidado_vazio(aluno_id)

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
            percentual_presenca = Decimal("0.00")
            if total_convocacoes > 0:
                percentual_presenca = round(
                    (Decimal(total_presencas) / Decimal(total_convocacoes))
                    * Decimal("100"),
                    2,
                )

            # Obter dados do aluno
            aluno_info = None
            if presencas.exists():
                primeira_presenca = presencas.first()
                aluno_info = {
                    "id": primeira_presenca.aluno.id,
                    "nome": primeira_presenca.aluno.nome,
                    "cpf": primeira_presenca.aluno.cpf,
                }

            # Estatísticas por atividade
            estatisticas_atividades = CalculadoraEstatisticas._calcular_por_atividade(
                presencas
            )

            # Status geral
            status = CalculadoraEstatisticas._determinar_status_aluno(
                percentual_presenca, total_carencias
            )

            consolidado = {
                "aluno": aluno_info,
                "periodo": {"inicio": periodo_inicio, "fim": periodo_fim},
                "totais": {
                    "convocacoes": total_convocacoes,
                    "presencas": total_presencas,
                    "faltas": total_faltas,
                    "voluntario_extra": agregacoes["total_voluntario_extra"] or 0,
                    "voluntario_simples": agregacoes["total_voluntario_simples"] or 0,
                    "total_voluntarios": total_voluntarios,
                    "carencias": total_carencias,
                    "registros": agregacoes["total_registros"],
                },
                "percentuais": {
                    "presenca": float(percentual_presenca),
                    "faltas": float(
                        round(
                            (Decimal(total_faltas) / Decimal(total_convocacoes))
                            * Decimal("100"),
                            2,
                        )
                        if total_convocacoes > 0
                        else Decimal("0.00")
                    ),
                },
                "status": status,
                "atividades": estatisticas_atividades,
                "data_calculo": timezone.now(),
            }

            logger.info(
                f"Consolidado calculado para aluno {aluno_id}: "
                f"{percentual_presenca}% presença, {total_carencias} carências"
            )

            return consolidado

        except Exception as e:
            logger.error(f"Erro ao calcular consolidado do aluno {aluno_id}: {str(e)}")
            raise ValidationError(f"Erro no cálculo consolidado: {str(e)}")

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

        Args:
            turma_id: ID da turma (opcional)
            atividade_id: ID da atividade (opcional)
            periodo_inicio: Data início do período (opcional)
            periodo_fim: Data fim do período (opcional)
            ordenar_por: Campo para ordenação ('nome', 'percentual', 'carencias')

        Returns:
            Dict com tabela consolidada e estatísticas gerais
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
                return CalculadoraEstatisticas._criar_tabela_vazia()

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
                status = CalculadoraEstatisticas._determinar_status_aluno(
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
            linhas_tabela = CalculadoraEstatisticas._ordenar_tabela(
                linhas_tabela, ordenar_por
            )

            # Estatísticas gerais
            estatisticas_gerais = CalculadoraEstatisticas._calcular_estatisticas_gerais(
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
    def calcular_estatisticas_turma(
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
            Dict com estatísticas da turma
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
                return CalculadoraEstatisticas._criar_estatisticas_turma_vazia(turma_id)

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
            estatisticas_atividades = CalculadoraEstatisticas._calcular_por_atividade(
                presencas
            )

            # Estatísticas por aluno
            estatisticas_alunos = CalculadoraEstatisticas._calcular_por_aluno(presencas)

            # Distribuição de carências
            distribuicao_carencias = (
                CalculadoraEstatisticas._calcular_distribuicao_carencias(presencas)
            )

            # Informações da turma
            turma_info = None
            if presencas.exists():
                primeira_presenca = presencas.first()
                turma_info = {
                    "id": primeira_presenca.turma.id,
                    "nome": primeira_presenca.turma.nome,
                    "perc_carencia": getattr(
                        primeira_presenca.turma, "perc_carencia", None
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
    def calcular_carencias(
        presenca_detalhada_id: int, forcar_recalculo: bool = False
    ) -> Dict[str, Any]:
        """
        Calcula carências para uma presença detalhada específica.

        Args:
            presenca_detalhada_id: ID da presença detalhada
            forcar_recalculo: Se True, força recálculo mesmo que já calculado

        Returns:
            Dict com informações das carências calculadas
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
                if (
                    hasattr(presenca.turma, "perc_carencia")
                    and presenca.turma.perc_carencia
                ):
                    percentual_atual = presenca.calcular_percentual()
                    percentual_minimo = presenca.turma.perc_carencia

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
    def recalcular_todas_carencias(
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
            Dict com resultado do recálculo
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
                    resultado = CalculadoraEstatisticas.calcular_carencias(
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

    # Métodos auxiliares privados

    @staticmethod
    def _criar_consolidado_vazio(aluno_id: int) -> Dict[str, Any]:
        """Cria consolidado vazio para aluno sem dados."""
        return {
            "aluno": {"id": aluno_id, "nome": None, "cpf": None},
            "periodo": {"inicio": None, "fim": None},
            "totais": {
                "convocacoes": 0,
                "presencas": 0,
                "faltas": 0,
                "voluntario_extra": 0,
                "voluntario_simples": 0,
                "total_voluntarios": 0,
                "carencias": 0,
                "registros": 0,
            },
            "percentuais": {"presenca": 0.0, "faltas": 0.0},
            "status": "sem_dados",
            "atividades": [],
            "data_calculo": timezone.now(),
        }

    @staticmethod
    def _criar_tabela_vazia() -> Dict[str, Any]:
        """Cria tabela consolidada vazia."""
        return {
            "linhas": [],
            "estatisticas_gerais": {
                "total_alunos": 0,
                "percentual_medio": 0.0,
                "total_convocacoes": 0,
                "total_presencas": 0,
                "total_carencias": 0,
            },
            "filtros_aplicados": {},
            "total_alunos": 0,
            "data_geracao": timezone.now(),
        }

    @staticmethod
    def _criar_estatisticas_turma_vazia(turma_id: int) -> Dict[str, Any]:
        """Cria estatísticas vazias para turma."""
        return {
            "turma": {"id": turma_id, "nome": None, "perc_carencia": None},
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
        """Calcula estatísticas agrupadas por atividade."""
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

            atividade_data["percentual"] = float(percentual)
            atividade_data["total_voluntarios"] = (
                atividade_data["voluntario_extra"]
                + atividade_data["voluntario_simples"]
            )
            atividade_data["total_alunos"] = len(atividade_data["alunos"])
            del atividade_data["alunos"]  # Remove set para serialização

            resultado.append(atividade_data)

        return sorted(resultado, key=lambda x: x["nome"])

    @staticmethod
    def _calcular_por_aluno(presencas_queryset) -> List[Dict[str, Any]]:
        """Calcula estatísticas agrupadas por aluno."""
        alunos = {}

        for presenca in presencas_queryset:
            aluno_id = presenca.aluno.id

            if aluno_id not in alunos:
                alunos[aluno_id] = {
                    "id": aluno_id,
                    "nome": presenca.aluno.nome,
                    "cpf": presenca.aluno.cpf,
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

            aluno_data["percentual"] = float(percentual)
            aluno_data["total_voluntarios"] = (
                aluno_data["voluntario_extra"] + aluno_data["voluntario_simples"]
            )
            aluno_data["status"] = CalculadoraEstatisticas._determinar_status_aluno(
                percentual, aluno_data["carencias"]
            )

            resultado.append(aluno_data)

        return sorted(resultado, key=lambda x: x["nome"])

    @staticmethod
    def _calcular_distribuicao_carencias(presencas_queryset) -> Dict[str, int]:
        """Calcula distribuição de carências."""
        distribuicao = {
            "sem_carencia": 0,
            "1_a_2_carencias": 0,
            "3_a_5_carencias": 0,
            "mais_de_5_carencias": 0,
        }

        alunos_carencias = {}
        for presenca in presencas_queryset:
            aluno_id = presenca.aluno.id
            if aluno_id not in alunos_carencias:
                alunos_carencias[aluno_id] = 0
            alunos_carencias[aluno_id] += presenca.carencias

        for total_carencias in alunos_carencias.values():
            if total_carencias == 0:
                distribuicao["sem_carencia"] += 1
            elif total_carencias <= 2:
                distribuicao["1_a_2_carencias"] += 1
            elif total_carencias <= 5:
                distribuicao["3_a_5_carencias"] += 1
            else:
                distribuicao["mais_de_5_carencias"] += 1

        return distribuicao

    @staticmethod
    def _determinar_status_aluno(percentual: Decimal, carencias: int) -> str:
        """Determina o status do aluno baseado em percentual e carências."""
        if percentual >= 90 and carencias == 0:
            return "excelente"
        elif percentual >= 80 and carencias <= 2:
            return "bom"
        elif percentual >= 70 and carencias <= 5:
            return "regular"
        elif percentual >= 60:
            return "atencao"
        else:
            return "critico"

    @staticmethod
    def _ordenar_tabela(linhas: List[Dict], ordenar_por: str) -> List[Dict]:
        """Ordena tabela por campo especificado."""
        if ordenar_por == "percentual":
            return sorted(linhas, key=lambda x: x["percentual_geral"], reverse=True)
        elif ordenar_por == "carencias":
            return sorted(linhas, key=lambda x: x["totais"]["carencias"])
        else:  # ordenar_por == 'nome'
            return sorted(linhas, key=lambda x: x["aluno"]["nome"])

    @staticmethod
    def _calcular_estatisticas_gerais(linhas: List[Dict]) -> Dict[str, Any]:
        """Calcula estatísticas gerais da tabela."""
        if not linhas:
            return {
                "total_alunos": 0,
                "percentual_medio": 0.0,
                "total_convocacoes": 0,
                "total_presencas": 0,
                "total_carencias": 0,
            }

        total_alunos = len(linhas)
        total_convocacoes = sum(linha["totais"]["convocacoes"] for linha in linhas)
        total_presencas = sum(linha["totais"]["presencas"] for linha in linhas)
        total_carencias = sum(linha["totais"]["carencias"] for linha in linhas)

        percentual_medio = 0.0
        if total_convocacoes > 0:
            percentual_medio = round((total_presencas / total_convocacoes) * 100, 2)

        return {
            "total_alunos": total_alunos,
            "percentual_medio": percentual_medio,
            "total_convocacoes": total_convocacoes,
            "total_presencas": total_presencas,
            "total_carencias": total_carencias,
        }
