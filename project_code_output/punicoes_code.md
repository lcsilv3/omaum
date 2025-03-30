# Código da Funcionalidade: punicoes
*Gerado automaticamente*



## punicoes\admin.py

python
from django.contrib import admin
from .models import Punicao, TipoPunicao

@admin.register(Punicao)
class PunicaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'tipo_punicao', 'data_aplicacao', 'status')
    list_filter = ('tipo_punicao', 'status', 'data_aplicacao')
    search_fields = ('aluno__nome', 'descricao')
    date_hierarchy = 'data_aplicacao'

@admin.register(TipoPunicao)
class TipoPunicaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'gravidade')
    list_filter = ('gravidade',)
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
import importlib

# Importando modelos usando importlib para evitar importações circulares
def get_model(app_name, model_name):
    module = importlib.import_module(f"{app_name}.models")
    return getattr(module, model_name)

class PunicaoForm(forms.ModelForm):
    class Meta:
        model = get_model('punicoes', 'Punicao')
        fields = ['aluno', 'tipo_punicao', 'descricao', 'data_aplicacao', 'data_termino', 'status', 'observacoes']
        widgets = {
            'data_aplicacao': forms.DateInput(attrs={'type': 'date'}),
            'data_termino': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
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
from django.utils import timezone
import importlib

# Importando modelos usando importlib para evitar importações circulares
def get_model(app_name, model_name):
    module = importlib.import_module(f"{app_name}.models")
    return getattr(module, model_name)

class TipoPunicao(models.Model):
    GRAVIDADE_CHOICES = [
        ('leve', 'Leve'),
        ('media', 'Média'),
        ('grave', 'Grave'),
        ('gravissima', 'Gravíssima'),
    ]
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    gravidade = models.CharField(max_length=20, choices=GRAVIDADE_CHOICES, default='media')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Tipo de Punição'
        verbose_name_plural = 'Tipos de Punição'
        ordering = ['nome']

class Punicao(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    aluno = models.ForeignKey('alunos.Aluno', on_delete=models.CASCADE, related_name='punicoes')
    tipo_punicao = models.ForeignKey(TipoPunicao, on_delete=models.PROTECT, related_name='punicoes')
    descricao = models.TextField()
    data_aplicacao = models.DateField()
    data_termino = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True, null=True)
    
    # Campos de auditoria
    registrado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='punicoes_registradas')
    data_registro = models.DateTimeField(default=timezone.now)
    atualizado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='punicoes_atualizadas', null=True, blank=True)
    data_atualizacao = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Atualiza a data de atualização quando o objeto é modificado
        if self.pk:
            self.data_atualizacao = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Punição de {self.aluno.nome} - {self.tipo_punicao.nome}"
    
    class Meta:
        verbose_name = 'Punição'
        verbose_name_plural = 'Punições'
        ordering = ['-data_aplicacao']





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
def editar_punicao(request, id):
    Punicao = get_model('punicoes', 'Punicao')
    PunicaoForm = get_form('punicoes', 'PunicaoForm')
    
    punicao = get_object_or_404(Punicao, id=id)
    
    if request.method == 'POST':
        form = PunicaoForm(request.POST, instance=punicao)
        if form.is_valid():
            punicao = form.save(commit=False)
            punicao.atualizado_por = request.user
            punicao.save()
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
# Generated by Django 5.1.7 on 2025-03-27 11:39

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
            name='Punicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField()),
                ('data', models.DateField()),
                ('tipo_punicao', models.CharField(max_length=50)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('data_registro', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='punicoes', to='alunos.aluno')),
                ('registrado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-data'],
                'permissions': [('gerar_relatorio_punicao', 'Pode gerar relatório de punições')],
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





## punicoes\templates\punicoes\detalhar_punicao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes da Punição</h1>
  
  <div class="card">
    <div class="card-header">
      <h2>Punição de {{ punicao.aluno.nome }}</h2>
    </div>
    <div class="card-body">
      <p><strong>Aluno:</strong> {{ punicao.aluno.nome }}</p>
      <p><strong>Tipo de Punição:</strong> {{ punicao.tipo_punicao.nome }}</p>
      <p><strong>Gravidade:</strong> {{ punicao.tipo_punicao.get_gravidade_display }}</p>
      <p><strong>Data de Aplicação:</strong> {{ punicao.data_aplicacao|date:"d/m/Y" }}</p>
      {% if punicao.data_termino %}
        <p><strong>Data de Término:</strong> {{ punicao.data_termino|date:"d/m/Y" }}</p>
      {% endif %}
      <p>
        <strong>Status:</strong> 
        {% if punicao.status == 'pendente' %}
          <span class="badge bg-warning">Pendente</span>
        {% elif punicao.status == 'em_andamento' %}
          <span class="badge bg-primary">Em Andamento</span>
        {% elif punicao.status == 'concluida' %}
          <span class="badge bg-success">Concluída</span>
        {% elif punicao.status == 'cancelada' %}
          <span class="badge bg-secondary">Cancelada</span>
        {% endif %}
      </p>
      <p><strong>Descrição:</strong> {{ punicao.descricao }}</p>
      {% if punicao.observacoes %}
        <p><strong>Observações:</strong> {{ punicao.observacoes }}</p>
      {% endif %}
      <p><strong>Registrado por:</strong> {{ punicao.registrado_por.username }}</p>
      <p><strong>Data de registro:</strong> {{ punicao.data_registro|date:"d/m/Y H:i" }}</p>
      {% if punicao.atualizado_por %}
        <p><strong>Atualizado por:</strong> {{ punicao.atualizado_por.username }}</p>
        <p><strong>Data de atualização:</strong> {{ punicao.data_atualizacao|date:"d/m/Y H:i" }}</p>
      {% endif %}
    </div>
    <div class="card-footer">
      <a href="{% url 'punicoes:editar_punicao' punicao.id %}" class="btn btn-warning">Editar</a>
      <a href="{% url 'punicoes:excluir_punicao' punicao.id %}" class="btn btn-danger">Excluir</a>
      <a href="{% url 'punicoes:listar_punicoes' %}" class="btn btn-secondary">Voltar</a>
    </div>
  </div>
</div>
{% endblock %}





## punicoes\templates\punicoes\detalhe_punicao.html

html
{% extends 'core/base.html' %}

{% block content %}
<h1>Detalhes da Punição</h1>
<dl>
    <dt>Aluno:</dt>
    <dd>{{ punicao.aluno.nome }}</dd>
    <dt>Tipo:</dt>
    <dd>{{ punicao.tipo_punicao }}</dd>
    <dt>Data:</dt>
    <dd>{{ punicao.data }}</dd>
    <dt>Descrição:</dt>
    <dd>{{ punicao.descricao }}</dd>
    <dt>Observações:</dt>
    <dd>{{ punicao.observacoes|default:"Nenhuma observação" }}</dd>
</dl>
<a href="{% url 'editar_punicao' punicao.id %}" class="btn btn-warning">Editar</a>
<a href="{% url 'listar_punicoes' %}" class="btn btn-secondary">Voltar</a>
{% endblock %}




## punicoes\templates\punicoes\editar_punicao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Punição</h1>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        
        <button type="submit" class="btn btn-primary">Atualizar Punição</button>
        <a href="{% url 'punicoes:listar_punicoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}





## punicoes\templates\punicoes\editar_tipo_punicao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Editar Tipo de Punição</h1>
  
  <form method="post">
    {% csrf_token %}
    {% include 'includes/form_errors.html' %}
    
    {% for field in form %}
      {% include 'includes/form_field.html' %}
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Atualizar Tipo de Punição</button>
    <a href="{% url 'punicoes:listar_tipos_punicao' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}





## punicoes\templates\punicoes\excluir_punicao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Punição</h1>
  
    <div class="alert alert-danger">
      <p>Tem certeza que deseja excluir a punição de <strong>{{ punicao.aluno.nome }}</strong> do tipo <strong>{{ punicao.tipo_punicao.nome }}</strong> aplicada em <strong>{{ punicao.data_aplicacao|date:"d/m/Y" }}</strong>?</p>
    </div>
  
    <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Sim, excluir</button>
      <a href="{% url 'punicoes:listar_punicoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




## punicoes\templates\punicoes\excluir_tipo_punicao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Excluir Tipo de Punição</h1>
  
  <div class="alert alert-danger">
    <p>Tem certeza que deseja excluir o tipo de punição <strong>{{ tipo_punicao.nome }}</strong>?</p>
    {% if punicoes_associadas %}
      <div class="mt-3">
        <p><strong>Atenção:</strong> Existem {{ punicoes_associadas }} punições associadas a este tipo. A exclusão deste tipo pode afetar esses registros.</p>
      </div>
    {% endif %}
  </div>
  
  <form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Sim, excluir</button>
    <a href="{% url 'punicoes:listar_tipos_punicao' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}





## punicoes\templates\punicoes\listar_punicoes.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Punições</h1>
  
    <div class="d-flex justify-content-between mb-3">
      <a href="{% url 'punicoes:criar_punicao' %}" class="btn btn-primary">Nova Punição</a>
      <a href="{% url 'punicoes:listar_tipos_punicao' %}" class="btn btn-info">Gerenciar Tipos de Punição</a>
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
            <label for="tipo" class="form-label">Tipo de Punição</label>
            <select name="tipo" id="tipo" class="form-select">
              <option value="">Todos</option>
              {% for tipo in tipos_punicao %}
                <option value="{{ tipo.id }}" {% if request.GET.tipo == tipo.id|stringformat:"i" %}selected{% endif %}>
                  {{ tipo.nome }}
                </option>
              {% endfor %}
            </select>
          </div>
          <div class="col-md-4">
            <label for="status" class="form-label">Status</label>
            <select name="status" id="status" class="form-select">
              <option value="">Todos</option>
              <option value="pendente" {% if request.GET.status == 'pendente' %}selected{% endif %}>Pendente</option>
              <option value="em_andamento" {% if request.GET.status == 'em_andamento' %}selected{% endif %}>Em Andamento</option>
              <option value="concluida" {% if request.GET.status == 'concluida' %}selected{% endif %}>Concluída</option>
              <option value="cancelada" {% if request.GET.status == 'cancelada' %}selected{% endif %}>Cancelada</option>
            </select>
          </div>
          <div class="col-12 mt-3">
            <button type="submit" class="btn btn-primary">Filtrar</button>
            <a href="{% url 'punicoes:listar_punicoes' %}" class="btn btn-secondary">Limpar Filtros</a>
          </div>
        </form>
      </div>
    </div>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Aluno</th>
          <th>Tipo de Punição</th>
          <th>Data de Aplicação</th>
          <th>Data de Término</th>
          <th>Status</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        {% for punicao in punicoes %}
        <tr>
          <td>{{ punicao.aluno.nome }}</td>
          <td>{{ punicao.tipo_punicao.nome }}</td>
          <td>{{ punicao.data_aplicacao|date:"d/m/Y" }}</td>
          <td>{{ punicao.data_termino|date:"d/m/Y"|default:"-" }}</td>
          <td>
            {% if punicao.status == 'pendente' %}
              <span class="badge bg-warning">Pendente</span>
            {% elif punicao.status == 'em_andamento' %}
              <span class="badge bg-primary">Em Andamento</span>
            {% elif punicao.status == 'concluida' %}
              <span class="badge bg-success">Concluída</span>
            {% elif punicao.status == 'cancelada' %}
              <span class="badge bg-secondary">Cancelada</span>
            {% endif %}
          </td>
          <td>
            <a href="{% url 'punicoes:detalhar_punicao' punicao.id %}" class="btn btn-sm btn-info">Detalhes</a>
            <a href="{% url 'punicoes:editar_punicao' punicao.id %}" class="btn btn-sm btn-warning">Editar</a>
            <a href="{% url 'punicoes:excluir_punicao' punicao.id %}" class="btn btn-sm btn-danger">Excluir</a>
          </td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="6">Nenhuma punição encontrada.</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  
    {% if punicoes.has_other_pages %}
    <nav aria-label="Paginação">
      <ul class="pagination justify-content-center">
        {% if punicoes.has_previous %}
          <li class="page-item">
            <a class="page-link" href="?page=1{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.tipo %}&tipo={{ request.GET.tipo }}{% endif %}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}" aria-label="Primeira">
              <span aria-hidden="true">««</span>
            </a>
          </li>
          <li class="page-item">
            <a class="page-link" href="?page={{ punicoes.previous_page_number }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.tipo %}&tipo={{ request.GET.tipo }}{% endif %}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}" aria-label="Anterior">
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
        
        {% for i in punicoes.paginator.page_range %}
          {% if punicoes.number == i %}
            <li class="page-item active"><a class="page-link" href="#">{{ i }}</a></li>
          {% elif i > punicoes.number|add:'-3' and i < punicoes.number|add:'3' %}
            <li class="page-item">
              <a class="page-link" href="?page={{ i }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.tipo %}&tipo={{ request.GET.tipo }}{% endif %}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}">{{ i }}</a>
            </li>
          {% endif %}
        {% endfor %}
        
        {% if punicoes.has_next %}
          <li class="page-item">
            <a class="page-link" href="?page={{ punicoes.next_page_number }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.tipo %}&tipo={{ request.GET.tipo }}{% endif %}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}" aria-label="Próxima">
              <span aria-hidden="true">»</span>
            </a>
          </li>
          <li class="page-item">
            <a class="page-link" href="?page={{ punicoes.paginator.num_pages }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.tipo %}&tipo={{ request.GET.tipo }}{% endif %}{% if request.GET.status %}&status={{ request.GET.status }}{% endif %}" aria-label="Última">
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





## punicoes\templates\punicoes\listar_tipos_punicao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Tipos de Punição</h1>
  
  <div class="d-flex justify-content-between mb-3">
    <a href="{% url 'punicoes:criar_tipo_punicao' %}" class="btn btn-primary">Novo Tipo de Punição</a>
    <a href="{% url 'punicoes:listar_punicoes' %}" class="btn btn-secondary">Voltar para Punições</a>
  </div>
  
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Nome</th>
        <th>Descrição</th>
        <th>Gravidade</th>
        <th>Ações</th>
      </tr>
    </thead>
    <tbody>
      {% for tipo in tipos_punicao %}
      <tr>
        <td>{{ tipo.nome }}</td>
        <td>{{ tipo.descricao|truncatechars:50 }}</td>
        <td>
          {% if tipo.gravidade == 'leve' %}
            <span class="badge bg-success">Leve</span>
          {% elif tipo.gravidade == 'media' %}
            <span class="badge bg-warning">Média</span>
          {% elif tipo.gravidade == 'grave' %}
            <span class="badge bg-danger">Grave</span>
          {% elif tipo.gravidade == 'gravissima' %}
            <span class="badge bg-dark">Gravíssima</span>
          {% endif %}
        </td>
        <td>
          <a href="{% url 'punicoes:editar_tipo_punicao' tipo.id %}" class="btn btn-sm btn-warning">Editar</a>
          <a href="{% url 'punicoes:excluir_tipo_punicao' tipo.id %}" class="btn btn-sm btn-danger">Excluir</a>
        </td>
      </tr>
      {% empty %}
      <tr>
        <td colspan="4">Nenhum tipo de punição cadastrado.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}



