# Código da Funcionalidade: core
*Gerado automaticamente*



## core\admin.py

python
from django.contrib import admin
from .models import ConfiguracaoSistema, LogAtividade

@admin.register(ConfiguracaoSistema)
class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('nome_sistema', 'versao', 'data_atualizacao', 'manutencao_ativa')
    list_editable = ('manutencao_ativa',)
    readonly_fields = ('data_atualizacao',)

@admin.register(LogAtividade)
class LogAtividadeAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'acao', 'usuario', 'data')
    list_filter = ('tipo', 'data', 'usuario')
    search_fields = ('acao', 'usuario', 'detalhes')
    readonly_fields = ('data',)




## core\apps.py

python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'




## core\forms.py

python
from django import forms
from core.models import Aluno, Curso, Turma, AtividadeAcademica, AtividadeRitualistica
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ('nome', 'matricula', 'curso')

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nome', 'descricao')

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ('nome', 'curso', 'data_inicio', 'data_fim', 'vagas')

class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = AtividadeAcademica
        # Corrigir para usar os campos corretos
        fields = ('nome', 'descricao', 'data_inicio', 'data_fim', 'turma')

class AtividadeRitualisticaForm(forms.ModelForm):
    class Meta:
        model = AtividadeRitualistica
        fields = ['nome', 'descricao', 'turma', 'alunos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turma'].queryset = Turma.objects.all()
        self.fields['alunos'].queryset = Aluno.objects.all()
        self.fields['alunos'].widget = forms.CheckboxSelectMultiple()

class AlunoTurmaForm(forms.Form):
    aluno = forms.ModelChoiceField(queryset=Aluno.objects.all(), label="Aluno")

    def __init__(self, *args, **kwargs):
        turma = kwargs.pop('turma', None)
        super().__init__(*args, **kwargs)
        if turma:
            self.fields['aluno'].queryset = Aluno.objects.exclude(turmas=turma)

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



## core\middleware.py

python
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




## core\models.py

python
from django.db import models
from django.utils import timezone

class ConfiguracaoSistema(models.Model):
    """Configurações globais do sistema"""
    nome_sistema = models.CharField(max_length=100, default="OMAUM")
    versao = models.CharField(max_length=20, default="1.0.0")
    data_atualizacao = models.DateTimeField(default=timezone.now)
    manutencao_ativa = models.BooleanField(default=False)
    mensagem_manutencao = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nome_sistema} v{self.versao}"
    
    class Meta:
        verbose_name = 'Configuração do Sistema'
        verbose_name_plural = 'Configurações do Sistema'

class LogAtividade(models.Model):
    """Registro de atividades do sistema"""
    TIPO_CHOICES = [
        ('INFO', 'Informação'),
        ('AVISO', 'Aviso'),
        ('ERRO', 'Erro'),
        ('DEBUG', 'Depuração'),
    ]
    
    usuario = models.CharField(max_length=100)
    acao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='INFO')
    data = models.DateTimeField(default=timezone.now)
    detalhes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo}: {self.acao} por {self.usuario}"
    
    class Meta:
        verbose_name = 'Log de Atividade'
        verbose_name_plural = 'Logs de Atividades'
        ordering = ['-data']



## core\tests.py

python
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware

from .models import ConfiguracaoSistema, LogAtividade
from .views import pagina_inicial, entrar, painel_controle, atualizar_configuracao
from .utils import registrar_log, adicionar_mensagem, garantir_configuracao_sistema
from .middleware import ManutencaoMiddleware


class ConfiguracaoSistemaTests(TestCase):
    """Testes para o modelo ConfiguracaoSistema"""
    
    def test_criacao_configuracao(self):
        """Testa a criação de uma configuração do sistema"""
        config = ConfiguracaoSistema.objects.create(
            nome_sistema="Sistema de Teste",
            versao="1.0.0",
            manutencao_ativa=False
        )
        self.assertEqual(config.nome_sistema, "Sistema de Teste")
        self.assertEqual(config.versao, "1.0.0")
        self.assertFalse(config.manutencao_ativa)
    
    def test_str_representation(self):
        """Testa a representação string do modelo"""
        config = ConfiguracaoSistema.objects.create(
            nome_sistema="Sistema de Teste",
            versao="1.0.0"
        )
        self.assertEqual(str(config), "Sistema de Teste v1.0.0")


class LogAtividadeTests(TestCase):
    """Testes para o modelo LogAtividade"""
    
    def test_criacao_log(self):
        """Testa a criação de um log de atividade"""
        log = LogAtividade.objects.create(
            usuario="usuario_teste",
            acao="Ação de teste",
            tipo="INFO",
            detalhes="Detalhes da ação de teste"
        )
        self.assertEqual(log.usuario, "usuario_teste")
        self.assertEqual(log.acao, "Ação de teste")
        self.assertEqual(log.tipo, "INFO")
        self.assertEqual(log.detalhes, "Detalhes da ação de teste")
    
    def test_str_representation(self):
        """Testa a representação string do modelo"""
        log = LogAtividade.objects.create(
            usuario="usuario_teste",
            acao="Ação de teste",
            tipo="INFO"
        )
        self.assertEqual(str(log), "INFO: Ação de teste por usuario_teste")
    
    def test_ordering(self):
        """Testa a ordenação dos logs (mais recentes primeiro)"""
        log1 = LogAtividade.objects.create(usuario="user1", acao="acao1")
        log2 = LogAtividade.objects.create(usuario="user2", acao="acao2")
        logs = LogAtividade.objects.all()
        self.assertEqual(logs[0], log2)  # O segundo log deve aparecer primeiro


class UtilsTests(TestCase):
    """Testes para as funções utilitárias"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
    
    def test_registrar_log(self):
        """Testa o registro de logs"""
        request = self.factory.get('/')
        request.user = self.user
        
        # Registra um log
        registrar_log(request, "Teste de log", "INFO", "Detalhes do teste")
        
        # Verifica se o log foi criado
        log = LogAtividade.objects.last()
        self.assertEqual(log.usuario, "testuser")
        self.assertEqual(log.acao, "Teste de log")
        self.assertEqual(log.tipo, "INFO")
        self.assertEqual(log.detalhes, "Detalhes do teste")
    
    def test_registrar_log_anonimo(self):
        """Testa o registro de logs para usuários anônimos"""
        request = self.factory.get('/')
        request.user = AnonymousUser()
        
        # Registra um log
        registrar_log(request, "Teste de log anônimo")
        
        # Verifica se o log foi criado
        log = LogAtividade.objects.last()
        self.assertEqual(log.usuario, "Anônimo")
        self.assertEqual(log.acao, "Teste de log anônimo")
    
    def test_garantir_configuracao_sistema(self):
        """Testa a função que garante a existência de uma configuração"""
        # Inicialmente não deve haver configurações
        self.assertEqual(ConfiguracaoSistema.objects.count(), 0)
        
        # Chama a função para garantir uma configuração
        config = garantir_configuracao_sistema()
        
        # Deve haver exatamente uma configuração
        self.assertEqual(ConfiguracaoSistema.objects.count(), 1)
        self.assertEqual(config.nome_sistema, "OMAUM")
        
        # Chamar novamente não deve criar outra configuração
        config2 = garantir_configuracao_sistema()
        self.assertEqual(ConfiguracaoSistema.objects.count(), 1)
        self.assertEqual(config, config2)


class ViewsTests(TestCase):
    """Testes para as views"""
    
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        
        # Cria um usuário normal
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
        
        # Cria um usuário staff
        self.staff_user = User.objects.create_user(
            username='staffuser', 
            email='staff@example.com', 
            password='staffpassword',
            is_staff=True
        )
        
        # Garante que existe uma configuração
        self.config = garantir_configuracao_sistema()
    
    def test_pagina_inicial(self):
        """Testa a página inicial"""
        response = self.client.get(reverse('core:pagina_inicial'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertContains(response, self.config.nome_sistema)
    
    def test_pagina_inicial_em_manutencao(self):
        """Testa a página inicial quando o sistema está em manutenção"""
        # Ativa o modo de manutenção
        self.config.manutencao_ativa = True
        self.config.mensagem_manutencao = "Sistema em manutenção para testes"
        self.config.save()
        
        # Usuário anônimo deve ver a página de manutenção
        response = self.client.get(reverse('core:pagina_inicial'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/manutencao.html')
        self.assertContains(response, "Sistema em manutenção para testes")
        
        # Usuário staff deve ver a página normal mesmo em manutenção
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('core:pagina_inicial'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
    
    def test_entrar_get(self):
        """Testa a página de login (GET)"""
        response = self.client.get(reverse('core:entrar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
    
    def test_entrar_post_sucesso(self):
        """Testa o login com sucesso"""
        response = self.client.post(reverse('core:entrar'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, reverse('core:pagina_inicial'))
        
        # Verifica se o log foi registrado
        log = LogAtividade.objects.last()
        self.assertEqual(log.usuario, "testuser")
        self.assertEqual(log.acao, "Login realizado com sucesso")
    
    def test_entrar_post_falha(self):
        """Testa o login com credenciais inválidas"""
        response = self.client.post(reverse('core:entrar'), {
            'username': 'testuser',
            'password': 'senhaerrada'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
    
    def test_sair(self):
        """Testa o logout"""
        # Primeiro faz login
        self.client.login(username='testuser', password='testpassword')
        
        # Depois faz logout
        response = self.client.get(reverse('core:sair'))
        self.assertRedirects(response, reverse('core:pagina_inicial'))
        
        # Verifica se o usuário está deslogado
        response = self.client.get(reverse('core:painel_controle'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("core:painel_controle")}')
    
    def test_painel_controle_sem_permissao(self):
        """Testa acesso ao painel de controle sem permissão"""
        # Usuário não autenticado deve ser redirecionado para login
        response = self.client.get(reverse('core:painel_controle'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("core:painel_controle")}')
        
        # Usuário normal não deve ter acesso
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('core:painel_controle'))
        self.assertRedirects(response, reverse('core:pagina_inicial'))
    
    def test_painel_controle_com_permissao(self):
        """Testa acesso ao painel de controle com permissão"""
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('core:painel_controle'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/painel_controle.html')
    
    def test_atualizar_configuracao_sem_permissao(self):
        """Testa atualização de configuração sem permissão"""
        # Usuário não autenticado deve ser redirecionado para login
        response = self.client.get(reverse('core:atualizar_configuracao'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("core:atualizar_configuracao")}')
        
        # Usuário normal não deve ter acesso
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('core:atualizar_configuracao'))
        self.assertRedirects(response, reverse('core:pagina_inicial'))
    
    def test_atualizar_configuracao_get(self):
        """Testa a página de atualização de configuração (GET)"""
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('core:atualizar_configuracao'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/atualizar_configuracao.html')
    
    def test_atualizar_configuracao_post(self):
        """Testa a atualização de configuração (POST)"""
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.post(reverse('core:atualizar_configuracao'), {
            'nome_sistema': 'Sistema Atualizado',
            'versao': '2.0.0',
            'manutencao_ativa': 'on',
            'mensagem_manutencao': 'Mensagem de manutenção atualizada'
        })
        self.assertRedirects(response, reverse('core:painel_controle'))
        
        # Verifica se a configuração foi atualizada
        config = ConfiguracaoSistema.objects.get(pk=1)
        self.assertEqual(config.nome_sistema, 'Sistema Atualizado')
        self.assertEqual(config.versao, '2.0.0')
        self.assertTrue(config.manutencao_ativa)
        self.assertEqual(config.mensagem_manutencao, 'Mensagem de manutenção atualizada')
        
        # Verifica se o log foi registrado
        log = LogAtividade.objects.last()
        self.assertEqual(log.acao, 'Configurações do sistema atualizadas')


class MiddlewareTests(TestCase):
    """Testes para o middleware de manutenção"""
    
    def setUp(self):
        self.factory = RequestFactory()
        
        # Cria um usuário normal
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
        
        # Cria um usuário staff
        self.staff_user = User.objects.create_user(
            username='staffuser', 
            email='staff@example.com', 
            password='staffpassword',
            is_staff=True
        )
        
        # Garante que existe uma configuração
        self.config = garantir_configuracao_sistema()
        
        # Define uma função simples para o middleware chamar
        def get_response(request):
            return "response"
        
        self.middleware = ManutencaoMiddleware(get_response)
    
    def test_middleware_sem_manutencao(self):
        """Testa o middleware quando o sistema não está em manutenção"""
        self.config.manutencao_ativa = False
        self.config.save()
        
        request = self.factory.get('/')
        request.user = self.user
        
        response = self.middleware(request)
        self.assertEqual(response, "response")
    
    def test_middleware_com_manutencao_usuario_normal(self):
        """Testa o middleware quando o sistema está em manutenção para usuário normal"""
        self.config.manutencao_ativa = True
        self.config.mensagem_manutencao = "Sistema em manutenção para testes"
        self.config.save()
        
        request = self.factory.get('/')
        request.user = self.user
        
        #



## core\urls.py

python
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('entrar/', views.entrar, name='entrar'),
    path('sair/', views.sair, name='sair'),
    path('painel-controle/', views.painel_controle, name='painel_controle'),
    path('atualizar-configuracao/', views.atualizar_configuracao, name='atualizar_configuracao'),
]



## core\utils.py

python
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




## core\views.py

python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .utils import registrar_log, adicionar_mensagem, garantir_configuracao_sistema
from .models import ConfiguracaoSistema
from django.utils import timezone

def pagina_inicial(request):
    """Renderiza a página inicial do sistema"""
    config = garantir_configuracao_sistema()
    
    # Se o sistema estiver em manutenção e o usuário não for admin
    if config.manutencao_ativa and not request.user.is_staff:
        return render(request, 'core/manutencao.html', {
            'mensagem': config.mensagem_manutencao
        })
    
    return render(request, 'core/home.html', {
        'titulo': config.nome_sistema
    })

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

from django.contrib.auth import logout

def sair(request):
    """Realiza o logout do usuário"""
    if request.user.is_authenticated:
        registrar_log(request, 'Logout realizado com sucesso')
        logout(request)
        adicionar_mensagem(request, 'info', 'Você saiu do sistema com sucesso.')
    
    return redirect('core:pagina_inicial')




## core\templates\core\atualizar_configuracao.html

html
{% extends "core/base.html" %}

{% block title %}Atualizar Configurações do Sistema{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Atualizar Configurações do Sistema</h1>
    
    <div class="card mt-4">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="nome_sistema" class="form-label">Nome do Sistema</label>
                    <input type="text" class="form-control" id="nome_sistema" name="nome_sistema" value="{{ config.nome_sistema }}" required>
                </div>
                
                <div class="mb-3">
                    <label for="versao" class="form-label">Versão</label>
                    <input type="text" class="form-control" id="versao" name="versao" value="{{ config.versao }}" required>
                </div>
                
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="manutencao_ativa" name="manutencao_ativa" {% if config.manutencao_ativa %}checked{% endif %}>
                    <label class="form-check-label" for="manutencao_ativa">Sistema em Manutenção</label>
                </div>
                
                <div class="mb-3">
                    <label for="mensagem_manutencao" class="form-label">Mensagem de Manutenção</label>
                    <textarea class="form-control" id="mensagem_manutencao" name="mensagem_manutencao" rows="3">{{ config.mensagem_manutencao }}</textarea>
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'core:painel_controle' %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Salvar Alterações</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




## core\templates\core\base.html

html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Sistema</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'core:painel_controle' %}">Painel de Controle</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'core:sair' %}">Sair</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'core:entrar' %}">Entrar</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>




## core\templates\core\home.html

html
{% extends "core/base.html" %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="jumbotron">
        <h1 class="display-4">Bem-vindo ao {{ titulo }}</h1>
        <p class="lead">Sistema de Gestão para Organizações Maçônicas</p>
        <hr class="my-4">
        <p>Utilize o menu acima para navegar pelo sistema.</p>
        
        {% if user.is_authenticated %}
            <div class="mt-4">
                <h3>Acesso Rápido</h3>
                <div class="row mt-3">
                    <div class="col-md-4 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Atividades Acadêmicas</h5>
                                <p class="card-text">Gerencie atividades acadêmicas do sistema.</p>
                                <a href="{% url 'atividades:atividade_academica_list' %}" class="btn btn-primary">Acessar</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Atividades Ritualísticas</h5>
                                <p class="card-text">Gerencie atividades ritualísticas do sistema.</p>
                                <a href="{% url 'atividades:atividade_ritualistica_list' %}" class="btn btn-primary">Acessar</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Alunos</h5>
                                <p class="card-text">Gerencie os alunos cadastrados no sistema.</p>
                                <a href="{% url 'alunos:listar' %}" class="btn btn-primary">Acessar</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {% else %}
            <a class="btn btn-primary btn-lg" href="{% url 'core:entrar' %}" role="button">Entrar no Sistema</a>
        {% endif %}
    </div>
</div>
{% endblock %}




## core\templates\core\lista_categorias.html

html
{% extends "core/base.html" %}

{% block title %}Categorias{% endblock %}

{% block content %}
    <h1>Categorias</h1>
    
    <div class="row mt-4">
        {% for categoria in categorias %}
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ categoria.nome }}</h5>
                        <p class="card-text">{{ categoria.descricao|truncatewords:20 }}</p>
                        <a href="{% url 'core:detalhe_categoria' categoria.id %}" class="btn btn-primary">Ver detalhes</a>
                    </div>
                </div>
            </div>
        {% empty %}
            <div class="col-12">
                <p>Nenhuma categoria encontrada.</p>
            </div>
        {% endfor %}
    </div>
{% endblock %}




## core\templates\core\login.html

html
{% extends "core/base.html" %}

{% block title %}Entrar no Sistema{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">Entrar no Sistema</h4>
                </div>
                <div class="card-body">
                    <form method="post" class="needs-validation" novalidate>
                        {% csrf_token %}
                        
                        {% if form.errors %}
                            <div class="alert alert-danger">
                                Seu nome de usuário e senha não correspondem. Por favor, tente novamente.
                            </div>
                        {% endif %}
                        
                        <div class="mb-3">
                            <label for="id_username" class="form-label">Nome de usuário</label>
                            <input type="text" name="username" id="id_username" class="form-control" required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="id_password" class="form-label">Senha</label>
                            <input type="password" name="password" id="id_password" class="form-control" required>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">Entrar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}




## core\templates\core\manutencao.html

html
{% extends "core/base.html" %}

{% block title %}Sistema em Manutenção{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8 text-center">
            <div class="alert alert-warning">
                <h2><i class="fas fa-tools"></i> Sistema em Manutenção</h2>
                <p class="lead mt-3">
                    Estamos realizando melhorias no sistema. Por favor, tente novamente mais tarde.
                </p>
                {% if mensagem %}
                    <div class="mt-4">
                        <p>{{ mensagem }}</p>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}




## core\templates\core\painel_controle.html

html
{% extends "core/base.html" %}

{% block title %}Painel de Controle{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Painel de Controle</h1>
    
    <div class="row mt-4">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Configurações do Sistema</h5>
                </div>
                <div class="card-body">
                    <p><strong>Nome do Sistema:</strong> {{ config.nome_sistema }}</p>
                    <p><strong>Versão:</strong> {{ config.versao }}</p>
                    <p><strong>Última Atualização:</strong> {{ config.data_atualizacao|date:"d/m/Y H:i" }}</p>
                    <p>
                        <strong>Status:</strong> 
                        {% if config.manutencao_ativa %}
                            <span class="badge bg-warning">Em Manutenção</span>
                        {% else %}
                            <span class="badge bg-success">Operacional</span>
                        {% endif %}
                    </p>
                    
                    <a href="{% url 'core:atualizar_configuracao' %}" class="btn btn-primary">
                        Editar Configurações
                    </a>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Logs Recentes</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Tipo</th>
                                    <th>Ação</th>
                                    <th>Usuário</th>
                                    <th>Data</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for log in logs_recentes %}
                                <tr>
                                    <td>
                                        {% if log.tipo == 'INFO' %}
                                            <span class="badge bg-info">INFO</span>
                                        {% elif log.tipo == 'AVISO' %}
                                            <span class="badge bg-warning">AVISO</span>
                                        {% elif log.tipo == 'ERRO' %}
                                            <span class="badge bg-danger">ERRO</span>
                                        {% else %}
                                            <span class="badge bg-secondary">{{ log.tipo }}</span>
                                        {% endif %}
                                    </td>
                                    <td>{{ log.acao }}</td>
                                    <td>{{ log.usuario }}</td>
                                    <td>{{ log.data|date:"d/m/Y H:i" }}</td>
                                </tr>
                                {% empty %}
                                <tr>
                                    <td colspan="4" class="text-center">Nenhum log encontrado</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    
                    <a href="{% url 'admin:core_logatividade_changelist' %}" class="btn btn-primary">
                        Ver Todos os Logs
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}


