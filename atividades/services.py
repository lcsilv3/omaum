"""
Serviços para o app Atividades.
Este módulo contém a lógica de negócio relacionada às atividades,
seguindo o padrão Service Layer.
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import date
from typing import Optional
from .models import Atividade, Presenca
from .repositories import AtividadeRepository, PresencaRepository


class AtividadeService:
    """Serviços para gerenciamento de atividades."""

    @staticmethod
    def listar_atividades():
        """Lista todas as atividades."""
        return AtividadeRepository.get_all()

    @staticmethod
    def obter_atividade_por_id(atividade_id: int) -> Optional[Atividade]:
        """Obtém uma atividade por ID."""
        return AtividadeRepository.get_by_id_or_none(atividade_id)

    @staticmethod
    def listar_atividades_ativas():
        """Lista apenas as atividades ativas."""
        return AtividadeRepository.get_ativas()

    @staticmethod
    def listar_atividades_por_turma(turma_id: int):
        """Lista atividades de uma turma específica."""
        return AtividadeRepository.get_by_turma(turma_id)

    @staticmethod
    def listar_atividades_por_curso(curso_id: int):
        """Lista atividades de um curso específico."""
        return AtividadeRepository.get_by_curso(curso_id)

    @staticmethod
    def listar_atividades_por_periodo(data_inicio: date, data_fim: date):
        """Lista atividades em um período específico."""
        return AtividadeRepository.get_by_periodo(data_inicio, data_fim)

    @staticmethod
    def buscar_atividades(termo: str):
        """Busca atividades por termo."""
        return AtividadeRepository.search(termo)

    @staticmethod
    @transaction.atomic
    def criar_atividade(dados: dict) -> Atividade:
        """Cria uma nova atividade."""
        # Validações básicas
        if not dados.get('nome'):
            raise ValidationError("Nome da atividade é obrigatório.")

        if not dados.get('data_inicio'):
            raise ValidationError("Data de início é obrigatória.")

        # Criar a atividade
        atividade = Atividade.objects.create(**dados)
        return atividade

    @staticmethod
    @transaction.atomic
    def atualizar_atividade(atividade_id: int,
                           dados: dict) -> Optional[Atividade]:
        """Atualiza uma atividade existente."""
        atividade = AtividadeRepository.get_by_id_or_none(atividade_id)
        if not atividade:
            return None

        for campo, valor in dados.items():
            setattr(atividade, campo, valor)

        atividade.save()
        return atividade

    @staticmethod
    @transaction.atomic
    def deletar_atividade(atividade_id: int) -> bool:
        """Deleta uma atividade."""
        atividade = AtividadeRepository.get_by_id_or_none(atividade_id)
        if not atividade:
            return False

        atividade.delete()
        return True


class PresencaService:
    """Serviços para gerenciamento de presenças."""

    @staticmethod
    def registrar_presenca(aluno_id: int, atividade_id: int, turma_id: int,
                          presente: bool = True,
                          registrado_por: str = "Sistema") -> Presenca:
        """Registra presença em uma atividade."""
        atividade = AtividadeRepository.get_by_id(atividade_id)

        presenca, created = Presenca.objects.get_or_create(
            aluno_id=aluno_id,
            atividade=atividade,
            turma_id=turma_id,
            data=atividade.data_inicio,
            defaults={
                'presente': presente,
                'registrado_por': registrado_por
            }
        )

        if not created:
            presenca.presente = presente
            presenca.registrado_por = registrado_por
            presenca.save()

        return presenca

    @staticmethod
    def obter_presencas_aluno(aluno_id: int):
        """Obtém todas as presenças de um aluno."""
        return PresencaRepository.get_by_aluno(aluno_id)

    @staticmethod
    def obter_presencas_atividade(atividade_id: int):
        """Obtém todas as presenças de uma atividade."""
        return PresencaRepository.get_by_atividade(atividade_id)

    @staticmethod
    def obter_presencas_turma(turma_id: int):
        """Obtém todas as presenças de uma turma."""
        return PresencaRepository.get_by_turma(turma_id)

    @staticmethod
    def calcular_frequencia_aluno(aluno_id: int,
                                 atividade_id: int = None) -> dict:
        """Calcula a frequência de um aluno."""
        if atividade_id:
            presencas = PresencaRepository.get_by_aluno_e_atividade(
                aluno_id, atividade_id
            )
        else:
            presencas = PresencaRepository.get_by_aluno(aluno_id)

        total = presencas.count()
        presentes = presencas.filter(presente=True).count()

        if total == 0:
            return {'total': 0, 'presentes': 0, 'percentual': 0.0}

        percentual = (presentes / total) * 100

        return {
            'total': total,
            'presentes': presentes,
            'percentual': round(percentual, 2)
        }

    @staticmethod
    @transaction.atomic
    def deletar_presenca(presenca_id: int) -> bool:
        """Deleta uma presença."""
        presenca = PresencaRepository.get_by_id_or_none(presenca_id)
        if not presenca:
            return False

        presenca.delete()
        return True
