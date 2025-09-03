"""
FASE 3B: Operações em lote otimizadas para presencas.
Implementa bulk operations para melhor performance.
"""

import logging
from datetime import date
from typing import List, Dict, Any
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Presenca, ObservacaoPresenca
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade

logger = logging.getLogger(__name__)


class BulkPresencaOperations:
    """Classe para operações em lote otimizadas."""

    @staticmethod
    @transaction.atomic
    def criar_presencas_lote(
        dados_presencas: List[Dict[str, Any]], registrado_por: str
    ) -> Dict[str, int]:
        """
        Cria múltiplas presenças em lote com validação otimizada.

        Args:
            dados_presencas: Lista de dicionários com dados das presenças
            registrado_por: Username do usuário que está registrando

        Returns:
            Dict com estatísticas da operação
        """
        logger.info(f"Iniciando criação em lote de {len(dados_presencas)} presenças")

        # Validar estrutura dos dados
        for i, dados in enumerate(dados_presencas):
            required_fields = [
                "aluno_id",
                "turma_id",
                "atividade_id",
                "data",
                "presente",
            ]
            missing_fields = [field for field in required_fields if field not in dados]
            if missing_fields:
                raise ValidationError(
                    f"Item {i}: Campos obrigatórios ausentes: {missing_fields}"
                )

        # Pré-carregar todos os objetos relacionados em uma única query
        aluno_ids = {dados["aluno_id"] for dados in dados_presencas}
        turma_ids = {dados["turma_id"] for dados in dados_presencas}
        atividade_ids = {dados["atividade_id"] for dados in dados_presencas}

        alunos = {a.id: a for a in Aluno.objects.filter(id__in=aluno_ids)}
        turmas = {t.id: t for t in Turma.objects.filter(id__in=turma_ids)}
        atividades = {a.id: a for a in Atividade.objects.filter(id__in=atividade_ids)}

        # Validar que todos os objetos existem
        for dados in dados_presencas:
            if dados["aluno_id"] not in alunos:
                raise ValidationError(f"Aluno ID {dados['aluno_id']} não encontrado")
            if dados["turma_id"] not in turmas:
                raise ValidationError(f"Turma ID {dados['turma_id']} não encontrada")
            if dados["atividade_id"] not in atividades:
                raise ValidationError(
                    f"Atividade ID {dados['atividade_id']} não encontrada"
                )

        # Verificar presenças existentes para evitar duplicatas
        existing_keys = set()
        for dados in dados_presencas:
            key = (
                dados["aluno_id"],
                dados["turma_id"],
                dados["atividade_id"],
                dados["data"],
            )
            existing_keys.add(key)

        existing_presencas = set(
            Presenca.objects.filter(
                aluno_id__in=aluno_ids,
                turma_id__in=turma_ids,
                atividade_id__in=atividade_ids,
                data__in=[dados["data"] for dados in dados_presencas],
            ).values_list("aluno_id", "turma_id", "atividade_id", "data")
        )

        # Preparar objetos para inserção
        presencas_para_criar = []
        presencas_para_atualizar = []
        observacoes_para_criar = []

        for dados in dados_presencas:
            key = (
                dados["aluno_id"],
                dados["turma_id"],
                dados["atividade_id"],
                dados["data"],
            )

            presenca_obj = Presenca(
                aluno_id=dados["aluno_id"],
                turma_id=dados["turma_id"],
                atividade_id=dados["atividade_id"],
                data=dados["data"],
                presente=dados["presente"],
                registrado_por=registrado_por,
                data_registro=timezone.now(),
            )

            if key in existing_presencas:
                # Atualizar presença existente
                presencas_para_atualizar.append(presenca_obj)
            else:
                # Criar nova presença
                presencas_para_criar.append(presenca_obj)

            # Preparar observação se fornecida
            if dados.get("observacao"):
                observacao = ObservacaoPresenca(
                    aluno_id=dados["aluno_id"],
                    turma_id=dados["turma_id"],
                    atividade_id=dados["atividade_id"],
                    data=dados["data"],
                    texto=dados["observacao"],
                    registrado_por=registrado_por,
                    data_registro=timezone.now(),
                )
                observacoes_para_criar.append(observacao)

        # Executar operações em lote
        stats = {"criadas": 0, "atualizadas": 0, "observacoes": 0, "erros": 0}

        try:
            # Bulk create para novas presenças
            if presencas_para_criar:
                created_presencas = Presenca.objects.bulk_create(
                    presencas_para_criar, batch_size=1000, ignore_conflicts=True
                )
                stats["criadas"] = len(created_presencas)

            # Bulk update para presenças existentes (requer Django 4.2+)
            if presencas_para_atualizar:
                # Para versões anteriores do Django, usar update individual ou raw SQL
                for presenca in presencas_para_atualizar:
                    Presenca.objects.filter(
                        aluno_id=presenca.aluno_id,
                        turma_id=presenca.turma_id,
                        atividade_id=presenca.atividade_id,
                        data=presenca.data,
                    ).update(
                        presente=presenca.presente,
                        registrado_por=presenca.registrado_por,
                        data_registro=presenca.data_registro,
                    )
                stats["atualizadas"] = len(presencas_para_atualizar)

            # Bulk create para observações
            if observacoes_para_criar:
                ObservacaoPresenca.objects.bulk_create(
                    observacoes_para_criar, batch_size=1000, ignore_conflicts=True
                )
                stats["observacoes"] = len(observacoes_para_criar)

            logger.info(f"Bulk operation concluída: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Erro na operação em lote: {str(e)}")
            stats["erros"] = 1
            raise e

    @staticmethod
    @transaction.atomic
    def excluir_presencas_lote(presenca_ids: List[int]) -> int:
        """
        Exclui múltiplas presenças em lote.

        Args:
            presenca_ids: Lista de IDs das presenças a excluir

        Returns:
            Número de presenças excluídas
        """
        logger.info(f"Excluindo {len(presenca_ids)} presenças em lote")

        # Excluir observações relacionadas primeiro
        ObservacaoPresenca.objects.filter(
            aluno__in=Presenca.objects.filter(id__in=presenca_ids).values("aluno"),
            turma__in=Presenca.objects.filter(id__in=presenca_ids).values("turma"),
            data__in=Presenca.objects.filter(id__in=presenca_ids).values("data"),
        ).delete()

        # Excluir as presenças
        deleted_count, _ = Presenca.objects.filter(id__in=presenca_ids).delete()

        logger.info(f"Excluídas {deleted_count} presenças")
        return deleted_count

    @staticmethod
    def otimizar_queries_estatisticas(
        turma_id: int = None, periodo_inicio: date = None, periodo_fim: date = None
    ) -> Dict[str, Any]:
        """
        Calcula estatísticas usando queries agregadas otimizadas.

        Args:
            turma_id: ID da turma (opcional)
            periodo_inicio: Data de início do período
            periodo_fim: Data de fim do período

        Returns:
            Dicionário com estatísticas calculadas
        """
        logger.info("Calculando estatísticas com queries otimizadas")

        # Query base otimizada
        queryset = Presenca.objects.select_related("aluno", "turma", "atividade")

        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
        if periodo_inicio:
            queryset = queryset.filter(data__gte=periodo_inicio)
        if periodo_fim:
            queryset = queryset.filter(data__lte=periodo_fim)

        # Usar aggregation para cálculos em uma única query
        from django.db.models import Count, Case, When, IntegerField, Avg

        stats = queryset.aggregate(
            total_registros=Count("id"),
            total_presentes=Count(
                Case(When(presente=True, then=1), output_field=IntegerField())
            ),
            total_ausentes=Count(
                Case(When(presente=False, then=1), output_field=IntegerField())
            ),
            total_alunos=Count("aluno", distinct=True),
            total_turmas=Count("turma", distinct=True),
            total_atividades=Count("atividade", distinct=True),
            percentual_presenca=Avg(
                Case(
                    When(presente=True, then=100),
                    default=0,
                    output_field=IntegerField(),
                )
            ),
        )

        # Adicionar estatísticas por aluno usando subquery
        stats["por_aluno"] = list(
            queryset.values("aluno__nome", "aluno__cpf")
            .annotate(
                total=Count("id"),
                presentes=Count(
                    Case(When(presente=True, then=1), output_field=IntegerField())
                ),
                ausentes=Count(
                    Case(When(presente=False, then=1), output_field=IntegerField())
                ),
            )
            .order_by("aluno__nome")
        )

        logger.info(
            f"Estatísticas calculadas: {stats['total_registros']} registros processados"
        )
        return stats
