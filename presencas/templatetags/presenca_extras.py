from django import template

from presencas.reports import RELATORIOS

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Retorna o valor de 'key' em 'dictionary', ou {} se não existir.
    Útil para acessar dicionários aninhados em templates Django.
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key, {})
    return {}


@register.simple_tag
def get_relatorios_presencas():
    """Retorna a lista de relatórios disponíveis para presenças."""

    return RELATORIOS
