from django import template
from django.utils import timezone
from ..models import ConfiguracaoCorporativa

register = template.Library()


@register.inclusion_tag("corporativo/cabecalho_relatorio.html")
def cabecalho_relatorio(titulo_relatorio):
    config = ConfiguracaoCorporativa.get_configuracao()
    return {
        "config": config,
        "titulo_relatorio": titulo_relatorio,
        "data_hora_atual": timezone.now(),
    }


@register.inclusion_tag("corporativo/rodape_relatorio.html")
def rodape_relatorio(numero_pagina=None):
    config = ConfiguracaoCorporativa.get_configuracao()
    return {
        "config": config,
        "numero_pagina": numero_pagina,
    }


@register.simple_tag
def nome_organizacao():
    config = ConfiguracaoCorporativa.get_configuracao()
    return config.nome_organizacao


@register.simple_tag
def data_hora_formatada():
    config = ConfiguracaoCorporativa.get_configuracao()
    return timezone.now().strftime(config.formato_data_hora)
