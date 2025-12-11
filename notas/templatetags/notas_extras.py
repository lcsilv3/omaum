from django import template

from notas.reports import RELATORIOS

register = template.Library()


@register.simple_tag
def get_relatorios_notas():
    """Retorna a lista de relatórios disponíveis para o app Notas."""

    return RELATORIOS
