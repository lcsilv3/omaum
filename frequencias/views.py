"""
Views para o aplicativo de frequências.

Este arquivo agora funciona como um agregador que importa todas as funções
dos módulos separados para manter a compatibilidade com o código existente.
"""

import logging

from .views.frequencia_mensal import (
    listar_frequencias,
    criar_frequencia_mensal,
    editar_frequencia_mensal,
    excluir_frequencia_mensal,
    detalhar_frequencia_mensal,
    recalcular_carencias
)

from .views.carencia import (
    editar_carencia,
    resolver_carencia,
    detalhar_carencia,
    iniciar_acompanhamento
)

from .views.notificacao import (
    criar_notificacao,
    detalhar_notificacao,
    editar_notificacao,
    enviar_notificacao,
    reenviar_notificacao,
    responder_aluno,
    listar_notificacoes_carencia
)

from .views.relatorio import (
    relatorio_frequencias,
    exportar_frequencia_csv,
    historico_frequencia,
    exportar_historico
)

from .views.dashboard import (
    dashboard,
    painel_frequencias,
    visualizar_painel_frequencias
)

from .views.api_views import (
    obter_dados_frequencia,
    obter_dados_painel_frequencias
)

# Importar funções utilitárias do módulo utils
from .utils import (
    get_models,
    get_forms,
    get_turma_model,
    get_model_dynamically
)

# Configurar logger
logger = logging.getLogger(__name__)