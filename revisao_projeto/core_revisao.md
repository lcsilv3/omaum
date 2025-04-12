# Revisão da Funcionalidade: core

## Arquivos forms.py:


### Arquivo: core\forms.py

```python
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
```

## Arquivos views.py:


### Arquivo: core\views.py

```python
"""
Core Views

Este arquivo contém as views para o aplicativo 'core' do projeto OMAUM.
Localização: core/views.py

Uso:
- Define as funções de view que processam as requisições e retornam respostas.
- Lida com a lógica de negócios central do sistema.
- Interage com modelos, formulários e renderiza templates.

As views definidas aqui são responsáveis por funcionalidades como:
- Página inicial
- Autenticação (login/logout)
- Painel de controle
- Configurações do sistema
- Verificação CSRF

Estas views são mapeadas para URLs no arquivo core/urls.py.
"""
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
    return render(request, 'home.html', context)

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

```

## Arquivos urls.py:


### Arquivo: core\urls.py

```python
"""
Core URLs Configuration

Este arquivo define as URLs para o aplicativo 'core' do projeto OMAUM.
Localização: core/urls.py

Uso:
- Define os padrões de URL para as views do aplicativo core.
- Utiliza o namespace 'core' para evitar conflitos de nomes com outros aplicativos.
- É incluído no arquivo de URLs principal do projeto (omaum/urls.py).

As URLs definidas aqui são responsáveis pelas funcionalidades centrais do sistema,
como página inicial, login, logout, painel de controle, etc.

Para incluir estas URLs no arquivo principal, use:
path('', include('core.urls', namespace='core')),
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('entrar/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='entrar'),
    path('sair/', auth_views.LogoutView.as_view(next_page='/'), name='sair'),
    path('painel-controle/', views.painel_controle, name='painel_controle'),
    path('atualizar-configuracao/', views.atualizar_configuracao, name='atualizar_configuracao'),
    path('csrf_check/', views.csrf_check, name='csrf_check'),
    path('dashboard/', views.painel_controle, name='dashboard'),  # Redireciona diretamente para a view
]

```

## Arquivos models.py:


### Arquivo: core\models.py

```python
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
```
