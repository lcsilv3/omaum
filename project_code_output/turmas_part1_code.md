# Código da Funcionalidade: turmas - Parte 1/3
*Gerado automaticamente*



## turmas\admin.py

python
from django.contrib import admin
from .models import Turma, Matricula

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'curso', 'data_inicio', 'data_fim', 'status', 'capacidade']
    list_filter = ['status', 'curso']
    search_fields = ['nome', 'curso__nome']
    date_hierarchy = 'data_inicio'

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'turma', 'data_matricula']
    list_filter = ['data_matricula']
    search_fields = ['aluno__nome', 'turma__nome']
    date_hierarchy = 'data_matricula'





## turmas\apps.py

python
from django.apps import AppConfig


class TurmasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'turmas'





## turmas\forms.py

python
from django import forms
from .models import Turma, Matricula  # Importe os modelos necessários

def get_matricula_model():
    """Obtém o modelo Matricula dinamicamente."""
    turmas_module = import_module('turmas.models')
    return getattr(turmas_module, 'Matricula')

def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    turmas_module = import_module('turmas.models')
    return getattr(turmas_module, 'Turma')

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_curso_model():
    cursos_module = import_module('cursos.models')
    return getattr(cursos_module, 'Curso')
class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'curso', 'data_inicio', 'data_fim', 'capacidade', 'status', 'descricao']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['curso'].queryset = get_curso_model().objects.all()

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_inicio >= data_fim:
            raise forms.ValidationError("A data de início deve ser anterior à data de fim.")
        return cleaned_data

class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula  # or get_matricula_model() if you're using dynamic imports
        fields = ['aluno', 'turma']  # Make sure 'data_matricula' is NOT in this list
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            # Make sure there's NO line for 'data_matricula' here
        }

    def __init__(self, *args, **kwargs):
        turma = kwargs.pop('turma', None)
        super().__init__(*args, **kwargs)

        if turma:
            # Filtra alunos pelo curso da turma
            self.fields['aluno'].queryset = get_aluno_model().objects.filter(curso=turma.curso)
            self.fields['aluno'].queryset = self.fields['aluno'].queryset.filter(curso=turma.curso)




## turmas\models.py

python
from django.db import models
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_curso_model():
    cursos_module = import_module('cursos.models')
    return getattr(cursos_module, 'Curso')

class Turma(models.Model):
    OPCOES_STATUS = [
        ('A', 'Ativa'),
        ('I', 'Inativa'),
        ('C', 'Concluída'),
    ]
    
    nome = models.CharField('Nome', max_length=100)
    curso = models.ForeignKey(
        'cursos.Curso',
        on_delete=models.CASCADE,
        verbose_name='Curso',
        to_field='codigo_curso'  # Especificar que estamos referenciando o campo codigo_curso
    )
    data_inicio = models.DateField('Data de Início')
    data_fim = models.DateField('Data de Fim')
    status = models.CharField('Status', max_length=1, choices=OPCOES_STATUS, default='A')
    capacidade = models.PositiveIntegerField('Capacidade de Alunos', default=30)
    descricao = models.TextField('Descrição', blank=True)
    
    def __str__(self):
        return f"{self.nome} - {self.curso}"
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
    
    def clean(self):
        if self.data_fim and self.data_inicio and self.data_fim < self.data_inicio:
            raise ValidationError({'data_fim': 'A data de término deve ser posterior à data de início.'})
        
        # Atualiza status automaticamente com base nas datas
        hoje = timezone.now().date()
        if self.status == 'A' and self.data_fim < hoje:
            self.status = 'C'  # Marca como concluída se a data final já passou
    
    @property
    def alunos_matriculados(self):
        return self.matriculas.count()
    
    @property
    def vagas_disponiveis(self):
        return self.capacidade - self.alunos_matriculados
    
    def tem_alunos(self):
        """Verifica se a turma tem pelo menos um aluno matriculado"""
        return self.alunos_matriculados > 0
    
    def save(self, *args, **kwargs):
        # Se for uma turma nova, permitimos salvar sem alunos inicialmente
        if not self.pk:
            super().save(*args, **kwargs)
        else:
            # Para turmas existentes, verificamos se há pelo menos um aluno
            if not self.tem_alunos():
                raise ValidationError("Uma turma deve ter pelo menos um aluno matriculado.")
            super().save(*args, **kwargs)


class Matricula(models.Model):
    OPCOES_STATUS = [
        ('A', 'Ativa'),
        ('C', 'Cancelada'),
        ('F', 'Finalizada'),
    ]
    
    aluno = models.ForeignKey('alunos.Aluno', on_delete=models.CASCADE, verbose_name='Aluno')
    turma = models.ForeignKey('turmas.Turma', on_delete=models.CASCADE, verbose_name='Turma')
    data_matricula = models.DateField(verbose_name='Data da Matrícula')
    ativa = models.BooleanField(default=True, verbose_name='Matrícula Ativa')
    
    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        ordering = ['-data_matricula']
        unique_together = ['aluno', 'turma']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.turma.nome}"
    
    def clean(self):
        # Check if class is active
        if self.turma.status != 'A':
            raise ValidationError({'turma': _('Não é possível matricular em uma turma inativa ou concluída.')})
        
        # Check if there are available spots
        if not self.pk and self.turma.vagas_disponiveis <= 0:  # Only for new enrollments
            raise ValidationError({'turma': _('Não há vagas disponíveis nesta turma.')})
        
        # Check if student's course matches the class's course
        if self.aluno.curso != self.turma.curso:
            raise ValidationError({'aluno': _('O aluno deve pertencer ao mesmo curso da turma.')})




## turmas\tests.py

python
from django.test import TestCase

# Create your tests here.





## turmas\urls.py

python
from django.urls import path
from . import views

app_name = 'turmas'

urlpatterns = [
    path('', views.listar_turmas, name='listar_turmas'),
    path('criar/', views.criar_turma, name='criar_turma'),
    path('<int:id>/', views.detalhar_turma, name='detalhar_turma'),
    path('<int:id>/editar/', views.editar_turma, name='editar_turma'),
    path('<int:id>/excluir/', views.excluir_turma, name='excluir_turma'),
    path('<int:turma_id>/matricular/', views.matricular_aluno, name='matricular_aluno'),
    path('<int:turma_id>/alunos/', views.listar_alunos_matriculados, name='listar_alunos_matriculados'),
    path('<int:turma_id>/alunos/<int:aluno_id>/cancelar/', views.cancelar_matricula, name='cancelar_matricula'),
]





## turmas\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from importlib import import_module
from .models import Turma, Matricula
from .forms import TurmaForm, MatriculaForm

# Função para importar dinamicamente o modelo Aluno
def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')
@login_required
def listar_turmas(request):
    query = request.GET.get('q')
    curso_id = request.GET.get('curso')
    status = request.GET.get('status')

    turmas = Turma.objects.all().select_related('curso')

    if query:
        turmas = turmas.filter(
            Q(nome__icontains=query) | 
            Q(curso__nome__icontains=query)
        )

    if curso_id:
        turmas = turmas.filter(curso_id=curso_id)

    if status:
        turmas = turmas.filter(status=status)

    # Obtém todos os cursos para o filtro dropdown
    Curso = import_module('cursos.models').Curso
    cursos = Curso.objects.all()

    paginator = Paginator(turmas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'turmas': page_obj,
        'query': query,
        'cursos': cursos,
        'curso_selecionado': curso_id,
        'opcoes_status': Turma.OPCOES_STATUS,
        'status_selecionado': status
    }

    return render(request, 'turmas/listar_turmas.html', context)

@login_required
def criar_turma(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            turma = form.save()
            messages.success(request, 'Turma criada com sucesso!')
            return redirect('turmas:listar_turmas')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = TurmaForm()

    return render(request, 'turmas/criar_turma.html', {'form': form})

@login_required
def detalhar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    matriculas = Matricula.objects.filter(turma=turma).select_related('aluno')

    context = {
        'turma': turma,
        'matriculas': matriculas,
        'total_matriculas': matriculas.count(),
        'vagas_disponiveis': turma.capacidade - matriculas.count()
    }

    return render(request, 'turmas/detalhar_turma.html', context)

@login_required
def editar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma atualizada com sucesso!')
            return redirect('turmas:listar_turmas')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'turmas/editar_turma.html', {'form': form, 'turma': turma})

@login_required
def excluir_turma(request, id):
    turma = get_object_or_404(Turma, id=id)

    if request.method == 'POST':
        if turma.matriculas.exists():
            messages.error(request, 'Não é possível excluir uma turma com alunos matriculados.')
            return redirect('turmas:detalhar_turma', id=turma.id)

        turma.delete()
        messages.success(request, 'Turma excluída com sucesso!')
        return redirect('turmas:listar_turmas')

    return render(request, 'turmas/excluir_turma.html', {'turma': turma})

@login_required
def matricular_aluno(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    Aluno = get_aluno_model()

    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            aluno = form.cleaned_data['aluno']
            if Matricula.objects.filter(turma=turma, aluno=aluno).exists():
                messages.error(request, 'Este aluno já está matriculado nesta turma.')
            else:
                Matricula.objects.create(turma=turma, aluno=aluno)
                messages.success(request, 'Aluno matriculado com sucesso!')
            return redirect('turmas:detalhar_turma', id=turma.id)
    else:
        form = MatriculaForm()

    context = {
        'form': form,
        'turma': turma,
    }
    return render(request, 'turmas/matricular_aluno.html', context)

@login_required
def cancelar_matricula(request, turma_id, aluno_id):
    matricula = get_object_or_404(Matricula, turma_id=turma_id, aluno_id=aluno_id)

    if request.method == 'POST':
        matricula.delete()
        messages.success(request, 'Matrícula cancelada com sucesso!')
        return redirect('turmas:detalhar_turma', id=turma_id)

    return render(request, 'turmas/cancelar_matricula.html', {'matricula': matricula})

@login_required
def listar_alunos_matriculados(request, turma_id):
    """Lista todos os alunos matriculados em uma turma"""
    turma = get_object_or_404(Turma, pk=turma_id)
    alunos = turma.alunos.all()
    
    return render(request, 'turmas/listar_alunos_matriculados.html', {
        'turma': turma,
        'alunos': alunos,
        'titulo': f'Alunos Matriculados na Turma: {turma.nome}'
    })

# Views para Cursos (mantidas para compatibilidade)
def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'turmas/listar_cursos.html', {'cursos': cursos})

def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso criado com sucesso!')
            return redirect('turmas:listar_cursos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CursoForm()
    return render(request, 'turmas/criar_curso.html', {'form': form})

def detalhar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    return render(request, 'turmas/detalhar_curso.html', {'curso': curso})

def editar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso atualizado com sucesso!')
            return redirect('turmas:listar_cursos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'turmas/editar_curso.html', {'form': form, 'curso': curso})

def excluir_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso excluído com sucesso!')
        return redirect('turmas:listar_cursos')
    return render(request, 'turmas/excluir_curso.html', {'curso': curso})




## turmas\migrations\0001_initial.py

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
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('data_inicio', models.DateField(verbose_name='Data de Início')),
                ('data_fim', models.DateField(verbose_name='Data de Fim')),
                ('status', models.CharField(choices=[('A', 'Ativa'), ('I', 'Inativa'), ('C', 'Concluída')], default='A', max_length=1, verbose_name='Status')),
                ('capacidade', models.PositiveIntegerField(default=30, verbose_name='Capacidade de Alunos')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso', verbose_name='Curso')),
            ],
            options={
                'verbose_name': 'Turma',
                'verbose_name_plural': 'Turmas',
            },
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_matricula', models.DateField(verbose_name='Data da Matrícula')),
                ('ativa', models.BooleanField(default=True, verbose_name='Matrícula Ativa')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alunos.aluno', verbose_name='Aluno')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turmas.turma', verbose_name='Turma')),
            ],
            options={
                'verbose_name': 'Matrícula',
                'verbose_name_plural': 'Matrículas',
                'ordering': ['-data_matricula'],
                'unique_together': {('aluno', 'turma')},
            },
        ),
    ]





## turmas\templates\turmas\cancelar_matricula.html

html
{% extends 'base.html' %}

{% block title %}Cancelar Matrícula{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Cancelar Matrícula</h1>
    
    {% if ultima_matricula %}
        <div class="alert alert-danger">
            <p>Não é possível cancelar esta matrícula porque é a única matrícula ativa na turma.</p>
            <p>Uma turma deve ter pelo menos um aluno matriculado.</p>
        </div>
        <a href="{% url 'turmas:detalhar_turma' matricula.turma.id %}" class="btn btn-primary">Voltar para Detalhes da Turma</a>
    {% else %}
        <div class="alert alert-warning">
            <p>Você tem certeza que deseja cancelar a matrícula de "{{ matricula.aluno.nome }}" na turma "{{ matricula.turma.nome }}"?</p>
        </div>
        
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger">Confirmar Cancelamento</button>
            <a href="{% url 'turmas:detalhar_turma' matricula.turma.id %}" class="btn btn-secondary">Cancelar</a>
        </form>
    {% endif %}
</div>
{% endblock %}





## turmas\templates\turmas\confirmar_cancelamento_matricula.html

html
{% extends 'core/base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="card">
        <div class="card-header bg-danger text-white">
            <h4>Confirmar Cancelamento de Matrícula</h4>
        </div>
        <div class="card-body">
            <p class="lead">Você tem certeza que deseja cancelar a matrícula do aluno <strong>{{ aluno.nome }}</strong> na turma <strong>{{ turma.nome }}</strong>?</p>
            <p>Esta ação não poderá ser desfeita.</p>
            
            <div class="mt-4">
                <form method="post">
                    {% csrf_token %}
                    <div class="d-flex justify-content-between">
                        <a href="{% url 'turmas:listar_alunos_matriculados' turma.id %}" class="btn btn-secondary">Cancelar</a>
                        <button type="submit" class="btn btn-danger">Confirmar Cancelamento</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
    <a href="javascript:history.back()" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}



