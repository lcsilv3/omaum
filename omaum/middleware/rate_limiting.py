"""
FASE 3C: Rate limiting para proteção da API.
"""

import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from django.core.cache import cache
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RateLimitMiddleware(MiddlewareMixin):
    """
    Middleware para rate limiting baseado em IP e usuário.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Configurações padrão de rate limiting
        self.default_limits = {
            'requests_per_minute': getattr(settings, 'RATE_LIMIT_REQUESTS_PER_MINUTE', 60),
            'requests_per_hour': getattr(settings, 'RATE_LIMIT_REQUESTS_PER_HOUR', 1000),
            'burst_limit': getattr(settings, 'RATE_LIMIT_BURST', 10),  # Picos permitidos
        }
        
        # Limites especiais para diferentes endpoints
        self.endpoint_limits = {
            '/api/presencas/': {
                'requests_per_minute': 30,
                'requests_per_hour': 500,
                'burst_limit': 5,
            },
            '/api/exportacao/': {
                'requests_per_minute': 5,
                'requests_per_hour': 50,
                'burst_limit': 2,
            },
            '/api/estatisticas/': {
                'requests_per_minute': 20,
                'requests_per_hour': 200,
                'burst_limit': 3,
            },
        }
        
        super().__init__(get_response)
    
    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Verifica rate limiting antes de processar a requisição."""
        
        # Ignorar rate limiting para usuários staff em desenvolvimento
        if settings.DEBUG and hasattr(request, 'user') and request.user.is_staff:
            return None
        
        # Obter identificador do cliente
        client_id = self._get_client_identifier(request)
        
        # Verificar limites
        is_limited, limit_info = self._check_rate_limits(request, client_id)
        
        if is_limited:
            return self._create_rate_limit_response(limit_info)
        
        return None
    
    def _get_client_identifier(self, request: HttpRequest) -> str:
        """Obtém identificador único do cliente."""
        # Priorizar usuário autenticado
        if hasattr(request, 'user') and request.user.is_authenticated:
            return f"user_{request.user.id}"
        
        # Usar IP como fallback
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        
        return f"ip_{ip}"
    
    def _check_rate_limits(self, request: HttpRequest, client_id: str) -> tuple[bool, Dict[str, Any]]:
        """Verifica se o cliente excedeu os limites."""
        
        # Obter limites para o endpoint
        limits = self._get_endpoint_limits(request.path)
        
        current_time = time.time()
        
        # Chaves de cache para diferentes janelas de tempo
        minute_key = f"rate_limit_minute_{client_id}_{int(current_time // 60)}"
        hour_key = f"rate_limit_hour_{client_id}_{int(current_time // 3600)}"
        burst_key = f"rate_limit_burst_{client_id}"
        
        # Verificar limites
        minute_count = cache.get(minute_key, 0)
        hour_count = cache.get(hour_key, 0)
        burst_count = cache.get(burst_key, 0)
        
        # Verificar se excedeu algum limite
        if minute_count >= limits['requests_per_minute']:
            return True, {
                'type': 'minute',
                'limit': limits['requests_per_minute'],
                'current': minute_count,
                'reset_time': (int(current_time // 60) + 1) * 60
            }
        
        if hour_count >= limits['requests_per_hour']:
            return True, {
                'type': 'hour',
                'limit': limits['requests_per_hour'],
                'current': hour_count,
                'reset_time': (int(current_time // 3600) + 1) * 3600
            }
        
        # Verificar burst limit (últimos 10 segundos)
        if burst_count >= limits['burst_limit']:
            return True, {
                'type': 'burst',
                'limit': limits['burst_limit'],
                'current': burst_count,
                'reset_time': current_time + 10
            }
        
        # Incrementar contadores
        cache.set(minute_key, minute_count + 1, timeout=60)
        cache.set(hour_key, hour_count + 1, timeout=3600)
        cache.set(burst_key, burst_count + 1, timeout=10)
        
        return False, {}
    
    def _get_endpoint_limits(self, path: str) -> Dict[str, int]:
        """Obtém limites específicos para o endpoint."""
        
        # Verificar se há limite específico para o caminho
        for endpoint_pattern, limits in self.endpoint_limits.items():
            if path.startswith(endpoint_pattern):
                return limits
        
        # Usar limites padrão
        return self.default_limits
    
    def _create_rate_limit_response(self, limit_info: Dict[str, Any]) -> JsonResponse:
        """Cria resposta de rate limit excedido."""
        
        reset_time = datetime.fromtimestamp(limit_info['reset_time'])
        
        response_data = {
            'error': 'Rate limit exceeded',
            'message': f"Você excedeu o limite de {limit_info['limit']} requisições por {limit_info['type']}",
            'limit': limit_info['limit'],
            'current': limit_info['current'],
            'reset_at': reset_time.isoformat(),
            'retry_after': int(limit_info['reset_time'] - time.time())
        }
        
        response = JsonResponse(response_data, status=429)
        response['Retry-After'] = str(int(limit_info['reset_time'] - time.time()))
        response['X-RateLimit-Limit'] = str(limit_info['limit'])
        response['X-RateLimit-Remaining'] = str(max(0, limit_info['limit'] - limit_info['current']))
        response['X-RateLimit-Reset'] = str(int(limit_info['reset_time']))
        
        # Log da violação de rate limit
        logger.warning(
            "Rate limit excedido: %s limit de %s (atual: %s)",
            limit_info['type'], limit_info['limit'], limit_info['current'],
            extra={'limit_info': limit_info}
        )
        
        return response


class APIThrottlingMixin:
    """
    Mixin para adicionar throttling específico em views da API.
    """
    
    throttle_rates = {
        'list': {'requests_per_minute': 30, 'burst_limit': 5},
        'create': {'requests_per_minute': 10, 'burst_limit': 2},
        'update': {'requests_per_minute': 20, 'burst_limit': 3},
        'delete': {'requests_per_minute': 5, 'burst_limit': 1},
        'bulk': {'requests_per_minute': 3, 'burst_limit': 1},
    }
    
    def check_throttling(self, request: HttpRequest, action: str = 'default') -> Optional[JsonResponse]:
        """
        Verifica throttling específico para ações da API.
        
        Args:
            request: Requisição HTTP
            action: Tipo de ação (list, create, update, delete, bulk)
        
        Returns:
            JsonResponse se excedeu limite, None caso contrário
        """
        
        if not hasattr(self, 'throttle_rates') or action not in self.throttle_rates:
            return None
        
        limits = self.throttle_rates[action]
        client_id = self._get_client_identifier(request)
        
        current_time = time.time()
        minute_key = f"api_throttle_{action}_{client_id}_{int(current_time // 60)}"
        burst_key = f"api_throttle_burst_{action}_{client_id}"
        
        minute_count = cache.get(minute_key, 0)
        burst_count = cache.get(burst_key, 0)
        
        # Verificar limites
        if minute_count >= limits['requests_per_minute']:
            return self._create_throttle_response('minute', limits['requests_per_minute'], minute_count)
        
        if burst_count >= limits['burst_limit']:
            return self._create_throttle_response('burst', limits['burst_limit'], burst_count)
        
        # Incrementar contadores
        cache.set(minute_key, minute_count + 1, timeout=60)
        cache.set(burst_key, burst_count + 1, timeout=10)
        
        return None
    
    def _get_client_identifier(self, request: HttpRequest) -> str:
        """Obtém identificador do cliente para throttling."""
        if hasattr(request, 'user') and request.user.is_authenticated:
            return f"user_{request.user.id}"
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        
        return f"ip_{ip}"
    
    def _create_throttle_response(self, limit_type: str, limit: int, current: int) -> JsonResponse:
        """Cria resposta de throttling."""
        return JsonResponse({
            'error': 'API throttling exceeded',
            'message': f"Você excedeu o limite de {limit} requisições por {limit_type} para esta ação",
            'limit': limit,
            'current': current,
        }, status=429)


def rate_limit_decorator(requests_per_minute: int = 60, burst_limit: int = 10):
    """
    Decorator para aplicar rate limiting específico a uma view.
    
    Args:
        requests_per_minute: Limite de requisições por minuto
        burst_limit: Limite de picos (10 segundos)
    """
    
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Verificar rate limiting
            client_id = _get_client_identifier(request)
            
            current_time = time.time()
            minute_key = f"custom_rate_limit_{client_id}_{int(current_time // 60)}"
            burst_key = f"custom_burst_limit_{client_id}"
            
            minute_count = cache.get(minute_key, 0)
            burst_count = cache.get(burst_key, 0)
            
            if minute_count >= requests_per_minute:
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'limit': requests_per_minute,
                    'current': minute_count,
                }, status=429)
            
            if burst_count >= burst_limit:
                return JsonResponse({
                    'error': 'Burst limit exceeded',
                    'limit': burst_limit,
                    'current': burst_count,
                }, status=429)
            
            # Incrementar contadores
            cache.set(minute_key, minute_count + 1, timeout=60)
            cache.set(burst_key, burst_count + 1, timeout=10)
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def _get_client_identifier(request: HttpRequest) -> str:
    """Função auxiliar para obter identificador do cliente."""
    if hasattr(request, 'user') and request.user.is_authenticated:
        return f"user_{request.user.id}"
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    
    return f"ip_{ip}"
