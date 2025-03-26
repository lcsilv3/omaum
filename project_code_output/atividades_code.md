# Código da Funcionalidade: atividades
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
    list_display = ('nome', 'descricao', 'data_inicio', 'data_fim', 'turma')
    list_filter = ('turma',)
    search_fields = ('nome', 'descricao')
    filter_horizontal = ('alunos',)





## atividades\apps.py

python
from django.apps import AppConfig


class AtividadesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'atividades'





## atividades\forms.py

python
from django import forms
import importlib

def criar_form_atividade_academica():
    """
    Cria o formulário para atividades acadêmicas usando importação dinâmica
    para evitar referências circulares.
    """
    class AtividadeAcademicaForm(forms.ModelForm):
        class Meta:
            model = None  # Será definido no __init__
            fields = ('nome', 'descricao', 'data_inicio', 'data_fim', 'turma')
            
        def __init__(self, *args, **kwargs):
            # Importação dinâmica do modelo
            from .models import AtividadeAcademica
            self.Meta.model = AtividadeAcademica
            super().__init__(*args, **kwargs)
            
            # Importação dinâmica da turma
            turmas_module = importlib.import_module('turmas.models')
            Turma = getattr(turmas_module, 'Turma')
            
            # Configurar queryset
            self.fields['turma'].queryset = Turma.objects.all()
    
    return AtividadeAcademicaForm

def criar_form_atividade_ritualistica():
    """
    Cria o formulário para atividades ritualísticas usando importação dinâmica
    para evitar referências circulares.
    """
    class AtividadeRitualisticaForm(forms.ModelForm):
        todos_alunos = forms.BooleanField(required=False, label="Incluir todos os alunos da turma")
        
        class Meta:
            model = None  # Será definido no __init__
            fields = ['nome', 'descricao', 'data_inicio', 'data_fim', 'turma', 'alunos', 'todos_alunos']

        def __init__(self, *args, **kwargs):
            # Importação dinâmica dos modelos
            from .models import AtividadeRitualistica
            self.Meta.model = AtividadeRitualistica
            
            super().__init__(*args, **kwargs)
            
            # Importação dinâmica usando importlib
            turmas_module = importlib.import_module('turmas.models')
            alunos_module = importlib.import_module('alunos.models')
            
            Turma = getattr(turmas_module, 'Turma')
            Aluno = getattr(alunos_module, 'Aluno')
            
            # Configurar os querysets
            self.fields['turma'].queryset = Turma.objects.all()
            self.fields['alunos'].queryset = Aluno.objects.all()
            self.fields['alunos'].widget = forms.CheckboxSelectMultiple()
            self.fields['alunos'].required = False
   
    return AtividadeRitualisticaForm




## atividades\models.py

python
from django.db import models
from django.utils import timezone

class AtividadeAcademica(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    # Substituir o campo data por data_inicio e data_fim
    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField(blank=True, null=True)
    # Referência ao app correto
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE, related_name='atividades_academicas')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Atividade Acadêmica'
        verbose_name_plural = 'Atividades Acadêmicas'

class AtividadeRitualistica(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    # Substituir o campo data por data_inicio e data_fim
    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField(blank=True, null=True)
    # Referência ao app correto
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE, related_name='atividades_ritualisticas')
    # Referência ao app correto
    alunos = models.ManyToManyField('alunos.Aluno', related_name='atividades_ritualisticas')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Atividade Ritualística'
        verbose_name_plural = 'Atividades Ritualísticas'





## atividades\tests.py

python
from django.test import TestCase

# Create your tests here.





## atividades\urls.py

python
from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    path('academicas/', views.atividade_academica_list, name='atividade_academica_list'),
    path('ritualisticas/', views.listar_atividades_ritualisticas, name='atividade_ritualistica_list'),
    
    # URLs para atividades acadêmicas
    path('academicas/criar/', views.criar_atividade_academica, name='academica_criar'),
    path('academicas/editar/<int:pk>/', views.editar_atividade_academica, name='academica_editar'),
    path('academicas/excluir/<int:pk>/', views.excluir_atividade_academica, name='academica_excluir'),
    path('academicas/lista/', views.atividade_academica_list, name='academica_lista'),
    
    # URLs para atividades ritualísticas
    path('ritualisticas/criar/', views.criar_atividade_ritualistica, name='ritualistica_criar'),
    path('ritualisticas/editar/<int:pk>/', views.editar_atividade_ritualistica, name='ritualistica_editar'),
    path('ritualisticas/excluir/<int:pk>/', views.excluir_atividade_ritualistica, name='ritualistica_excluir'),
    path('ritualisticas/lista/', views.listar_atividades_ritualisticas, name='ritualistica_lista'),
]




## atividades\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
import importlib

# Importação dinâmica dos modelos
from .models import AtividadeAcademica, AtividadeRitualistica
from .forms import criar_form_atividade_academica, criar_form_atividade_ritualistica

from django.shortcuts import render
from .models import AtividadeAcademica

def atividade_academica_list(request):
    atividades = AtividadeAcademica.objects.all()
    return render(request, 'atividades/atividade_academica_list.html', {'atividades': atividades})

def criar_atividade_academica(request):
    """Cria uma nova atividade acadêmica"""
    AtividadeAcademicaForm = criar_form_atividade_academica()
   
    if request.method == 'POST':
        form = AtividadeAcademicaForm(request.POST)
        if form.is_valid():
            try:
                atividade = form.save()
                messages.success(request, 'Atividade acadêmica criada com sucesso!')
                return redirect('atividades:academica_lista')
            except Exception as e:
                messages.error(request, f'Erro ao criar atividade: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Erro no campo {field}: {error}')
    else:
        form = AtividadeAcademicaForm()
   
    return render(request, 'atividades/academica_formulario.html', {'form': form})

def editar_atividade_academica(request, pk):
    """Edita uma atividade acadêmica existente"""
    AtividadeAcademicaForm = criar_form_atividade_academica()
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    
    if request.method == 'POST':
        form = AtividadeAcademicaForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade acadêmica atualizada com sucesso!')
            return redirect('atividades:academica_lista')
    else:
        form = AtividadeAcademicaForm(instance=atividade)
    
    return render(request, 'atividades/academica_formulario.html', {'form': form})

def excluir_atividade_academica(request, pk):
    """Exclui uma atividade acadêmica"""
    atividade = get_object_or_404(AtividadeAcademica, pk=pk)
    
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, 'Atividade acadêmica excluída com sucesso!')
        return redirect('atividades:academica_lista')
    
    return render(request, 'atividades/academica_confirmar_exclusao.html', {'object': atividade})

# Views para Atividades Ritualísticas
def listar_atividades_ritualisticas(request):
    """Exibe a lista de atividades ritualísticas com filtros e paginação"""
    # Importação dinâmica
    turmas_module = importlib.import_module('turmas.models')
    Turma = getattr(turmas_module, 'Turma')
    
    # Obter todas as atividades
    atividades = AtividadeRitualistica.objects.all()
    
    # Busca por nome
    search_query = request.GET.get('search', '')
    if search_query:
        atividades = atividades.filter(nome__icontains=search_query)
    
    # Filtro por turma
    turma_id = request.GET.get('turma', '')
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
    
    # Ordenação
    order_by = request.GET.get('order_by', 'nome')
    order_dir = request.GET.get('order_dir', 'asc')
    
    if order_dir == 'desc':
        order_by = f'-{order_by}'
        
    atividades = atividades.order_by(order_by)
    
    # Paginação
    paginator = Paginator(atividades, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Contexto para o template
    context = {
        'atividades_ritualisticas': page_obj,
        'search_query': search_query,
        'turmas': Turma.objects.all(),
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    
    return render(request, 'atividades/ritualistica_lista.html', context)

def criar_atividade_ritualistica(request):
    """Cria uma nova atividade ritualística"""
    AtividadeRitualisticaForm = criar_form_atividade_ritualistica()
    
    if request.method == 'POST':
        form = AtividadeRitualisticaForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            
            # Tratar a opção de incluir todos os alunos
            if form.cleaned_data.get('todos_alunos'):
                turma = form.cleaned_data.get('turma')
                if turma:
                    # Importação dinâmica usando importlib
                    alunos_module = importlib.import_module('alunos.models')
                    Aluno = getattr(alunos_module, 'Aluno')
                    
                    # Adicionar todos os alunos da turma
                    alunos = Aluno.objects.filter(turmas=turma)
                    instance.alunos.set(alunos)
            else:
                # Salvar os alunos selecionados no formulário
                form.save_m2m()
            
            messages.success(request, 'Atividade ritualística criada com sucesso!')
            return redirect('atividades:ritualistica_lista')
    else:
        form = AtividadeRitualisticaForm()
    
    return render(request, 'atividades/atividade_ritualistica_form.html', {'form': form})

def editar_atividade_ritualistica(request, pk):
    """Edita uma atividade ritualística existente"""
    AtividadeRitualisticaForm = criar_form_atividade_ritualistica()
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    if request.method == 'POST':
        form = AtividadeRitualisticaForm(request.POST, instance=atividade)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            
            # Tratar a opção de incluir todos os alunos
            if form.cleaned_data.get('todos_alunos'):
                turma = form.cleaned_data.get('turma')
                if turma:
                    # Importação dinâmica usando importlib
                    alunos_module = importlib.import_module('alunos.models')
                    Aluno = getattr(alunos_module, 'Aluno')
                    
                    # Adicionar todos os alunos da turma
                    alunos = Aluno.objects.filter(turmas=turma)
                    instance.alunos.set(alunos)
            else:
                # Salvar os alunos selecionados no formulário
                form.save_m2m()
            
            messages.success(request, 'Atividade ritualística atualizada com sucesso!')
            return redirect('atividades:ritualistica_lista')
    else:
        form = AtividadeRitualisticaForm(instance=atividade)
    
    return render(request, 'atividades/atividade_ritualistica_form.html', {'form': form})

def excluir_atividade_ritualistica(request, pk):
    """Exclui uma atividade ritualística"""
    atividade = get_object_or_404(AtividadeRitualistica, pk=pk)
    
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, 'Atividade ritualística excluída com sucesso!')
        return redirect('atividades:ritualistica_lista')
    
    return render(request, 'atividades/ritualistica_confirmar_exclusao.html', {'object': atividade})





## atividades\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-03-23 20:14

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alunos', '__first__'),
        ('turmas', '0003_alter_turma_curso_alter_turma_data_fim_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtividadeAcademica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atividades_academicas', to='turmas.turma')),
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
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('alunos', models.ManyToManyField(related_name='atividades_ritualisticas', to='alunos.aluno')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atividades_ritualisticas', to='turmas.turma')),
            ],
            options={
                'verbose_name': 'Atividade Ritualística',
                'verbose_name_plural': 'Atividades Ritualísticas',
            },
        ),
    ]





## atividades\migrations\0002_rename_data_to_data_inicio_and_add_data_fim.py

python
# Generated by Django 5.1.7 on 2025-03-25 14:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('atividades', '0001_initial'),
    ]

    operations = [
        # For AtividadeAcademica
        migrations.RenameField(
            model_name='atividadeacademica',
            old_name='data',
            new_name='data_inicio',
        ),
        migrations.AddField(
            model_name='atividadeacademica',
            name='data_fim',
            field=models.DateTimeField(blank=True, null=True),
        ),
        
        # For AtividadeRitualistica
        migrations.RenameField(
            model_name='atividaderitualistica',
            old_name='data',
            new_name='data_inicio',
        ),
        migrations.AddField(
            model_name='atividaderitualistica',
            name='data_fim',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]





## atividades\templates\atividades\academica_confirmar_exclusao.html

html
{% extends "base.html" %}

{% block title %}Confirmar Exclusão{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Confirmar Exclusão</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="lead">Tem certeza que deseja excluir a atividade acadêmica "{{ object.nome }}"?</p>
            <p class="text-danger">Esta ação não pode ser desfeita.</p>
            
            <form method="post">
                {% csrf_token %}
                <button type="submit" class="btn btn-danger">Sim, excluir</button>
                <a href="{% url 'atividades:academica_lista' %}" class="btn btn-secondary">Cancelar</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}





## atividades\templates\atividades\academica_formulario.html

html
{% extends "base.html" %}

{% block title %}
    {% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Acadêmica
{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">
        {% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Acadêmica
    </h1>
    
    <form method="post">
        {% csrf_token %}
        
        <div class="card">
            <div class="card-body">
                {% for field in form %}
                <div class="mb-3">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                    <div class="text-danger">
                        {{ field.errors }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="mt-3">
            <button type="submit" class="btn btn-primary">Salvar</button>
            <a href="{% url 'atividades:academica_lista' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}





## atividades\templates\atividades\academica_lista.html

html
{% extends "base.html" %}

{% block title %}Atividades Acadêmicas{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Atividades Acadêmicas</h1>
    
    <div class="d-flex justify-content-between mb-3">
        <a href="{% url 'atividades:academica_criar' %}" class="btn btn-primary">Nova Atividade</a>
        
        <form class="d-flex" method="get">
            <input class="form-control me-2" type="search" placeholder="Buscar atividades" 
                   name="search" value="{{ search_query }}">
            <button class="btn btn-outline-primary" type="submit">Buscar</button>
        </form>
    </div>
    
    <div class="mb-3">
        <form method="get" class="d-flex flex-wrap gap-2">
            {% if search_query %}
            <input type="hidden" name="search" value="{{ search_query }}">
            {% endif %}
            
            <div class="form-group">
                <label for="turma_filter">Filtrar por Turma:</label>
                <select name="turma" id="turma_filter" class="form-control">
                    <option value="">Todas as Turmas</option>
                    {% for turma in turmas %}
                    <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"i" %}selected{% endif %}>{{ turma.nome }}</option>
                    {% endfor %}
                </select>
            </div>
            
            <div class="form-group">
                <label for="data_inicio_filter">Data de Início (a partir de):</label>
                <input type="date" name="data_inicio_min" id="data_inicio_filter" class="form-control" value="{{ request.GET.data_inicio_min }}">
            </div>
            
            <div class="form-group">
                <label for="data_fim_filter">Data de Fim (até):</label>
                <input type="date" name="data_fim_max" id="data_fim_filter" class="form-control" value="{{ request.GET.data_fim_max }}">
            </div>
            
            <div class="form-group d-flex align-items-end">
                <button type="submit" class="btn btn-primary">Filtrar</button>
                <a href="{% url 'atividades:academica_lista' %}" class="btn btn-secondary ms-2">Limpar Filtros</a>
            </div>
        </form>
    </div>
    
    <div class="card">
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>
                            <a href="?{% if request.GET.order_by == 'nome' and request.GET.order_dir == 'asc' %}order_by=nome&order_dir=desc{% else %}order_by=nome&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}">
                                Nome
                                {% if request.GET.order_by == 'nome' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'turma' and request.GET.order_dir == 'asc' %}order_by=turma&order_dir=desc{% else %}order_by=turma&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}">
                                Turma
                                {% if request.GET.order_by == 'turma' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'data_inicio' and request.GET.order_dir == 'asc' %}order_by=data_inicio&order_dir=desc{% else %}order_by=data_inicio&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}">
                                Data de Início
                                {% if request.GET.order_by == 'data_inicio' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'data_fim' and request.GET.order_dir == 'asc' %}order_by=data_fim&order_dir=desc{% else %}order_by=data_fim&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}">
                                Data de Fim
                                {% if request.GET.order_by == 'data_fim' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {% for atividade in atividades %}
                    <tr>
                        <td>{{ atividade.nome }}</td>
                        <td>{{ atividade.turma }}</td>
                        <td>{{ atividade.data_inicio|date:"d/m/Y" }}</td>
                        <td>{{ atividade.data_fim|date:"d/m/Y" }}</td>
                        <td>
                            <a href="{% url 'atividades:academica_editar' atividade.id %}" class="btn btn-sm btn-warning">Editar</a>
                            <button type="button" class="btn btn-sm btn-danger" 
                                    data-bs-toggle="modal" 
                                    data-bs-target="#deleteModal{{ atividade.id }}">
                                Excluir
                            </button>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center">Nenhuma atividade acadêmica encontrada.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% if is_paginated %}
    <nav aria-label="Paginação">
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page=1{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}" aria-label="Primeira">
                    <span aria-hidden="true">««</span>
                </a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}" aria-label="Anterior">
                    <span aria-hidden="true">«</span>
                </a>
            </li>
            {% else %}
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Primeira">
                    <span aria-hidden="true">««</span>
                </a>
            </li>
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Anterior">
                    <span aria-hidden="true">«</span>
                </a>
            </li>
            {% endif %}
            
            {% for num in page_obj.paginator.page_range %}
                {% if page_obj.number == num %}
                <li class="page-item active"><a class="page-link" href="?page={{ num }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}">{{ num }}</a></li>
                {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                <li class="page-item"><a class="page-link" href="?page={{ num }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}">{{ num }}</a></li>
                {% endif %}
            {% endfor %}
            
            {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}" aria-label="Próxima">
                    <span aria-hidden="true">»</span>
                </a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}" aria-label="Última">
                    <span aria-hidden="true">»»</span>
                </a>
            </li>
            {% else %}
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Próxima">
                    <span aria-hidden="true">»</span>
                </a>
            </li>
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Última">
                    <span aria-hidden="true">»»</span>
                </a>
            </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
</div>
{% for atividade in atividades %}
<!-- Modal de confirmação para cada atividade -->
<div class="modal fade" id="deleteModal{{ atividade.id }}" tabindex="-1" aria-labelledby="deleteModalLabel{{ atividade.id }}" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="deleteModalLabel{{ atividade.id }}">Confirmar Exclusão</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
            </div>
            <div class="modal-body">
                <p>Tem certeza que deseja excluir a atividade acadêmica <strong>"{{ atividade.nome }}"</strong>?</p>
                <p class="text-danger">Esta ação não pode ser desfeita.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <a href="{% url 'atividades:academica_excluir' atividade.id %}" class="btn btn-danger">Sim, excluir</a>
            </div>
        </div>
    </div>
</div>
{% endfor %}
{% endblock %}





## atividades\templates\atividades\atividade_ritualistica_form.html

html
{% extends 'base.html' %}

{% block title %}
    {% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Ritualística
{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">
        {% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Ritualística
    </h1>
    
    <form method="post">
        {% csrf_token %}
        
        <div class="card">
            <div class="card-body">
                {% for field in form %}
                <div class="mb-3">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                    <div class="text-danger">
                        {{ field.errors }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="mt-3">
            <button type="submit" class="btn btn-primary">Salvar</button>
            <a href="{% url 'atividades:ritualistica_lista' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const todosAlunosCheckbox = document.getElementById('id_todos_alunos');
        const alunosField = document.getElementById('id_alunos');
        const alunosContainer = alunosField.closest('.mb-3');
        const turmaSelect = document.getElementById('id_turma');
        
        // Function to toggle the visibility and state of the alunos field
        function toggleAlunosField() {
            if (todosAlunosCheckbox.checked) {
                alunosContainer.style.opacity = '0.5';
                alunosField.disabled = true;
                
                // Add a visual indicator that the field is disabled
                const helpText = document.createElement('small');
                helpText.id = 'alunos-help-text';
                helpText.className = 'form-text text-muted';
                helpText.textContent = 'Todos os alunos da turma serão incluídos automaticamente';
                
                // Remove existing help text if any
                const existingHelpText = document.getElementById('alunos-help-text');
                if (existingHelpText) {
                    existingHelpText.remove();
                }
                
                alunosContainer.appendChild(helpText);
            } else {
                alunosContainer.style.opacity = '1';
                alunosField.disabled = false;
                
                // Remove the help text
                const helpText = document.getElementById('alunos-help-text');
                if (helpText) {
                    helpText.remove();
                }
            }
        }
        
        // Function to update available students based on selected turma
        function updateAlunosList() {
            const turmaId = turmaSelect.value;
            if (!turmaId) return;
            
            // Show loading indicator
            alunosContainer.style.opacity = '0.5';
            
            // Fetch students for the selected turma via AJAX
            fetch(`/api/turmas/${turmaId}/alunos/`)
                .then(response => response.json())
                .then(data => {
                    // Clear current options
                    while (alunosField.firstChild) {
                        alunosField.removeChild(alunosField.firstChild);
                    }
                    
                    // Add new options
                    data.forEach(aluno => {
                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.name = 'alunos';
                        checkbox.value = aluno.id;
                        checkbox.id = `aluno_${aluno.id}`;
                        
                        const label = document.createElement('label');
                        label.htmlFor = `aluno_${aluno.id}`;
                        label.textContent = aluno.nome;
                        
                        const div = document.createElement('div');
                        div.className = 'form-check';
                        div.appendChild(checkbox);
                        div.appendChild(label);
                        
                        alunosField.appendChild(div);
                    });
                    
                    alunosContainer.style.opacity = '1';
                })
                .catch(error => {
                    console.error('Error fetching students:', error);
                    alunosContainer.style.opacity = '1';
                });
        }
        
        // Event listeners
        todosAlunosCheckbox.addEventListener('change', toggleAlunosField);
        turmaSelect.addEventListener('change', function() {
            if (!todosAlunosCheckbox.checked) {
                updateAlunosList();
            }
        });
        
        // Initial setup
        toggleAlunosField();
        if (turmaSelect.value && !todosAlunosCheckbox.checked) {
            updateAlunosList();
        }
    });
</script>
{% endblock %}




## atividades\templates\atividades\ritualistica_confirmar_exclusao.html

html
{% extends "base.html" %}

{% block title %}Confirmar Exclusão{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Confirmar Exclusão</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="lead">Tem certeza que deseja excluir a atividade ritualística "{{ object.nome }}"?</p>
            <p class="text-danger">Esta ação não pode ser desfeita.</p>
            
            <form method="post">
                {% csrf_token %}
                <button type="submit" class="btn btn-danger">Sim, excluir</button>
                <a href="{% url 'atividades:ritualistica_lista' %}" class="btn btn-secondary">Cancelar</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}





## atividades\templates\atividades\ritualistica_lista.html

html
{% extends 'base.html' %}

{% block title %}Atividades Ritualísticas{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Atividades Ritualísticas</h1>
    
    <div class="d-flex justify-content-between mb-3">
        <a href="{% url 'atividades:ritualistica_criar' %}" class="btn btn-primary">Nova Atividade Ritualística</a>
        
        <form class="d-flex" method="get">
            <input class="form-control me-2" type="search" placeholder="Buscar atividades"
                   name="search" value="{{ search_query }}">
            <button class="btn btn-outline-primary" type="submit">Buscar</button>
        </form>
    </div>
    
    <!-- Filtros adicionais -->
    <div class="mb-3">
        <form method="get" class="d-flex flex-wrap gap-2">
            {% if search_query %}
            <input type="hidden" name="search" value="{{ search_query }}">
            {% endif %}
            
            <div class="form-group me-2">
                <label for="turma_filter">Filtrar por Turma:</label>
                <select name="turma" id="turma_filter" class="form-control">
                    <option value="">Todas as Turmas</option>
                    {% for turma in turmas %}
                    <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"i" %}selected{% endif %}>{{ turma.nome }}</option>
                    {% endfor %}
                </select>
            </div>
            
            <div class="form-group me-2">
                <label for="data_inicio_filter">Data de Início (a partir de):</label>
                <input type="date" name="data_inicio_min" id="data_inicio_filter" class="form-control" value="{{ request.GET.data_inicio_min }}">
            </div>
            
            <div class="form-group me-2">
                <label for="data_fim_filter">Data de Fim (até):</label>
                <input type="date" name="data_fim_max" id="data_fim_filter" class="form-control" value="{{ request.GET.data_fim_max }}">
            </div>
            
            <div class="form-group d-flex align-items-end">
                <button type="submit" class="btn btn-primary">Filtrar</button>
                <a href="{% url 'atividades:ritualistica_lista' %}" class="btn btn-secondary ms-2">Limpar Filtros</a>
            </div>
        </form>
    </div>
    
    <div class="card">
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>
                            <a href="?{% if request.GET.order_by == 'nome' and request.GET.order_dir == 'asc' %}order_by=nome&order_dir=desc{% else %}order_by=nome&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">
                                Nome
                                {% if request.GET.order_by == 'nome' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'turma' and request.GET.order_dir == 'asc' %}order_by=turma&order_dir=desc{% else %}order_by=turma&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">
                                Turma
                                {% if request.GET.order_by == 'turma' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'data_inicio' and request.GET.order_dir == 'asc' %}order_by=data_inicio&order_dir=desc{% else %}order_by=data_inicio&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">
                                Data de Início
                                {% if request.GET.order_by == 'data_inicio' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'data_fim' and request.GET.order_dir == 'asc' %}order_by=data_fim&order_dir=desc{% else %}order_by=data_fim&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">
                                Data de Fim
                                {% if request.GET.order_by == 'data_fim' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {% for atividade in atividades_ritualisticas %}
                    <tr>
                        <td>{{ atividade.nome }}</td>
                        <td>{{ atividade.turma }}</td>
                        <td>{{ atividade.data_inicio|date:"d/m/Y" }}</td>
                        <td>{{ atividade.data_fim|date:"d/m/Y" }}</td>
                        <td>
                            <a href="{% url 'atividades:ritualistica_editar' atividade.id %}" class="btn btn-sm btn-warning">Editar</a>
                            <a href="{% url 'atividades:ritualistica_excluir' atividade.id %}" 
                               class="btn btn-sm btn-danger"
                               onclick="return confirm('Tem certeza que deseja excluir a atividade ritualística \'{{ atividade.nome }}\'? Esta ação não pode ser desfeita.')">
                                Excluir
                            </a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center">Nenhuma atividade ritualística encontrada.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- Paginação -->
    {% if is_paginated %}
    <nav aria-label="Paginação" class="mt-3">
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page=1{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}" aria-label="Primeira">
                    <span aria-hidden="true">&laquo;&laquo;</span>
                </a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}" aria-label="Anterior">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
            {% else %}
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Primeira">
                    <span aria-hidden="true">&laquo;&laquo;</span>
                </a>
            </li>
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Anterior">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
            {% endif %}
            
            {% for num in page_obj.paginator.page_range %}
                {% if page_obj.number == num %}
                <li class="page-item active"><a class="page-link" href="?page={{ num }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">{{ num }}</a></li>
                {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                <li class="page-item"><a class="page-link" href="?page={{ num }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">{{ num }}</a></li>
                {% endif %}
            {% endfor %}
            
            {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}" aria-label="Próxima">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}" aria-label="Última">
                    <span aria-hidden="true">&raquo;&raquo;</span>
                </a>
            </li>
            {% else %}
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Próxima">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
            <li class="page-item





## atividades\tests\test_models.py

python
from django.test import TestCase
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from cursos.models import Curso
from alunos.models import Aluno
from datetime import date, timedelta
from django.utils import timezone

class AtividadeAcademicaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        
    def test_criar_atividade(self):
        data_inicio = timezone.now()
        data_fim = data_inicio + timedelta(days=7)
        
        atividade = AtividadeAcademica.objects.create(
            nome='Aula de Matemática',
            descricao='Aula introdutória sobre álgebra.',
            data_inicio=data_inicio,
            data_fim=data_fim,
            turma=self.turma
        )
        
        self.assertEqual(atividade.nome, 'Aula de Matemática')
        self.assertEqual(atividade.descricao, 'Aula introdutória sobre álgebra.')
        self.assertEqual(atividade.data_inicio, data_inicio)
        self.assertEqual(atividade.data_fim, data_fim)
        self.assertEqual(atividade.turma, self.turma)
        self.assertEqual(str(atividade), 'Aula de Matemática')

class AtividadeRitualisticaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        self.aluno1 = Aluno.objects.create(
            nome='Aluno 1',
            email='aluno1@teste.com'
        )
        self.aluno1.turmas.add(self.turma)
        self.aluno2 = Aluno.objects.create(
            nome='Aluno 2',
            email='aluno2@teste.com'
        )
        self.aluno2.turmas.add(self.turma)
        
    def test_criar_atividade_ritualistica(self):
        data_inicio = timezone.now()
        data_fim = data_inicio + timedelta(days=7)
        
        atividade = AtividadeRitualistica.objects.create(
            nome='Ritual de Iniciação',
            descricao='Ritual para novos membros',
            data_inicio=data_inicio,
            data_fim=data_fim,
            turma=self.turma
        )
        atividade.alunos.add(self.aluno1, self.aluno2)
        
        self.assertEqual(atividade.nome, 'Ritual de Iniciação')
        self.assertEqual(atividade.descricao, 'Ritual para novos membros')
        self.assertEqual(atividade.data_inicio, data_inicio)
        self.assertEqual(atividade.data_fim, data_fim)
        self.assertEqual(atividade.turma, self.turma)
        self.assertEqual(atividade.alunos.count(), 2)
        self.assertTrue(self.aluno1 in atividade.alunos.all())
        self.assertTrue(self.aluno2 in atividade.alunos.all())
        self.assertEqual(str(atividade), 'Ritual de Iniciação')





## atividades\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from cursos.models import Curso
from alunos.models import Aluno
from datetime import date, timedelta
from django.utils import timezone

class AtividadeAcademicaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            codigo_curso='CUR01',
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        self.data_inicio = timezone.now()
        self.data_fim = self.data_inicio + timedelta(days=7)
        self.atividade = AtividadeAcademica.objects.create(
            nome='Aula de Matemática',
            descricao='Aula introdutória sobre álgebra.',
            data_inicio=self.data_inicio,
            data_fim=self.data_fim,
            turma=self.turma
        )

    def test_listar_atividades(self):
        response = self.client.get(reverse('atividades:academica_lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aula de Matemática')
        
    def test_filtrar_atividades_por_turma(self):
        # Criar outra turma e atividade
        turma2 = Turma.objects.create(
            nome='Turma 2',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        AtividadeAcademica.objects.create(
            nome='Aula de Física',
            descricao='Introdução à física',
            data_inicio=self.data_inicio,
            data_fim=self.data_fim,
            turma=turma2
        )
        
        # Filtrar por turma1
        response = self.client.get(f"{reverse('atividades:academica_lista')}?turma={self.turma.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aula de Matemática')
        self.assertNotContains(response, 'Aula de Física')
        
        # Filtrar por turma2
        response = self.client.get(f"{reverse('atividades:academica_lista')}?turma={turma2.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aula de Física')
        self.assertNotContains(response, 'Aula de Matemática')

    def test_criar_atividade(self):
        response = self.client.get(reverse('atividades:academica_criar'))
        self.assertEqual(response.status_code, 200)
        
        # Testar POST para criar atividade
        data = {
            'nome': 'Nova Atividade',
            'descricao': 'Descrição da nova atividade',
            'data_inicio': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_fim': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
            'turma': self.turma.id
        }
        response = self.client.post(reverse('atividades:academica_criar'), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verificar se a atividade foi criada
        self.assertTrue(AtividadeAcademica.objects.filter(nome='Nova Atividade').exists())
    
    def test_editar_atividade(self):
        response = self.client.get(reverse('atividades:academica_editar', args=[self.atividade.id]))
        self.assertEqual(response.status_code, 200)
        
        # Testar POST para editar atividade
        data = {
            'nome': 'Aula de Matemática Atualizada',
            'descricao': 'Descrição atualizada',
            'data_inicio': self.data_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            'data_fim': self.data_fim.strftime('%Y-%m-%d %H:%M:%S'),
            'turma': self.turma.id
        }
        response = self.client.post(reverse('atividades:academica_editar', args=[self.atividade.id]), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verificar se a atividade foi atualizada
        self.atividade.refresh_from_db()
        self.assertEqual(self.atividade.nome, 'Aula de Matemática Atualizada')
        self.assertEqual(self.atividade.descricao, 'Descrição atualizada')
    
    def test_excluir_atividade(self):
        response = self.client.get(reverse('atividades:academica_excluir',



