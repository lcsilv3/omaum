"""
Módulo base com funções e classes utilitárias compartilhadas entre as views.
"""

import logging
from importlib import import_module
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


def get_pagamento_model():
    """Obtém o modelo Pagamento dinamicamente."""
    pagamentos_module = import_module("pagamentos.models")
    return getattr(pagamentos_module, "Pagamento")


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_pagamento_or_404(pagamento_id):
    """Obtém um pagamento pelo ID ou retorna 404."""
    Pagamento = get_pagamento_model()
    return get_object_or_404(Pagamento, id=pagamento_id)


# Verificar disponibilidade de bibliotecas para exportação
import importlib.util

EXCEL_AVAILABLE = importlib.util.find_spec("xlsxwriter") is not None
PDF_AVAILABLE = importlib.util.find_spec("weasyprint") is not None


# Decorator composto para views que precisam de autenticação e modelo de pagamento
def pagamento_view(view_func):
    """
    Decorator que combina login_required e fornece o modelo Pagamento.
    Também captura exceções comuns.
    """

    @login_required
    def wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Erro na view {view_func.__name__}: {str(e)}", exc_info=True)
            from django.contrib import messages

            messages.error(request, f"Erro: {str(e)}")
            from django.shortcuts import redirect

            return redirect("pagamentos:listar_pagamentos")

    return wrapped_view
