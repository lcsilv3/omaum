# Revisão da Funcionalidade: atividades

## Arquivos forms.py:


### Arquivo: atividades\forms.py

```python
print("ARQUIVO FORMS.PY CARREGADO")
from django import forms
from importlib import import_module
# resto do c√≥digo...

def get_atividade_academica_model():
    try:
        atividades_module = import_module('atividades.models')
        return getattr(atividades_module, 'AtividadeAcademica')
    except (ImportError, AttributeError):
        return None

def get_atividade_ritualistica_model():
    try:
        atividades_module = import_module('atividades.models')
        return getattr(atividades_module, 'AtividadeRitualistica')
    except (ImportError, AttributeError):
        return None

class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = get_atividade_academica_model()
        fields = ['nome', 'descricao', 'data_inicio', 'data_fim', 'turma']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
        }

class AtividadeRitualisticaForm(forms.ModelForm):
    todos_alunos = forms.BooleanField(
        required=False, 
        label="Incluir todos os alunos da turma",
        initial=False
    )
    
    class Meta:
        model = get_atividade_ritualistica_model()
        fields = ['nome', 'descricao', 'data', 'hora_inicio', 'hora_fim', 'local', 'turma', 'participantes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'participantes': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
def criar_form_atividade_academica():
    return AtividadeAcademicaForm
def criar_form_atividade_ritualistica():
    return AtividadeRitualisticaForm

```

## Arquivos views.py:


### Arquivo: atividades\views.py

```python
import importlib
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse

# Set up logger
logger = logging.getLogger(__name__)

print(
    "ARQUIVO VIEWS.PY CARREGADO:",
    importlib.import_module("django.conf").settings.BASE_DIR,
)


def get_return_url(request, default_url):
    """Obtém a URL de retorno do request ou usa o valor padrão."""
    return_url = request.GET.get("return_url", "")
    # Verificação básica de segurança
    if not return_url or not return_url.startswith("/"):
        return default_url
    return return_url


def get_form_class(form_name):
    """Importa dinamicamente uma classe de formulário para evitar importações circulares."""
    forms_module = importlib.import_module("atividades.forms")
    return getattr(forms_module, form_name)


def get_model_class(model_name, module_name="atividades.models"):
    """Importa dinamicamente uma classe de modelo para evitar importações circulares."""
    models_module = importlib.import_module(module_name)
    return getattr(models_module, model_name)


@login_required
def index(request):
    """Página inicial do módulo de atividades."""
    return render(request, 'atividades/index.html')


@login_required
def listar_atividades_academicas(request):
    """Lista todas as atividades acadêmicas."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividades = AtividadeAcademica.objects.all()

    # Armazenar a URL atual na sessão para uso posterior
    request.session["last_academicas_list_url"] = request.get_full_path()

    return render(
        request,
        "atividades/listar_atividades_academicas.html",
        {
            "atividades": atividades,
            "return_url": request.path,  # Armazena URL atual para retorno
        },
    )


@login_required
def listar_atividades_ritualisticas(request):
    """Lista todas as atividades ritualísticas."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividades = AtividadeRitualistica.objects.all()

    # Armazenar a URL atual na sessão para uso posterior
    request.session["last_ritualisticas_list_url"] = request.get_full_path()

    # Salvar URL referenciadora, exceto se vier do próprio formulário de atividade ritualística
    referer = request.META.get("HTTP_REFERER", "")
    if referer and not any(
        x in referer
        for x in ["criar_atividade_ritualistica", "editar_atividade_ritualistica"]
    ):
        request.session["atividade_ritualistica_referer"] = referer

    # Usar a URL referenciadora armazenada ou a página inicial como fallback
    previous_url = request.session.get("atividade_ritualistica_referer", "/")

    return render(
        request,
        "atividades/listar_atividades_ritualisticas.html",
        {
            "atividades": atividades,
            "previous_url": previous_url,
        },
    )


@login_required
def criar_atividade_academica(request):
    """Função para criar uma nova atividade acadêmica."""
    AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        form = AtividadeAcademicaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Atividade acadêmica criada com sucesso.")
            return redirect(return_url)
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = AtividadeAcademicaForm()

    return render(
        request,
        "atividades/formulario_atividade_academica.html",
        {"form": form, "return_url": return_url},
    )


@login_required
def editar_atividade_academica(request, pk):
    """Função para editar uma atividade acadêmica existente."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            form = AtividadeAcademicaForm(request.POST, instance=atividade)
            if form.is_valid():
                form.save()
                messages.success(request, "Atividade acadêmica atualizada com sucesso.")
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            messages.error(
                request,
                f"Erro ao processar formulário de atividade acadêmica: {str(e)}",
            )
    else:
        form = AtividadeAcademicaForm(instance=atividade)

    return render(
        request,
        "atividades/formulario_atividade_academica.html",
        {"form": form, "atividade": atividade, "return_url": return_url},
    )


@login_required
def excluir_atividade_academica(request, pk):
    """Função para excluir uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(request, "Atividade acadêmica excluída com sucesso.")
            return redirect(return_url)
        except Exception as e:
            messages.error(request, f"Erro ao excluir atividade acadêmica: {str(e)}")
            return redirect("atividades:listar_atividades_academicas")

    return render(
        request,
        "atividades/confirmar_exclusao_academica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def confirmar_exclusao_academica(request, pk):
    """Função para confirmar a exclusão de uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(request, "Atividade acadêmica excluída com sucesso.")
            return redirect(return_url)
        except Exception as e:
            messages.error(request, f"Erro ao excluir atividade acadêmica: {str(e)}")
            return redirect("atividades:detalhar_atividade_academica", pk=pk)

    return render(
        request,
        "atividades/confirmar_exclusao_academica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def detalhar_atividade_academica(request, pk):
    """Função para mostrar detalhes de uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_academicas")
    )

    return render(
        request,
        "atividades/detalhar_atividade_academica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def criar_atividade_ritualistica(request):
    """Função para criar uma nova atividade ritualística."""
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            form = AtividadeRitualisticaForm(request.POST)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.save()

                # Processar o campo todos_alunos se existir
                if hasattr(form, "cleaned_data") and form.cleaned_data.get(
                    "todos_alunos"
                ):
                    # Obter todos os alunos da turma e adicioná-los à atividade
                    Aluno = get_model_class("Aluno", module_name="alunos.models")
                    alunos_da_turma = Aluno.objects.filter(turmas=atividade.turma)
                    for aluno in alunos_da_turma:
                        atividade.participantes.add(aluno)
                else:
                    # Salvar apenas os participantes selecionados no formulário
                    form.save_m2m()

                messages.success(request, "Atividade ritualística criada com sucesso.")
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            messages.error(
                request,
                f"Erro ao processar formulário de atividade ritualística: {str(e)}",
            )
    else:
        form = AtividadeRitualisticaForm()

    return render(
        request,
        "atividades/criar_atividade_ritualistica.html",
        {"form": form, "return_url": return_url},
    )


@login_required
def editar_atividade_ritualistica(request, pk):
    """Função para editar uma atividade ritualística existente."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            form = AtividadeRitualisticaForm(request.POST, instance=atividade)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.save()

                # Processar o campo todos_alunos se existir
                if hasattr(form, "cleaned_data") and form.cleaned_data.get(
                    "todos_alunos"
                ):
                    # Limpar participantes existentes
                    atividade.participantes.clear()
                    # Obter todos os alunos da turma e adicioná-los à atividade
                    Aluno = get_model_class("Aluno", module_name="alunos.models")
                    alunos_da_turma = Aluno.objects.filter(turmas=atividade.turma)
                    for aluno in alunos_da_turma:
                        atividade.participantes.add(aluno)
                else:
                    # Salvar apenas os participantes selecionados no formulário
                    form.save_m2m()

                messages.success(
                    request, "Atividade ritualística atualizada com sucesso."
                )
                return redirect(return_url)
            else:
                messages.error(request, "Corrija os erros no formulário.")
        except Exception as e:
            messages.error(
                request,
                f"Erro ao processar formulário de atividade ritualística: {str(e)}",
            )
    else:
        form = AtividadeRitualisticaForm(instance=atividade)

    return render(
        request,
        "atividades/editar_atividade_ritualistica.html",
        {"form": form, "atividade": atividade, "return_url": return_url},
    )


@login_required
def excluir_atividade_ritualistica(request, pk):
    """Função para excluir uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(request, "Atividade ritualística excluída com sucesso.")
            return redirect(return_url)
        except Exception as e:
            messages.error(request, f"Erro ao excluir atividade ritualística: {str(e)}")
            return redirect("atividades:listar_atividades_ritualisticas")

    return render(
        request,
        "atividades/confirmar_exclusao_ritualistica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def confirmar_exclusao_ritualistica(request, pk):
    """Função para confirmar a exclusão de uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(request, "Atividade ritualística excluída com sucesso.")
            return redirect(return_url)
        except Exception as e:
            messages.error(request, f"Erro ao excluir atividade ritualística: {str(e)}")
            return redirect("atividades:detalhar_atividade_ritualistica", pk=pk)

    return render(
        request,
        "atividades/confirmar_exclusao_ritualistica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def detalhar_atividade_ritualistica(request, pk):
    """Função para mostrar detalhes de uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    return_url = request.GET.get(
        "return_url", reverse("atividades:listar_atividades_ritualisticas")
    )

    return render(
        request,
        "atividades/detalhar_atividade_ritualistica.html",
        {"atividade": atividade, "return_url": return_url},
    )

```

## Arquivos urls.py:


### Arquivo: atividades\urls.py

```python
from django.urls import path
from . import views

app_name = 'atividades'  # Definindo o namespace

urlpatterns = [
    path('', views.index, name='listar'),  # Página de índice/agregador
    # Atividades Acadêmicas
    path('academicas/', views.listar_atividades_academicas, name='listar_atividades_academicas'),
    path('academicas/criar/', views.criar_atividade_academica, name='criar_atividade_academica'),
    path('academicas/editar/<int:pk>/', views.editar_atividade_academica, name='editar_atividade_academica'),
    path('academicas/excluir/<int:pk>/', views.excluir_atividade_academica, name='excluir_atividade_academica'),
    path('academicas/detalhar/<int:pk>/', views.detalhar_atividade_academica, name='detalhar_atividade_academica'),
    path('academicas/confirmar-exclusao/<int:pk>/', views.confirmar_exclusao_academica, name='confirmar_exclusao_academica'),
    
    # Atividades Ritualísticas
    path('ritualisticas/', views.listar_atividades_ritualisticas, name='listar_atividades_ritualisticas'),
    path('ritualisticas/criar/', views.criar_atividade_ritualistica, name='criar_atividade_ritualistica'),
    path('ritualisticas/editar/<int:pk>/', views.editar_atividade_ritualistica, name='editar_atividade_ritualistica'),
    path('ritualisticas/excluir/<int:pk>/', views.excluir_atividade_ritualistica, name='excluir_atividade_ritualistica'),
    path('ritualisticas/detalhar/<int:pk>/', views.detalhar_atividade_ritualistica, name='detalhar_atividade_ritualistica'),
    path('ritualisticas/confirmar-exclusao/<int:pk>/', views.confirmar_exclusao_ritualistica, name='confirmar_exclusao_ritualistica'),
]

```

## Arquivos models.py:


### Arquivo: atividades\models.py

```python
# Adicione o seguinte código temporário para diagnóstico no início do arquivo:

print("CARREGANDO MODELS.PY")
# Imprimir os campos do modelo para diagnóstico
try:
    from django.db import models
    import inspect
    
    # Carregar o módulo atual
    import sys
    current_module = sys.modules[__name__]
    
    # Encontrar todas as classes de modelo no módulo
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, models.Model) and obj != models.Model:
            print(f"Modelo: {name}")
            for field in obj._meta.fields:
                print(f"  - {field.name} ({field.__class__.__name__})")
except Exception as e:
    print(f"Erro ao inspecionar modelos: {e}")

from django.db import models
from django.utils import timezone
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_turma_model():
    turmas_module = import_module('turmas.models')
    return getattr(turmas_module, 'Turma')

class AtividadeAcademica(models.Model):
    TIPO_CHOICES = (
        ('aula', 'Aula'),
        ('palestra', 'Palestra'),
        ('workshop', 'Workshop'),
        ('seminario', 'Seminário'),
        ('outro', 'Outro'),
    )
    
    STATUS_CHOICES = (
        ('agendada', 'Agendada'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    )
    
    nome = models.CharField(max_length=100)
    
    @property
    def titulo(self):
        return self.nome
    
    @titulo.setter
    def titulo(self, value):
        self.nome = value
        
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    data_inicio = models.DateTimeField(default=timezone.now, verbose_name="Data de Início")
    data_fim = models.DateTimeField(blank=True, null=True, verbose_name="Data de Término")
    responsavel = models.CharField(max_length=100, blank=True, null=True, verbose_name="Responsável")
    local = models.CharField(max_length=100, blank=True, null=True, verbose_name="Local")
    tipo_atividade = models.CharField(max_length=20, choices=TIPO_CHOICES, default='aula', verbose_name="Tipo de Atividade")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendada', verbose_name="Status")
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE, related_name='atividades_academicas')    
    def __str__(self):
        return self.titulo or self.nome
    
    class Meta:
        verbose_name = 'Atividade Acadêmica'
        verbose_name_plural = 'Atividades Acadêmicas'

class AtividadeRitualistica(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    data = models.DateField(verbose_name='Data')
    hora_inicio = models.TimeField(verbose_name='Hora de Início')
    hora_fim = models.TimeField(verbose_name='Hora de Término')
    local = models.CharField(max_length=100, verbose_name='Local')
    turma = models.ForeignKey(
        get_turma_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Turma'
    )
    participantes = models.ManyToManyField(
        get_aluno_model(), 
        blank=True, 
        verbose_name='Participantes',
        related_name='atividades_ritualisticas'
    )
    
    def __str__(self):
        return f"{self.nome} - {self.data}"
    
    class Meta:
        verbose_name = 'Atividade Ritualística'
        verbose_name_plural = 'Atividades Ritualísticas'
        ordering = ['-data', 'hora_inicio']

```

## Arquivos de Template:


### Arquivo: atividades\templates\atividades\confirmar_exclusao_academica.html

```html
{% extends 'base.html' %}

{% block title %}Confirmar Exclusão de Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Confirmar Exclusão</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade acadêmica "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
            <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
            <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
            <p><strong>Local:</strong> {{ atividade.local|default:"Não informado" }}</p>
            <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
            <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma.nome }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <!-- Adicionar um campo oculto para a URL de retorno -->
        <input type="hidden" name="return_url" value="{{ return_url }}">
        <button type="submit" class="btn btn-danger">Sim, excluir</button>
        <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
    </form></div>
{% endblock %}

```


### Arquivo: atividades\templates\atividades\confirmar_exclusao_ritualistica.html

```html
{% extends 'base.html' %}

{% block title %}Excluir Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Ritualística</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade ritualística "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
            <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
            <p><strong>Local:</strong> {{ atividade.local }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
            <p><strong>Total de Participantes:</strong> {{ atividade.participantes.count }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <input type="hidden" name="return_url" value="{{ return_url }}">
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}
```


### Arquivo: atividades\templates\atividades\criar_atividade_academica.html

```html
{% extends 'base.html' %}

{% block title %}Criar Nova Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Criar Nova Atividade Acadêmica</h1>
        <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=<form action="" class="nome"></form> %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.responsavel %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Local</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Classificação</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}
<div class="d-flex justify-content-between mb-5">
    <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Voltar para a lista</a>
    <button type="submit" class="btn btn-primary">Criar Atividade</button>
</div>
```


### Arquivo: atividades\templates\atividades\criar_atividade_ritualistica.html

```html
{% extends 'base.html' %}

{% block title %}Criar Nova Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Criar Nova Atividade Ritualística</h1>
        <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Horário</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turma e Participantes</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.todos_alunos %}
                        <small class="form-text text-muted">Marque esta opção para incluir automaticamente todos os alunos da turma.</small>
                    </div>
                </div>
                
                <div class="row mt-3" id="participantes-container">
                    <div class="col-md-12">
                        <label for="{{ form.participantes.id_for_label }}">{{ form.participantes.label }}</label>
                        <div class="border p-3 rounded">
                            {{ form.participantes }}
                        </div>
                        {% if form.participantes.errors %}
                            <div class="text-danger">
                                {{ form.participantes.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const todosAlunosCheckbox = document.getElementById('{{ form.todos_alunos.id_for_label }}');
        const participantesContainer = document.getElementById('participantes-container');
        
        function toggleParticipantes() {
            if (todosAlunosCheckbox.checked) {
                participantesContainer.style.display = 'none';
            } else {
                participantesContainer.style.display = 'block';
            }
        }
        
        // Inicializar
        toggleParticipantes();
        
        // Adicionar listener para mudanças
        todosAlunosCheckbox.addEventListener('change', toggleParticipantes);
    });
</script>
{% endblock %}

```


### Arquivo: atividades\templates\atividades\detalhar_atividade_academica.html

```html
{% extends 'base.html' %}

{% block title %}Detalhes da Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Detalhes da Atividade Acadêmica</h1>
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">{{ atividade.nome }}</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
                    <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
                    <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Turma:</strong> {{ atividade.turma.nome }}</p>
                    <p><strong>Status:</strong> 
                        {% if atividade.ativa %}
                            <span class="badge bg-success">Ativa</span>
                        {% else %}
                            <span class="badge bg-danger">Inativa</span>
                        {% endif %}
                    </p>
                </div>
            </div>
            
            <div class="mt-3">
                <a href="{% url 'atividades:editar_atividade_academica' atividade.pk %}?return_url={{ request.path|urlencode }}" class="btn btn-primary">Editar</a>
                <a href="{% url 'atividades:confirmar_exclusao_academica' atividade.pk %}?return_url={{ request.path|urlencode }}" class="btn btn-danger">Excluir</a>
                <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Voltar para Lista</a>
            </div>        </div>
    </div>
</div>
{% endblock %}

```


### Arquivo: atividades\templates\atividades\detalhar_atividade_ritualistica.html

```html
{% extends 'base.html' %}

{% block title %}Detalhes da Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{{ atividade.nome }}</h1>
        <div>
            <a href="{{ return_url }}" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-secondary me-2">Lista de Atividades</a>
            <a href="{% url 'atividades:editar_atividade_ritualistica' atividade.id %}?return_url={{ request.path|urlencode }}" class="btn btn-warning me-2">Editar</a>
            <a href="{% url 'atividades:confirmar_exclusao_ritualistica' atividade.id %}?return_url={{ request.path|urlencode }}" class="btn btn-danger">Excluir</a>
        </div>
    </div>    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Informações Básicas</h5>
                </div>
                <div class="card-body">
                    <p><strong>Descrição:</strong> {{ atividade.descricao|default:"Não informada" }}</p>
                    <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
                    <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
                    <p><strong>Local:</strong> {{ atividade.local }}</p>
                    <p><strong>Turma:</strong> {{ atividade.turma }}</p>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Estatísticas</h5>
                </div>
                <div class="card-body">
                    <p><strong>Total de Participantes:</strong> {{ total_participantes }}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Participantes</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Número Iniciático</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in atividade.participantes.all %}
                            <tr>
                                <td>{{ aluno.nome }}</td>
                                <td>{{ aluno.numero_iniciatico|default:"N/A" }}</td>
                                <td>{{ aluno.email }}</td>
                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="3" class="text-center">
                                    <p class="my-3">Nenhum participante cadastrado para esta atividade.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}

```


### Arquivo: atividades\templates\atividades\editar_atividade_academica.html

```html
{% extends 'base.html' %}

{% block title %}Editar Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Atividade Acadêmica</h1>
        <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Voltar para detalhes</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.responsavel %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Local</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Classificação</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Atualizar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}

```


### Arquivo: atividades\templates\atividades\editar_atividade_ritualistica.html

```html
{% extends 'base.html' %}

{% block title %}Editar Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Atividade Ritualística</h1>
        <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Voltar para detalhes</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Horário</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turma e Participantes</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.todos_alunos %}
                        <small class="form-text text-muted">Marque esta opção para incluir automaticamente todos os alunos da turma.</small>
                    </div>
                </div>
                
                <div class="row mt-3" id="participantes-container">
                    <div class="col-md-12">
                        <label for="{{ form.participantes.id_for_label }}">{{ form.participantes.label }}</label>
                        <div class="border p-3 rounded">
                            {{ form.participantes }}
                        </div>
                        {% if form.participantes.errors %}
                            <div class="text-danger">
                                {{ form.participantes.errors }}
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Atualizar Atividade</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const todosAlunosCheckbox = document.getElementById('{{ form.todos_alunos.id_for_label }}');
        const participantesContainer = document.getElementById('participantes-container');
        
        function toggleParticipantes() {
            if (todosAlunosCheckbox.checked) {
                participantesContainer.style.display = 'none';
            } else {
                participantesContainer.style.display = 'block';
            }
        }
        
        // Inicializar
        toggleParticipantes();
        
        // Adicionar listener para mudanças
        todosAlunosCheckbox.addEventListener('change', toggleParticipantes);
    });
</script>
{% endblock %}

```


### Arquivo: atividades\templates\atividades\excluir_atividade_academica.html

```html
{% extends 'base.html' %}

{% block title %}Excluir Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Acadêmica</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade acadêmica "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Responsável:</strong> {{ atividade.responsavel|default:"Não informado" }}</p>
            <p><strong>Data de Início:</strong> {{ atividade.data_inicio|date:"d/m/Y H:i" }}</p>
            <p><strong>Data de Término:</strong> {{ atividade.data_fim|date:"d/m/Y H:i"|default:"Não definida" }}</p>
            <p><strong>Local:</strong> {{ atividade.local|default:"Não informado" }}</p>
            <p><strong>Tipo:</strong> {{ atividade.get_tipo_atividade_display }}</p>
            <p><strong>Status:</strong> {{ atividade.get_status_display }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}

```


### Arquivo: atividades\templates\atividades\excluir_atividade_ritualistica.html

```html
{% extends 'base.html' %}

{% block title %}Excluir Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Atividade Ritualística</h1>
    
    <div class="alert alert-danger">
        <p>Tem certeza que deseja excluir a atividade ritualística "{{ atividade.nome }}"?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5>Informações da Atividade</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome:</strong> {{ atividade.nome }}</p>
            <p><strong>Data:</strong> {{ atividade.data|date:"d/m/Y" }}</p>
            <p><strong>Horário:</strong> {{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</p>
            <p><strong>Local:</strong> {{ atividade.local }}</p>
            <p><strong>Turma:</strong> {{ atividade.turma }}</p>
            <p><strong>Total de Participantes:</strong> {{ atividade.participantes.count }}</p>
        </div>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="d-flex">
            <button type="submit" class="btn btn-danger me-2">Sim, excluir</button>
            <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}

```


### Arquivo: atividades\templates\atividades\formulario_atividade_academica.html

```html
{% extends 'base.html' %}
{% block title %}Criar Nova Atividade Acadêmica{% endblock %}
{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Acadêmica</h1>
        <a href="{{ return_url }}" class="btn btn-secondary me-2">Voltar</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.responsavel %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Local</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_inicio %}
                    </div>
                    <div class="col-md-3">
                        {% include 'includes/form_field.html' with field=form.data_fim %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Classificação</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.tipo_atividade %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.status %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <!-- Use a URL de retorno fornecida pela view -->
            <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                {% if atividade %}Atualizar{% else %}Criar{% endif %} Atividade
            </button>
        </div>
    </form>
</div>
{% endblock %}

```


### Arquivo: atividades\templates\atividades\formulario_atividade_ritualistica.html

```html
{% extends 'base.html' %}

{% block title %}{% if atividade %}Editar{% else %}Nova{% endif %} Atividade Ritualística{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if atividade %}Editar{% else %}Nova{% endif %} Atividade Ritualística</h1>
        <a href="{{ return_url }}" class="btn btn-secondary">Voltar para a lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.nome %}
                    </div>
                    <div class="col-md-6">
                        {% include 'includes/form_field.html' with field=form.local %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.descricao %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Data e Horário</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.data %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_inicio %}
                    </div>
                    <div class="col-md-4">
                        {% include 'includes/form_field.html' with field=form.hora_fim %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5>Turma e Participantes</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.turma %}
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-md-12">
                        {% include 'includes/form_field.html' with field=form.participantes %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between mb-5">
            <a href="{{ return_url }}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">
                {% if atividade %}Atualizar{% else %}Criar{% endif %} Atividade
            </button>
        </div>
    </form>
</div>
{% endblock %}
```


### Arquivo: atividades\templates\atividades\index.html

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Atividades - OMAUM{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Atividades</h1>
        <a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>
    </div>
    
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Atividades Acadêmicas</h5>
                    <p class="card-text">Gerenciamento de atividades relacionadas ao ensino e aprendizagem.</p>
                    <p class="card-text text-muted">Aulas, workshops, palestras, seminários e outras atividades educacionais.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:listar_atividades_academicas' %}" class="btn btn-primary">Gerenciar Atividades Acadêmicas</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-6 mb-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">Atividades Ritualísticas</h5>
                    <p class="card-text">Gerenciamento de atividades relacionadas a rituais e cerimônias.</p>
                    <p class="card-text text-muted">Cerimônias, rituais, meditações coletivas e outras práticas espirituais.</p>
                </div>
                <div class="card-footer bg-transparent border-top-0">
                    <a href="{% url 'atividades:listar_atividades_ritualisticas' %}" class="btn btn-primary">Gerenciar Atividades Ritualísticas</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

```


### Arquivo: atividades\templates\atividades\listar_atividades_academicas.html

```html
{% extends 'base.html' %}

{% block title %}Lista de Atividades Acadêmicas{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Atividades Acadêmicas</h1>
        <div>
            <!-- Use uma URL específica em vez de javascript:history.back() -->
            <a href="{% url 'core:pagina_inicial' %}" class="btn btn-secondary me-2">Página Inicial</a>
            
            <!-- Botão para criar nova atividade acadêmica com URL de retorno -->
            <a href="{% url 'atividades:criar_atividade_academica' %}?return_url={{ request.path|urlencode }}" class="btn btn-primary">
                Nova Atividade Acadêmica
            </a>
        </div>
    </div>    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por título, descrição ou responsável..." value="{{ query }}">
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Filtrar</button>
                </div>
            </form>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Título</th>
                            <th>Responsável</th>
                            <th>Data de Início</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for atividade in atividades %}
                            <tr>
                                <td>{{ atividade.nome }}</td>
                                <td>{{ atividade.descrição }}</td>
                                <td>{{ atividade.data_inicio|date:"d/m/Y" }}</td>
                                <td>{{ atividade.get_status_display }}</td>
                                <td>
                                    <a href="{% url 'atividades:detalhar_atividade_academica' atividade.id %}" class="btn btn-sm btn-info">Detalhes</a>
                                    <a href="{% url 'atividades:editar_atividade_academica' atividade.id %}" class="btn btn-sm btn-warning">Editar</a>
                                    <a href="{% url 'atividades:excluir_atividade_academica' atividade.id %}" class="btn btn-sm btn-danger">Excluir</a>                                </td>                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="5" class="text-center">
                                    <p class="my-3">Nenhuma atividade acadêmica cadastrada.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <p class="text-muted mb-0">Total: {{ atividades.count|default:"0" }} atividade(s)</p>
            {% if page_obj.has_other_pages %}
                <nav aria-label="Paginação">
                    <ul class="pagination justify-content-center mb-0">
                        {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}">Anterior</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Anterior</span>
                            </li>
                        {% endif %}

                        {% for num in page_obj.paginator.page_range %}
                            {% if page_obj.number == num %}
                                <li class="page-item active">
                                    <span class="page-link">{{ num }}</span>
                                </li>
                            {% else %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ num }}&q={{ query }}">{{ num }}</a>
                                </li>
                            {% endif %}
                        {% endfor %}

                        {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}">Próxima</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Próxima</span>
                            </li>
                        {% endif %}
                    </ul>
                </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

```


### Arquivo: atividades\templates\atividades\listar_atividades_ritualisticas.html

```html
{% extends 'base.html' %}

{% block title %}Lista de Atividades Ritualísticas{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões na mesma linha -->
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h1>Lista de Atividades Ritualísticas</h1>
        <div>
            <a href="{% url 'core:pagina_inicial' %}" class="btn btn-secondary me-2">Página Inicial</a>
            <!-- Botão para criar nova atividade ritualística -->
            <a href="{% url 'atividades:criar_atividade_ritualistica' %}?return_url={{ request.path|urlencode }}" class="btn btn-primary">
                Nova Atividade Ritualística
            </a>
        </div>
    </div>    
    <!-- Barra de busca e filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <form method="get" class="row g-3">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Buscar por nome, descrição ou local..." value="{{ query }}">
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Filtrar</button>
                </div>
            </form>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Data</th>
                            <th>Horário</th>
                            <th>Local</th>
                            <th>Turma</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for atividade in atividades %}
                            <tr>
                                <td>{{ atividade.nome }}</td>
                                <td>{{ atividade.data|date:"d/m/Y" }}</td>
                                <td>{{ atividade.hora_inicio }} - {{ atividade.hora_fim }}</td>
                                <td>{{ atividade.local }}</td>
                                <td>{{ atividade.turma }}</td>
                                <td>
                                    <a href="{% url 'atividades:detalhar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-info">Detalhes</a>
                                    <a href="{% url 'atividades:editar_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-warning">Editar</a>
                                    <a href="{% url 'atividades:excluir_atividade_ritualistica' atividade.id %}" class="btn btn-sm btn-danger">Excluir</a>                                </td>                            </tr>
                        {% empty %}
                            <tr>
                                <td colspan="6" class="text-center">
                                    <p class="my-3">Nenhuma atividade ritualística cadastrada.</p>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="card-footer">
            <p class="text-muted mb-0">Total: {{ atividades.count|default:"0" }} atividade(s)</p>
            {% if page_obj.has_other_pages %}
                <nav aria-label="Paginação">
                    <ul class="pagination justify-content-center mb-0">
                        {% if page_obj.has_previous %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}">Anterior</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Anterior</span>
                            </li>
                        {% endif %}

                        {% for num in page_obj.paginator.page_range %}
                            {% if page_obj.number == num %}
                                <li class="page-item active">
                                    <span class="page-link">{{ num }}</span>
                                </li>
                            {% else %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ num }}&q={{ query }}">{{ num }}</a>
                                </li>
                            {% endif %}
                        {% endfor %}

                        {% if page_obj.has_next %}
                            <li class="page-item">
                                <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}">Próxima</a>
                            </li>
                        {% else %}
                            <li class="page-item disabled">
                                <span class="page-link">Próxima</span>
                            </li>
                        {% endif %}
                    </ul>
                </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

```
