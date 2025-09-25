from django import template
from importlib import import_module
from django.conf import settings

register = template.Library()


# A lógica de coleta permanece a mesma
def coletar_relatorios():
    relatorios = []
    for app in settings.INSTALLED_APPS:
        try:
            mod = import_module(f"{app}.reports")
            encontrados = getattr(mod, "RELATORIOS", [])
            if encontrados:
                relatorios.extend(encontrados)
        except ImportError:
            continue
        except Exception:
            continue
    return relatorios


# A tag agora é uma inclusion_tag
@register.inclusion_tag("templatetags/_relatorios_menu_items.html")
def render_relatorios_menu():
    """
    Renderiza o menu de relatórios usando um template dedicado.
    """
    todos_relatorios = coletar_relatorios()
    # Passa a lista de relatórios para o template da tag
    return {"relatorios": todos_relatorios}
