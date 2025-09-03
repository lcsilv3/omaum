"""
FASE 3C: Configuração de logging estruturado e monitoramento.
"""

import logging
from pathlib import Path


class StructuredFormatter(logging.Formatter):
    """
    Formatter personalizado para logs estruturados.
    """

    def format(self, record):
        # Adicionar informações estruturadas ao log
        if hasattr(record, "extra_data"):
            record.msg = f"{record.msg} | Extra: {record.extra_data}"

        # Adicionar contexto de performance se disponível
        if hasattr(record, "metrics"):
            metrics = record.metrics
            record.msg = f"{record.msg} | Duration: {metrics.get('duration', 'N/A')}s | Queries: {metrics.get('queries_count', 'N/A')}"

        return super().format(record)


def setup_logging(base_dir: Path, debug: bool = False):
    """
    Configura sistema de logging estruturado.

    Args:
        base_dir: Diretório base do projeto
        debug: Se está em modo debug
    """

    # Criar diretório de logs se não existir
    logs_dir = base_dir / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Configuração base
    level = logging.DEBUG if debug else logging.INFO

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
            "structured": {
                "()": StructuredFormatter,
                "format": "{asctime} | {levelname} | {name} | {message}",
                "style": "{",
            },
            "json": {
                "format": '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
            },
        },
        "handlers": {
            "console": {
                "level": level,
                "class": "logging.StreamHandler",
                "formatter": "simple" if debug else "structured",
            },
            "file_general": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": logs_dir / "django.log",
                "maxBytes": 1024 * 1024 * 15,  # 15MB
                "backupCount": 10,
                "formatter": "verbose",
            },
            "file_performance": {
                "level": "WARNING",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": logs_dir / "performance.log",
                "maxBytes": 1024 * 1024 * 10,  # 10MB
                "backupCount": 5,
                "formatter": "structured",
            },
            "file_security": {
                "level": "WARNING",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": logs_dir / "security.log",
                "maxBytes": 1024 * 1024 * 10,  # 10MB
                "backupCount": 5,
                "formatter": "structured",
            },
            "file_celery": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": logs_dir / "celery.log",
                "maxBytes": 1024 * 1024 * 10,  # 10MB
                "backupCount": 5,
                "formatter": "verbose",
            },
            "file_api": {
                "level": "INFO",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": logs_dir / "api.log",
                "maxBytes": 1024 * 1024 * 10,  # 10MB
                "backupCount": 5,
                "formatter": "json",
            },
            "file_errors": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": logs_dir / "errors.log",
                "maxBytes": 1024 * 1024 * 20,  # 20MB
                "backupCount": 10,
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file_general", "console"],
                "level": level,
                "propagate": False,
            },
            "django.request": {
                "handlers": ["file_errors", "console"],
                "level": "ERROR",
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["file_performance"] if not debug else ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            "omaum.middleware.performance": {
                "handlers": ["file_performance"],
                "level": "WARNING",
                "propagate": False,
            },
            "omaum.middleware.rate_limiting": {
                "handlers": ["file_security"],
                "level": "WARNING",
                "propagate": False,
            },
            "presencas": {
                "handlers": ["file_general", "console"] if debug else ["file_general"],
                "level": level,
                "propagate": False,
            },
            "presencas.api": {
                "handlers": ["file_api"],
                "level": "INFO",
                "propagate": False,
            },
            "presencas.tasks": {
                "handlers": ["file_celery"],
                "level": "INFO",
                "propagate": False,
            },
            "celery": {
                "handlers": ["file_celery", "console"] if debug else ["file_celery"],
                "level": level,
                "propagate": False,
            },
            "celery.task": {
                "handlers": ["file_celery"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "root": {
            "level": level,
            "handlers": ["console", "file_general"],
        },
    }


class PerformanceLogger:
    """
    Logger especializado para métricas de performance.
    """

    def __init__(self, logger_name: str = "performance"):
        self.logger = logging.getLogger(logger_name)

    def log_request_metrics(
        self,
        request_path: str,
        duration: float,
        queries_count: int,
        status_code: int,
        user_id: int = None,
    ):
        """Log de métricas de requisição."""
        self.logger.info(
            f"Request completed: {request_path}",
            extra={
                "metrics": {
                    "duration": duration,
                    "queries_count": queries_count,
                    "status_code": status_code,
                    "user_id": user_id,
                    "path": request_path,
                }
            },
        )

    def log_slow_query(self, query: str, duration: float, path: str):
        """Log de query lenta."""
        self.logger.warning(
            f"Slow query detected: {duration:.4f}s",
            extra={
                "query_info": {
                    "duration": duration,
                    "path": path,
                    "query": query[:200],  # Limitar tamanho da query no log
                }
            },
        )

    def log_cache_metrics(
        self, operation: str, key: str, hit: bool, duration: float = None
    ):
        """Log de operações de cache."""
        self.logger.info(
            f"Cache {operation}: {'HIT' if hit else 'MISS'} for key {key}",
            extra={
                "cache_metrics": {
                    "operation": operation,
                    "key": key,
                    "hit": hit,
                    "duration": duration,
                }
            },
        )


class SecurityLogger:
    """
    Logger especializado para eventos de segurança.
    """

    def __init__(self, logger_name: str = "security"):
        self.logger = logging.getLogger(logger_name)

    def log_rate_limit_violation(
        self, client_id: str, path: str, limit_type: str, current: int, limit: int
    ):
        """Log de violação de rate limit."""
        self.logger.warning(
            f"Rate limit exceeded: {client_id} on {path}",
            extra={
                "security_event": {
                    "type": "rate_limit_violation",
                    "client_id": client_id,
                    "path": path,
                    "limit_type": limit_type,
                    "current": current,
                    "limit": limit,
                }
            },
        )

    def log_suspicious_activity(
        self, client_id: str, path: str, pattern: str, user_agent: str = None
    ):
        """Log de atividade suspeita."""
        self.logger.warning(
            f"Suspicious activity detected: {pattern} from {client_id}",
            extra={
                "security_event": {
                    "type": "suspicious_activity",
                    "client_id": client_id,
                    "path": path,
                    "pattern": pattern,
                    "user_agent": user_agent,
                }
            },
        )

    def log_admin_access_attempt(
        self, client_id: str, path: str, authenticated: bool, user_id: int = None
    ):
        """Log de tentativa de acesso ao admin."""
        self.logger.warning(
            f"Admin access attempt: {client_id} ({'authenticated' if authenticated else 'unauthenticated'})",
            extra={
                "security_event": {
                    "type": "admin_access_attempt",
                    "client_id": client_id,
                    "path": path,
                    "authenticated": authenticated,
                    "user_id": user_id,
                }
            },
        )


class APILogger:
    """
    Logger especializado para APIs.
    """

    def __init__(self, logger_name: str = "presencas.api"):
        self.logger = logging.getLogger(logger_name)

    def log_api_request(
        self,
        method: str,
        endpoint: str,
        user_id: int = None,
        params: dict = None,
        duration: float = None,
    ):
        """Log de requisição da API."""
        self.logger.info(
            f"API {method} {endpoint}",
            extra={
                "api_event": {
                    "method": method,
                    "endpoint": endpoint,
                    "user_id": user_id,
                    "params": params,
                    "duration": duration,
                }
            },
        )

    def log_api_error(
        self,
        method: str,
        endpoint: str,
        error: str,
        status_code: int,
        user_id: int = None,
    ):
        """Log de erro da API."""
        self.logger.error(
            f"API Error {method} {endpoint}: {error}",
            extra={
                "api_error": {
                    "method": method,
                    "endpoint": endpoint,
                    "error": error,
                    "status_code": status_code,
                    "user_id": user_id,
                }
            },
        )

    def log_bulk_operation(
        self,
        operation: str,
        count: int,
        duration: float,
        user_id: int = None,
        success: bool = True,
    ):
        """Log de operação em lote."""
        level = logging.INFO if success else logging.ERROR
        self.logger.log(
            level,
            f"Bulk {operation}: {count} items in {duration:.2f}s",
            extra={
                "bulk_operation": {
                    "operation": operation,
                    "count": count,
                    "duration": duration,
                    "user_id": user_id,
                    "success": success,
                }
            },
        )


class CeleryLogger:
    """
    Logger especializado para tasks do Celery.
    """

    def __init__(self, logger_name: str = "presencas.tasks"):
        self.logger = logging.getLogger(logger_name)

    def log_task_start(
        self, task_name: str, task_id: str, args: tuple = None, kwargs: dict = None
    ):
        """Log de início de task."""
        self.logger.info(
            f"Task started: {task_name} [{task_id}]",
            extra={
                "task_event": {
                    "name": task_name,
                    "id": task_id,
                    "args": str(args) if args else None,
                    "kwargs": kwargs,
                    "status": "started",
                }
            },
        )

    def log_task_completion(
        self, task_name: str, task_id: str, duration: float, result: dict = None
    ):
        """Log de conclusão de task."""
        self.logger.info(
            f"Task completed: {task_name} [{task_id}] in {duration:.2f}s",
            extra={
                "task_event": {
                    "name": task_name,
                    "id": task_id,
                    "duration": duration,
                    "result": result,
                    "status": "completed",
                }
            },
        )

    def log_task_failure(
        self, task_name: str, task_id: str, error: str, retry_count: int = 0
    ):
        """Log de falha de task."""
        self.logger.error(
            f"Task failed: {task_name} [{task_id}]: {error}",
            extra={
                "task_event": {
                    "name": task_name,
                    "id": task_id,
                    "error": error,
                    "retry_count": retry_count,
                    "status": "failed",
                }
            },
        )
