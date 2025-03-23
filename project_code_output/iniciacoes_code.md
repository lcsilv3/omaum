# Código da Funcionalidade: iniciacoes
*Gerado automaticamente*



## iniciacoes\admin.py

python
from django.contrib import admin
from .models import Iniciacao

@admin.register(Iniciacao)
class IniciacaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'nome_curso', 'data_iniciacao')
    list_filter = ('nome_curso', 'data_iniciacao')
    search_fields = ('aluno__nome', 'nome_curso')
    date_hierarchy = 'data_iniciacao'
    ordering = ('-data_iniciacao',)
    raw_id_fields = ('aluno',)




## iniciacoes\apps.py

python
from django.apps import AppConfig


class IniciacoesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iniciacoes'




## iniciacoes\forms.py

python
from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Iniciacao

class IniciacaoForm(forms.ModelForm):
    class Meta:
        model = Iniciacao
        fields = ['aluno', 'nome_curso', 'data_iniciacao', 'observacoes']
        widgets = {
            'data_iniciacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'nome_curso': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'aluno': 'Aluno',
            'nome_curso': 'Nome do Curso',
            'data_iniciacao': 'Data de Iniciação',
            'observacoes': 'Observações'
        }
        help_texts = {
            'nome_curso': 'Digite o nome completo do curso de iniciação',
            'data_iniciacao': 'Selecione a data em que o aluno foi iniciado no curso'
        }

    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        nome_curso = cleaned_data.get('nome_curso')
        data_iniciacao = cleaned_data.get('data_iniciacao')
        
        # Verifica se já existe uma iniciação para este aluno neste curso
        if aluno and nome_curso:
            # Exclui a instância atual em caso de edição
            instance_id = self.instance.id if self.instance else None
            
            # Verifica se já existe outra iniciação com o mesmo aluno e curso
            if Iniciacao.objects.filter(aluno=aluno, nome_curso=nome_curso).exclude(id=instance_id).exists():
                raise ValidationError(
                    f"O aluno {aluno.nome} já possui uma iniciação no curso {nome_curso}."
                )
        
        return cleaned_data

    def clean_data_iniciacao(self):
        data_iniciacao = self.cleaned_data.get('data_iniciacao')
        
        if data_iniciacao and data_iniciacao > date.today():
            raise ValidationError("A data de iniciação não pode ser no futuro.")
        
        return data_iniciacao



## iniciacoes\models.py

python
from django.db import models
from alunos.models import Aluno


class Iniciacao(models.Model):
    """
    Modelo para armazenar informações sobre iniciações de alunos em cursos.
    
    Atributos:
        aluno (ForeignKey): Referência ao aluno que recebeu a iniciação
        nome_curso (str): Nome do curso de iniciação
        data_iniciacao (date): Data em que a iniciação ocorreu
        observacoes (str, opcional): Observações adicionais sobre a iniciação
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='iniciacoes')
    nome_curso = models.CharField(max_length=100)
    data_iniciacao = models.DateField()
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Iniciação - {self.aluno.nome} - {self.nome_curso}"

    class Meta:
        ordering = ['-data_iniciacao']
        verbose_name = 'Iniciação'
        verbose_name_plural = 'Iniciações'




## iniciacoes\tests.py

python
from django.test import TestCase

# Create your tests here.




## iniciacoes\urls.py

python
from django.urls import path
from . import views

app_name = 'iniciacoes'

urlpatterns = [
    path('', views.listar_iniciacoes, name='listar_iniciacoes'),
    path('criar/', views.criar_iniciacao, name='criar_iniciacao'),
    path('<int:id>/', views.detalhe_iniciacao, name='detalhe_iniciacao'),
    path('<int:id>/editar/', views.editar_iniciacao, name='editar_iniciacao'),
    path('<int:id>/excluir/', views.excluir_iniciacao, name='excluir_iniciacao'),
    path('exportar/csv/', views.exportar_iniciacoes_csv, name='exportar_iniciacoes_csv'),
]




## iniciacoes\views.py

python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Iniciacao
from .forms import IniciacaoForm
from alunos.models import Aluno
from django.contrib.auth.decorators import login_required


@login_required
def listar_iniciacoes(request):
    # Parâmetros de filtro
    aluno_id = request.GET.get('aluno')
    nome_curso = request.GET.get('curso')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    # Query base
    iniciacoes = Iniciacao.objects.all()
    
    # Aplicar filtros
    if aluno_id:
        iniciacoes = iniciacoes.filter(aluno_id=aluno_id)
    
    if nome_curso:
        iniciacoes = iniciacoes.filter(nome_curso__icontains=nome_curso)
    
    if data_inicio:
        iniciacoes = iniciacoes.filter(data_iniciacao__gte=data_inicio)
    
    if data_fim:
        iniciacoes = iniciacoes.filter(data_iniciacao__lte=data_fim)
    
    # Busca geral
    search_query = request.GET.get('search', '')
    if search_query:
        iniciacoes = iniciacoes.filter(
            Q(aluno__nome__icontains=search_query) |
            Q(nome_curso__icontains=search_query)
        )
    
    # Paginação
    paginator = Paginator(iniciacoes, 10)  # 10 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Lista de alunos para o filtro
    alunos = Aluno.objects.all()
    
    context = {
        'page_obj': page_obj,
        'alunos': alunos,
        'filtros': {
            'aluno_id': aluno_id,
            'nome_curso': nome_curso,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'search': search_query
        }
    }
    
    return render(request, 'iniciacoes/listar_iniciacoes.html', context)


@login_required
def criar_iniciacao(request):
    if request.method == 'POST':
        form = IniciacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Iniciação criada com sucesso.')
            return redirect('iniciacoes:listar_iniciacoes')
    else:
        form = IniciacaoForm()
    return render(request, 'iniciacoes/criar_iniciacao.html', {'form': form})


@login_required
def detalhe_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    return render(request, 'iniciacoes/detalhe_iniciacao.html', {'iniciacao': iniciacao})


@login_required
def editar_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    if request.method == 'POST':
        form = IniciacaoForm(request.POST, instance=iniciacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Iniciação atualizada com sucesso.')
            return redirect('iniciacoes:listar_iniciacoes')
    else:
        form = IniciacaoForm(instance=iniciacao)
    return render(request, 'iniciacoes/editar_iniciacao.html', {'form': form, 'iniciacao': iniciacao})


@login_required
def excluir_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    if request.method == 'POST':
        iniciacao.delete()
        messages.success(request, 'Iniciação excluída com sucesso.')
        return redirect('iniciacoes:listar_iniciacoes')
    return render(request, 'iniciacoes/excluir_iniciacao.html', {'iniciacao': iniciacao})

import csv
from django.http import HttpResponse

@login_required
def exportar_iniciacoes_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iniciacoes.csv"'
    
    # Aplicar os mesmos filtros da listagem
    aluno_id = request.GET.get('aluno')
    nome_curso = request.GET.get('curso')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    search_query = request.GET.get('search', '')
    
    # Query base
    iniciacoes = Iniciacao.objects.all()
    
    # Aplicar filtros (mesmo código da view listar_iniciacoes)
    if aluno_id:
        iniciacoes = iniciacoes.filter(aluno_id=aluno_id)
    
    if nome_curso:
        iniciacoes = iniciacoes.filter(nome_curso__icontains=nome_curso)
    
    if data_inicio:
        iniciacoes = iniciacoes.filter(data_iniciacao__gte=data_inicio)
    
    if data_fim:
        iniciacoes = iniciacoes.filter(data_iniciacao__lte=data_fim)
    
    if search_query:
        iniciacoes = iniciacoes.filter(
            Q(aluno__nome__icontains=search_query) |
            Q(nome_curso__icontains=search_query)
        )
    
    writer = csv.writer(response)
    writer.writerow(['Aluno', 'Curso', 'Data de Iniciação', 'Observações'])
    
    for iniciacao in iniciacoes:
        writer.writerow([
            iniciacao.aluno.nome,
            iniciacao.nome_curso,
            iniciacao.data_iniciacao.strftime('%d/%m/%Y'),
            iniciacao.observacoes or ''
        ])
    
    # Adicionar mensagem de sucesso
    messages.success(request, f'Arquivo CSV com {iniciacoes.count()} iniciações exportado com sucesso.')
    
    return response




## iniciacoes\templates\iniciacoes\criar_iniciacao.html

html
{% extends 'base.html' %}

{% block title %}Nova Iniciação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card shadow-sm">
        <div class="card-header bg-primary text-white">
            <h1 class="h3 mb-0">Nova Iniciação</h1>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                {% if form.errors %}
                <div class="alert alert-danger">
                    <strong>Erro ao salvar o formulário:</strong>
                    <ul>
                        {% for field, errors in form.errors.items %}
                            {% for error in errors %}
                                <li>{{ error }}</li>
                            {% endfor %}
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="{{ form.aluno.id_for_label }}">{{ form.aluno.label }}</label>
                            {{ form.aluno }}
                            {% if form.aluno.help_text %}
                            <small class="form-text text-muted">{{ form.aluno.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="{{ form.nome_curso.id_for_label }}">{{ form.nome_curso.label }}</label>
                            {{ form.nome_curso }}
                            {% if form.nome_curso.help_text %}
                            <small class="form-text text-muted">{{ form.nome_curso.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="{{ form.data_iniciacao.id_for_label }}">{{ form.data_iniciacao.label }}</label>
                            {{ form.data_iniciacao }}
                            {% if form.data_iniciacao.help_text %}
                            <small class="form-text text-muted">{{ form.data_iniciacao.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <div class="row mb-3">
                    <div class="col-md-12">
                        <div class="form-group">
                            <label for="{{ form.observacoes.id_for_label }}">{{ form.observacoes.label }}</label>
                            {{ form.observacoes }}
                        </div>
                    </div>
                </div>
                
                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Salvar
                    </button>
                    <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">
                        <i class="fas fa-arrow-left"></i> Cancelar
                    </a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




## iniciacoes\templates\iniciacoes\detalhe_iniciacao.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Iniciação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card shadow-sm">
        <div class="card-header bg-info text-white">
            <h1 class="h3 mb-0">Detalhes da Iniciação</h1>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <h5 class="card-title">Informações Gerais</h5>
                    <dl class="row">
                        <dt class="col-sm-4">Aluno:</dt>
                        <dd class="col-sm-8">{{ iniciacao.aluno.nome }}</dd>
                        
                        <dt class="col-sm-4">Curso:</dt>
                        <dd class="col-sm-8">{{ iniciacao.nome_curso }}</dd>
                        
                        <dt class="col-sm-4">Data:</dt>
                        <dd class="col-sm-8">{{ iniciacao.data_iniciacao|date:"d/m/Y" }}</dd>
                    </dl>
                </div>
                <div class="col-md-6">
                    <h5 class="card-title">Observações</h5>
                    <p class="card-text">{{ iniciacao.observacoes|default:"Nenhuma observação registrada."|linebreaks }}</p>
                </div>
            </div>
            
            <div class="mt-4">
                <a href="{% url 'iniciacoes:editar_iniciacao' iniciacao.id %}" class="btn btn-warning">
                    <i class="fas fa-edit"></i> Editar
                </a>
                <a href="{% url 'iniciacoes:excluir_iniciacao' iniciacao.id %}" class="btn btn-danger">
                    <i class="fas fa-trash"></i> Excluir
                </a>
                <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">
                    <i class="fas fa-arrow-left"></i> Voltar
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}



## iniciacoes\templates\iniciacoes\editar_iniciacao.html

html
{% extends 'base.html' %}

{% block title %}Editar Iniciação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card shadow-sm">
        <div class="card-header bg-warning">
            <h1 class="h3 mb-0">Editar Iniciação</h1>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
               
                {% if form.errors %}
                <div class="alert alert-danger">
                    <strong>Erro ao salvar o formulário:</strong>
                    <ul>
                        {% for field, errors in form.errors.items %}
                            {% for error in errors %}
                                <li>{{ error }}</li>
                            {% endfor %}
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
               
                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="{{ form.aluno.id_for_label }}">{{ form.aluno.label }}</label>
                            {{ form.aluno }}
                            {% if form.aluno.help_text %}
                            <small class="form-text text-muted">{{ form.aluno.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="{{ form.nome_curso.id_for_label }}">{{ form.nome_curso.label }}</label>
                            {{ form.nome_curso }}
                            {% if form.nome_curso.help_text %}
                            <small class="form-text text-muted">{{ form.nome_curso.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                </div>
               
                <div class="row mb-3">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label for="{{ form.data_iniciacao.id_for_label }}">{{ form.data_iniciacao.label }}</label>
                            {{ form.data_iniciacao }}
                            {% if form.data_iniciacao.help_text %}
                            <small class="form-text text-muted">{{ form.data_iniciacao.help_text }}</small>
                            {% endif %}
                        </div>
                    </div>
                </div>
               
                <div class="row mb-3">
                    <div class="col-md-12">
                        <div class="form-group">
                            <label for="{{ form.observacoes.id_for_label }}">{{ form.observacoes.label }}</label>
                            {{ form.observacoes }}
                        </div>
                    </div>
                </div>
               
                <div class="mt-4">
                    <button type="submit" class="btn btn-warning">
                        <i class="fas fa-save"></i> Salvar Alterações
                    </button>
                    <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">
                        <i class="fas fa-arrow-left"></i> Cancelar
                    </a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



## iniciacoes\templates\iniciacoes\excluir_iniciacao.html

html
{% extends 'base.html' %}

{% block title %}Excluir Iniciação{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card shadow-sm border-danger">
        <div class="card-header bg-danger text-white">
            <h1 class="h3 mb-0">Excluir Iniciação</h1>
        </div>
        <div class="card-body">
            <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle"></i> Atenção: Esta ação não pode ser desfeita!
            </div>
            
            <p class="lead">Tem certeza que deseja excluir a iniciação abaixo?</p>
            
            <dl class="row">
                <dt class="col-sm-3">Aluno:</dt>
                <dd class="col-sm-9">{{ iniciacao.aluno.nome }}</dd>
                
                <dt class="col-sm-3">Curso:</dt>
                <dd class="col-sm-9">{{ iniciacao.nome_curso }}</dd>
                
                <dt class="col-sm-3">Data:</dt>
                <dd class="col-sm-9">{{ iniciacao.data_iniciacao|date:"d/m/Y" }}</dd>
            </dl>
            
            <form method="post" class="mt-4">
                {% csrf_token %}
                <button type="submit" class="btn btn-danger">
                    <i class="fas fa-trash"></i> Confirmar Exclusão
                </button>
                <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">
                    <i class="fas fa-times"></i> Cancelar
                </a>
            </form>
        </div>
    </div>
</div>
{% endblock %}



## iniciacoes\templates\iniciacoes\listar_iniciacoes.html

html
{% extends 'base.html' %}

{% block title %}Lista de Iniciações{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card shadow-sm">
        <div class="card-header bg-primary text-white">
            <h1 class="h3 mb-0">Lista de Iniciações</h1>
        </div>
        <div class="card-body">
            <!-- Botão de Nova Iniciação -->
            <div class="mb-3">
                <a href="{% url 'iniciacoes:criar_iniciacao' %}" class="btn btn-success">
                    <i class="fas fa-plus-circle"></i> Nova Iniciação
                </a>
            </div>
            
            <!-- Filtros Avançados -->
            <div class="card mb-4">
                <div class="card-header bg-light">
                    <h5 class="mb-0">Filtros</h5>
                </div>
                <div class="card-body">
                    <form method="get" class="row g-3">
                        <!-- Busca geral -->
                        <div class="col-md-12 mb-2">
                            <div class="input-group">
                                <input type="text" name="search" class="form-control" placeholder="Buscar por aluno ou curso" value="{{ filtros.search }}">
                                <button class="btn btn-outline-primary" type="submit">Buscar</button>
                            </div>
                        </div>
                        
                        <!-- Filtros específicos -->
                        <div class="col-md-3">
                            <label for="aluno" class="form-label">Aluno</label>
                            <select name="aluno" id="aluno" class="form-select">
                                <option value="">Todos os alunos</option>
                                {% for aluno in alunos %}
                                <option value="{{ aluno.id }}" {% if filtros.aluno_id == aluno.id|stringformat:"s" %}selected{% endif %}>
                                    {{ aluno.nome }}
                                </option>
                                {% endfor %}
                            </select>
                        </div>
                        
                        <div class="col-md-3">
                            <label for="curso" class="form-label">Curso</label>
                            <input type="text" name="curso" id="curso" class="form-control" value="{{ filtros.nome_curso }}">
                        </div>
                        
                        <div class="col-md-3">
                            <label for="data_inicio" class="form-label">Data Inicial</label>
                            <input type="date" name="data_inicio" id="data_inicio" class="form-control" value="{{ filtros.data_inicio }}">
                        </div>
                        
                        <div class="col-md-3">
                            <label for="data_fim" class="form-label">Data Final</label>
                            <input type="date" name="data_fim" id="data_fim" class="form-control" value="{{ filtros.data_fim }}">
                        </div>
                        
                        <div class="col-12 mt-3">
                            <button type="submit" class="btn btn-primary">Filtrar</button>
                            <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Limpar Filtros</a>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- Tabela de Iniciações -->
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Aluno</th>
                            <th>Curso</th>
                            <th>Data</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for iniciacao in page_obj %}
                        <tr>
                            <td>{{ iniciacao.aluno.nome }}</td>
                            <td>{{ iniciacao.nome_curso }}</td>
                            <td>{{ iniciacao.data_iniciacao|date:"d/m/Y" }}</td>
                            <td>
                                <div class="btn-group" role="group">
                                    <a href="{% url 'iniciacoes:detalhe_iniciacao' iniciacao.id %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-eye"></i> Detalhes
                                    </a>
                                    <a href="{% url 'iniciacoes:editar_iniciacao' iniciacao.id %}" class="btn btn-sm btn-warning">
                                        <i class="fas fa-edit"></i> Editar
                                    </a>
                                    <a href="{% url 'iniciacoes:excluir_iniciacao' iniciacao.id %}" class="btn btn-sm btn-danger">
                                        <i class="fas fa-trash"></i> Excluir
                                    </a>
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="4" class="text-center">Nenhuma iniciação encontrada.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            
            <!-- Paginação -->
            {% if page_obj.has_other_pages %}
            <nav aria-label="Paginação">
                <ul class="pagination justify-content-center">
                    {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page=1{% for key, value in filtros.items %}{% if value %}&{{ key }}={{ value }}{% endif %}{% endfor %}" aria-label="Primeira">
                            <span aria-hidden="true">««</span>
                        </a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% for key, value in filtros.items %}{% if value %}&{{ key }}={{ value }}{% endif %}{% endfor %}" aria-label="Anterior">
                            <span aria-hidden="true">«</span>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <a class="page-link" href="#" tabindex="-1" aria-disabled="true">««</a>
                    </li>
                    <li class="page-item disabled">
                        <a class="page-link" href="#" tabindex="-1" aria-disabled="true">«</a>
                    </li>
                    {% endif %}
                    
                    {% for num in page_obj.paginator.page_range %}
                        {% if page_obj.number == num %}
                        <li class="page-item active" aria-current="page">
                            <span class="page-link">{{ num }}</span>
                        </li>
                        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ num }}{% for key, value in filtros.items %}{% if value %}&{{ key }}={{ value }}{% endif %}{% endfor %}">{{ num }}</a>
                        </li>
                        {% endif %}
                    {% endfor %}
                    
                    {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}{% for key, value in filtros.items %}{% if value %}&{{ key }}={{ value }}{% endif %}{% endfor %}" aria-label="Próxima">
                            <span aria-hidden="true">»</span>
                        </a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% for key, value in filtros.items %}{% if value %}&{{ key }}={{ value }}{% endif %}{% endfor %}" aria-label="Última">
                            <span aria-hidden="true">»»</span>
                        </a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <a class="page-link" href="#" tabindex="-1" aria-disabled="true">»</a>
                    </li>
                    <li class="page-item disabled">
                        <a class="page-link" href="#" tabindex="-1" aria-disabled="true">»»</a>
                    </li>
                    {% endif %}
                </ul>
            </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}



## iniciacoes\tests\test_forms.py

python
from django.test import TestCase
from iniciacoes.forms import IniciacaoForm
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time

class IniciacaoFormTest(TestCase):
    def setUp(self):
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )
        
        # Criar uma iniciação para testar a validação de duplicidade
        self.iniciacao = Iniciacao.objects.create(
            aluno=self.aluno,
            nome_curso='Curso de Iniciação',
            data_iniciacao=date(2023, 10, 1)
        )
    
    def test_form_valido(self):
        # Testando um formulário com dados válidos
        form_data = {
            'aluno': self.aluno.id,
            'nome_curso': 'Curso de Meditação',  # Curso diferente
            'data_iniciacao': date(2023, 11, 1),
            'observacoes': 'Teste de observação'
        }
        form = IniciacaoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalido_curso_duplicado(self):
        # Testando um formulário com curso duplicado para o mesmo aluno
        form_data = {
            'aluno': self.aluno.id,
            'nome_curso': 'Curso de Iniciação',  # Mesmo curso que já existe
            'data_iniciacao': date(2023, 11, 1),
            'observacoes': 'Teste de observação'
        }
        form = IniciacaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
    
    def test_form_campos_obrigatorios(self):
        # Testando um formulário sem campos obrigatórios
        form_data = {
            'observacoes': 'Apenas observações'
        }
        form = IniciacaoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('aluno', form.errors)
        self.assertIn('nome_curso', form.errors)
        self.assertIn('data_iniciacao', form.errors)




## iniciacoes\tests\test_models.py

python
from django.test import TestCase
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time

class IniciacaoModelTest(TestCase):
    def setUp(self):
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )

    def test_criar_iniciacao(self):
        iniciacao = Iniciacao.objects.create(
            aluno=self.aluno,
            nome_curso='Curso de Iniciação',
            data_iniciacao=date(2023, 10, 1)
        )
        self.assertEqual(iniciacao.nome_curso, 'Curso de Iniciação')
        self.assertEqual(iniciacao.aluno, self.aluno)




## iniciacoes\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time

class IniciacaoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Criar um usuário de teste e fazer login
        self.usuario = User.objects.create_user(username='usuarioteste', password='12345')
        self.client.login(username='usuarioteste', password='12345')
        
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )
        self.iniciacao = Iniciacao.objects.create(
            aluno=self.aluno,
            nome_curso='Curso de Iniciação',
            data_iniciacao=date(2023, 10, 1)
        )

    def test_listar_iniciacoes(self):
        response = self.client.get(reverse('iniciacoes:listar_iniciacoes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Silva')
        self.assertContains(response, 'Curso de Iniciação')




## iniciacoes\tests\test_views_avancado.py

python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time, timedelta
import json

class IniciacaoViewAvancadoTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Criar um usuário de teste e fazer login
        self.usuario = User.objects.create_user(username='usuarioteste', password='12345')
        self.client.login(username='usuarioteste', password='12345')
        
        # Criar vários alunos para testar paginação e filtros
        self.aluno1 = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )
        
        self.aluno2 = Aluno.objects.create(
            cpf='98765432109',
            nome='Maria Oliveira',
            data_nascimento=date(1992, 5, 15),
            hora_nascimento=time(10, 0),
            email='maria@example.com',
            sexo='F',
            nacionalidade='Brasileira',
            naturalidade='Rio de Janeiro',
            rua='Rua Exemplo',
            numero_imovel='456',
            cidade='Rio de Janeiro',
            estado='RJ',
            bairro='Copacabana',
            cep='22000000',
            nome_primeiro_contato='Pedro Oliveira',
            celular_primeiro_contato='21999999999',
            tipo_relacionamento_primeiro_contato='Pai',
            nome_segundo_contato='Ana Oliveira',
            celular_segundo_contato='21988888888',
            tipo_relacionamento_segundo_contato='Mãe',
            tipo_sanguineo='O',
            fator_rh='-'
        )
        
        # Criar várias iniciações para testar paginação
        data_base = date(2023, 1, 1)
        cursos = ['Yoga', 'Meditação', 'Reiki', 'Tai Chi', 'Chi Kung', 
                 'Aromaterapia', 'Cromoterapia', 'Acupuntura', 'Shiatsu', 
                 'Reflexologia', 'Ayurveda', 'Fitoterapia']
        
        for i, curso in enumerate(cursos):
            aluno = self.aluno1 if i % 2 == 0 else self.aluno2
            Iniciacao.objects.create(
                aluno=aluno,
                nome_curso=curso,
                data_iniciacao=data_base + timedelta(days=i*30),
                observacoes=f"Observação para o curso de {curso}"
            )
    
    def test_paginacao(self):
        response = self.client.get(reverse('iniciacoes:listar_iniciacoes'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), 10)  # 10 itens por página
        
        # Testar segunda página
        response = self.client.get(f"{reverse('iniciacoes:listar_iniciacoes')}?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 2)  # 2 itens restantes
    
    def test_filtro_aluno(self):
        url = f"{reverse('iniciacoes:listar_iniciacoes')}?aluno={self.aluno1.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se apenas as iniciações do aluno1 estão presentes
        for iniciacao in response.context['page_obj']:
            self.assertEqual(iniciacao.aluno.id, self.aluno1.id)
    
    def test_filtro_curso(self):
        url = f"{reverse('iniciacoes:listar_iniciacoes')}?curso=Yoga"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se apenas as iniciações com "Yoga" no nome do curso estão presentes
        for iniciacao in response.context['page_obj']:
            self.assertIn('Yoga', iniciacao.nome_curso)
    
    def test_filtro_data(self):
        data_inicio = date(2023, 3, 1).strftime('%Y-%m-%d')
        data_fim = date(2023, 6, 30).strftime('%Y-%m-%d')
        url = f"{reverse('iniciacoes:listar_iniciacoes')}?data_inicio={data_inicio}&data_fim={data_fim}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se apenas as iniciações dentro do período estão presentes
        for iniciacao in response.context['page_obj']:
            self.assertTrue(iniciacao.data_iniciacao >= date(2023, 3, 1))
            self.assertTrue(iniciacao.data_iniciacao <= date(2023, 6, 30))
    
    def test_busca_geral(self):
        url = f"{reverse('iniciacoes:listar_iniciacoes')}?search=Reiki"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se apenas as iniciações com "Reiki" no nome do curso estão presentes
        for iniciacao in response.context['page_obj']:
            self.assertIn('Reiki', iniciacao.nome_curso)
    
    def test_criar_iniciacao_duplicada(self):
        # Tentar criar uma iniciação duplicada (mesmo aluno e curso)
        iniciacao_existente = Iniciacao.objects.filter(aluno=self.aluno1).first()
        
        form_data = {
            'aluno': self.aluno1.id,
            'nome_curso': iniciacao_existente.nome_curso,
            'data_iniciacao': '2023-12-01',
            'observacoes': 'Tentativa de duplicação'
        }
        
        response = self.client.post(reverse('iniciacoes:criar_iniciacao'), form_data)
        self.assertEqual(response.status_code, 200)  # Permanece no formulário
        self.assertContains(response, "já possui uma iniciação no curso")


