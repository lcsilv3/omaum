from django.shortcuts import render
from .utils import garantir_configuracao_sistema

class ManutencaoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar se o sistema está em manutenção
        config = garantir_configuracao_sistema()
        
        # Ignorar verificação para staff e para a página de login
        if (config.manutencao_ativa and 
            not request.user.is_staff and 
            not request.path.startswith('/admin') and
            not request.path.endswith('/entrar/')):
            return render(request, 'core/manutencao.html', {
                'mensagem': config.mensagem_manutencao
            })
            
        response = self.get_response(request)
        return response
