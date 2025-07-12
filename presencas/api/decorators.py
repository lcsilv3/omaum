"""
Decoradores para API do sistema de presenças.
"""

import json
import logging
from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .utils import api_response, log_api_request, validate_required_fields

logger = logging.getLogger(__name__)


def api_login_required(view_func):
    """
    Decorator que combina login_required com resposta JSON.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return api_response(
                success=False,
                message="Autenticação necessária",
                errors=["Usuário não autenticado"],
                status_code=401
            )
        return view_func(request, *args, **kwargs)
    return wrapper


def api_require_methods(methods):
    """
    Decorator que valida métodos HTTP e retorna resposta JSON.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return api_response(
                    success=False,
                    message=f"Método {request.method} não permitido",
                    errors=[f"Métodos permitidos: {', '.join(methods)}"],
                    status_code=405
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def api_validate_json(required_fields=None):
    """
    Decorator que valida JSON e campos obrigatórios.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method in ['POST', 'PUT', 'PATCH']:
                try:
                    if not hasattr(request, 'json'):
                        data = json.loads(request.body.decode('utf-8'))
                        request.json = data
                    
                    # Validar campos obrigatórios
                    if required_fields:
                        errors = validate_required_fields(request.json, required_fields)
                        if errors:
                            return api_response(
                                success=False,
                                message="Campos obrigatórios ausentes",
                                errors=errors,
                                status_code=400
                            )
                
                except json.JSONDecodeError:
                    return api_response(
                        success=False,
                        message="JSON inválido",
                        errors=["Formato JSON inválido"],
                        status_code=400
                    )
                except Exception as e:
                    logger.error(f"Erro na validação JSON: {str(e)}")
                    return api_response(
                        success=False,
                        message="Erro na validação dos dados",
                        errors=[str(e)],
                        status_code=400
                    )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def api_log_request(endpoint_name):
    """
    Decorator que registra requisições da API.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Registrar requisição
            log_api_request(
                request,
                endpoint_name,
                request.user.id if request.user.is_authenticated else None,
                {
                    'args': args,
                    'kwargs': kwargs
                }
            )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def api_handle_exceptions(view_func):
    """
    Decorator que captura exceções e retorna resposta JSON.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(
                f"Erro não tratado na API: {str(e)}",
                extra={
                    'view_func': view_func.__name__,
                    'request_path': request.path,
                    'request_method': request.method,
                    'user_id': request.user.id if request.user.is_authenticated else None
                }
            )
            
            return api_response(
                success=False,
                message="Erro interno do servidor",
                errors=["Ocorreu um erro inesperado"],
                status_code=500
            )
    return wrapper


def api_csrf_exempt(view_func):
    """
    Decorator que isenta CSRF para APIs.
    """
    return csrf_exempt(view_func)


def api_standard_decorators(methods=None, required_fields=None, endpoint_name=None):
    """
    Decorator composto com validações padrão para APIs.
    """
    def decorator(view_func):
        # Aplicar decorators em ordem
        decorated_func = view_func
        
        # 1. Capturar exceções
        decorated_func = api_handle_exceptions(decorated_func)
        
        # 2. Validar JSON
        if required_fields:
            decorated_func = api_validate_json(required_fields)(decorated_func)
        
        # 3. Validar métodos HTTP
        if methods:
            decorated_func = api_require_methods(methods)(decorated_func)
        
        # 4. Registrar requisição
        if endpoint_name:
            decorated_func = api_log_request(endpoint_name)(decorated_func)
        
        # 5. Validar login
        decorated_func = api_login_required(decorated_func)
        
        # 6. Isentar CSRF
        decorated_func = api_csrf_exempt(decorated_func)
        
        return decorated_func
    return decorator


def api_throttle(rate_limit=100):
    """
    Decorator para rate limiting básico.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            from django.core.cache import cache
            from datetime import datetime, timedelta
            
            # Identificar cliente
            if request.user.is_authenticated:
                client_id = f"user_{request.user.id}"
            else:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                client_id = f"ip_{ip}"
            
            # Chave do cache
            cache_key = f"throttle_{view_func.__name__}_{client_id}"
            
            # Obter contador atual
            current_requests = cache.get(cache_key, 0)
            
            # Verificar limite
            if current_requests >= rate_limit:
                return api_response(
                    success=False,
                    message="Limite de requisições excedido",
                    errors=["Muitas requisições. Tente novamente em alguns minutos."],
                    status_code=429
                )
            
            # Incrementar contador
            cache.set(cache_key, current_requests + 1, 3600)  # 1 hora
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def api_require_permission(permission):
    """
    Decorator que verifica permissões específicas.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.has_perm(permission):
                return api_response(
                    success=False,
                    message="Permissão negada",
                    errors=["Usuário não tem permissão para esta ação"],
                    status_code=403
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def api_validate_queryset_exists(model_class, param_name, lookup_field='id'):
    """
    Decorator que valida se objeto existe no banco.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                # Obter valor do parâmetro
                if request.method == 'GET':
                    param_value = request.GET.get(param_name)
                else:
                    param_value = getattr(request, 'json', {}).get(param_name)
                
                if param_value:
                    # Verificar se objeto existe
                    lookup = {lookup_field: param_value}
                    if not model_class.objects.filter(**lookup).exists():
                        return api_response(
                            success=False,
                            message=f"{model_class.__name__} não encontrado",
                            errors=[f"Objeto com {lookup_field}={param_value} não existe"],
                            status_code=404
                        )
                
                return view_func(request, *args, **kwargs)
            
            except Exception as e:
                logger.error(f"Erro na validação de queryset: {str(e)}")
                return api_response(
                    success=False,
                    message="Erro na validação",
                    errors=[str(e)],
                    status_code=400
                )
        return wrapper
    return decorator
