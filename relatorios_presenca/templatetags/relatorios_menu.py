from importlib import import_module
from urllib.parse import urlencode

from django import template
from django.conf import settings
from django.urls import NoReverseMatch, reverse

register = template.Library()


# Relatórios que não devem aparecer no menu (ex.: dashboards genéricos)
EXCLUDED_RELATORIO_URLS = {
    "alunos:painel",
}


def coletar_relatorios():
    relatorios = []
    for app in settings.INSTALLED_APPS:
        try:
            mod = import_module(f"{app}.reports")
            encontrados = getattr(mod, "RELATORIOS", [])
            if encontrados:
                relatorios.extend(
                    [
                        rel
                        for rel in encontrados
                        if rel.get("url") not in EXCLUDED_RELATORIO_URLS
                    ]
                )
        except ImportError:
            continue
        except Exception:
            continue
    return relatorios


def _reverse_safe(url_name, kwargs=None):
    if not url_name:
        return None
    try:
        return reverse(url_name, kwargs=kwargs or None)
    except NoReverseMatch:
        return None


def _montar_export_links(relatorio, link_base):
    exportacoes = relatorio.get("exportacoes") or []
    links = []
    for item in exportacoes:
        label = None
        destino = None

        if isinstance(item, dict):
            label = (
                item.get("label") or item.get("tipo") or item.get("formato") or "export"
            )
            destino = _reverse_safe(
                item.get("url_name") or relatorio.get("url"), item.get("kwargs")
            )
            query = item.get("query") or {}
            if destino and query:
                destino = f"{destino}?{urlencode(query, doseq=True)}"
        else:
            destino = link_base
            label = str(item)
            if destino:
                separador = "&" if "?" in destino else "?"
                destino = f"{destino}{separador}export={item}"

        if destino:
            links.append(
                {
                    "label": (label or "EXPORT").upper(),
                    "url": destino,
                }
            )

    return links


def preparar_relatorios():
    relatorios_brutos = coletar_relatorios()
    relatorios_normalizados = []

    for relatorio in relatorios_brutos:
        link = _reverse_safe(relatorio.get("url"))
        export_links = _montar_export_links(relatorio, link)

        relatorios_normalizados.append(
            {
                "nome": relatorio.get("nome"),
                "descricao": relatorio.get("descricao"),
                "link": link or "#",
                "export_links": export_links,
            }
        )

    return sorted(relatorios_normalizados, key=lambda item: item["nome"] or "")


# A tag agora é uma inclusion_tag
@register.inclusion_tag("templatetags/_relatorios_menu_items.html")
def render_relatorios_menu():
    """
    Renderiza o menu de relatórios usando um template dedicado.
    """
    return {"relatorios": preparar_relatorios()}
