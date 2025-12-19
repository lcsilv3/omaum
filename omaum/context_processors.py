"""
Context Processors para o projeto OMAUM.
Este módulo adiciona variáveis globais ao contexto do Django.
"""

import logging
from django.conf import settings
from pagamentos.views.dashboard_views import get_pagamento_model

logger = logging.getLogger(__name__)

# pylint: disable=no-member


def pagamentos_context(request):
    """
    Adiciona a variável pagamentos_atrasados_count ao contexto global.
    """
    Pagamento = get_pagamento_model()  # noqa: E1101

    if request.user.is_authenticated:
        pagamentos_atrasados_qs = Pagamento.objects.filter(status="ATRASADO").select_related('aluno')
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


def environment_context(_request):
    """Expõe informações do ambiente atual para o frontend."""

    label = getattr(settings, "ENVIRONMENT_LABEL", "Ambiente não configurado")
    css_classes = getattr(
        settings, "ENVIRONMENT_BADGE_CLASSES", "bg-secondary text-white"
    )
    hint = getattr(settings, "ENVIRONMENT_HINT", "")
    show_banner = getattr(settings, "ENVIRONMENT_SHOW_BANNER", True)

    return {
        "environment_banner": {
            "label": label,
            "classes": css_classes,
            "hint": hint,
            "show": show_banner,
        }
    }
