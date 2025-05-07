# Importar funções utilitárias
from .utils import get_return_url, get_form_class, get_model_class

# Importar funções de visualização principal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def listar_atividades(request):
    """Página inicial do módulo de atividades."""
    return render(request, "atividades/listar_atividades.html")

# Importar funções de atividades acadêmicas
from .academicas import (
    listar_atividades_academicas,
    criar_atividade_academica,
    editar_atividade_academica,
    excluir_atividade_academica,
    confirmar_exclusao_academica,
    detalhar_atividade_academica,
    copiar_atividade_academica,
)

# Importar funções de atividades ritualísticas
from .ritualisticas import (
    listar_atividades_ritualisticas,
    criar_atividade_ritualistica,
    editar_atividade_ritualistica,
    excluir_atividade_ritualistica,
    confirmar_exclusao_ritualistica,
    detalhar_atividade_ritualistica,
    copiar_atividade_ritualistica,
)

# Importar funções de calendário
from .calendario import (
    calendario_atividades,
    api_eventos_calendario,
    api_detalhe_evento,
)

# Importar funções de relatórios
from .relatorios import (
    relatorio_atividades,
    exportar_atividades,
)

# Importar funções de dashboard
from .dashboard import dashboard_atividades

from .importacao import importar_atividades