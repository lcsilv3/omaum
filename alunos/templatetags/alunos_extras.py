import os
from django import template

register = template.Library()


@register.filter
def file_exists(filepath):
    return os.path.exists(filepath)


@register.filter
def mask_cpf(value):
    """Aplica máscara de CPF (000.000.000-00) se possível."""
    from alunos.utils import mask_cpf as mask

    return mask(str(value)) if value else ""
