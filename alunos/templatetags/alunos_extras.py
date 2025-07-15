import os
from django import template

register = template.Library()


@register.filter
def file_exists(filepath):
    return os.path.exists(filepath)
