# presencas/views/__init__.py

# Importar funções de listagem
from .listagem import (
    listar_presencas
)

# Importar funções de atividade
from .atividade import (
    registrar_presencas_atividade,
    editar_presenca
)

# Importar funções de múltiplas presenças
from .multiplas import (
    registrar_presencas_multiplas,
    formulario_presencas_multiplas
)

# Expor todas as funções para que possam ser importadas de presencas.views
__all__ = [
    'listar_presencas',
    'registrar_presencas_atividade',
    'editar_presenca',
    'registrar_presencas_multiplas',
    'formulario_presencas_multiplas'
]