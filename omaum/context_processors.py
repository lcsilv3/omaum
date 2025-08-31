"""
Context Processors para o projeto OMAUM.
Este módulo adiciona variáveis globais ao contexto do Django.
"""

import logging
from pagamentos.views.dashboard_views import get_pagamento_model

logger = logging.getLogger(__name__)

# pylint: disable=no-member


def pagamentos_context(request):
    """
    Adiciona a variável pagamentos_atrasados_count ao contexto global.
    """
    Pagamento = get_pagamento_model()  # noqa: E1101

    if request.user.is_authenticated:
        pagamentos_atrasados_qs = Pagamento.objects.filter(status="ATRASADO")
        pagamentos_atrasados = list(pagamentos_atrasados_qs)
        pagamentos_atrasados_count = pagamentos_atrasados_qs.count()
    else:
        pagamentos_atrasados = []
        pagamentos_atrasados_count = 0

    logger.debug(
        "Context processor executado: pagamentos_atrasados_count=%d",
        pagamentos_atrasados_count,
    )
    return {
        "pagamentos_atrasados_count": pagamentos_atrasados_count,
        "pagamentos_atrasados": pagamentos_atrasados,
    }
