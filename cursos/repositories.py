"""
Repositórios para o app Cursos.
Este módulo contém todas as operações de acesso a dados do app cursos,
seguindo o padrão Repository para separar a lógica de negócio do acesso aos dados.
"""

from django.db.models import QuerySet, Q
from .models import Curso


class CursoRepository:
    """Repository para operações de acesso a dados do modelo Curso."""

    @staticmethod
    def get_all() -> QuerySet[Curso]:
        """Retorna todos os cursos ordenados por id."""
        return Curso.objects.all().order_by("id")

    @staticmethod
    def get_by_id(curso_id: int) -> Curso:
        """Busca um curso pelo ID."""
        return Curso.objects.get(pk=curso_id)

    @staticmethod
    def get_by_id_or_none(curso_id: int) -> Curso:
        """Busca um curso pelo ID, retorna None se não encontrar."""
        try:
            return Curso.objects.get(pk=curso_id)
        except Curso.DoesNotExist:
            return None

    @staticmethod
    def get_ativos() -> QuerySet[Curso]:
        """Retorna todos os cursos ativos."""
        return Curso.objects.filter(ativo=True).order_by("nome")

    @staticmethod
    def filter_by_nome(nome: str) -> QuerySet[Curso]:
        """Filtra cursos pelo nome (busca parcial, case-insensitive)."""
        return Curso.objects.filter(nome__icontains=nome)

    @staticmethod
    def search(termo: str) -> QuerySet[Curso]:
        """Busca cursos por nome ou descrição."""
        return Curso.objects.filter(
            Q(nome__icontains=termo) | Q(descricao__icontains=termo)
        )

    @staticmethod
    def create(nome: str, descricao: str = "", ativo: bool = True) -> Curso:
        """Cria um novo curso."""
        return Curso.objects.create(nome=nome, descricao=descricao, ativo=ativo)

    @staticmethod
    def update(curso: Curso, **dados) -> Curso:
        """Atualiza um curso com os dados fornecidos."""
        for campo, valor in dados.items():
            setattr(curso, campo, valor)
        curso.save()
        return curso

    @staticmethod
    def delete(curso: Curso) -> None:
        """Remove um curso do banco de dados."""
        curso.delete()

    @staticmethod
    def count() -> int:
        """Retorna o total de cursos."""
        return Curso.objects.count()

    @staticmethod
    def exists_by_nome(nome: str, exclude_id: int = None) -> bool:
        """Verifica se já existe um curso com o nome informado."""
        queryset = Curso.objects.filter(nome__iexact=nome)
        if exclude_id:
            queryset = queryset.exclude(pk=exclude_id)
        return queryset.exists()
