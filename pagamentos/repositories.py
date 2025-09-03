"""
Repositories para o app Pagamentos - Camada de acesso a dados
"""

import importlib
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class PagamentoRepository:
    """
    Repository para gerenciar acesso aos dados dos pagamentos
    """

    def __init__(self):
        self.model = self._get_model()

    def _get_model(self):
        """Importação dinâmica do modelo"""
        try:
            models_module = importlib.import_module("pagamentos.models")
            return getattr(models_module, "Pagamento")
        except (ImportError, AttributeError) as e:
            logger.error(f"Erro ao importar modelo Pagamento: {e}")
            raise ImportError(f"Erro ao importar modelo Pagamento: {e}")

    def get_all(self):
        """Retorna todos os pagamentos"""
        try:
            return self.model.objects.select_related("aluno", "turma").all()
        except Exception as e:
            logger.error(f"Erro ao buscar todos os pagamentos: {e}")
            raise

    def get_by_id(self, pagamento_id):
        """Retorna um pagamento por ID"""
        try:
            return self.model.objects.select_related("aluno", "turma").get(
                id=pagamento_id
            )
        except self.model.DoesNotExist:
            raise ObjectDoesNotExist(f"Pagamento com ID {pagamento_id} não encontrado")
        except Exception as e:
            logger.error(f"Erro ao buscar pagamento por ID {pagamento_id}: {e}")
            raise

    def get_by_aluno(self, aluno_id):
        """Retorna pagamentos de um aluno específico"""
        try:
            return self.model.objects.select_related("aluno", "turma").filter(
                aluno_id=aluno_id
            )
        except Exception as e:
            logger.error(f"Erro ao buscar pagamentos do aluno {aluno_id}: {e}")
            raise

    def get_by_turma(self, turma_id):
        """Retorna pagamentos de uma turma específica"""
        try:
            return self.model.objects.select_related("aluno", "turma").filter(
                turma_id=turma_id
            )
        except Exception as e:
            logger.error(f"Erro ao buscar pagamentos da turma {turma_id}: {e}")
            raise

    def get_by_status(self, status):
        """Retorna pagamentos por status"""
        try:
            return self.model.objects.select_related("aluno", "turma").filter(
                status=status
            )
        except Exception as e:
            logger.error(f"Erro ao buscar pagamentos por status {status}: {e}")
            raise

    def get_vencidos(self):
        """Retorna pagamentos vencidos"""
        try:
            hoje = timezone.now().date()
            return self.model.objects.select_related("aluno", "turma").filter(
                status="PENDENTE", data_vencimento__lt=hoje
            )
        except Exception as e:
            logger.error(f"Erro ao buscar pagamentos vencidos: {e}")
            raise

    def get_by_periodo(self, data_inicio, data_fim):
        """Retorna pagamentos por período"""
        try:
            return self.model.objects.select_related("aluno", "turma").filter(
                data_vencimento__gte=data_inicio, data_vencimento__lte=data_fim
            )
        except Exception as e:
            logger.error(f"Erro ao buscar pagamentos por período: {e}")
            raise

    def get_by_aluno_turma_referencia(
        self, aluno_id, turma_id, mes_referencia, ano_referencia
    ):
        """Retorna pagamento específico por aluno, turma e referência"""
        try:
            return (
                self.model.objects.select_related("aluno", "turma")
                .filter(
                    aluno_id=aluno_id,
                    turma_id=turma_id,
                    mes_referencia=mes_referencia,
                    ano_referencia=ano_referencia,
                )
                .first()
            )
        except Exception as e:
            logger.error(f"Erro ao buscar pagamento por referência: {e}")
            raise

    def get_by_valor_range(self, valor_min, valor_max):
        """Retorna pagamentos dentro de uma faixa de valores"""
        try:
            return self.model.objects.select_related("aluno", "turma").filter(
                valor__gte=valor_min, valor__lte=valor_max
            )
        except Exception as e:
            logger.error(f"Erro ao buscar pagamentos por faixa de valor: {e}")
            raise

    @transaction.atomic
    def create(self, pagamento_data):
        """Cria um novo pagamento"""
        try:
            # Buscar instâncias relacionadas
            aluno = self._get_aluno_by_id(pagamento_data.get("aluno_id"))
            turma = self._get_turma_by_id(pagamento_data.get("turma_id"))

            # Criar pagamento
            pagamento = self.model.objects.create(
                aluno=aluno,
                turma=turma,
                valor=Decimal(str(pagamento_data.get("valor"))),
                data_vencimento=pagamento_data.get("data_vencimento"),
                mes_referencia=pagamento_data.get("mes_referencia"),
                ano_referencia=pagamento_data.get("ano_referencia"),
                status=pagamento_data.get("status", "PENDENTE"),
                observacoes=pagamento_data.get("observacoes", ""),
                data_pagamento=pagamento_data.get("data_pagamento"),
            )

            logger.info(f"Pagamento criado com sucesso: ID {pagamento.id}")
            return pagamento
        except Exception as e:
            logger.error(f"Erro ao criar pagamento: {e}")
            raise

    @transaction.atomic
    def update(self, pagamento_id, pagamento_data):
        """Atualiza um pagamento existente"""
        try:
            pagamento = self.get_by_id(pagamento_id)

            # Atualizar campos
            if "valor" in pagamento_data:
                pagamento.valor = Decimal(str(pagamento_data["valor"]))
            if "data_vencimento" in pagamento_data:
                pagamento.data_vencimento = pagamento_data["data_vencimento"]
            if "mes_referencia" in pagamento_data:
                pagamento.mes_referencia = pagamento_data["mes_referencia"]
            if "ano_referencia" in pagamento_data:
                pagamento.ano_referencia = pagamento_data["ano_referencia"]
            if "status" in pagamento_data:
                pagamento.status = pagamento_data["status"]
            if "observacoes" in pagamento_data:
                pagamento.observacoes = pagamento_data["observacoes"]
            if "data_pagamento" in pagamento_data:
                pagamento.data_pagamento = pagamento_data["data_pagamento"]
            if "aluno_id" in pagamento_data:
                pagamento.aluno = self._get_aluno_by_id(pagamento_data["aluno_id"])
            if "turma_id" in pagamento_data:
                pagamento.turma = self._get_turma_by_id(pagamento_data["turma_id"])

            pagamento.save()

            logger.info(f"Pagamento atualizado com sucesso: ID {pagamento_id}")
            return pagamento
        except Exception as e:
            logger.error(f"Erro ao atualizar pagamento {pagamento_id}: {e}")
            raise

    @transaction.atomic
    def delete(self, pagamento_id):
        """Remove um pagamento"""
        try:
            pagamento = self.get_by_id(pagamento_id)
            pagamento.delete()
            logger.info(f"Pagamento deletado com sucesso: ID {pagamento_id}")
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar pagamento {pagamento_id}: {e}")
            raise

    def exists(self, pagamento_id):
        """Verifica se um pagamento existe"""
        try:
            return self.model.objects.filter(id=pagamento_id).exists()
        except Exception as e:
            logger.error(
                f"Erro ao verificar existência do pagamento {pagamento_id}: {e}"
            )
            raise

    def count(self):
        """Retorna o total de pagamentos"""
        try:
            return self.model.objects.count()
        except Exception as e:
            logger.error(f"Erro ao contar pagamentos: {e}")
            raise

    def get_total_valor_by_status(self, status):
        """Retorna o valor total por status"""
        try:
            from django.db.models import Sum

            resultado = self.model.objects.filter(status=status).aggregate(
                total=Sum("valor")
            )
            return resultado["total"] or Decimal("0.00")
        except Exception as e:
            logger.error(f"Erro ao calcular total por status {status}: {e}")
            raise

    def get_estatisticas_pagamentos(self):
        """Retorna estatísticas gerais dos pagamentos"""
        try:
            from django.db.models import Sum, Avg, Count

            stats = self.model.objects.aggregate(
                total_pagamentos=Count("id"),
                valor_total=Sum("valor"),
                valor_medio=Avg("valor"),
            )

            # Contar por status
            status_counts = {}
            for status in ["PENDENTE", "PAGO", "CANCELADO", "VENCIDO"]:
                status_counts[status] = self.model.objects.filter(status=status).count()

            return {
                "total_pagamentos": stats["total_pagamentos"] or 0,
                "valor_total": float(stats["valor_total"] or 0),
                "valor_medio": float(stats["valor_medio"] or 0),
                "distribuicao_status": status_counts,
            }
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas: {e}")
            raise

    def _get_aluno_by_id(self, aluno_id):
        """Busca aluno por ID usando importação dinâmica"""
        try:
            alunos_module = importlib.import_module("alunos.models")
            Aluno = getattr(alunos_module, "Aluno")
            return Aluno.objects.get(id=aluno_id)
        except Exception as e:
            logger.error(f"Erro ao buscar aluno {aluno_id}: {e}")
            raise ObjectDoesNotExist(f"Aluno com ID {aluno_id} não encontrado")

    def _get_turma_by_id(self, turma_id):
        """Busca turma por ID usando importação dinâmica"""
        try:
            turmas_module = importlib.import_module("turmas.models")
            Turma = getattr(turmas_module, "Turma")
            return Turma.objects.get(id=turma_id)
        except Exception as e:
            logger.error(f"Erro ao buscar turma {turma_id}: {e}")
            raise ObjectDoesNotExist(f"Turma com ID {turma_id} não encontrada")
