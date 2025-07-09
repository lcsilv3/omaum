"""
Serviços para o app Atividades.
Este módulo contém a lógica de negócio relacionada às atividades acadêmicas
e ritualísticas, seguindo o padrão Service Layer.
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import date
from typing import Optional
from .models import (
    AtividadeAcademica,
    AtividadeRitualistica,
    PresencaAcademica,
    PresencaRitualistica
)
from .repositories import (
    AtividadeAcademicaRepository,
    AtividadeRitualisticaRepository,
    PresencaAcademicaRepository,
    PresencaRitualisticaRepository
)


class AtividadeAcademicaService:
    """Serviços para gerenciamento de atividades acadêmicas."""

    @staticmethod
    def listar_atividades():
        """Lista todas as atividades acadêmicas."""
        return AtividadeAcademicaRepository.get_all()

    @staticmethod
    def obter_atividade_por_id(
        atividade_id: int
    ) -> Optional[AtividadeAcademica]:
        """Obtém uma atividade acadêmica por ID."""
        return AtividadeAcademicaRepository.get_by_id_or_none(atividade_id)

    @staticmethod
    def listar_atividades_ativas():
        """Lista apenas as atividades acadêmicas ativas."""
        return AtividadeAcademicaRepository.get_ativas()

    @staticmethod
    def listar_atividades_por_turma(turma_id: int):
        """Lista atividades acadêmicas de uma turma específica."""
        return AtividadeAcademicaRepository.get_by_turma(turma_id)

    @staticmethod
    def listar_atividades_por_curso(curso_id: int):
        """Lista atividades acadêmicas de um curso específico."""
        return AtividadeAcademicaRepository.get_by_curso(curso_id)

    @staticmethod
    def listar_atividades_por_periodo(data_inicio: date, data_fim: date):
        """Lista atividades acadêmicas em um período específico."""
        return AtividadeAcademicaRepository.get_by_periodo(
            data_inicio, data_fim
        )

    @staticmethod
    def buscar_atividades(termo: str):
        """Busca atividades acadêmicas por termo."""
        return AtividadeAcademicaRepository.search(termo)

    @staticmethod
    @transaction.atomic
    def criar_atividade(dados: dict) -> AtividadeAcademica:
        """Cria uma nova atividade acadêmica."""
        # Validações básicas
        if not dados.get('nome'):
            raise ValidationError("Nome da atividade é obrigatório.")

        if not dados.get('data_inicio'):
            raise ValidationError("Data de início é obrigatória.")

        # Criar a atividade
        atividade = AtividadeAcademica.objects.create(**dados)
        return atividade

    @staticmethod
    @transaction.atomic
    def atualizar_atividade(
        atividade_id: int,
        dados: dict
    ) -> Optional[AtividadeAcademica]:
        """Atualiza uma atividade acadêmica existente."""
        atividade = AtividadeAcademicaRepository.get_by_id_or_none(
            atividade_id
        )
        if not atividade:
            return None

        for campo, valor in dados.items():
            setattr(atividade, campo, valor)

        atividade.save()
        return atividade

    @staticmethod
    @transaction.atomic
    def deletar_atividade(atividade_id: int) -> bool:
        """Deleta uma atividade acadêmica."""
        atividade = AtividadeAcademicaRepository.get_by_id_or_none(
            atividade_id
        )
        if not atividade:
            return False

        atividade.delete()
        return True


class AtividadeRitualisticaService:
    """Serviços para gerenciamento de atividades ritualísticas."""

    @staticmethod
    def listar_atividades():
        """Lista todas as atividades ritualísticas."""
        return AtividadeRitualisticaRepository.get_all()

    @staticmethod
    def obter_atividade_por_id(
        atividade_id: int
    ) -> Optional[AtividadeRitualistica]:
        """Obtém uma atividade ritualística por ID."""
        return AtividadeRitualisticaRepository.get_by_id_or_none(atividade_id)

    @staticmethod
    def listar_atividades_ativas():
        """Lista apenas as atividades ritualísticas ativas."""
        return AtividadeRitualisticaRepository.get_ativas()

    @staticmethod
    def listar_atividades_por_turma(turma_id: int):
        """Lista atividades ritualísticas de uma turma específica."""
        return AtividadeRitualisticaRepository.get_by_turma(turma_id)

    @staticmethod
    @transaction.atomic
    def criar_atividade(dados: dict) -> AtividadeRitualistica:
        """Cria uma nova atividade ritualística."""
        # Validações básicas
        if not dados.get('nome'):
            raise ValidationError("Nome da atividade é obrigatório.")

        if not dados.get('data'):
            raise ValidationError("Data é obrigatória.")

        # Criar a atividade
        atividade = AtividadeRitualistica.objects.create(**dados)
        return atividade

    @staticmethod
    @transaction.atomic
    def atualizar_atividade(
        atividade_id: int,
        dados: dict
    ) -> Optional[AtividadeRitualistica]:
        """Atualiza uma atividade ritualística existente."""
        atividade = AtividadeRitualisticaRepository.get_by_id_or_none(
            atividade_id
        )
        if not atividade:
            return None

        for campo, valor in dados.items():
            setattr(atividade, campo, valor)

        atividade.save()
        return atividade


class PresencaService:
    """Serviços para gerenciamento de presenças."""

    @staticmethod
    def registrar_presenca_academica(
        aluno_cpf: str,
        atividade_id: int,
        turma_id: int,
        presente: bool = True,
        registrado_por: str = "Sistema"
    ) -> PresencaAcademica:
        """Registra presença em uma atividade acadêmica."""
        atividade = AtividadeAcademicaRepository.get_by_id(atividade_id)

        presenca, created = PresencaAcademica.objects.get_or_create(
            aluno_id=aluno_cpf,
            atividade=atividade,
            turma_id=turma_id,
            data=atividade.data_inicio.date(),
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
    def registrar_presenca_ritualistica(
        aluno_cpf: str,
        atividade_id: int,
        turma_id: int,
        presente: bool = True,
        registrado_por: str = "Sistema"
    ) -> PresencaRitualistica:
        """Registra presença em uma atividade ritualística."""
        atividade = AtividadeRitualisticaRepository.get_by_id(atividade_id)

        presenca, created = PresencaRitualistica.objects.get_or_create(
            aluno_id=aluno_cpf,
            atividade=atividade,
            turma_id=turma_id,
            data=atividade.data,
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
    def obter_presencas_aluno_academicas(aluno_cpf: str):
        """Obtém todas as presenças acadêmicas de um aluno."""
        return PresencaAcademicaRepository.get_by_aluno(aluno_cpf)

    @staticmethod
    def obter_presencas_aluno_ritualisticas(aluno_cpf: str):
        """Obtém todas as presenças ritualísticas de um aluno."""
        return PresencaRitualisticaRepository.get_by_aluno(aluno_cpf)
