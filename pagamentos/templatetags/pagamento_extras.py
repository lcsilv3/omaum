from django import template

from pagamentos.reports import RELATORIOS

register = template.Library()


@register.simple_tag
def get_relatorios_pagamentos():
    """Retorna a lista de relatórios disponíveis para o app Pagamentos."""

    return RELATORIOS
