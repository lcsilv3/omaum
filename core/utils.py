from django.contrib import messages
from .models import LogAtividade

def registrar_log(request, acao, tipo='INFO', detalhes=None):
    """
    Registra uma ação no log de atividades do sistema
    
    Args:
        request: O objeto request do Django
        acao: Descrição da ação realizada
        tipo: Tipo de log (INFO, AVISO, ERRO, DEBUG)
        detalhes: Detalhes adicionais sobre a ação
    """
    usuario = request.user.username if request.user.is_authenticated else 'Anônimo'
    
    LogAtividade.objects.create(
        usuario=usuario,
        acao=acao,
        tipo=tipo,
        detalhes=detalhes
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
        'sucesso': messages.SUCCESS,
        'erro': messages.ERROR,
        'aviso': messages.WARNING,
        'info': messages.INFO,
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
            'nome_sistema': 'OMAUM',
            'versao': '1.0.0',
            'manutencao_ativa': False,
            'mensagem_manutencao': 'Sistema em manutenção. Tente novamente mais tarde.'
        }
    )
    
    return config
