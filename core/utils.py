import logging
from importlib import import_module
from django.contrib import messages
from django.utils import timezone

logger = logging.getLogger(__name__)


def get_model_dynamically(app_name, model_name):
    """
    Importa dinamicamente um modelo para evitar importações circulares.
    Mapeia nomes legados para novos modelos unificados.

    Args:
        app_name (str): Nome do aplicativo Django
        model_name (str): Nome do modelo a ser importado

    Returns:
        Model: Classe do modelo Django

    Raises:
        ImportError: Se o módulo não puder ser importado
        AttributeError: Se o modelo não existir no módulo
    """
    # Mapeamento de compatibilidade: alias legados para modelos unificados
    legacy_mapping = {
        ("presencas", "Presenca"): ("presencas", "RegistroPresenca"),
    }
    
    # Se encontra um alias legado, mapear para o novo
    if (app_name, model_name) in legacy_mapping:
        app_name, model_name = legacy_mapping[(app_name, model_name)]
        logger.info(f"Mapeamento legado aplicado: {app_name}.{model_name}")
    
    try:
        module = import_module(f"{app_name}.models")
        return getattr(module, model_name)
    except (ImportError, AttributeError) as e:
        logger.error(
            f"Erro ao importar modelo {model_name} do app {app_name}: {str(e)}"
        )
        raise


def get_form_dynamically(app_name, form_name):
    """
    Importa dinamicamente um formulário para evitar importações circulares.

    Args:
        app_name (str): Nome do aplicativo Django
        form_name (str): Nome do formulário a ser importado

    Returns:
        Form: Classe do formulário Django

    Raises:
        ImportError: Se o módulo não puder ser importado
        AttributeError: Se o formulário não existir no módulo
    """
    try:
        module = import_module(f"{app_name}.forms")
        return getattr(module, form_name)
    except (ImportError, AttributeError) as e:
        logger.error(
            f"Erro ao importar formulário {form_name} do app {app_name}: {str(e)}"
        )
        raise


def get_view_dynamically(app_name, view_name):
    """
    Obtém uma view dinamicamente para evitar importações circulares.

    Args:
        app_name (str): Nome do aplicativo Django (ex: 'alunos', 'turmas')
        view_name (str): Nome da função de view (ex: 'listar_alunos', 'criar_turma')

    Returns:
        function: A função de view solicitada

    Raises:
        ImportError: Se o módulo não puder ser importado
        AttributeError: Se a view não existir no módulo
    """
    module = import_module(f"{app_name}.views")
    return getattr(module, view_name)


def registrar_log(request, acao, tipo="INFO", detalhes=None):
    """
    Registra uma ação no log de atividades do sistema.

    Args:
        request: O objeto request do Django
        acao (str): Descrição da ação realizada
        tipo (str): Tipo de log (INFO, AVISO, ERRO, DEBUG)
        detalhes (str, optional): Detalhes adicionais sobre a ação
    """
    try:
        from core.models import LogAtividade

        usuario = request.user.username if request.user.is_authenticated else "Anônimo"

        LogAtividade.objects.create(
            usuario=usuario,
            acao=acao,
            tipo=tipo,
            data=timezone.now(),
            detalhes=detalhes,
        )
    except Exception as e:
        logger.error(f"Erro ao registrar log: {str(e)}")


def adicionar_mensagem(request, tipo, texto):
    """
    Adiciona uma mensagem flash para o usuário.

    Args:
        request: O objeto request do Django
        tipo (str): Tipo de mensagem (sucesso, info, aviso, erro)
        texto (str): Texto da mensagem
    """
    tipos_mensagem = {
        "sucesso": messages.SUCCESS,
        "info": messages.INFO,
        "aviso": messages.WARNING,
        "erro": messages.ERROR,
    }

    nivel = tipos_mensagem.get(tipo.lower(), messages.INFO)
    messages.add_message(request, nivel, texto)


def garantir_configuracao_sistema():
    """
    Garante que exista pelo menos uma configuração do sistema.
    Se não existir, cria uma com valores padrão.

    Returns:
        ConfiguracaoSistema: Objeto de configuração do sistema
    """
    try:
        from core.models import ConfiguracaoSistema

        config, created = ConfiguracaoSistema.objects.get_or_create(
            id=1,
            defaults={
                "nome_sistema": "Sistema de Gestão de Iniciados da OmAum",
                "versao": "1.0.0",
                "data_atualizacao": timezone.now(),
                "manutencao_ativa": False,
                "mensagem_manutencao": "Sistema em manutenção. Tente novamente mais tarde.",
            },
        )

        return config
    except Exception as e:
        logger.error(f"Erro ao garantir configuração do sistema: {str(e)}")
        raise
