from django import template
from importlib import import_module
from django.conf import settings

register = template.Library()


def coletar_relatorios():
    relatorios = []
    for app in settings.INSTALLED_APPS:
        try:
            mod = import_module(f"{app}.reports")
            relatorios += getattr(mod, "RELATORIOS", [])
        except ModuleNotFoundError:
            continue
    return relatorios


@register.simple_tag
def listar_relatorios():
    return coletar_relatorios()
