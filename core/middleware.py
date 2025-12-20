from django.utils import timezone
from datetime import timedelta
import importlib


def manutencao_middleware(get_response):
    """
    Middleware para controle de manutenção do sistema.
    """

    def middleware(request):
        # Importa o modelo aqui para evitar importação circular
        ConfiguracaoSistema = importlib.import_module("core.models").ConfiguracaoSistema

        # Verifica se o sistema está em manutenção
        try:
            config = ConfiguracaoSistema.objects.first()
            if config and config.manutencao_ativa:
                # Se o usuário não for staff, redireciona para a página de manutenção
                if not hasattr(request, "user") or not request.user.is_staff:
                    from django.shortcuts import render

                    return render(
                        request,
                        "core/manutencao.html",
                        {"mensagem": config.mensagem_manutencao},
                    )
        except Exception:
            # Em caso de erro, continua normalmente
            pass

        response = get_response(request)
        return response

    return middleware


def renovacao_sessao_middleware(get_response):
    """
    Middleware para renovação de sessão e controle de inatividade do usuário.
    """

    def middleware(request):
        if hasattr(request, "user") and request.user.is_authenticated:
            # Obtém o horário da última atividade da sessão
            ultima_atividade = request.session.get("ultima_atividade")

            # Obtém o horário atual
            agora = timezone.now()

            # Se houver um registro de última atividade e for mais antigo que o limite de aviso
            if ultima_atividade:
                try:
                    ultima_atividade = timezone.datetime.fromisoformat(ultima_atividade)
                    tempo_desde_ultima_atividade = agora - ultima_atividade

                    # Se o usuário estiver inativo por muito tempo
                    if tempo_desde_ultima_atividade > timedelta(
                        seconds=3600
                    ):  # SESSION_SECURITY_EXPIRE_AFTER
                        # Poderia forçar logout aqui se desejado
                        pass
                    # Se estiver se aproximando do limite de inatividade, definir um aviso
                    elif tempo_desde_ultima_atividade > timedelta(
                        seconds=3000
                    ):  # SESSION_SECURITY_WARN_AFTER
                        request.session["mostrar_aviso_inatividade"] = True
                except (ValueError, TypeError):
                    # Se houver erro ao converter a data, reinicia o contador
                    pass

            # Atualiza o horário da última atividade
            request.session["ultima_atividade"] = agora.isoformat()
            request.session["mostrar_aviso_inatividade"] = False

        response = get_response(request)
        return response

    return middleware


def ajax_authentication_middleware(get_response):
    """
    Middleware para tratar requisições AJAX não autenticadas.
    Retorna JSON 401 em vez de redirecionar para página de login.
    """

    def middleware(request):
        # Verifica se é uma requisição AJAX não autenticada
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            import logging

            logger = logging.getLogger(__name__)
            logger.info(
                f"[DEBUG] AJAX Middleware - User: {getattr(request, 'user', 'No user attr')}, Auth: {getattr(getattr(request, 'user', None), 'is_authenticated', 'No auth attr')}, Path: {request.path}"
            )
            # Verifica se o usuário não está autenticado
            if not hasattr(request, "user") or not request.user.is_authenticated:
                from django.http import JsonResponse

                logger.info(
                    f"[DEBUG] AJAX Middleware - Retornando 401 para {request.path}"
                )
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Sessão expirada. Faça login novamente.",
                    },
                    status=401,
                )

        import logging
        logger = logging.getLogger(__name__)
        if request.path == "/atividades/" and request.headers.get("x-requested-with") == "XMLHttpRequest":
            logger.info(f"🔥 [MIDDLEWARE] ANTES de chamar get_response() para {request.path}")
        
        response = get_response(request)
        
        if request.path == "/atividades/" and request.headers.get("x-requested-with") == "XMLHttpRequest":
            logger.info(f"🔥 [MIDDLEWARE] DEPOIS de chamar get_response() - Status: {response.status_code}, Content-Type: {response.get('Content-Type', 'N/A')}")
        
        return response

    return middleware
