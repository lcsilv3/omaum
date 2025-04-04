# Código da Funcionalidade: punicoes - Parte 1/2
*Gerado automaticamente*



## punicoes\admin.py

python
from django.contrib import admin
from .models import Punicao, TipoPunicao

@admin.register(Punicao)
class PunicaoAdmin(admin.ModelAdmin):
    list_display = ['aluno']
    list_filter = []
    search_fields = ('aluno__nome', 'descricao')
    date_hierarchy = 'data_aplicacao'

@admin.register(TipoPunicao)
class TipoPunicaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    list_filter = []
    search_fields = ('nome', 'descricao')




## punicoes\apps.py

python
from django.apps import AppConfig

class PunicoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'punicoes'
    verbose_name = 'Punições'





## punicoes\forms.py

python
from django import forms
from importlib import import_module

def get_punicao_model():
    punicoes_module = import_module('punicoes.models')
    return getattr(punicoes_module, 'Punicao')

def get_tipo_punicao_model():
    punicoes_module = import_module('punicoes.models')
    return getattr(punicoes_module, 'TipoPunicao')

class PunicaoForm(forms.ModelForm):
    class Meta:
        model = get_punicao_model()
        fields = ['aluno', 'tipo_punicao', 'data_aplicacao', 'motivo', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'tipo_punicao': forms.Select(attrs={'class': 'form-control'}),
            'data_aplicacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TipoPunicaoForm(forms.ModelForm):
    class Meta:
        model = get_model('punicoes', 'TipoPunicao')
        fields = ['nome', 'descricao', 'gravidade']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }




## punicoes\models.py

python
from django.db import models
from django.contrib.auth.models import User
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

class TipoPunicao(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Tipo de Punição'
        verbose_name_plural = 'Tipos de Punição'
        ordering = ['nome']

class Punicao(models.Model):
    aluno = models.ForeignKey(
        get_aluno_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Aluno',
        to_field='cpf'  # Especificar que estamos referenciando o campo cpf
    )
    tipo_punicao = models.ForeignKey(
        TipoPunicao, 
        on_delete=models.CASCADE, 
        verbose_name='Tipo de Punição'
    )
    data_aplicacao = models.DateField(verbose_name='Data de Aplicação')
    motivo = models.TextField(verbose_name='Motivo')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    aplicada_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='Aplicada por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f"{self.aluno.nome} - {self.tipo_punicao.nome} - {self.data_aplicacao}"

    class Meta:
        verbose_name = 'Punição'
        verbose_name_plural = 'Punições'
        ordering = ['-data_aplicacao', 'aluno__nome']





## punicoes\urls.py

python
from django.urls import path
from . import views

app_name = 'punicoes'

urlpatterns = [
    path('', views.listar_punicoes, name='listar_punicoes'),
    path('nova/', views.criar_punicao, name='criar_punicao'),
    path('<int:id>/editar/', views.editar_punicao, name='editar_punicao'),
    path('<int:id>/excluir/', views.excluir_punicao, name='excluir_punicao'),
    path('<int:id>/detalhes/', views.detalhar_punicao, name='detalhar_punicao'),
    path('tipos/', views.listar_tipos_punicao, name='listar_tipos_punicao'),
    path('tipos/novo/', views.criar_tipo_punicao, name='criar_tipo_punicao'),
    path('tipos/<int:id>/editar/', views.editar_tipo_punicao, name='editar_tipo_punicao'),
    path('tipos/<int:id>/excluir/', views.excluir_tipo_punicao, name='excluir_tipo_punicao'),
]





## punicoes\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import importlib

# Importando modelos e formulários usando importlib para evitar importações circulares
def get_model(app_name, model_name):
    module = importlib.import_module(f"{app_name}.models")
    return getattr(module, model_name)

def get_form(app_name, form_name):
    module = importlib.import_module(f"{app_name}.forms")
    return getattr(module, form_name)

@login_required
def listar_punicoes(request):
    Punicao = get_model('punicoes', 'Punicao')
    Aluno = get_model('alunos', 'Aluno')
    TipoPunicao = get_model('punicoes', 'TipoPunicao')
    
    # Filtros
    filtro_aluno = request.GET.get('aluno')
    filtro_tipo = request.GET.get('tipo')
    filtro_status = request.GET.get('status')
    
    punicoes = Punicao.objects.all().order_by('-data_aplicacao')
    
    if filtro_aluno:
        punicoes = punicoes.filter(aluno_id=filtro_aluno)
    
    if filtro_tipo:
        punicoes = punicoes.filter(tipo_punicao_id=filtro_tipo)
    
    if filtro_status:
        punicoes = punicoes.filter(status=filtro_status)
    
    # Paginação
    paginator = Paginator(punicoes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Dados para filtros
    alunos = Aluno.objects.all().order_by('nome')
    tipos_punicao = TipoPunicao.objects.all().order_by('nome')
    
    context = {
        'punicoes': page_obj,
        'alunos': alunos,
        'tipos_punicao': tipos_punicao,
    }
    
    return render(request, 'punicoes/listar_punicoes.html', context)

@login_required
def criar_punicao(request):
    PunicaoForm = get_form('punicoes', 'PunicaoForm')
    
    if request.method == 'POST':
        form = PunicaoForm(request.POST)
        if form.is_valid():
            punicao = form.save(commit=False)
            punicao.registrado_por = request.user
            punicao.save()
            messages.success(request, 'Punição registrada com sucesso!')
            return redirect('punicoes:listar_punicoes')
    else:
        form = PunicaoForm()
    
    return render(request, 'punicoes/criar_punicao.html', {'form': form})

@login_required
def aplicar_punicao(request):
    """Aplica uma punição a um aluno."""
    if request.method == 'POST':
        form = PunicaoForm(request.POST)
        if form.is_valid():
            punicao = form.save(commit=False)
            punicao.aplicada_por = request.user
            punicao.save()
            messages.success(request, 'Punição aplicada com sucesso!')
            return redirect('punicoes:listar_punicoes')
    else:
        form = PunicaoForm()
    
    return render(request, 'punicoes/aplicar_punicao.html', {'form': form})

@login_required
def editar_punicao(request, id):
    """Edita uma punição."""
    punicao = get_object_or_404(Punicao, id=id)
    
    if request.method == 'POST':
        form = PunicaoForm(request.POST, instance=punicao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Punição atualizada com sucesso!')
            return redirect('punicoes:listar_punicoes')
    else:
        form = PunicaoForm(instance=punicao)
    
    return render(request, 'punicoes/editar_punicao.html', {'form': form, 'punicao': punicao})

@login_required
def excluir_punicao(request, id):
    Punicao = get_model('punicoes', 'Punicao')
    
    punicao = get_object_or_404(Punicao, id=id)
    
    if request.method == 'POST':
        punicao.delete()
        messages.success(request, 'Punição excluída com sucesso!')
        return redirect('punicoes:listar_punicoes')
    
    return render(request, 'punicoes/excluir_punicao.html', {'punicao': punicao})

@login_required
def detalhar_punicao(request, id):
    Punicao = get_model('punicoes', 'Punicao')
    
    punicao = get_object_or_404(Punicao, id=id)
    
    return render(request, 'punicoes/detalhar_punicao.html', {'punicao': punicao})

@login_required
def listar_tipos_punicao(request):
    TipoPunicao = get_model('punicoes', 'TipoPunicao')
    
    tipos_punicao = TipoPunicao.objects.all().order_by('nome')
    
    return render(request, 'punicoes/listar_tipos_punicao.html', {'tipos_punicao': tipos_punicao})

@login_required
def criar_tipo_punicao(request):
    TipoPunicaoForm = get_form('punicoes', 'TipoPunicaoForm')
    
    if request.method == 'POST':
        form = TipoPunicaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de punição criado com sucesso!')
            return redirect('punicoes:listar_tipos_punicao')
    else:
        form = TipoPunicaoForm()
    
    return render(request, 'punicoes/criar_tipo_punicao.html', {'form': form})

@login_required
def editar_tipo_punicao(request, id):
    TipoPunicao = get_model('punicoes', 'TipoPunicao')
    TipoPunicaoForm = get_form('punicoes', 'TipoPunicaoForm')
    
    tipo_punicao = get_object_or_404(TipoPunicao, id=id)
    
    if request.method == 'POST':
        form = TipoPunicaoForm(request.POST, instance=tipo_punicao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de punição atualizado com sucesso!')
            return redirect('punicoes:listar_tipos_punicao')
    else:
        form = TipoPunicaoForm(instance=tipo_punicao)
    
    return render(request, 'punicoes/editar_tipo_punicao.html', {'form': form, 'tipo_punicao': tipo_punicao})

@login_required
def excluir_tipo_punicao(request, id):
    TipoPunicao = get_model('punicoes', 'TipoPunicao')
    Punicao = get_model('punicoes', 'Punicao')
    
    tipo_punicao = get_object_or_404(TipoPunicao, id=id)
    
    # Verificar se existem punições associadas a este tipo
    punicoes_associadas = Punicao.objects.filter(tipo_punicao=tipo_punicao).count()
    
    if request.method == 'POST':
        tipo_punicao.delete()
        messages.success(request, 'Tipo de punição excluído com sucesso!')
        return redirect('punicoes:listar_tipos_punicao')
    
    return render(request, 'punicoes/excluir_tipo_punicao.html', {
        'tipo_punicao': tipo_punicao,
        'punicoes_associadas': punicoes_associadas
    })




## punicoes\__init__.py

python
# Arquivo de inicialização do aplicativo de punições





## punicoes\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-04-03 20:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alunos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoPunicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Tipo de Punição',
                'verbose_name_plural': 'Tipos de Punição',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Punicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_aplicacao', models.DateField(verbose_name='Data de Aplicação')),
                ('motivo', models.TextField(verbose_name='Motivo')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alunos.aluno', verbose_name='Aluno')),
                ('aplicada_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Aplicada por')),
                ('tipo_punicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='punicoes.tipopunicao', verbose_name='Tipo de Punição')),
            ],
            options={
                'verbose_name': 'Punição',
                'verbose_name_plural': 'Punições',
                'ordering': ['-data_aplicacao', 'aluno__nome'],
            },
        ),
    ]





## punicoes\templates\punicoes\criar_punicao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Nova Punição</h1>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        
        <button type="submit" class="btn btn-primary">Registrar Punição</button>
        <a href="{% url 'punicoes:listar_punicoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}





## punicoes\templates\punicoes\criar_tipo_punicao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Novo Tipo de Punição</h1>
  
  <form method="post">



