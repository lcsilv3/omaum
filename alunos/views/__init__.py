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