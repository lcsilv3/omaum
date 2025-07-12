"""
Template tags para o consolidado de presenças.
"""
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Obtém um item de um dicionário usando uma chave.
    
    Usage: {{ dict|get_item:key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def multiply(value, arg):
    """
    Multiplica um valor por outro.
    
    Usage: {{ value|multiply:arg }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def percentage(value, total):
    """
    Calcula percentual de um valor em relação ao total.
    
    Usage: {{ value|percentage:total }}
    """
    try:
        if float(total) == 0:
            return 0
        return (float(value) / float(total)) * 100
    except (ValueError, TypeError):
        return 0


@register.filter
def format_percentage(value):
    """
    Formata um valor como percentual.
    
    Usage: {{ value|format_percentage }}
    """
    try:
        return f"{float(value):.1f}%"
    except (ValueError, TypeError):
        return "0.0%"


@register.simple_tag
def url_replace(request, field, value):
    """
    Substitui um parâmetro na URL mantendo os outros.
    
    Usage: {% url_replace request 'page' 2 %}
    """
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.simple_tag
def url_remove(request, field):
    """
    Remove um parâmetro da URL mantendo os outros.
    
    Usage: {% url_remove request 'page' %}
    """
    dict_ = request.GET.copy()
    if field in dict_:
        del dict_[field]
    return dict_.urlencode()


@register.inclusion_tag('presencas/consolidado/partials/pagination.html')
def pagination_atividades(page_obj, request):
    """
    Renderiza paginação para atividades.
    
    Usage: {% pagination_atividades page_obj request %}
    """
    return {
        'page_obj': page_obj,
        'request': request,
    }


@register.inclusion_tag('presencas/consolidado/partials/celula_editavel.html')
def celula_editavel(presenca_id, campo, valor, pode_editar=True):
    """
    Renderiza célula editável.
    
    Usage: {% celula_editavel presenca.id 'convocacoes' presenca.convocacoes %}
    """
    return {
        'presenca_id': presenca_id,
        'campo': campo,
        'valor': valor,
        'pode_editar': pode_editar,
    }


@register.inclusion_tag('presencas/consolidado/partials/percentual_cell.html')
def percentual_cell(percentual):
    """
    Renderiza célula de percentual com cores.
    
    Usage: {% percentual_cell presenca.percentual_presenca %}
    """
    css_class = 'percentual-alto'
    if percentual < 50:
        css_class = 'percentual-baixo'
    elif percentual < 75:
        css_class = 'percentual-medio'
    
    return {
        'percentual': percentual,
        'css_class': css_class,
    }


@register.filter
def is_baixo_percentual(percentual):
    """
    Verifica se percentual é baixo (< 50%).
    
    Usage: {{ percentual|is_baixo_percentual }}
    """
    try:
        return float(percentual) < 50
    except (ValueError, TypeError):
        return False


@register.filter
def is_medio_percentual(percentual):
    """
    Verifica se percentual é médio (50% <= x < 75%).
    
    Usage: {{ percentual|is_medio_percentual }}
    """
    try:
        valor = float(percentual)
        return 50 <= valor < 75
    except (ValueError, TypeError):
        return False


@register.filter
def is_alto_percentual(percentual):
    """
    Verifica se percentual é alto (>= 75%).
    
    Usage: {{ percentual|is_alto_percentual }}
    """
    try:
        return float(percentual) >= 75
    except (ValueError, TypeError):
        return False


@register.simple_tag
def get_percentual_class(percentual):
    """
    Retorna classe CSS baseada no percentual.
    
    Usage: {% get_percentual_class percentual %}
    """
    try:
        valor = float(percentual)
        if valor < 50:
            return 'percentual-baixo'
        elif valor < 75:
            return 'percentual-medio'
        else:
            return 'percentual-alto'
    except (ValueError, TypeError):
        return 'percentual-baixo'


@register.simple_tag
def build_filter_url(request, **kwargs):
    """
    Constrói URL com filtros.
    
    Usage: {% build_filter_url request turma_id=1 curso_id=2 %}
    """
    dict_ = request.GET.copy()
    for key, value in kwargs.items():
        if value:
            dict_[key] = value
        elif key in dict_:
            del dict_[key]
    return dict_.urlencode()
