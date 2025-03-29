from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .utils import registrar_log, adicionar_mensagem, garantir_configuracao_sistema
from .models import ConfiguracaoSistema
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

def pagina_inicial(request):
    # Change this to use your original template
    return render(request, 'core/home.html', {})

def entrar(request):
    """Página de login do sistema"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                registrar_log(request, f'Login realizado com sucesso')
                adicionar_mensagem(request, 'sucesso', 'Login realizado com sucesso!')
                return redirect('core:pagina_inicial')
            else:
                adicionar_mensagem(request, 'erro', 'Nome de usuário ou senha inválidos.')
        else:
            adicionar_mensagem(request, 'erro', 'Nome de usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def painel_controle(request):
    """Painel de controle do sistema (apenas para staff)"""
    if not request.user.is_staff:
        adicionar_mensagem(request, 'erro', 'Você não tem permissão para acessar esta página.')
        return redirect('core:pagina_inicial')
    
    config = ConfiguracaoSistema.objects.first()
    logs_recentes = LogAtividade.objects.all()[:10]
    return render(request, 'core/painel_controle.html', {
        'config': config,
        'logs_recentes': logs_recentes
    })

@login_required
def atualizar_configuracao(request):
    """Atualiza as configurações do sistema"""
    if not request.user.is_staff:
        adicionar_mensagem(request, 'erro', 'Você não tem permissão para acessar esta página.')
        return redirect('core:pagina_inicial')
    
    config = garantir_configuracao_sistema()
    if request.method == 'POST':
        nome_sistema = request.POST.get('nome_sistema')
        versao = request.POST.get('versao')
        manutencao_ativa = request.POST.get('manutencao_ativa') == 'on'
        mensagem_manutencao = request.POST.get('mensagem_manutencao')
        
        config.nome_sistema = nome_sistema
        config.versao = versao
        config.manutencao_ativa = manutencao_ativa
        config.mensagem_manutencao = mensagem_manutencao
        config.data_atualizacao = timezone.now()
        config.save()
        
        registrar_log(request, 'Configurações do sistema atualizadas', 'INFO')
        adicionar_mensagem(request, 'sucesso', 'Configurações atualizadas com sucesso!')
        return redirect('core:painel_controle')
    
    return render(request, 'core/atualizar_configuracao.html', {
        'config': config
    })

def sair(request):
    """Realiza o logout do usuário"""
    if request.user.is_authenticated:
        registrar_log(request, 'Logout realizado com sucesso')
        logout(request)
        adicionar_mensagem(request, 'info', 'Você saiu do sistema com sucesso.')
    return redirect('core:pagina_inicial')

@ensure_csrf_cookie
def csrf_check(request):
    """
    View para verificar se o token CSRF ainda é válido.
    Retorna status 200 se o token for válido, caso contrário retorna 403.
    """
    if request.is_ajax() or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=403)
