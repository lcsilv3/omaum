"""
Inicialização do pacote de views do aplicativo alunos.
Importa todas as views dos submodulos para disponibilizá-las no namespace 'alunos.views'.
"""
# Views relacionadas ao CRUD básico de alunos
from .aluno_views import (
    listar_alunos,
    criar_aluno,
    detalhar_aluno,
    editar_aluno,
    excluir_aluno,
)

# Views relacionadas a instrutores
from .instrutor_views import (
    confirmar_remocao_instrutoria,
    diagnostico_instrutores,
)

# Views relacionadas a relatórios e exportação
from .relatorio_views import (
    dashboard,
    exportar_alunos,
    importar_alunos,
    relatorio_alunos,
)

# Views relacionadas a endpoints de API
from .api_views import (
    search_alunos,
    search_instrutores,
    get_aluno,
    verificar_elegibilidade_instrutor_api as verificar_elegibilidade_instrutor,
)