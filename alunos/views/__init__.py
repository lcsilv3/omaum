from importlib import import_module

main = import_module("alunos.views.main")
relatorio_views = import_module("alunos.views.relatorio_views")
api_views = import_module("alunos.api_views")
from .main import (
    listar_alunos_view,
    criar_aluno,
    detalhar_aluno,
    editar_aluno,
    excluir_aluno,
    search_alunos,
)
from .relatorio_views import (
    painel,
    relatorio_ficha_cadastral,
    relatorio_dados_iniciaticos,
    relatorio_historico_aluno,
    relatorio_auditoria_dados,
    relatorio_demografico,
    relatorio_aniversariantes,
)
from .instrutor_views import confirmar_remocao_instrutoria, diagnostico_instrutores
from .aluno_views import (
    listar_tipos_codigos_ajax,
    listar_codigos_por_tipo_ajax,
    adicionar_evento_historico_ajax,
    historico_iniciatico_paginado_ajax,
)

__all__ = [
    "main",
    "relatorio_views",
    "api_views",
    "listar_alunos_view",
    "criar_aluno",
    "detalhar_aluno",
    "editar_aluno",
    "excluir_aluno",
    "search_alunos",
    "painel",
    "relatorio_ficha_cadastral",
    "relatorio_dados_iniciaticos",
    "relatorio_historico_aluno",
    "relatorio_auditoria_dados",
    "relatorio_demografico",
    "relatorio_aniversariantes",
    "confirmar_remocao_instrutoria",
    "diagnostico_instrutores",
    "listar_tipos_codigos_ajax",
    "listar_codigos_por_tipo_ajax",
    "adicionar_evento_historico_ajax",
    "historico_iniciatico_paginado_ajax",
]
