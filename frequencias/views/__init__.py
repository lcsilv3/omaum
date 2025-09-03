"""
Pacote de views para o aplicativo de frequências.
Este arquivo permite que o diretório views seja tratado como um pacote Python.
"""

# Importar todas as funções de views que você quer expor
from .frequencia_mensal import (
    listar_frequencias,
    criar_frequencia_mensal,
    editar_frequencia_mensal,
    excluir_frequencia_mensal,
    detalhar_frequencia_mensal,
    recalcular_carencias,
)

from .carencia import (
    editar_carencia,
    resolver_carencia,
    detalhar_carencia,
    iniciar_acompanhamento,
)

from .notificacao import (
    criar_notificacao,
    detalhar_notificacao,
    editar_notificacao,
    enviar_notificacao,
    reenviar_notificacao,
    responder_aluno,
    listar_notificacoes_carencia,
)

from .relatorio import (
    relatorio_frequencias,
    exportar_frequencia_csv,
    historico_frequencia,
    exportar_historico,
)

from .dashboard import dashboard, painel_frequencias, visualizar_painel_frequencias

from .api_views import obter_dados_frequencia, obter_dados_painel_frequencias

# Importar as novas funções
from .exportacao import exportar_frequencias, importar_frequencias

__all__ = [
    "listar_frequencias",
    "criar_frequencia_mensal",
    "editar_frequencia_mensal",
    "excluir_frequencia_mensal",
    "detalhar_frequencia_mensal",
    "recalcular_carencias",
    "editar_carencia",
    "resolver_carencia",
    "detalhar_carencia",
    "iniciar_acompanhamento",
    "criar_notificacao",
    "detalhar_notificacao",
    "editar_notificacao",
    "enviar_notificacao",
    "reenviar_notificacao",
    "responder_aluno",
    "listar_notificacoes_carencia",
    "relatorio_frequencias",
    "exportar_frequencia_csv",
    "historico_frequencia",
    "exportar_historico",
    "dashboard",
    "painel_frequencias",
    "visualizar_painel_frequencias",
    "obter_dados_frequencia",
    "obter_dados_painel_frequencias",
    "exportar_frequencias",
    "importar_frequencias",
]
