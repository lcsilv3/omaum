# Código da Funcionalidade: turmas
*Gerado automaticamente*



## turmas\admin.py

python
from django.contrib import admin
from .models import Turma

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome']  # Ajuste conforme os campos do seu modelo




## turmas\apps.py

python
from django.apps import AppConfig


class TurmasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'turmas'




## turmas\forms.py

python
from django import forms
from .models import Turma
from cursos.models import Curso
from django.core.exceptions import ValidationError

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'curso', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise ValidationError("O nome da turma deve ter pelo menos 3 caracteres.")
        return nome

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_inicio >= data_fim:
            raise ValidationError("A data de início deve ser anterior à data de fim.")
        return cleaned_data

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'descricao', 'duracao']

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise ValidationError("O nome do curso deve ter pelo menos 3 caracteres.")
        return nome



## turmas\models.py

python
from django.db import models
from cursos.models import Curso

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return f"{self.nome} - {self.curso}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"



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
    # URLs para Cursos
    path('cursos/', views.listar_cursos, name='listar_cursos'),
    path('cursos/criar/', views.criar_curso, name='criar_curso'),
    path('cursos/<int:id>/editar/', views.editar_curso, name='editar_curso'),
    path('cursos/<int:id>/excluir/', views.excluir_curso, name='excluir_curso'),
    path('cursos/<int:id>/', views.detalhar_curso, name='detalhar_curso'),
    
    # URLs para Turmas
    path('', views.listar_turmas, name='listar_turmas'),
    path('criar/', views.criar_turma, name='criar_turma'),
    path('<int:id>/editar/', views.editar_turma, name='editar_turma'),
    path('<int:id>/excluir/', views.excluir_turma, name='excluir_turma'),
    path('<int:id>/', views.detalhar_turma, name='detalhar_turma'),
]



## turmas\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Turma
from cursos.models import Curso
from .forms import TurmaForm, CursoForm

# Views para Turmas
def listar_turmas(request):
    turmas = Turma.objects.all()
    return render(request, 'turmas/listar_turmas.html', {'turmas': turmas})

def criar_turma(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma criada com sucesso!')
            return redirect('turmas:listar_turmas')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = TurmaForm()
    return render(request, 'turmas/criar_turma.html', {'form': form})

def detalhar_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    return render(request, 'turmas/detalhar_turma.html', {'turma': turma})

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

def excluir_turma(request, id):
    turma = get_object_or_404(Turma, id=id)
    if request.method == 'POST':
        turma.delete()
        messages.success(request, 'Turma excluída com sucesso!')
        return redirect('turmas:listar_turmas')
    return render(request, 'turmas/excluir_turma.html', {'turma': turma})

# Views para Cursos
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
# Generated by Django 5.1.7 on 2025-03-16 21:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alunos', '__first__'),
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True)),
                ('alunos', models.ManyToManyField(blank=True, to='alunos.aluno')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
            ],
        ),
    ]




## turmas\migrations\0002_curso_alter_turma_options_remove_turma_alunos_and_more.py

python
# Generated by Django 5.1.7 on 2025-03-16 23:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turmas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('codigo_curso', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Código do Curso')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.TextField(verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
            },
        ),
        migrations.AlterModelOptions(
            name='turma',
            options={'verbose_name': 'Turma', 'verbose_name_plural': 'Turmas'},
        ),
        migrations.RemoveField(
            model_name='turma',
            name='alunos',
        ),
        migrations.RemoveField(
            model_name='turma',
            name='descricao',
        ),
        migrations.AlterField(
            model_name='turma',
            name='data_fim',
            field=models.DateField(verbose_name='Data de Fim'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='data_inicio',
            field=models.DateField(verbose_name='Data de Início'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='nome',
            field=models.CharField(max_length=100, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turmas.curso', verbose_name='Curso'),
        ),
    ]




## turmas\migrations\0003_alter_turma_curso_alter_turma_data_fim_and_more.py

python
# Generated by Django 5.1.7 on 2025-03-17 03:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0003_curso_descricao_curso_duracao'),
        ('turmas', '0002_curso_alter_turma_options_remove_turma_alunos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='data_fim',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='turma',
            name='data_inicio',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='turma',
            name='nome',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Curso',
        ),
    ]




## turmas\templates\turmas\criar_turma.html

html
{% extends 'base.html' %}

{% block title %}Criar Turma{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Criar Nova Turma</h1>
    
    <form method="post">
        {% csrf_token %}
        
        {% if form.non_field_errors %}
            <div class="alert alert-danger">
                {% for error in form.non_field_errors %}
                    {{ error }}
                {% endfor %}
            </div>
        {% endif %}
        
        {% for field in form %}
            <div class="form-group mb-3">
                <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                {{ field }}
                {% if field.errors %}
                    <div class="alert alert-danger mt-1">
                        {% for error in field.errors %}
                            {{ error }}
                        {% endfor %}
                    </div>
                {% endif %}
                {% if field.help_text %}
                    <small class="form-text text-muted">{{ field.help_text }}</small>
                {% endif %}
            </div>
        {% endfor %}
        
        <button type="submit" class="btn btn-primary">Salvar</button>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




## turmas\templates\turmas\detalhes_turma.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}




## turmas\templates\turmas\editar_turma.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Turma</h1>
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        <button type="submit" class="btn btn-primary">Atualizar Turma</button>
        <a href="{% url 'listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}



## turmas\templates\turmas\listar_turmas.html

html
{% extends 'base.html' %}

{% block title %}Lista de Turmas{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Lista de Turmas</h1>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <a href="{% url 'turmas:criar_turma' %}" class="btn btn-primary mb-3">
        <i class="fas fa-plus"></i> Nova Turma
    </a>
    
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Curso</th>
                <th>Data de Início</th>
                <th>Data de Fim</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for turma in turmas %}
            <tr>
                <td>{{ turma.nome }}</td>
                <td>{{ turma.curso }}</td>
                <td>{{ turma.data_inicio|date:"d/m/Y" }}</td>
                <td>{{ turma.data_fim|date:"d/m/Y" }}</td>
                <td>
                    <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-sm btn-info">Detalhes</a>
                    <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-sm btn-warning">Editar</a>
                    <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-sm btn-danger">Excluir</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5" class="text-center">Nenhuma turma encontrada.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}




## turmas\templates\turmas\turma_form.html

html
{% extends 'base.html' %}

{% block content %}
  <h1>Criar Turma</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Criar</button>
  </form>
{% endblock %}



## turmas\tests\test_models.py

python
from django.test import TestCase
from turmas.models import Turma
from cursos.models import Curso
from datetime import date

class TurmaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )

    def test_criar_turma(self):
        turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 10, 1),
            data_fim=date(2023, 12, 31)
        )

        self.assertEqual(turma.nome, 'Turma de Teste')
        self.assertEqual(turma.curso, self.curso)
        self.assertEqual(str(turma), 'Turma de Teste - Curso de Teste')

class CargoAdministrativoTest(TestCase):
    def test_criar_cargo(self):
        cargo = CargoAdministrativo.objects.create(
            codigo_cargo='CARGO001',
            nome='Coordenador',
            descricao='Responsável pela coordenação do curso.'
        )
        self.assertEqual(cargo.nome, 'Coordenador')
        self.assertEqual(cargo.codigo_cargo, 'CARGO001')



## turmas\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from turmas.models import Turma
from cursos.models import Curso
from datetime import date

class TurmaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 10, 1),
            data_fim=date(2023, 12, 31)
        )

    def test_listar_turmas(self):
        response = self.client.get(reverse('turmas:turma_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Turma de Teste')
        self.assertContains(response, 'Curso de Teste')

    def test_criar_turma(self):
        response = self.client.post(reverse('turmas:turma_create'), {
            'nome': 'Nova Turma',
            'curso': self.curso.id,
            'data_inicio': '2024-01-01',
            'data_fim': '2024-03-31'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Turma.objects.filter(nome='Nova Turma').exists())

    def test_atualizar_turma(self):
        response = self.client.post(reverse('turmas:turma_update', args=[self.turma.id]), {
            'nome': 'Turma Atualizada',
            'curso': self.curso.id,
            'data_inicio': '2023-11-01',
            'data_fim': '2024-01-31'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.turma.refresh_from_db()
        self.assertEqual(self.turma.nome, 'Turma Atualizada')

    def test_deletar_turma(self):
        response = self.client.post(reverse('turmas:turma_delete', args=[self.turma.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Turma.objects.filter(id=self.turma.id).exists())

class CursoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )

    def test_listar_cursos(self):
        response = self.client.get(reverse('turmas:curso_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Curso de Teste')

    def test_criar_curso(self):
        response = self.client.post(reverse('turmas:curso_create'), {
            'nome': 'Novo Curso',
            'descricao': 'Descrição do novo curso'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Curso.objects.filter(nome='Novo Curso').exists())

    def test_atualizar_curso(self):
        response = self.client.post(reverse('turmas:curso_update', args=[self.curso.id]), {
            'nome': 'Curso Atualizado',
            'descricao': 'Descrição atualizada'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.curso.refresh_from_db()
        self.assertEqual(self.curso.nome, 'Curso Atualizado')

    def test_deletar_curso(self):
        response = self.client.post(reverse('turmas:curso_delete', args=[self.curso.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Curso.objects.filter(id=self.curso.id).exists())


