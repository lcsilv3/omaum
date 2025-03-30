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
    path('nova/', views.criar_iniciacao, name='criar_iniciacao'),
    path('<int:id>/editar/', views.editar_iniciacao, name='editar_iniciacao'),
    path('<int:id>/excluir/', views.excluir_iniciacao, name='excluir_iniciacao'),
    path('<int:id>/detalhes/', views.detalhar_iniciacao, name='detalhar_iniciacao'),
    path('graus/', views.listar_graus, name='listar_graus'),
    path('graus/novo/', views.criar_grau, name='criar_grau'),
    path('graus/<int:id>/editar/', views.editar_grau, name='editar_grau'),
    path('graus/<int:id>/excluir/', views.excluir_grau, name='excluir_grau'),
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





## iniciacoes\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-03-27 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alunos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iniciacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_curso', models.CharField(max_length=100)),
                ('data_iniciacao', models.DateField()),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iniciacoes', to='alunos.aluno')),
            ],
            options={
                'verbose_name': 'Iniciação',
                'verbose_name_plural': 'Iniciações',
                'ordering': ['-data_iniciacao'],
            },
        ),
    ]





## iniciacoes\templates\iniciacoes\criar_grau.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Novo Grau de Iniciação</h1>
  
  <form method="post">
    {% csrf_token %}
    {% include 'includes/form_errors.html' %}
    
    {% for field in form %}
      {% include 'includes/form_field.html' %}
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Criar Grau</button>
    <a href="{% url 'iniciacoes:listar_graus' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}





## iniciacoes\templates\iniciacoes\criar_iniciacao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Nova Iniciação</h1>
  
    <form method="post">
      {% csrf_token %}
      {% include 'includes/form_errors.html' %}
    
      {% for field in form %}
        {% include 'includes/form_field.html' %}
      {% endfor %}
    
      <button type="submit" class="btn btn-primary">Registrar Iniciação</button>
      <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}





## iniciacoes\templates\iniciacoes\detalhar_iniciacao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes da Iniciação</h1>
  
  <div class="card">
    <div class="card-header">
      <h2>Iniciação de {{ iniciacao.aluno.nome }}</h2>
    </div>
    <div class="card-body">
      <p><strong>Aluno:</strong> {{ iniciacao.aluno.nome }}</p>
      <p><strong>Grau:</strong> {{ iniciacao.grau.nome }}</p>
      <p><strong>Data:</strong> {{ iniciacao.data|date:"d/m/Y" }}</p>
      <p><strong>Local:</strong> {{ iniciacao.local }}</p>
      <p>
        <strong>Status:</strong> 
        {% if iniciacao.concluida %}
          <span class="badge bg-success">Concluída</span>
        {% else %}
          <span class="badge bg-warning">Pendente</span>
        {% endif %}
      </p>
      {% if iniciacao.observacoes %}
        <p><strong>Observações:</strong> {{ iniciacao.observacoes }}</p>
      {% endif %}
      <p><strong>Registrado por:</strong> {{ iniciacao.registrado_por.username }}</p>
      <p><strong>Data de registro:</strong> {{ iniciacao.data_registro|date:"d/m/Y H:i" }}</p>
      {% if iniciacao.atualizado_por %}
        <p><strong>Atualizado por:</strong> {{ iniciacao.atualizado_por.username }}</p>
        <p><strong>Data de atualização:</strong> {{ iniciacao.data_atualizacao|date:"d/m/Y H:i" }}</p>
      {% endif %}
    </div>
    <div class="card-footer">
      <a href="{% url 'iniciacoes:editar_iniciacao' iniciacao.id %}" class="btn btn-warning">Editar</a>
      <a href="{% url 'iniciacoes:excluir_iniciacao' iniciacao.id %}" class="btn btn-danger">Excluir</a>
      <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Voltar</a>
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




## iniciacoes\templates\iniciacoes\editar_grau.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Editar Grau de Iniciação</h1>
  
  <form method="post">
    {% csrf_token %}
    {% include 'includes/form_errors.html' %}
    
    {% for field in form %}
      {% include 'includes/form_field.html' %}
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Atualizar Grau</button>
    <a href="{% url 'iniciacoes:listar_graus' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}





## iniciacoes\templates\iniciacoes\editar_iniciacao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Iniciação</h1>
  
    <form method="post">
      {% csrf_token %}
      {% include 'includes/form_errors.html' %}
    
      {% for field in form %}
        {% include 'includes/form_field.html' %}
      {% endfor %}
    
      <button type="submit" class="btn btn-primary">Atualizar Iniciação</button>
      <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




## iniciacoes\templates\iniciacoes\excluir_grau.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Excluir Grau de Iniciação</h1>
  
  <div class="alert alert-danger">
    <p>Tem certeza que deseja excluir o grau <strong>{{ grau.nome }}</strong>?</p>
    {% if iniciacoes_associadas %}
      <div class="mt-3">
        <p><strong>Atenção:</strong> Existem {{ iniciacoes_associadas }} iniciações associadas a este grau. A exclusão deste grau pode afetar esses registros.</p>
      </div>
    {% endif %}
  </div>
  
  <form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Sim, excluir</button>
    <a href="{% url 'iniciacoes:listar_graus' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}





## iniciacoes\templates\iniciacoes\excluir_iniciacao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Iniciação</h1>
  
    <div class="alert alert-danger">
      <p>Tem certeza que deseja excluir a iniciação de <strong>{{ iniciacao.aluno.nome }}</strong> no grau <strong>{{ iniciacao.grau.nome }}</strong> realizada em <strong>{{ iniciacao.data|date:"d/m/Y" }}</strong>?</p>
    </div>
  
    <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Sim, excluir</button>
      <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




## iniciacoes\templates\iniciacoes\listar_graus.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Graus de Iniciação</h1>
  
  <div class="d-flex justify-content-between mb-3">
    <a href="{% url 'iniciacoes:criar_grau' %}" class="btn btn-primary">Novo Grau</a>
    <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Voltar para Iniciações</a>
  </div>
  
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Nome</th>
        <th>Número</th>
        <th>Descrição</th>
        <th>Requisitos</th>
        <th>Ações</th>
      </tr>
    </thead>
    <tbody>
      {% for grau in graus %}
      <tr>
        <td>{{ grau.nome }}</td>
        <td>{{ grau.numero }}</td>
        <td>{{ grau.descricao|truncatechars:50 }}</td>
        <td>{{ grau.requisitos|truncatechars:50 }}</td>
        <td>
          <a href="{% url 'iniciacoes:editar_grau' grau.id %}" class="btn btn-sm btn-warning">Editar</a>
          <a href="{% url 'iniciacoes:excluir_grau' grau.id %}" class="btn btn-sm btn-danger">Excluir</a>
        </td>
      </tr>
      {% empty %}
      <tr>
        <td colspan="5">Nenhum grau cadastrado.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}





## iniciacoes\templates\iniciacoes\listar_iniciacoes.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Iniciações</h1>
  
    <div class="d-flex justify-content-between mb-3">
      <a href="{% url 'iniciacoes:criar_iniciacao' %}" class="btn btn-primary">Nova Iniciação</a>
      <a href="{% url 'iniciacoes:listar_graus' %}" class="btn btn-info">Gerenciar Graus</a>
    </div>
  
    <div class="card mb-4">
      <div class="card-header">
        <h5>Filtros</h5>
      </div>
      <div class="card-body">
        <form method="get" class="row g-3">
          <div class="col-md-4">
            <label for="aluno" class="form-label">Aluno</label>
            <select name="aluno" id="aluno" class="form-select">
              <option value="">Todos</option>
              {% for aluno in alunos %}
                <option value="{{ aluno.id }}" {% if request.GET.aluno == aluno.id|stringformat:"i" %}selected{% endif %}>
                  {{ aluno.nome }}
                </option>
              {% endfor %}
            </select>
          </div>
          <div class="col-md-4">
            <label for="grau" class="form-label">Grau</label>
            <select name="grau" id="grau" class="form-select">
              <option value="">Todos</option>
              {% for grau in graus %}
                <option value="{{ grau.id }}" {% if request.GET.grau == grau.id|stringformat:"i" %}selected{% endif %}>
                  {{ grau.nome }}
                </option>
              {% endfor %}
            </select>
          </div>
          <div class="col-md-4">
            <label for="data" class="form-label">Data</label>
            <input type="date" name="data" id="data" class="form-control" value="{{ request.GET.data }}">
          </div>
          <div class="col-12 mt-3">
            <button type="submit" class="btn btn-primary">Filtrar</button>
            <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Limpar Filtros</a>
          </div>
        </form>
      </div>
    </div>
  
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Aluno</th>
          <th>Grau</th>
          <th>Data</th>
          <th>Local</th>
          <th>Status</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        {% for iniciacao in iniciacoes %}
        <tr>
          <td>{{ iniciacao.aluno.nome }}</td>
          <td>{{ iniciacao.grau.nome }}</td>
          <td>{{ iniciacao.data|date:"d/m/Y" }}</td>
          <td>{{ iniciacao.local }}</td>
          <td>
            {% if iniciacao.concluida %}
              <span class="badge bg-success">Concluída</span>
            {% else %}
              <span class="badge bg-warning">Pendente</span>
            {% endif %}
          </td>
          <td>
            <a href="{% url 'iniciacoes:detalhar_iniciacao' iniciacao.id %}" class="btn btn-sm btn-info">Detalhes</a>
            <a href="{% url 'iniciacoes:editar_iniciacao' iniciacao.id %}" class="btn btn-sm btn-warning">Editar</a>
            <a href="{% url 'iniciacoes:excluir_iniciacao' iniciacao.id %}" class="btn btn-sm btn-danger">Excluir</a>
          </td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="6">Nenhuma iniciação encontrada.</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  
    {% if iniciacoes.has_other_pages %}
    <nav aria-label="Paginação">
      <ul class="pagination justify-content-center">
        {% if iniciacoes.has_previous %}
          <li class="page-item">
            <a class="page-link" href="?page=1{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Primeira">
              <span aria-hidden="true">««</span>
            </a>
          </li>
          <li class="page-item">
            <a class="page-link" href="?page={{ iniciacoes.previous_page_number }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Anterior">
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
      
        {% for i in iniciacoes.paginator.page_range %}
          {% if iniciacoes.number == i %}
            <li class="page-item active"><a class="page-link" href="#">{{ i }}</a></li>
          {% elif i > iniciacoes.number|add:'-3' and i < iniciacoes.number|add:'3' %}
            <li class="page-item">
              <a class="page-link" href="?page={{ i }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}">{{ i }}</a>
            </li>
          {% endif %}
        {% endfor %}
      
        {% if iniciacoes.has_next %}
          <li class="page-item">
            <a class="page-link" href="?page={{ iniciacoes.next_page_number }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Próxima">
              <span aria-hidden="true">»</span>
            </a>
          </li>
          <li class="page-item">
            <a class="page-link" href="?page={{ iniciacoes.paginator.num_pages }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Última">
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



