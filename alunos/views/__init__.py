"""
Inicialização do pacote de views do aplicativo alunos.
Importa todas as views dos submodulos para disponibilizá-las no namespace 'alunos.views'.
"""

# Import views from submodules
from .aluno_views import *
from .api_views import *
from .instrutor_views import *
from .relatorio_views import *
from .mixins import *

# Explicitly import the function to ensure it's available
from .api_views import get_aluno_detalhes as get_aluno_detalhes

# Definir __all__ para evitar F401 errors
__all__ = [
    "listar_alunos",
    "criar_aluno",
    "editar_aluno",
    "detalhar_aluno",
    "excluir_aluno",
    "get_aluno_detalhes",
    "search_alunos",
    "search_instrutores",
    "listar_instrutores",
    "criar_instrutor",
    "editar_instrutor",
    "detalhar_instrutor",
    "excluir_instrutor",
    "confirmar_remocao_instrutoria",
    "diagnostico_instrutores",
    "relatorio_alunos",
    "exportar_alunos",
    "importar_alunos",
    "painel",
    "AlunoQuerysetMixin",
]
