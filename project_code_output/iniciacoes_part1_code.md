# Código da Funcionalidade: iniciacoes - Parte 1/3
*Gerado automaticamente*



## iniciacoes\admin.py

python
from django.contrib import admin
from .models import Iniciacao

@admin.register(Iniciacao)
class IniciacaoAdmin(admin.ModelAdmin):
    # Adjust list_display and list_filter to use fields that actually exist
    # Remove 'data' since it doesn't exist in the model
    list_display = ['aluno']  # Keep only fields that exist
    list_filter = []  # Remove 'data' since it doesn't exist
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
        # Remova 'nome' da lista de campos
        fields = ['aluno', 'curso', 'data_iniciacao', 'grau', 'observacoes']
        widgets = {
            'data_iniciacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'grau': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'aluno': 'Aluno',
            'curso': 'Curso',
            'data_iniciacao': 'Data de Iniciação',
            'grau': 'Grau',
            'observacoes': 'Observações'
        }
        help_texts = {
            'curso': 'Selecione o curso de iniciação',
            'data_iniciacao': 'Selecione a data em que o aluno foi iniciado no curso'
        }

    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        curso = cleaned_data.get('curso')
        data_iniciacao = cleaned_data.get('data_iniciacao')
        
        # Verifica se já existe uma iniciação para este aluno neste curso
        if aluno and curso:
            # Exclui a instância atual em caso de edição
            instance_id = self.instance.id if self.instance else None
            
            # Verifica se já existe outra iniciação com o mesmo aluno e curso
            if Iniciacao.objects.filter(
                aluno=aluno, 
                curso=curso
            ).exclude(id=instance_id).exists():
                raise ValidationError(
                    f"O aluno {aluno.nome} já possui uma iniciação no curso {curso.nome}."
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
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_curso_model():
    cursos_module = import_module('cursos.models')
    return getattr(cursos_module, 'Curso')

class Iniciacao(models.Model):
    aluno = models.ForeignKey(
        get_aluno_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Aluno',
        to_field='cpf'  # Especificar que estamos referenciando o campo cpf
    )
    curso = models.ForeignKey(
        get_curso_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Curso'
    )
    data_iniciacao = models.DateField(verbose_name='Data da Iniciação')
    grau = models.CharField(max_length=50, verbose_name='Grau')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.curso.nome} - {self.grau}"
    
    class Meta:
        verbose_name = 'Iniciação'
        verbose_name_plural = 'Iniciações'
        ordering = ['-data_iniciacao']
        unique_together = ['aluno', 'curso', 'grau']





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
def detalhar_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    return render(request, 'iniciacoes/detalhar_iniciacao.html', {'iniciacao': iniciacao})


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

@login_required
def listar_graus(request):
    """Lista todos os graus de iniciação."""
    graus = GrauIniciacao.objects.all()
    return render(request, 'iniciacoes/listar_graus.html', {'graus': graus})

@login_required
def criar_grau(request):
    """Cria um novo grau de iniciação."""
    if request.method == 'POST':
        form = GrauIniciacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grau de iniciação criado com sucesso!')
            return redirect('iniciacoes:listar_graus')
    else:
        form = GrauIniciacaoForm()
    return render(request, 'iniciacoes/criar_grau.html', {'form': form})

@login_required
def editar_grau(request, id):
    """Edita um grau de iniciação existente."""
    grau = get_object_or_404(GrauIniciacao, id=id)
    if request.method == 'POST':
        form = GrauIniciacaoForm(request.POST, instance=grau)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grau de iniciação atualizado com sucesso!')
            return redirect('iniciacoes:listar_graus')
    else:
        form = GrauIniciacaoForm(instance=grau)
    return render(request, 'iniciacoes/editar_grau.html', {'form': form, 'grau': grau})

@login_required
def excluir_grau(request, id):
    """Exclui um grau de iniciação."""
    grau = get_object_or_404(GrauIniciacao, id=id)
    if request.method == 'POST':
        grau.delete()
        messages.success(request, 'Grau de iniciação excluído com sucesso!')
        return redirect('iniciacoes:listar_graus')
    return render(request, 'iniciacoes/excluir_grau.html', {'grau': grau})





## iniciacoes\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-04-03 20:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alunos', '0001_initial'),
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iniciacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_iniciacao', models.DateField(verbose_name='Data da Iniciação')),
                ('grau', models.CharField(max_length=50, verbose_name='Grau')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alunos.aluno', verbose_name='Aluno')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso', verbose_name='Curso')),
            ],
            options={
                'verbose_name': 'Iniciação',
                'verbose_name_plural': 'Iniciações',
                'ordering': ['-data_iniciacao'],
                'unique_together': {('aluno', 'curso', 'grau')},
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



