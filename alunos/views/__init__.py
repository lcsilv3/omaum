from .main import (
    listar_alunos_view,
    criar_aluno,
    detalhar_aluno,
    editar_aluno,
    excluir_aluno,
    search_alunos,
)
from .relatorio_views import painel, exportar_alunos, importar_alunos, relatorio_alunos
from .instrutor_views import confirmar_remocao_instrutoria, diagnostico_instrutores
from .aluno_views import (
    listar_tipos_codigos_ajax,
    listar_codigos_por_tipo_ajax,
    adicionar_evento_historico_ajax,
    historico_iniciatico_paginado_ajax,
)
