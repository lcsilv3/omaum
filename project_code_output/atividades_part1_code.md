# Código da Funcionalidade: atividades - Parte 1/3
*Gerado automaticamente*



## atividades\admin.py

python
from django.contrib import admin
from .models import AtividadeAcademica, AtividadeRitualistica

@admin.register(AtividadeAcademica)
class AtividadeAcademicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'data_inicio', 'data_fim', 'turma')
    list_filter = ('turma',)
    search_fields = ('nome', 'descricao')

@admin.register(AtividadeRitualistica)
class AtividadeRitualisticaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    list_filter = ('turma',)
    search_fields = ('nome', 'descricao')
    filter_horizontal = []





## atividades\apps.py

python
from django.apps import AppConfig


class AtividadesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'atividades'





## atividades\forms.py

python
print("ARQUIVO FORMS.PY CARREGADO")
from django import forms
from importlib import import_module
# resto do código...

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





## atividades\models.py

python
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





## atividades\tests.py

python
from django.test import TestCase

# Create your tests here.





## atividades\urls.py

python
from django.urls import path
from . import views

app_name = 'atividades'  # Definindo o namespace

urlpatterns = [
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





## atividades\url_aliases.py

python
from django.urls import reverse

def listar_atividades_academicas(*args, **kwargs):
    return reverse('atividades:atividade_academica_list', args=args, kwargs=kwargs)

def criar_atividade_academica(*args, **kwargs):
    return reverse('atividades:atividade_academica_create', args=args, kwargs=kwargs)

def detalhar_atividade_academica(*args, **kwargs):
    return reverse('atividades:atividade_academica_detail', args=args, kwargs=kwargs)

def editar_atividade_academica(*args, **kwargs):
    return reverse('atividades:atividade_academica_update', args=args, kwargs=kwargs)

def excluir_atividade_academica(*args, **kwargs):
    return reverse('atividades:atividade_academica_delete', args=args, kwargs=kwargs)

def listar_atividades_ritualisticas(*args, **kwargs):
    return reverse('atividades:atividade_ritualistica_list', args=args, kwargs=kwargs)

def criar_atividade_ritualistica(*args, **kwargs):
    return reverse('atividades:atividade_ritualistica_create', args=args, kwargs=kwargs)

def detalhar_atividade_ritualistica(*args, **kwargs):
    return reverse('atividades:atividade_ritualistica_detail', args=args, kwargs=kwargs)

def editar_atividade_ritualistica(*args, **kwargs):
    return reverse('atividades:atividade_ritualistica_update', args=args, kwargs=kwargs)

def excluir_atividade_ritualistica(*args, **kwargs):
    return reverse('atividades:atividade_ritualistica_delete', args=args, kwargs=kwargs)





## atividades\views.py

python
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
    return_url = request.GET.get("return_url", reverse("atividades:listar_atividades_academicas"))
    
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
    return_url = request.GET.get("return_url", reverse("atividades:listar_atividades_academicas"))
    
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
    
    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(request, "Atividade acadêmica excluída com sucesso.")
            return redirect("atividades:listar_atividades_academicas")
        except Exception as e:
            messages.error(request, f"Erro ao excluir atividade acadêmica: {str(e)}")
    return redirect("atividades:listar_atividades_academicas")@login_required
def detalhar_atividade_academica(request, pk):
    """Função para mostrar detalhes de uma atividade acadêmica."""
    AtividadeAcademica = get_model_class("AtividadeAcademica")
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    return_url = request.GET.get("return_url", reverse("atividades:listar_atividades_academicas"))
    
    return render(
        request,
        "atividades/detalhar_atividade_academica.html",
        {"atividade": atividade, "return_url": return_url},
    )


@login_required
def criar_atividade_ritualistica(request):
    """Função para criar uma nova atividade ritualística."""
    AtividadeRitualisticaForm = get_form_class("AtividadeRitualisticaForm")
    return_url = request.GET.get("return_url", reverse("atividades:listar_atividades_ritualisticas"))
    
    if request.method == "POST":
        try:
            form = AtividadeRitualisticaForm(request.POST)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.save()
                
                # Processar o campo todos_alunos se existir
                if hasattr(form, 'cleaned_data') and form.cleaned_data.get('todos_alunos'):
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
    return_url = request.GET.get("return_url", reverse("atividades:listar_atividades_ritualisticas"))
    
    if request.method == "POST":
        try:
            form = AtividadeRitualisticaForm(request.POST, instance=atividade)
            if form.is_valid():
                atividade = form.save(commit=False)
                atividade.save()
                
                # Processar o campo todos_alunos se existir
                if hasattr(form, 'cleaned_data') and form.cleaned_data.get('todos_alunos'):
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
                
                messages.success(request, "Atividade ritualística atualizada com sucesso.")
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
def confirmar_exclusao_ritualistica(request, pk):
    """Função para confirmar a exclusão de uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    if request.method == "POST":
        try:
            atividade.delete()
            messages.success(request, "Atividade ritualística excluída com sucesso.")
            return redirect("atividades:listar_atividades_ritualisticas")
        except Exception as e:
            messages.error(request, f"Erro ao excluir atividade ritualística: {str(e)}")
            return redirect("atividades:detalhar_atividade_ritualistica", pk=pk)
    
    return render(
        request,
        "atividades/confirmar_exclusao_ritualistica.html",
        {"object": atividade},
    )

@login_required
def detalhar_atividade_ritualistica(request, pk):
    """Função para mostrar detalhes de uma atividade ritualística."""
    AtividadeRitualistica = get_model_class("AtividadeRitualistica")
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    total_participantes = atividade.participantes.count()
    
    return render(
        request,
        "atividades/detalhar_atividade_ritualistica.html",
        {
            "atividade": atividade,
            "total_participantes": total_participantes,
        },
    )





## atividades\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-04-03 20:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AtividadeAcademica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('data_inicio', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data de Início')),
                ('data_fim', models.DateTimeField(blank=True, null=True, verbose_name='Data de Término')),
                ('responsavel', models.CharField(blank=True, max_length=100, null=True, verbose_name='Responsável')),
                ('local', models.CharField(blank=True, max_length=100, null=True, verbose_name='Local')),
                ('tipo_atividade', models.CharField(choices=[('aula', 'Aula'), ('palestra', 'Palestra'), ('workshop', 'Workshop'), ('seminario', 'Seminário'), ('outro', 'Outro')], default='aula', max_length=20, verbose_name='Tipo de Atividade')),
                ('status', models.CharField(choices=[('agendada', 'Agendada'), ('em_andamento', 'Em Andamento'), ('concluida', 'Concluída'), ('cancelada', 'Cancelada')], default='agendada', max_length=20, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Atividade Acadêmica',
                'verbose_name_plural': 'Atividades Acadêmicas',
            },
        ),
        migrations.CreateModel(
            name='AtividadeRitualistica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('data', models.DateField(verbose_name='Data')),
                ('hora_inicio', models.TimeField(verbose_name='Hora de Início')),
                ('hora_fim', models.TimeField(verbose_name='Hora de Término')),
                ('local', models.CharField(max_length=100, verbose_name='Local')),
            ],
            options={
                'verbose_name': 'Atividade Ritualística',
                'verbose_name_plural': 'Atividades Ritualísticas',
                'ordering': ['-data', 'hora_inicio'],
            },
        ),
    ]





## atividades\migrations\0002_initial.py

python
# Generated by Django 5.1.7 on 2025-04-03 20:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alunos', '0001_initial'),
        ('atividades', '0001_initial'),
        ('turmas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividadeacademica',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atividades_academicas', to='turmas.turma'),
        ),
        migrations.AddField(
            model_name='atividaderitualistica',
            name='participantes',
            field=models.ManyToManyField(blank=True, related_name='atividades_ritualisticas', to='alunos.aluno', verbose_name='Participantes'),
        ),
        migrations.AddField(
            model_name='atividaderitualistica',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turmas.turma', verbose_name='Turma'),
        ),
    ]



