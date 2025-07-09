"""
Repositório para o app relatorios.
"""
from typing import Optional
from django.db.models import QuerySet
from django.db.models import Q
from .models import Relatorio


class RelatorioRepository:
    """Repository para operações relacionadas a Relatorio."""
    
    @staticmethod
    def get_all() -> QuerySet[Relatorio]:
        """Retorna todos os relatórios."""
        return Relatorio.objects.all()
    
    @staticmethod
    def get_by_id(relatorio_id: int) -> Optional[Relatorio]:
        """Retorna um relatório pelo ID."""
        try:
            return Relatorio.objects.get(id=relatorio_id)
        except Relatorio.DoesNotExist:
            return None
    
    @staticmethod
    def create(titulo: str, conteudo: str) -> Relatorio:
        """Cria um novo relatório."""
        return Relatorio.objects.create(
            titulo=titulo,
            conteudo=conteudo
        )
    
    @staticmethod
    def update(relatorio: Relatorio, titulo: str = None,
               conteudo: str = None) -> Relatorio:
        """Atualiza um relatório existente."""
        if titulo is not None:
            relatorio.titulo = titulo
        if conteudo is not None:
            relatorio.conteudo = conteudo
        relatorio.save()
        return relatorio
    
    @staticmethod
    def delete(relatorio: Relatorio) -> bool:
        """Remove um relatório."""
        try:
            relatorio.delete()
            return True
        except Exception:
            return False
    
    @staticmethod
    def buscar_por_titulo(titulo: str) -> QuerySet[Relatorio]:
        """Busca relatórios por título."""
        return Relatorio.objects.filter(
            titulo__icontains=titulo
        )
    
    @staticmethod
    def buscar_por_conteudo(conteudo: str) -> QuerySet[Relatorio]:
        """Busca relatórios por conteúdo."""
        return Relatorio.objects.filter(
            conteudo__icontains=conteudo
        )
    
    @staticmethod
    def buscar_geral(termo: str) -> QuerySet[Relatorio]:
        """Busca geral em títulos e conteúdos."""
        return Relatorio.objects.filter(
            Q(titulo__icontains=termo) |
            Q(conteudo__icontains=termo)
        )
    
    @staticmethod
    def get_ordenados_por_data() -> QuerySet[Relatorio]:
        """Retorna relatórios ordenados pela data de criação
        (mais recentes primeiro)."""
        return Relatorio.objects.order_by('-data_criacao')
    
    @staticmethod
    def count() -> int:
        """Retorna o número total de relatórios."""
        return Relatorio.objects.count()
