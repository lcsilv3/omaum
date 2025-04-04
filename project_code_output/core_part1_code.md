# Código da Funcionalidade: core - Parte 1/2
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
from django.utils import timezone
from datetime import timedelta
import importlib

def manutencao_middleware(get_response):
    """
    Middleware para controle de manutenção do sistema.
    """
    def middleware(request):
        # Importa o modelo aqui para evitar importação circular
        ConfiguracaoSistema = importlib.import_module('core.models').ConfiguracaoSistema
        
        # Verifica se o sistema está em manutenção
        try:
            config = ConfiguracaoSistema.objects.first()
            if config and config.manutencao_ativa:
                # Se o usuário não for staff, redireciona para a página de manutenção
                if not hasattr(request, 'user') or not request.user.is_staff:
                    from django.shortcuts import render
                    return render(request, 'core/manutencao.html', {
                        'mensagem': config.mensagem_manutencao
                    })
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
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Obtém o horário da última atividade da sessão
            ultima_atividade = request.session.get('ultima_atividade')
            
            # Obtém o horário atual
            agora = timezone.now()
            
            # Se houver um registro de última atividade e for mais antigo que o limite de aviso
            if ultima_atividade:
                try:
                    ultima_atividade = timezone.datetime.fromisoformat(ultima_atividade)
                    tempo_desde_ultima_atividade = agora - ultima_atividade
                    
                    # Se o usuário estiver inativo por muito tempo
                    if tempo_desde_ultima_atividade > timedelta(seconds=3600):  # SESSION_SECURITY_EXPIRE_AFTER
                        # Poderia forçar logout aqui se desejado
                        pass
                    # Se estiver se aproximando do limite de inatividade, definir um aviso
                    elif tempo_desde_ultima_atividade > timedelta(seconds=3000):  # SESSION_SECURITY_WARN_AFTER
                        request.session['mostrar_aviso_inatividade'] = True
                except (ValueError, TypeError):
                    # Se houver erro ao converter a data, reinicia o contador
                    pass
            
            # Atualiza o horário da última atividade
            request.session['ultima_atividade'] = agora.isoformat()
            request.session['mostrar_aviso_inatividade'] = False
        
        response = get_response(request)
        return response
    
    return middleware





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
        ordering = ['-data']  # Garante que os logs mais recentes apareçam primeiro




## core\tests.py

python
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
import importlib
import time  # Importar o módulo time para adicionar atraso

from .models import ConfiguracaoSistema, LogAtividade
from .views import pagina_inicial, entrar, painel_controle, atualizar_configuracao
from .utils import registrar_log, adicionar_mensagem, garantir_configuracao_sistema
from .middleware import manutencao_middleware


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
        from django.utils import timezone
        import datetime
        
        # Criar o primeiro log com uma data específica
        data_antiga = timezone.now() - datetime.timedelta(minutes=5)
        log1 = LogAtividade.objects.create(
            usuario="user1", 
            acao="acao1",
            data=data_antiga  # Definir uma data mais antiga
        )
        
        # Criar o segundo log com a data atual (mais recente)
        log2 = LogAtividade.objects.create(
            usuario="user2", 
            acao="acao2"
            # data padrão será timezone.now()
        )
        
        # Buscar todos os logs (devem estar ordenados por data decrescente)
        logs = LogAtividade.objects.all()
        
        # Verificar se o log2 (mais recente) aparece primeiro
        self.assertEqual(logs[0], log2)


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
        self.assertEqual(config.nome_sistema, "Sistema de Gestão de Iniciados da OmAum")
        
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
        self.assertEqual(response.status_code, 302)  # 302 é o código para redirecionamento
    
    def test_painel_controle_sem_permissao(self):
        """Testa acesso ao painel de controle sem permissão"""
        # Usuário não autenticado deve ser redirecionado para login
        response = self.client.get(reverse('core:painel_controle'))
        self.assertEqual(response.status_code, 302)  # 302 é o código para redirecionamento
        
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
        self.assertEqual(response.status_code, 302)  # 302 é o código para redirecionamento
        
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
        
        self.middleware = manutencao_middleware(get_response)
    
    def test_middleware_sem_manutencao(self):
        """Testa o middleware quando o sistema não está em manutenção"""
        self.config.manutencao_ativa = False
        self.config.save()
        
        request = self.factory.get('/')
        request.user = self.user
        
        response = self.middleware(request)
        self.assertEqual(response, "response")





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
    path('csrf_check/', views.csrf_check, name='csrf_check'),
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
            'nome_sistema': 'Sistema de Gestão de Iniciados da OmAum',
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
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .utils import registrar_log, adicionar_mensagem, garantir_configuracao_sistema
from .models import ConfiguracaoSistema, LogAtividade
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

def pagina_inicial(request):
    # Adicionar título para o template
    context = {
        'titulo': 'Sistema de Gestão de Iniciados da OmAum'
    }
    return render(request, 'core/home.html', context)

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
    
    # Adicionar título para o template
    context = {
        'form': form,
        'titulo': 'Sistema de Gestão de Iniciados da OmAum'
    }
    return render(request, 'core/login.html', context)

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
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})  # Sempre retornar OK para evitar falsos positivos





## core\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-04-03 17:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoSistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_sistema', models.CharField(default='OMAUM', max_length=100)),
                ('versao', models.CharField(default='1.0.0', max_length=20)),
                ('data_atualizacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('manutencao_ativa', models.BooleanField(default=False)),
                ('mensagem_manutencao', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Configuração do Sistema',
                'verbose_name_plural': 'Configurações do Sistema',
            },
        ),
        migrations.CreateModel(
            name='LogAtividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=100)),
                ('acao', models.CharField(max_length=255)),
                ('tipo', models.CharField(choices=[('INFO', 'Informação'), ('AVISO', 'Aviso'), ('ERRO', 'Erro'), ('DEBUG', 'Depuração')], default='INFO', max_length=10)),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('detalhes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Log de Atividade',
                'verbose_name_plural': 'Logs de Atividades',
                'ordering': ['-data'],
            },
        ),
    ]



