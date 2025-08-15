"""
Middleware para API do sistema de presenças.
"""

import json
import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .utils import log_api_request

logger = logging.getLogger(__name__)


class PresencasAPIMiddleware(MiddlewareMixin):
    """
    Middleware para APIs de presenças.
    Registra requisições e padroniza tratamento de erros.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def process_request(self, request):
        """
        Processa requisições para APIs de presenças.
        """
        # Aplicar apenas para URLs da API de presenças
        if request.path.startswith("/presencas/api/"):
            # Registrar requisição
            log_api_request(
                request,
                request.path,
                request.user.id if request.user.is_authenticated else None,
            )

            # Validar Content-Type para métodos que enviam dados
            if request.method in ["POST", "PUT", "PATCH"]:
                content_type = request.content_type.lower()
                if "application/json" not in content_type:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Content-Type deve ser application/json",
                            "errors": ["Content-Type inválido"],
                        },
                        status=400,
                    )

        return None

    def process_exception(self, request, exception):
        """
        Processa exceções não tratadas nas APIs de presenças.
        """
        # Aplicar apenas para URLs da API de presenças
        if request.path.startswith("/presencas/api/"):
            logger.error(
                f"Erro não tratado na API de presenças: {str(exception)}",
                extra={
                    "request_path": request.path,
                    "request_method": request.method,
                    "user_id": request.user.id
                    if request.user.is_authenticated
                    else None,
                },
            )

            # Retornar resposta de erro padronizada
            return JsonResponse(
                {
                    "success": False,
                    "message": "Erro interno do servidor",
                    "errors": ["Ocorreu um erro inesperado"],
                },
                status=500,
            )

        return None

    def process_response(self, request, response):
        """
        Processa respostas das APIs de presenças.
        """
        # Aplicar apenas para URLs da API de presenças
        if request.path.startswith("/presencas/api/"):
            # Adicionar headers CORS se necessário
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

            # Registrar resposta para auditoria
            if response.status_code >= 400:
                logger.warning(
                    f"Resposta de erro na API: {response.status_code}",
                    extra={
                        "request_path": request.path,
                        "request_method": request.method,
                        "status_code": response.status_code,
                        "user_id": request.user.id
                        if request.user.is_authenticated
                        else None,
                    },
                )

        return response


class JSONParsingMiddleware(MiddlewareMixin):
    """
    Middleware para parsing de JSON em requisições.
    """

    def process_request(self, request):
        """
        Processa requisições JSON.
        """
        if request.path.startswith("/presencas/api/"):
            if request.method in ["POST", "PUT", "PATCH"]:
                try:
                    if request.content_type == "application/json":
                        if hasattr(request, "body") and request.body:
                            request.json = json.loads(request.body.decode("utf-8"))
                        else:
                            request.json = {}
                except json.JSONDecodeError:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "JSON inválido",
                            "errors": ["Formato JSON inválido"],
                        },
                        status=400,
                    )

        return None


class RateLimitMiddleware(MiddlewareMixin):
    """
    Middleware para rate limiting básico.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_per_minute = 60
        self.requests_cache = {}
        super().__init__(get_response)

    def process_request(self, request):
        """
        Verifica rate limit para APIs de presenças.
        """
        if request.path.startswith("/presencas/api/"):
            from django.core.cache import cache

            # Identificar cliente
            if request.user.is_authenticated:
                client_id = f"user_{request.user.id}"
            else:
                client_id = self.get_client_ip(request)

            # Chave do cache
            cache_key = f"rate_limit_{client_id}"

            # Obter contador atual
            current_requests = cache.get(cache_key, 0)

            # Verificar limite
            if current_requests >= self.requests_per_minute:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Limite de requisições excedido",
                        "errors": [
                            "Muitas requisições. Tente novamente em alguns minutos."
                        ],
                    },
                    status=429,
                )

            # Incrementar contador
            cache.set(cache_key, current_requests + 1, 60)  # 1 minuto

        return None

    def get_client_ip(self, request):
        """
        Obtém IP do cliente.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
