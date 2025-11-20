from django import template

from turmas.reports import RELATORIOS

register = template.Library()


@register.filter
def div(value, arg):
    """Divide o valor pelo argumento."""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0


@register.filter
def mul(value, arg):
    """Multiplica o valor pelo argumento."""
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0


@register.simple_tag
def get_relatorios_turmas():
    """Retorna a lista de relatórios disponíveis para turmas."""
    return RELATORIOS
