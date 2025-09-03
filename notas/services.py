"""
Services para o app Notas - Lógica de negócios
"""

import importlib
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


class NotaService:
    """
    Service para gerenciar lógica de negócios relacionada às notas
    """

    def __init__(self):
        self.repository = self._get_repository()

    def _get_repository(self):
        """Importação dinâmica do repository"""
        try:
            repositories_module = importlib.import_module("notas.repositories")
            return getattr(repositories_module, "NotaRepository")()
        except (ImportError, AttributeError) as e:
            logger.error(f"Erro ao importar NotaRepository: {e}")
            raise ImportError(f"Erro ao importar NotaRepository: {e}")

    def get_all_notas(self):
        """Retorna todas as notas"""
        try:
            return self.repository.get_all()
        except Exception as e:
            logger.error(f"Erro ao buscar todas as notas: {e}")
            raise

    def get_nota_by_id(self, nota_id):
        """Retorna uma nota específica"""
        try:
            return self.repository.get_by_id(nota_id)
        except ObjectDoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar nota por ID {nota_id}: {e}")
            raise

    def get_notas_by_aluno(self, aluno_id):
        """Retorna notas de um aluno específico"""
        try:
            return self.repository.get_by_aluno(aluno_id)
        except Exception as e:
            logger.error(f"Erro ao buscar notas do aluno {aluno_id}: {e}")
            raise

    def get_notas_by_turma(self, turma_id):
        """Retorna notas de uma turma específica"""
        try:
            return self.repository.get_by_turma(turma_id)
        except Exception as e:
            logger.error(f"Erro ao buscar notas da turma {turma_id}: {e}")
            raise

    def get_notas_by_atividade(self, atividade_id):
        """Retorna notas de uma atividade específica"""
        try:
            return self.repository.get_by_atividade(atividade_id)
        except Exception as e:
            logger.error(f"Erro ao buscar notas da atividade {atividade_id}: {e}")
            raise

    def get_notas_by_periodo(self, data_inicio, data_fim):
        """Retorna notas por período"""
        try:
            return self.repository.get_by_periodo(data_inicio, data_fim)
        except Exception as e:
            logger.error(f"Erro ao buscar notas por período: {e}")
            raise

    @transaction.atomic
    def create_nota(self, nota_data):
        """Cria uma nova nota"""
        try:
            # Validações de negócio
            self._validate_nota_data(nota_data)

            # Verificar se já existe nota para o mesmo aluno e atividade
            existing_nota = self.repository.get_by_aluno_and_atividade(
                nota_data.get("aluno_id"), nota_data.get("atividade_id")
            )
            if existing_nota:
                raise ValidationError(
                    "Já existe uma nota para este aluno nesta atividade"
                )

            # Criar nota
            nota = self.repository.create(nota_data)

            # Log da operação
            logger.info(f"Nota criada com sucesso: ID {nota.id}")

            return nota
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Erro ao criar nota: {e}")
            raise

    @transaction.atomic
    def update_nota(self, nota_id, nota_data):
        """Atualiza uma nota existente"""
        try:
            # Verificar se a nota existe
            nota = self.get_nota_by_id(nota_id)
            if not nota:
                raise ObjectDoesNotExist("Nota não encontrada")

            # Validações de negócio
            self._validate_nota_data(nota_data, is_update=True)

            # Atualizar nota
            nota_atualizada = self.repository.update(nota_id, nota_data)

            # Log da operação
            logger.info(f"Nota atualizada com sucesso: ID {nota_id}")

            return nota_atualizada
        except (ObjectDoesNotExist, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Erro ao atualizar nota {nota_id}: {e}")
            raise

    @transaction.atomic
    def delete_nota(self, nota_id):
        """Remove uma nota"""
        try:
            # Verificar se a nota existe
            nota = self.get_nota_by_id(nota_id)
            if not nota:
                raise ObjectDoesNotExist("Nota não encontrada")

            # Verificar se pode ser deletada
            if not self._can_delete_nota(nota):
                raise ValidationError("Esta nota não pode ser deletada")

            # Deletar nota
            self.repository.delete(nota_id)

            # Log da operação
            logger.info(f"Nota deletada com sucesso: ID {nota_id}")

            return True
        except (ObjectDoesNotExist, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Erro ao deletar nota {nota_id}: {e}")
            raise

    def calcular_media_aluno(self, aluno_id, turma_id=None):
        """Calcula a média de um aluno"""
        try:
            notas = self.get_notas_by_aluno(aluno_id)
            if turma_id:
                notas = notas.filter(atividade__turma_id=turma_id)

            if not notas.exists():
                return {"media": 0, "total_notas": 0, "status": "sem_notas"}

            total = sum(float(nota.valor) for nota in notas)
            media = total / len(notas)

            return {
                "media": round(media, 2),
                "total_notas": len(notas),
                "status": "aprovado" if media >= 7.0 else "reprovado",
            }
        except Exception as e:
            logger.error(f"Erro ao calcular média do aluno {aluno_id}: {e}")
            raise

    def calcular_media_turma(self, turma_id):
        """Calcula a média geral de uma turma"""
        try:
            notas = self.get_notas_by_turma(turma_id)

            if not notas.exists():
                return {"media_geral": 0, "total_notas": 0, "alunos_com_notas": 0}

            total = sum(float(nota.valor) for nota in notas)
            media_geral = total / len(notas)

            # Contar alunos únicos com notas
            alunos_com_notas = notas.values("aluno").distinct().count()

            return {
                "media_geral": round(media_geral, 2),
                "total_notas": len(notas),
                "alunos_com_notas": alunos_com_notas,
            }
        except Exception as e:
            logger.error(f"Erro ao calcular média da turma {turma_id}: {e}")
            raise

    def gerar_relatorio_notas(self, filtros=None):
        """Gera relatório de notas"""
        try:
            notas = self.repository.get_all()

            # Aplicar filtros se fornecidos
            if filtros:
                if filtros.get("turma_id"):
                    notas = notas.filter(atividade__turma_id=filtros["turma_id"])
                if filtros.get("aluno_id"):
                    notas = notas.filter(aluno_id=filtros["aluno_id"])
                if filtros.get("data_inicio"):
                    notas = notas.filter(data_registro__gte=filtros["data_inicio"])
                if filtros.get("data_fim"):
                    notas = notas.filter(data_registro__lte=filtros["data_fim"])

            # Preparar dados do relatório
            relatorio = {
                "total_notas": notas.count(),
                "media_geral": 0,
                "distribuicao_notas": {},
                "data_geracao": timezone.now().isoformat(),
            }

            if notas.exists():
                # Calcular média geral
                total = sum(float(nota.valor) for nota in notas)
                relatorio["media_geral"] = round(total / notas.count(), 2)

                # Distribuição por faixas de nota
                distribuicao = {"0-3": 0, "4-6": 0, "7-8": 0, "9-10": 0}
                for nota in notas:
                    valor = float(nota.valor)
                    if valor <= 3:
                        distribuicao["0-3"] += 1
                    elif valor <= 6:
                        distribuicao["4-6"] += 1
                    elif valor <= 8:
                        distribuicao["7-8"] += 1
                    else:
                        distribuicao["9-10"] += 1

                relatorio["distribuicao_notas"] = distribuicao

            return relatorio
        except Exception as e:
            logger.error(f"Erro ao gerar relatório de notas: {e}")
            raise

    def _validate_nota_data(self, nota_data, is_update=False):
        """Valida os dados de uma nota"""
        # Validar valor da nota
        valor = nota_data.get("valor")
        if valor is not None:
            try:
                valor_float = float(valor)
                if valor_float < 0 or valor_float > 10:
                    raise ValidationError("A nota deve estar entre 0 e 10")
            except (ValueError, TypeError):
                raise ValidationError("Valor da nota deve ser um número válido")

        # Validar campos obrigatórios
        if not is_update:
            if not nota_data.get("aluno_id"):
                raise ValidationError("Aluno é obrigatório")
            if not nota_data.get("atividade_id"):
                raise ValidationError("Atividade é obrigatória")

        # Outras validações podem ser adicionadas aqui
        return True

    def _can_delete_nota(self, nota):
        """Verifica se uma nota pode ser deletada"""
        # Implementar regras de negócio específicas
        # Por exemplo, verificar se a nota não está em um período fechado
        return True
