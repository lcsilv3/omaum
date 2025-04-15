from django.utils import timezone
from datetime import timedelta
import importlib


def manutencao_middleware(get_response):
    """
    Middleware para controle de manutenção do sistema.
    """

    def middleware(request):
        # Importa o modelo aqui para evitar importação circular
        ConfiguracaoSistema = importlib.import_module(
            "core.models"
        ).ConfiguracaoSistema

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
                    ultima_atividade = timezone.datetime.fromisoformat(
                        ultima_atividade
                    )
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
