"""Reexports de modelos iniciáticos para compatibilidade sem registrar novos modelos.

Este módulo NÃO declara novos models.Model; apenas reexporta as classes
originais do app 'alunos'. Assim evitamos conflito de db_table (E028).

Uso futuro: remover imports em código legado e referenciar diretamente
alunos.models.TipoCodigo / alunos.models.Codigo.
"""

from alunos.models import TipoCodigo, Codigo  # noqa: F401

__all__ = ["TipoCodigo", "Codigo"]
