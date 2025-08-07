"""
FASE 3C: Middleware para monitoramento de performance e métricas.
"""

import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional
from collections import defaultdict

from django.core.cache import cache
from django.conf import settings
from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest, HttpResponse
from django.urls import resolve

logger = logging.getLogger(__name__)


class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """
    Middleware para monitoramento de performance do sistema de presenças.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.slow_query_threshold = getattr(settings, 'SLOW_QUERY_THRESHOLD', 1.0)  # segundos
        self.metrics_cache_timeout = getattr(settings, 'METRICS_CACHE_TIMEOUT', 300)  # 5 minutos
        super().__init__(get_response)
    
    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Inicializa o monitoramento da requisição."""
        request._start_time = time.time()
        request._start_queries = len(connection.queries)
        request._cache_hits = 0
        request._cache_misses = 0
        return None
    
    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """Processa métricas no final da requisição."""
        try:
            # Calcular métricas básicas
            end_time = time.time()
            duration = end_time - getattr(request, '_start_time', end_time)
            
            # Contar queries executadas
            total_queries = len(connection.queries) - getattr(request, '_start_queries', 0)
            
            # Obter informações da view
            url_info = self._get_url_info(request)
            
            # Métricas da requisição
            metrics = {
                'duration': round(duration, 4),
                'queries_count': total_queries,
                'path': request.path,
                'method': request.method,
                'view_name': url_info.get('view_name', 'unknown'),
                'app_name': url_info.get('app_name', 'unknown'),
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat(),
                'user_id': getattr(request.user, 'id', None) if hasattr(request, 'user') else None,
            }
            
            # Detectar consultas lentas
            if duration > self.slow_query_threshold:
                self._log_slow_request(request, metrics, connection.queries)
            
            # Detectar muitas queries (N+1 problem)
            if total_queries > 10:
                self._log_many_queries(request, metrics, total_queries)
            
            # Armazenar métricas agregadas
            self._store_aggregated_metrics(metrics)
            
            # Adicionar headers de debug em desenvolvimento
            if settings.DEBUG:
                response['X-Response-Time'] = f"{duration:.4f}s"
                response['X-DB-Queries'] = str(total_queries)
            
        except Exception as e:
            logger.error(f"Erro no middleware de performance: {e}")
        
        return response
    
    def _get_url_info(self, request: HttpRequest) -> Dict[str, str]:
        """Extrai informações da URL e view."""
        try:
            resolved = resolve(request.path)
            return {
                'view_name': resolved.view_name,
                'app_name': resolved.app_name or 'unknown',
                'url_name': resolved.url_name or 'unknown',
            }
        except Exception:
            return {'view_name': 'unknown', 'app_name': 'unknown', 'url_name': 'unknown'}
    
    def _log_slow_request(self, request: HttpRequest, metrics: Dict[str, Any], queries: list):
        """Log para requisições lentas."""
        logger.warning(
            f"Requisição lenta detectada: {metrics['path']} "
            f"({metrics['duration']}s, {metrics['queries_count']} queries)",
            extra={
                'metrics': metrics,
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'remote_addr': self._get_client_ip(request),
            }
        )
        
        # Log das queries mais lentas
        if hasattr(connection, 'queries'):
            slow_queries = [
                q for q in queries[-metrics['queries_count']:]
                if float(q.get('time', 0)) > 0.1
            ]
            
            if slow_queries:
                logger.warning(
                    f"Queries lentas na requisição {metrics['path']}:",
                    extra={'slow_queries': slow_queries[:5]}  # Limitar a 5 queries
                )
    
    def _log_many_queries(self, request: HttpRequest, metrics: Dict[str, Any], query_count: int):
        """Log para requisições com muitas queries."""
        logger.warning(
            f"Possível problema N+1 detectado: {metrics['path']} "
            f"({query_count} queries)",
            extra={
                'metrics': metrics,
                'suggestion': 'Considere usar select_related() ou prefetch_related()'
            }
        )
    
    def _store_aggregated_metrics(self, metrics: Dict[str, Any]):
        """Armazena métricas agregadas no cache."""
        try:
            cache_key = f"metrics_aggregated_{datetime.now().strftime('%Y%m%d_%H')}"
            
            # Obter métricas existentes
            aggregated = cache.get(cache_key, {
                'total_requests': 0,
                'total_duration': 0,
                'slow_requests': 0,
                'views': defaultdict(lambda: {
                    'count': 0,
                    'total_duration': 0,
                    'avg_queries': 0,
                    'error_count': 0
                }),
                'last_updated': datetime.now().isoformat()
            })
            
            # Atualizar totais
            aggregated['total_requests'] += 1
            aggregated['total_duration'] += metrics['duration']
            
            if metrics['duration'] > self.slow_query_threshold:
                aggregated['slow_requests'] += 1
            
            # Atualizar métricas por view
            view_key = f"{metrics['app_name']}.{metrics['view_name']}"
            view_metrics = aggregated['views'][view_key]
            view_metrics['count'] += 1
            view_metrics['total_duration'] += metrics['duration']
            view_metrics['avg_queries'] = (
                (view_metrics['avg_queries'] * (view_metrics['count'] - 1) + metrics['queries_count'])
                / view_metrics['count']
            )
            
            if metrics['status_code'] >= 400:
                view_metrics['error_count'] += 1
            
            aggregated['last_updated'] = datetime.now().isoformat()
            
            # Salvar no cache
            cache.set(cache_key, aggregated, timeout=self.metrics_cache_timeout * 4)
            
        except Exception as e:
            logger.error(f"Erro ao armazenar métricas agregadas: {e}")
    
    def _get_client_ip(self, request: HttpRequest) -> str:
        """Obtém o IP real do cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip


class CacheMonitoringMiddleware(MiddlewareMixin):
    """
    Middleware para monitoramento de cache hits/misses.
    """
    
    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Inicializa contadores de cache."""
        request._cache_operations = {'hits': 0, 'misses': 0, 'sets': 0}
        return None
    
    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """Adiciona estatísticas de cache."""
        if settings.DEBUG and hasattr(request, '_cache_operations'):
            operations = request._cache_operations
            response['X-Cache-Hits'] = str(operations['hits'])
            response['X-Cache-Misses'] = str(operations['misses'])
            response['X-Cache-Sets'] = str(operations['sets'])
            
            # Calcular hit rate
            total_ops = operations['hits'] + operations['misses']
            if total_ops > 0:
                hit_rate = round((operations['hits'] / total_ops) * 100, 2)
                response['X-Cache-Hit-Rate'] = f"{hit_rate}%"
        
        return response


class DatabaseConnectionMonitoringMiddleware(MiddlewareMixin):
    """
    Middleware para monitoramento de conexões com banco de dados.
    """
    
    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Monitora abertura de conexões."""
        # Verificar se há conexões abertas demais
        if hasattr(connection, 'queries_logged'):
            total_connections = len(connection.queries_logged)
            max_connections = getattr(settings, 'MAX_DB_CONNECTIONS_WARNING', 50)
            
            if total_connections > max_connections:
                logger.warning(
                    f"Muitas conexões de banco detectadas: {total_connections}",
                    extra={'path': request.path, 'method': request.method}
                )
        
        return None
    
    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """Monitora fechamento de conexões."""
        # Fechar conexões ociosas se necessário
        try:
            if hasattr(connection, 'close_if_unusable_or_obsolete'):
                connection.close_if_unusable_or_obsolete()
        except Exception as e:
            logger.error(f"Erro ao gerenciar conexões: {e}")
        
        return response


class SecurityAuditMiddleware(MiddlewareMixin):
    """
    Middleware para auditoria de segurança e detecção de tentativas suspeitas.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.suspicious_patterns = [
            'union select',
            'drop table',
            'delete from',
            '../',
            'script>',
            'javascript:',
        ]
        super().__init__(get_response)
    
    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """Analisa requisições em busca de padrões suspeitos."""
        try:
            # Verificar parâmetros suspeitos
            query_string = request.META.get('QUERY_STRING', '').lower()
            
            for pattern in self.suspicious_patterns:
                if pattern in query_string:
                    logger.warning(
                        f"Padrão suspeito detectado: {pattern}",
                        extra={
                            'path': request.path,
                            'query_string': query_string,
                            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                            'remote_addr': self._get_client_ip(request),
                            'user_id': getattr(request.user, 'id', None) if hasattr(request, 'user') else None,
                        }
                    )
                    break
            
            # Verificar tentativas de acesso a áreas restritas
            if request.path.startswith('/admin/') and not self._is_admin_user(request):
                logger.warning(
                    f"Tentativa de acesso não autorizado ao admin",
                    extra={
                        'path': request.path,
                        'remote_addr': self._get_client_ip(request),
                        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    }
                )
        
        except Exception as e:
            logger.error(f"Erro no middleware de segurança: {e}")
        
        return None
    
    def _is_admin_user(self, request: HttpRequest) -> bool:
        """Verifica se o usuário é admin."""
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return False
        return request.user.is_staff or request.user.is_superuser
    
    def _get_client_ip(self, request: HttpRequest) -> str:
        """Obtém o IP real do cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'unknown')
        return ip
