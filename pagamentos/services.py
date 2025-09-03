"""
Services para o app Pagamentos - Lógica de negócios
"""

import importlib
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class PagamentoService:
    """
    Service para gerenciar lógica de negócios relacionada aos pagamentos
    """

    def __init__(self):
        self.repository = self._get_repository()

    def _get_repository(self):
        """Importação dinâmica do repository"""
        try:
            repositories_module = importlib.import_module("pagamentos.repositories")
            return getattr(repositories_module, "PagamentoRepository")()
        except (ImportError, AttributeError) as e:
            logger.error(f"Erro ao importar PagamentoRepository: {e}")
            raise ImportError(f"Erro ao importar PagamentoRepository: {e}")

    def get_all_pagamentos(self):
        """Retorna todos os pagamentos"""
        try:
            return self.repository.get_all()
        except Exception as e:
            logger.error(f"Erro ao buscar todos os pagamentos: {e}")
            raise

    def get_pagamento_by_id(self, pagamento_id):
        """Retorna um pagamento específico"""
        try:
            return self.repository.get_by_id(pagamento_id)
        except ObjectDoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar pagamento por ID {pagamento_id}: {e}")
            raise

    def get_pagamentos_by_aluno(self, aluno_id):
        """Retorna pagamentos de um aluno específico"""
        try:
            return self.repository.get_by_aluno(aluno_id)
        except Exception as e:
            logger.error(f"Erro ao buscar pagamentos do aluno {aluno_id}: {e}")
            raise

    def get_pagamentos_by_turma(self, turma_id):
        """Retorna pagamentos de uma turma específica"""
        try:
            return self.repository.get_by_turma(turma_id)
        except Exception as e:
            logger.error(f"Erro ao buscar pagamentos da turma {turma_id}: {e}")
            raise

    def get_pagamentos_by_status(self, status):
        """Retorna pagamentos por status"""
        try:
            return self.repository.get_by_status(status)
        except Exception as e:
            logger.error(f"Erro ao buscar pagamentos por status {status}: {e}")
            raise

    def get_pagamentos_vencidos(self):
        """Retorna pagamentos vencidos"""
        try:
            return self.repository.get_vencidos()
        except Exception as e:
            logger.error(f"Erro ao buscar pagamentos vencidos: {e}")
            raise

    def get_pagamentos_by_periodo(self, data_inicio, data_fim):
        """Retorna pagamentos por período"""
        try:
            return self.repository.get_by_periodo(data_inicio, data_fim)
        except Exception as e:
            logger.error(f"Erro ao buscar pagamentos por período: {e}")
            raise

    @transaction.atomic
    def create_pagamento(self, pagamento_data):
        """Cria um novo pagamento"""
        try:
            # Validações de negócio
            self._validate_pagamento_data(pagamento_data)

            # Verificar se já existe pagamento para o mesmo aluno/turma/referência
            existing_pagamento = self.repository.get_by_aluno_turma_referencia(
                pagamento_data.get("aluno_id"),
                pagamento_data.get("turma_id"),
                pagamento_data.get("mes_referencia"),
                pagamento_data.get("ano_referencia"),
            )
            if existing_pagamento:
                raise ValidationError("Já existe um pagamento para esta referência")

            # Criar pagamento
            pagamento = self.repository.create(pagamento_data)

            # Log da operação
            logger.info(f"Pagamento criado com sucesso: ID {pagamento.id}")

            return pagamento
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Erro ao criar pagamento: {e}")
            raise

    @transaction.atomic
    def update_pagamento(self, pagamento_id, pagamento_data):
        """Atualiza um pagamento existente"""
        try:
            # Verificar se o pagamento existe
            pagamento = self.get_pagamento_by_id(pagamento_id)
            if not pagamento:
                raise ObjectDoesNotExist("Pagamento não encontrado")

            # Validações de negócio
            self._validate_pagamento_data(pagamento_data, is_update=True)

            # Atualizar pagamento
            pagamento_atualizado = self.repository.update(pagamento_id, pagamento_data)

            # Log da operação
            logger.info(f"Pagamento atualizado com sucesso: ID {pagamento_id}")

            return pagamento_atualizado
        except (ObjectDoesNotExist, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Erro ao atualizar pagamento {pagamento_id}: {e}")
            raise

    @transaction.atomic
    def delete_pagamento(self, pagamento_id):
        """Remove um pagamento"""
        try:
            # Verificar se o pagamento existe
            pagamento = self.get_pagamento_by_id(pagamento_id)
            if not pagamento:
                raise ObjectDoesNotExist("Pagamento não encontrado")

            # Verificar se pode ser deletado
            if not self._can_delete_pagamento(pagamento):
                raise ValidationError("Este pagamento não pode ser deletado")

            # Deletar pagamento
            self.repository.delete(pagamento_id)

            # Log da operação
            logger.info(f"Pagamento deletado com sucesso: ID {pagamento_id}")

            return True
        except (ObjectDoesNotExist, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Erro ao deletar pagamento {pagamento_id}: {e}")
            raise

    @transaction.atomic
    def confirmar_pagamento(self, pagamento_id, data_pagamento=None):
        """Confirma um pagamento"""
        try:
            pagamento = self.get_pagamento_by_id(pagamento_id)
            if not pagamento:
                raise ObjectDoesNotExist("Pagamento não encontrado")

            if pagamento.status == "PAGO":
                raise ValidationError("Pagamento já foi confirmado")

            # Atualizar status e data de pagamento
            update_data = {
                "status": "PAGO",
                "data_pagamento": data_pagamento or timezone.now().date(),
            }

            pagamento_atualizado = self.repository.update(pagamento_id, update_data)

            # Log da operação
            logger.info(f"Pagamento confirmado com sucesso: ID {pagamento_id}")

            return pagamento_atualizado
        except (ObjectDoesNotExist, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Erro ao confirmar pagamento {pagamento_id}: {e}")
            raise

    @transaction.atomic
    def cancelar_pagamento(self, pagamento_id, motivo=None):
        """Cancela um pagamento"""
        try:
            pagamento = self.get_pagamento_by_id(pagamento_id)
            if not pagamento:
                raise ObjectDoesNotExist("Pagamento não encontrado")

            if pagamento.status == "CANCELADO":
                raise ValidationError("Pagamento já foi cancelado")

            # Atualizar status
            update_data = {
                "status": "CANCELADO",
                "observacoes": motivo or "Pagamento cancelado",
            }

            pagamento_atualizado = self.repository.update(pagamento_id, update_data)

            # Log da operação
            logger.info(f"Pagamento cancelado com sucesso: ID {pagamento_id}")

            return pagamento_atualizado
        except (ObjectDoesNotExist, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Erro ao cancelar pagamento {pagamento_id}: {e}")
            raise

    def calcular_total_pagamentos(self, aluno_id=None, turma_id=None, status=None):
        """Calcula o total de pagamentos"""
        try:
            pagamentos = self.get_all_pagamentos()

            # Aplicar filtros
            if aluno_id:
                pagamentos = pagamentos.filter(aluno_id=aluno_id)
            if turma_id:
                pagamentos = pagamentos.filter(turma_id=turma_id)
            if status:
                pagamentos = pagamentos.filter(status=status)

            total = sum(float(pagamento.valor) for pagamento in pagamentos)

            return {
                "total": total,
                "quantidade": len(pagamentos),
                "media": total / len(pagamentos) if pagamentos else 0,
            }
        except Exception as e:
            logger.error(f"Erro ao calcular total de pagamentos: {e}")
            raise

    def gerar_relatorio_pagamentos(self, filtros=None):
        """Gera relatório de pagamentos"""
        try:
            pagamentos = self.get_all_pagamentos()

            # Aplicar filtros se fornecidos
            if filtros:
                if filtros.get("aluno_id"):
                    pagamentos = pagamentos.filter(aluno_id=filtros["aluno_id"])
                if filtros.get("turma_id"):
                    pagamentos = pagamentos.filter(turma_id=filtros["turma_id"])
                if filtros.get("status"):
                    pagamentos = pagamentos.filter(status=filtros["status"])
                if filtros.get("data_inicio"):
                    pagamentos = pagamentos.filter(
                        data_vencimento__gte=filtros["data_inicio"]
                    )
                if filtros.get("data_fim"):
                    pagamentos = pagamentos.filter(
                        data_vencimento__lte=filtros["data_fim"]
                    )

            # Preparar dados do relatório
            relatorio = {
                "total_pagamentos": pagamentos.count(),
                "valor_total": 0,
                "distribuicao_status": {},
                "pagamentos_vencidos": 0,
                "data_geracao": timezone.now().isoformat(),
            }

            if pagamentos.exists():
                # Calcular valor total
                relatorio["valor_total"] = float(
                    sum(pagamento.valor for pagamento in pagamentos)
                )

                # Distribuição por status
                status_counts = {}
                vencidos = 0

                for pagamento in pagamentos:
                    status = pagamento.status
                    status_counts[status] = status_counts.get(status, 0) + 1

                    # Verificar se está vencido
                    if (
                        pagamento.status == "PENDENTE"
                        and pagamento.data_vencimento < timezone.now().date()
                    ):
                        vencidos += 1

                relatorio["distribuicao_status"] = status_counts
                relatorio["pagamentos_vencidos"] = vencidos

            return relatorio
        except Exception as e:
            logger.error(f"Erro ao gerar relatório de pagamentos: {e}")
            raise

    def _validate_pagamento_data(self, pagamento_data, is_update=False):
        """Valida os dados de um pagamento"""
        # Validar valor
        valor = pagamento_data.get("valor")
        if valor is not None:
            try:
                valor_decimal = Decimal(str(valor))
                if valor_decimal <= 0:
                    raise ValidationError("O valor deve ser maior que zero")
            except (ValueError, TypeError):
                raise ValidationError("Valor deve ser um número válido")

        # Validar campos obrigatórios
        if not is_update:
            if not pagamento_data.get("aluno_id"):
                raise ValidationError("Aluno é obrigatório")
            if not pagamento_data.get("turma_id"):
                raise ValidationError("Turma é obrigatória")
            if not pagamento_data.get("data_vencimento"):
                raise ValidationError("Data de vencimento é obrigatória")

        # Validar status
        status = pagamento_data.get("status")
        if status and status not in ["PENDENTE", "PAGO", "CANCELADO", "VENCIDO"]:
            raise ValidationError("Status inválido")

        return True

    def _can_delete_pagamento(self, pagamento):
        """Verifica se um pagamento pode ser deletado"""
        # Não permitir deletar pagamentos já pagos
        if pagamento.status == "PAGO":
            return False

        # Outras regras de negócio podem ser adicionadas aqui
        return True
