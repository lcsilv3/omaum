from django import template
from alunos.reports import RELATORIOS

register = template.Library()


@register.inclusion_tag("alunos/_dropdown_relatorios_alunos.html")
def dropdown_relatorios_alunos():
    return {"relatorios_alunos": RELATORIOS}
