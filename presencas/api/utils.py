"""
Utilitários para API do sistema de presenças.
"""

from django.http import JsonResponse
from rest_framework.throttling import SimpleRateThrottle
import logging

logger = logging.getLogger(__name__)


class PresencasAPIThrottle(SimpleRateThrottle):
    """
    Throttle customizado para API de presenças.
    Controla a taxa de requisições por usuário.
    """
    
    scope = 'presencas_api'
    
    def get_cache_key(self, request, view):
        """
        Gera chave de cache baseada no usuário.
        """
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


def api_response(success=True, data=None, message="", errors=None, status_code=200):
    """
    Função utilitária para padronizar respostas da API.
    
    Args:
        success (bool): Se a operação foi bem-sucedida
        data (dict): Dados da resposta
        message (str): Mensagem de status
        errors (list): Lista de erros (se houver)
        status_code (int): Código de status HTTP
    
    Returns:
        JsonResponse: Resposta JSON padronizada
    """
    response = {
        'success': success,
        'message': message,
        'data': data or {},
        'errors': errors or []
    }
    
    return JsonResponse(response, status=status_code)


def log_api_request(request, endpoint, user_id=None, extra_data=None):
    """
    Registra requisições da API para auditoria.
    
    Args:
        request: Objeto request do Django
        endpoint (str): Nome do endpoint acessado
        user_id (int): ID do usuário (se autenticado)
        extra_data (dict): Dados extras para log
    """
    try:
        log_data = {
            'endpoint': endpoint,
            'method': request.method,
            'user_id': user_id or (request.user.id if request.user.is_authenticated else None),
            'ip_address': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'extra_data': extra_data or {}
        }
        
        logger.info(f"API Request: {log_data}")
        
    except Exception as e:
        logger.error(f"Erro ao registrar requisição API: {str(e)}")


def get_client_ip(request):
    """
    Obtém o IP do cliente da requisição.
    
    Args:
        request: Objeto request do Django
        
    Returns:
        str: IP do cliente
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_date_format(date_string, format_string='%Y-%m-%d'):
    """
    Valida formato de data.
    
    Args:
        date_string (str): String da data
        format_string (str): Formato esperado
        
    Returns:
        tuple: (is_valid, datetime_obj or None)
    """
    from datetime import datetime
    
    try:
        date_obj = datetime.strptime(date_string, format_string)
        return True, date_obj
    except ValueError:
        return False, None


def validate_required_fields(data, required_fields):
    """
    Valida campos obrigatórios em dados JSON.
    
    Args:
        data (dict): Dados para validar
        required_fields (list): Lista de campos obrigatórios
        
    Returns:
        list: Lista de erros encontrados
    """
    errors = []
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Campo '{field}' é obrigatório")
        elif data[field] is None or data[field] == '':
            errors.append(f"Campo '{field}' não pode estar vazio")
    
    return errors


def validate_numeric_fields(data, numeric_fields):
    """
    Valida campos numéricos.
    
    Args:
        data (dict): Dados para validar
        numeric_fields (list): Lista de campos que devem ser numéricos
        
    Returns:
        list: Lista de erros encontrados
    """
    errors = []
    
    for field in numeric_fields:
        if field in data:
            try:
                value = int(data[field])
                if value < 0:
                    errors.append(f"Campo '{field}' não pode ser negativo")
            except (ValueError, TypeError):
                errors.append(f"Campo '{field}' deve ser um número inteiro")
    
    return errors


def validate_business_rules(data):
    """
    Valida regras de negócio específicas para presenças.
    
    Args:
        data (dict): Dados para validar
        
    Returns:
        list: Lista de erros encontrados
    """
    errors = []
    
    # Regra: Presenças + Faltas <= Convocações
    if all(field in data for field in ['presencas', 'faltas', 'convocacoes']):
        try:
            presencas = int(data['presencas'])
            faltas = int(data['faltas'])
            convocacoes = int(data['convocacoes'])
            
            if presencas + faltas > convocacoes:
                errors.append("A soma de presenças e faltas não pode ser maior que convocações")
        except (ValueError, TypeError):
            pass  # Erro será capturado na validação numérica
    
    # Regra: Período deve ser primeiro dia do mês
    if 'periodo' in data:
        is_valid, date_obj = validate_date_format(data['periodo'])
        if is_valid and date_obj.day != 1:
            errors.append("O período deve ser o primeiro dia do mês")
    
    return errors


def paginate_queryset(queryset, page_number, page_size=20):
    """
    Pagina um queryset.
    
    Args:
        queryset: Queryset do Django
        page_number (int): Número da página
        page_size (int): Tamanho da página
        
    Returns:
        dict: Dados paginados
    """
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    paginator = Paginator(queryset, page_size)
    
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    return {
        'results': page.object_list,
        'page': page.number,
        'total_pages': paginator.num_pages,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
        'total_items': paginator.count
    }


def format_validation_errors(errors):
    """
    Formata erros de validação para resposta da API.
    
    Args:
        errors: Erros de validação (pode ser dict ou lista)
        
    Returns:
        list: Lista de erros formatados
    """
    formatted_errors = []
    
    if isinstance(errors, dict):
        for field, field_errors in errors.items():
            if isinstance(field_errors, list):
                for error in field_errors:
                    formatted_errors.append(f"{field}: {error}")
            else:
                formatted_errors.append(f"{field}: {field_errors}")
    elif isinstance(errors, list):
        formatted_errors = errors
    else:
        formatted_errors = [str(errors)]
    
    return formatted_errors


def safe_float_conversion(value, default=0.0):
    """
    Converte valor para float de forma segura.
    
    Args:
        value: Valor para converter
        default: Valor padrão se conversão falhar
        
    Returns:
        float: Valor convertido ou padrão
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int_conversion(value, default=0):
    """
    Converte valor para int de forma segura.
    
    Args:
        value: Valor para converter
        default: Valor padrão se conversão falhar
        
    Returns:
        int: Valor convertido ou padrão
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def calculate_percentage(numerator, denominator):
    """
    Calcula percentual de forma segura.
    
    Args:
        numerator: Numerador
        denominator: Denominador
        
    Returns:
        float: Percentual calculado (0.0 se denominador for 0)
    """
    if denominator == 0:
        return 0.0
    
    return (numerator / denominator) * 100


def format_period_display(period_date):
    """
    Formata data de período para exibição.
    
    Args:
        period_date: Data do período
        
    Returns:
        str: Data formatada (MM/YYYY)
    """
    if period_date:
        return period_date.strftime('%m/%Y')
    return None
