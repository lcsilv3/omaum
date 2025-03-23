from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    """Subtrai o argumento do valor"""
    return value - arg
