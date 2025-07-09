"""
Repositórios para o app Atividades.
Este módulo contém todas as operações de acesso a dados relacionadas
a atividades, seguindo o padrão Repository para separar a lógica
de negócio do acesso aos dados.
"""

from django.db.models import QuerySet, Q
from datetime import date
from .models import (
    AtividadeAcademica,
    AtividadeRitualistica,
    PresencaAcademica,
    PresencaRitualistica
)


class AtividadeAcademicaRepository:
    """Repository para operações de acesso a dados de AtividadeAcademica."""
    
    @staticmethod
    def get_all() -> QuerySet[AtividadeAcademica]:
        """Retorna todas as atividades acadêmicas ordenadas por data."""
        return AtividadeAcademica.objects.all().order_by('-data_inicio')
    
    @staticmethod
    def get_by_id(atividade_id: int) -> AtividadeAcademica:
        """Busca uma atividade acadêmica pelo ID."""
        return AtividadeAcademica.objects.get(pk=atividade_id)
    
    @staticmethod
    def get_by_id_or_none(atividade_id: int) -> AtividadeAcademica:
        """Busca uma atividade acadêmica pelo ID, retorna None se não encontrar."""
        try:
            return AtividadeAcademica.objects.get(pk=atividade_id)
        except AtividadeAcademica.DoesNotExist:
            return None
    
    @staticmethod
    def get_ativas() -> QuerySet[AtividadeAcademica]:
        """Retorna todas as atividades acadêmicas ativas."""
        return AtividadeAcademica.objects.filter(ativo=True).order_by(
            '-data_inicio'
        )
    
    @staticmethod
    def get_by_turma(turma_id: int) -> QuerySet[AtividadeAcademica]:
        """Retorna atividades acadêmicas de uma turma específica."""
        return AtividadeAcademica.objects.filter(turmas__id=turma_id)
    
    @staticmethod
    def get_by_curso(curso_id: int) -> QuerySet[AtividadeAcademica]:
        """Retorna atividades acadêmicas de um curso específico."""
        return AtividadeAcademica.objects.filter(curso_id=curso_id)
    
    @staticmethod
    def get_by_periodo(
        data_inicio: date,
        data_fim: date
    ) -> QuerySet[AtividadeAcademica]:
        """Retorna atividades acadêmicas em um período específico."""
        return AtividadeAcademica.objects.filter(
            data_inicio__date__gte=data_inicio,
            data_inicio__date__lte=data_fim
        )
    
    @staticmethod
    def get_by_status(status: str) -> QuerySet[AtividadeAcademica]:
        """Retorna atividades acadêmicas por status."""
        return AtividadeAcademica.objects.filter(status=status)
    
    @staticmethod
    def filter_by_tipo(tipo: str) -> QuerySet[AtividadeAcademica]:
        """Filtra atividades acadêmicas por tipo."""
        return AtividadeAcademica.objects.filter(tipo_atividade=tipo)
    
    @staticmethod
    def search(termo: str) -> QuerySet[AtividadeAcademica]:
        """Busca atividades acadêmicas por nome ou descrição."""
        return AtividadeAcademica.objects.filter(
            Q(nome__icontains=termo) |
            Q(descricao__icontains=termo)
        )


class AtividadeRitualisticaRepository:
    """Repository para operações de acesso a dados de AtividadeRitualistica."""
    
    @staticmethod
    def get_all() -> QuerySet[AtividadeRitualistica]:
        """Retorna todas as atividades ritualísticas ordenadas por data."""
        return AtividadeRitualistica.objects.all().order_by('-data')
    
    @staticmethod
    def get_by_id(atividade_id: int) -> AtividadeRitualistica:
        """Busca uma atividade ritualística pelo ID."""
        return AtividadeRitualistica.objects.get(pk=atividade_id)
    
    @staticmethod
    def get_by_id_or_none(atividade_id: int) -> AtividadeRitualistica:
        """Busca uma atividade ritualística pelo ID, retorna None se não encontrar."""
        try:
            return AtividadeRitualistica.objects.get(pk=atividade_id)
        except AtividadeRitualistica.DoesNotExist:
            return None
    
    @staticmethod
    def get_ativas() -> QuerySet[AtividadeRitualistica]:
        """Retorna todas as atividades ritualísticas ativas."""
        return AtividadeRitualistica.objects.filter(ativo=True).order_by(
            '-data'
        )
    
    @staticmethod
    def get_by_turma(turma_id: int) -> QuerySet[AtividadeRitualistica]:
        """Retorna atividades ritualísticas de uma turma específica."""
        return AtividadeRitualistica.objects.filter(turma_id=turma_id)
    
    @staticmethod
    def get_by_periodo(
        data_inicio: date,
        data_fim: date
    ) -> QuerySet[AtividadeRitualistica]:
        """Retorna atividades ritualísticas em um período específico."""
        return AtividadeRitualistica.objects.filter(
            data__gte=data_inicio,
            data__lte=data_fim
        )
    
    @staticmethod
    def get_by_status(status: str) -> QuerySet[AtividadeRitualistica]:
        """Retorna atividades ritualísticas por status."""
        return AtividadeRitualistica.objects.filter(status=status)


class PresencaAcademicaRepository:
    """Repository para operações de acesso a dados de PresencaAcademica."""
    
    @staticmethod
    def get_all() -> QuerySet[PresencaAcademica]:
        """Retorna todas as presenças acadêmicas."""
        return PresencaAcademica.objects.all().order_by('-data')
    
    @staticmethod
    def get_by_aluno(aluno_cpf: str) -> QuerySet[PresencaAcademica]:
        """Retorna presenças acadêmicas de um aluno específico."""
        return PresencaAcademica.objects.filter(aluno__cpf=aluno_cpf)
    
    @staticmethod
    def get_by_atividade(atividade_id: int) -> QuerySet[PresencaAcademica]:
        """Retorna presenças acadêmicas de uma atividade específica."""
        return PresencaAcademica.objects.filter(atividade_id=atividade_id)
    
    @staticmethod
    def get_by_turma(turma_id: int) -> QuerySet[PresencaAcademica]:
        """Retorna presenças acadêmicas de uma turma específica."""
        return PresencaAcademica.objects.filter(turma_id=turma_id)


class PresencaRitualisticaRepository:
    """Repository para operações de acesso a dados de PresencaRitualistica."""
    
    @staticmethod
    def get_all() -> QuerySet[PresencaRitualistica]:
        """Retorna todas as presenças ritualísticas."""
        return PresencaRitualistica.objects.all().order_by('-data')
    
    @staticmethod
    def get_by_aluno(aluno_cpf: str) -> QuerySet[PresencaRitualistica]:
        """Retorna presenças ritualísticas de um aluno específico."""
        return PresencaRitualistica.objects.filter(aluno__cpf=aluno_cpf)
    
    @staticmethod
    def get_by_atividade(atividade_id: int) -> QuerySet[PresencaRitualistica]:
        """Retorna presenças ritualísticas de uma atividade específica."""
        return PresencaRitualistica.objects.filter(atividade_id=atividade_id)
    
    @staticmethod
    def get_by_turma(turma_id: int) -> QuerySet[PresencaRitualistica]:
        """Retorna presenças ritualísticas de uma turma específica."""
        return PresencaRitualistica.objects.filter(turma_id=turma_id)
