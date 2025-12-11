from django import template
from frequencias.reports import RELATORIOS

register = template.Library()


@register.filter
def sub(value, arg):
    """Subtrai o argumento do valor"""
    return value - arg


@register.simple_tag
def get_relatorios_frequencias():
    """Retorna a lista de relatórios do app Frequências."""
    return RELATORIOS
