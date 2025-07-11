"""
Repositórios para o app Atividades.
Este módulo contém todas as operações de acesso a dados relacionadas
a atividades, seguindo o padrão Repository para separar a lógica
de negócio do acesso aos dados.
"""

from django.db.models import QuerySet, Q
from datetime import date
from .models import Atividade, Presenca


class AtividadeRepository:
    """Repository para operações de acesso a dados de Atividade."""
    
    @staticmethod
    def get_all() -> QuerySet[Atividade]:
        """Retorna todas as atividades ordenadas por data."""
        return Atividade.objects.all().order_by('-data_inicio')
    
    @staticmethod
    def get_by_id(atividade_id: int) -> Atividade:
        """Busca uma atividade pelo ID."""
        return Atividade.objects.get(pk=atividade_id)
    
    @staticmethod
    def get_by_id_or_none(atividade_id: int) -> Atividade:
        """Busca uma atividade pelo ID, retorna None se não encontrar."""
        try:
            return Atividade.objects.get(pk=atividade_id)
        except Atividade.DoesNotExist:
            return None
    
    @staticmethod
    def get_ativas() -> QuerySet[Atividade]:
        """Retorna todas as atividades ativas."""
        return Atividade.objects.filter(ativo=True).order_by('-data_inicio')
    
    @staticmethod
    def get_by_turma(turma_id: int) -> QuerySet[Atividade]:
        """Retorna atividades de uma turma específica."""
        return Atividade.objects.filter(turmas__id=turma_id)
    
    @staticmethod
    def get_by_curso(curso_id: int) -> QuerySet[Atividade]:
        """Retorna atividades de um curso específico."""
        return Atividade.objects.filter(curso_id=curso_id)
    
    @staticmethod
    def get_by_periodo(data_inicio: date, data_fim: date) -> QuerySet[Atividade]:
        """Retorna atividades em um período específico."""
        return Atividade.objects.filter(
            data_inicio__gte=data_inicio,
            data_inicio__lte=data_fim
        )
    
    @staticmethod
    def get_by_status(status: str) -> QuerySet[Atividade]:
        """Retorna atividades por status."""
        return Atividade.objects.filter(status=status)
    
    @staticmethod
    def filter_by_tipo(tipo: str) -> QuerySet[Atividade]:
        """Filtra atividades por tipo."""
        return Atividade.objects.filter(tipo_atividade=tipo)
    
    @staticmethod
    def search(termo: str) -> QuerySet[Atividade]:
        """Busca atividades por nome ou descrição."""
        return Atividade.objects.filter(
            Q(nome__icontains=termo) |
            Q(descricao__icontains=termo)
        )


class PresencaRepository:
    """Repository para operações de acesso a dados de Presenca."""
    
    @staticmethod
    def get_all() -> QuerySet[Presenca]:
        """Retorna todas as presenças."""
        return Presenca.objects.all().order_by('-data')
    
    @staticmethod
    def get_by_id(presenca_id: int) -> Presenca:
        """Busca uma presença pelo ID."""
        return Presenca.objects.get(pk=presenca_id)
    
    @staticmethod
    def get_by_id_or_none(presenca_id: int) -> Presenca:
        """Busca uma presença pelo ID, retorna None se não encontrar."""
        try:
            return Presenca.objects.get(pk=presenca_id)
        except Presenca.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_aluno(aluno_id: int) -> QuerySet[Presenca]:
        """Retorna presenças de um aluno específico."""
        return Presenca.objects.filter(aluno_id=aluno_id)
    
    @staticmethod
    def get_by_atividade(atividade_id: int) -> QuerySet[Presenca]:
        """Retorna presenças de uma atividade específica."""
        return Presenca.objects.filter(atividade_id=atividade_id)
    
    @staticmethod
    def get_by_turma(turma_id: int) -> QuerySet[Presenca]:
        """Retorna presenças de uma turma específica."""
        return Presenca.objects.filter(turma_id=turma_id)
    
    @staticmethod
    def get_by_aluno_e_atividade(aluno_id: int, 
                                atividade_id: int) -> QuerySet[Presenca]:
        """Retorna presenças de um aluno em uma atividade específica."""
        return Presenca.objects.filter(
            aluno_id=aluno_id,
            atividade_id=atividade_id
        )
    
    @staticmethod
    def get_presentes(atividade_id: int) -> QuerySet[Presenca]:
        """Retorna apenas presenças marcadas como presente."""
        return Presenca.objects.filter(
            atividade_id=atividade_id,
            presente=True
        )
    
    @staticmethod
    def get_ausentes(atividade_id: int) -> QuerySet[Presenca]:
        """Retorna apenas presenças marcadas como ausente."""
        return Presenca.objects.filter(
            atividade_id=atividade_id,
            presente=False
        )
