from django.contrib import messages
from .models import LogAtividade
from importlib import import_module

def get_model_dynamically(app_name, model_name):
    """
    Obtém um modelo dinamicamente para evitar importações circulares.
    
    Args:
        app_name (str): Nome do aplicativo Django (ex: 'alunos', 'turmas')
        model_name (str): Nome da classe do modelo (ex: 'Aluno', 'Turma')
        
    Returns:
        Model: A classe do modelo solicitada
        
    Raises:
        ImportError: Se o módulo não puder ser importado
        AttributeError: Se o modelo não existir no módulo
    """
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)

def get_form_dynamically(app_name, form_name):
    """
    Obtém um formulário dinamicamente para evitar importações circulares.
    
    Args:
        app_name (str): Nome do aplicativo Django (ex: 'alunos', 'turmas')
        form_name (str): Nome da classe do formulário (ex: 'AlunoForm', 'TurmaForm')
        
    Returns:
        Form: A classe do formulário solicitada
        
    Raises:
        ImportError: Se o módulo não puder ser importado
        AttributeError: Se o formulário não existir no módulo
    """
    module = import_module(f"{app_name}.forms")
    return getattr(module, form_name)

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
    Registra uma ação no log de atividades do sistema

    Args:
        request: O objeto request do Django
        acao: Descrição da ação realizada
        tipo: Tipo de log (INFO, AVISO, ERRO, DEBUG)
        detalhes: Detalhes adicionais sobre a ação
    """
    usuario = (
        request.user.username if request.user.is_authenticated else "Anônimo"
    )

    LogAtividade.objects.create(
        usuario=usuario, acao=acao, tipo=tipo, detalhes=detalhes
    )


def adicionar_mensagem(request, tipo, texto):
    """
    Adiciona uma mensagem para o usuário

    Args:
        request: O objeto request do Django
        tipo: Tipo de mensagem (success, error, warning, info)
        texto: Texto da mensagem
    """
    tipos_mensagem = {
        "sucesso": messages.SUCCESS,
        "erro": messages.ERROR,
        "aviso": messages.WARNING,
        "info": messages.INFO,
    }

    nivel = tipos_mensagem.get(tipo, messages.INFO)
    messages.add_message(request, nivel, texto)


def garantir_configuracao_sistema():
    """
    Garante que exista pelo menos uma configuração do sistema.
    Retorna a configuração existente ou cria uma nova.
    """
    from .models import ConfiguracaoSistema

    config, criado = ConfiguracaoSistema.objects.get_or_create(
        pk=1,
        defaults={
            "nome_sistema": "Sistema de Gestão de Iniciados da OmAum",
            "versao": "1.0.0",
            "manutencao_ativa": False,
            "mensagem_manutencao": "Sistema em manutenção. Tente novamente mais tarde.",
        },
    )

    return config
