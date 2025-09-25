from django import template
from alunos.reports import RELATORIOS

register = template.Library()


@register.simple_tag
def get_relatorios_alunos():
    """Retorna a lista de relatórios de alunos."""
    return RELATORIOS
