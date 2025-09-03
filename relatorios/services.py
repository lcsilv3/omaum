"""
Serviços para o app relatorios.
"""

from typing import Optional
from django.db.models import QuerySet
from .models import Relatorio
from .repositories import RelatorioRepository


class RelatorioService:
    """Serviço para lógica de negócio relacionada a Relatorio."""

    def __init__(self):
        self.repository = RelatorioRepository()

    def listar_todos(self) -> QuerySet[Relatorio]:
        """Lista todos os relatórios."""
        return self.repository.get_all()

    def obter_por_id(self, relatorio_id: int) -> Optional[Relatorio]:
        """Obtém um relatório por ID."""
        return self.repository.get_by_id(relatorio_id)

    def criar_relatorio(self, titulo: str, conteudo: str) -> Relatorio:
        """Cria um novo relatório."""
        # Validações de negócio
        if not titulo or not titulo.strip():
            raise ValueError("O título do relatório é obrigatório")

        if not conteudo or not conteudo.strip():
            raise ValueError("O conteúdo do relatório é obrigatório")

        # Verifica se já existe um relatório com o mesmo título
        if self.repository.buscar_por_titulo(titulo.strip()).exists():
            raise ValueError("Já existe um relatório com este título")

        return self.repository.create(titulo=titulo.strip(), conteudo=conteudo.strip())

    def atualizar_relatorio(
        self, relatorio_id: int, titulo: str = None, conteudo: str = None
    ) -> Optional[Relatorio]:
        """Atualiza um relatório existente."""
        relatorio = self.repository.get_by_id(relatorio_id)
        if not relatorio:
            return None

        # Validações de negócio
        if titulo is not None:
            if not titulo.strip():
                raise ValueError("O título do relatório não pode estar vazio")

            # Verifica se já existe outro relatório com o mesmo título
            existing = self.repository.buscar_por_titulo(titulo.strip())
            if existing.exclude(id=relatorio_id).exists():
                raise ValueError("Já existe um relatório com este título")

        if conteudo is not None:
            if not conteudo.strip():
                raise ValueError("O conteúdo do relatório não pode estar vazio")

        return self.repository.update(
            relatorio,
            titulo=titulo.strip() if titulo else None,
            conteudo=conteudo.strip() if conteudo else None,
        )

    def excluir_relatorio(self, relatorio_id: int) -> bool:
        """Remove um relatório."""
        relatorio = self.repository.get_by_id(relatorio_id)
        if not relatorio:
            return False

        return self.repository.delete(relatorio)

    def buscar_relatorios(self, termo: str) -> QuerySet[Relatorio]:
        """Busca relatórios por termo."""
        if not termo or not termo.strip():
            return self.repository.get_all()

        return self.repository.buscar_geral(termo.strip())

    def obter_relatorios_ordenados(self) -> QuerySet[Relatorio]:
        """Obtém relatórios ordenados por data de criação."""
        return self.repository.get_ordenados_por_data()

    def obter_estatisticas(self) -> dict:
        """Obtém estatísticas dos relatórios."""
        return {
            "total_relatorios": self.repository.count(),
            "relatorios_recentes": self.repository.get_ordenados_por_data()[:5],
        }
