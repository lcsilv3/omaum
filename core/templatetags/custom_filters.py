from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Obtém um item de um dicionário pelo valor da chave.
    Útil para acessar valores de dicionários em templates.
    """
    return dictionary.get(key)

@register.filter
def subtract(value, arg):
    """
    Subtrai o argumento do valor.
    """
    return value - arg

@register.filter
@stringfilter
def truncate_middle(value, arg):
    """
    Trunca uma string no meio, substituindo os caracteres do meio por '...'.
    O argumento é o comprimento total desejado.
    """
    try:
        length = int(arg)
    except ValueError:
        return value
    
    if len(value) <= length:
        return value
    
    # Calcular quantos caracteres manter em cada extremidade
    half_length = (length - 3) // 2
    if half_length < 1:
        half_length = 1
    
    return value[:half_length] + '...' + value[-half_length:]