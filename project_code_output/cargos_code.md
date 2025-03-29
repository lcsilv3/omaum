# Código da Funcionalidade: cargos
*Gerado automaticamente*



## cargos\admin.py

python
from django.contrib import admin
from .models import CargoAdministrativo

@admin.register(CargoAdministrativo)
class CargoAdministrativoAdmin(admin.ModelAdmin):
    list_display = ['codigo_cargo', 'nome', 'descricao']
    search_fields = ['codigo_cargo', 'nome']
    list_filter = ['codigo_cargo']





## cargos\apps.py

python
from django.apps import AppConfig


class CargosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cargos'





## cargos\forms.py

python
from django import forms
from .models import CargoAdministrativo

class CargoAdministrativoForm(forms.ModelForm):
    """
    Formulário para criação e edição de Cargos Administrativos.
    """
    class Meta:
        model = CargoAdministrativo
        fields = ['codigo_cargo', 'nome', 'descricao']
        widgets = {
            'codigo_cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'codigo_cargo': 'Código do Cargo',
            'nome': 'Nome',
            'descricao': 'Descrição',
        }
        help_texts = {
            'codigo_cargo': 'Código único que identifica o cargo (ex: COORD, DIR, etc.)',
            'nome': 'Nome completo do cargo administrativo',
            'descricao': 'Descrição detalhada das responsabilidades do cargo',
        }
        error_messages = {
            'codigo_cargo': {
                'unique': 'Este código de cargo já está em uso. Por favor, escolha outro.',
                'required': 'O código do cargo é obrigatório.',
                'max_length': 'O código do cargo não pode ter mais de 10 caracteres.',
            },
            'nome': {
                'required': 'O nome do cargo é obrigatório.',
                'max_length': 'O nome do cargo não pode ter mais de 100 caracteres.',
            },
        }

    def clean_codigo_cargo(self):
        """
        Validação personalizada para o campo codigo_cargo.
        Converte o código para maiúsculas e remove espaços extras.
        """
        codigo = self.cleaned_data.get('codigo_cargo')
        if codigo:
            return codigo.upper().strip()
        return codigo

    def clean_nome(self):
        """
        Validação personalizada para o campo nome.
        Capitaliza a primeira letra de cada palavra e remove espaços extras.
        """
        nome = self.cleaned_data.get('nome')
        if nome:
            return ' '.join(word.capitalize() for word in nome.split())
        return nome





## cargos\formulario_cargo.py

python
from django import forms
from .models import CargoAdministrativo

class CargoAdministrativoForm(forms.ModelForm):
    class Meta:
        model = CargoAdministrativo
        fields = ['codigo_cargo', 'nome', 'descricao']
        widgets = {
            'codigo_cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }





## cargos\formulario_cargos.py

python
from django import forms
from .models import CargoAdministrativo

class CargoAdministrativoForm(forms.ModelForm):
    class Meta:
        model = CargoAdministrativo
        fields = ['codigo_cargo', 'nome', 'descricao']
        widgets = {
            'codigo_cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }





## cargos\models.py

python
from django.db import models

class CargoAdministrativo(models.Model):
    """
    Representa um cargo administrativo no sistema. O cargo administrativo possui um código único, 
    um nome e uma descrição opcional.
    """
    codigo_cargo = models.CharField(max_length=10, unique=True, verbose_name="Código do Cargo")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return self.nome
        
    class Meta:
        verbose_name = "Cargo Administrativo"
        verbose_name_plural = "Cargos Administrativos"
        ordering = ['nome']





## cargos\tests.py

python
# Alterar esta linha:
# from .form_cargo import CargoAdministrativoForm
# Para:
from .formulario_cargo import CargoAdministrativoForm





## cargos\urls.py

python
from django.urls import path
from . import views

app_name = 'cargos'

urlpatterns = [
    path('', views.listar_cargos, name='listar_cargos'),
    path('novo/', views.criar_cargo, name='criar_cargo'),
    path('<int:id>/editar/', views.editar_cargo, name='editar_cargo'),
    path('<int:id>/excluir/', views.excluir_cargo, name='excluir_cargo'),
    path('<int:id>/detalhes/', views.detalhes_cargo, name='detalhes_cargo'),
]




## cargos\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CargoAdministrativo
from .formulario_cargo import CargoAdministrativoForm

def listar_cargos(request):
    cargos = CargoAdministrativo.objects.all()
    return render(request, 'cargos/listar_cargos.html', {'cargos': cargos})

def criar_cargo(request):
    if request.method == 'POST':
        form = CargoAdministrativoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo administrativo criado com sucesso!')
            return redirect('cargos:listar_cargos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CargoAdministrativoForm()
    return render(request, 'cargos/criar_cargo.html', {'form': form})

def editar_cargo(request, id):
    cargo = get_object_or_404(CargoAdministrativo, id=id)
    if request.method == 'POST':
        form = CargoAdministrativoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo administrativo atualizado com sucesso!')
            return redirect('cargos:listar_cargos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CargoAdministrativoForm(instance=cargo)
    return render(request, 'cargos/editar_cargo.html', {'form': form, 'cargo': cargo})

def excluir_cargo(request, id):
    cargo = get_object_or_404(CargoAdministrativo, id=id)
    if request.method == 'POST':
        cargo.delete()
        messages.success(request, 'Cargo administrativo excluído com sucesso!')
        return redirect('cargos:listar_cargos')
    return render(request, 'cargos/excluir_cargo.html', {'cargo': cargo})

def detalhes_cargo(request, id):
    cargo = get_object_or_404(CargoAdministrativo, id=id)
    return render(request, 'cargos/detalhes_cargo.html', {'cargo': cargo})





## cargos\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-03-27 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CargoAdministrativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_cargo', models.CharField(max_length=10, unique=True, verbose_name='Código do Cargo')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Cargo Administrativo',
                'verbose_name_plural': 'Cargos Administrativos',
                'ordering': ['nome'],
            },
        ),
    ]





## cargos\templates\cargos\confirmar_exclusao.html

html
{% extends 'base.html' %}

{% block title %}Confirmar Exclusão{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Confirmar Exclusão</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="lead">Tem certeza que deseja excluir o cargo administrativo "{{ cargo.nome }}"?</p>
            <p class="text-danger">Esta ação não pode ser desfeita.</p>
            
            <form method="post">
                {% csrf_token %}
                <button type="submit" class="btn btn-danger">Sim, excluir</button>
                <a href="{% url 'cargos:listar_cargos_administrativos' %}" class="btn btn-secondary">Cancelar</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}





## cargos\templates\cargos\criar_cargo.html

html
{% extends 'base.html' %}

{% block title %}Criar Novo Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Criar Novo Cargo Administrativo</h1>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        
        <button type="submit" class="btn btn-primary">Criar Cargo</button>
        <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}





## cargos\templates\cargos\detalhes_cargo.html

html
{% extends 'base.html' %}

{% block title %}Detalhes do Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes do Cargo Administrativo</h1>
  
  <div class="card">
    <div class="card-header">
      <h2>{{ cargo.nome }}</h2>
    </div>
    <div class="card-body">
      <p><strong>Código:</strong> {{ cargo.codigo_cargo }}</p>
      <p><strong>Descrição:</strong> {{ cargo.descricao|default:"Não informada" }}</p>
    </div>
    <div class="card-footer">
      <a href="{% url 'cargos:editar_cargo' cargo.id %}" class="btn btn-warning">Editar</a>
      <a href="{% url 'cargos:excluir_cargo' cargo.id %}" class="btn btn-danger">Excluir</a>
      <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Voltar</a>
    </div>
  </div>
</div>
{% endblock %}





## cargos\templates\cargos\detalhe_cargo.html

html
{% extends 'base.html' %}

{% block title %}Detalhes do Cargo{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Detalhes do Cargo Administrativo</h1>
    
    <div class="card">
        <div class="card-body">
            <h2>{{ cargo.nome }}</h2>
            <p><strong>Código:</strong> {{ cargo.codigo_cargo }}</p>
            <p><strong>Descrição:</strong> {{ cargo.descricao }}</p>
            
            <div class="mt-3">
                <a href="{% url 'cargos:editar_cargo' cargo.codigo_cargo %}" class="btn btn-warning">Editar</a>
                <a href="{% url 'cargos:excluir_cargo' cargo.codigo_cargo %}" class="btn btn-danger">Excluir</a>
                <a href="{% url 'cargos:listar_cargos_administrativos' %}" class="btn btn-secondary">Voltar para a Lista</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}





## cargos\templates\cargos\editar_cargo.html

html
{% extends 'base.html' %}

{% block title %}Editar Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Cargo Administrativo</h1>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        
        <button type="submit" class="btn btn-primary">Atualizar Cargo</button>
        <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}





## cargos\templates\cargos\excluir_cargo.html

html
{% extends 'base.html' %}

{% block title %}Excluir Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Cargo Administrativo</h1>
    <p>Tem certeza que deseja excluir o cargo administrativo "{{ cargo.nome }}" ({{ cargo.codigo_cargo }})?</p>
    
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Sim, excluir</button>
        <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}





## cargos\templates\cargos\formulario_cargo.html

html
{% extends 'base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">{{ titulo }}</h1>
    
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
            <a href="{% url 'cargos:listar_cargos_administrativos' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}





## cargos\templates\cargos\listar_cargos.html

html
{% extends 'base.html' %}

{% block title %}Cargos Administrativos{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Cargos Administrativos</h1>
  
    <a href="{% url 'cargos:criar_cargo' %}" class="btn btn-primary mb-3">Novo Cargo</a>
  
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Código</th>
          <th>Nome</th>
          <th>Descrição</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        {% for cargo in cargos %}
        <tr>
          <td>{{ cargo.codigo_cargo }}</td>
          <td>{{ cargo.nome }}</td>
          <td>{{ cargo.descricao|truncatechars:50|default:"-" }}</td>
          <td>
            <a href="{% url 'cargos:detalhes_cargo' cargo.id %}" class="btn btn-sm btn-info">Detalhes</a>
            <a href="{% url 'cargos:editar_cargo' cargo.id %}" class="btn btn-sm btn-warning">Editar</a>
            <a href="{% url 'cargos:excluir_cargo' cargo.id %}" class="btn btn-sm btn-danger">Excluir</a>
          </td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="4" class="text-center">Nenhum cargo administrativo cadastrado.</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
</div>
{% endblock %}




## cargos\tests\test_models.py

python
from django.test import TestCase
from cargos.models import CargoAdministrativo

class CargoAdministrativoTest(TestCase):
    def test_criar_cargo(self):
        cargo = CargoAdministrativo.objects.create(
            codigo_cargo='CARGO001',
            nome='Coordenador',
            descricao='Responsável pela coordenação do curso.'
        )
        self.assertEqual(cargo.nome, 'Coordenador')
        self.assertEqual(cargo.codigo_cargo, 'CARGO001')





## cargos\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from cargos.models import CargoAdministrativo

class CargoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cargo = CargoAdministrativo.objects.create(
            codigo_cargo='CARGO001',
            nome='Coordenador',
            descricao='Responsável pela coordenação do curso.'
        )

    def test_listar_cargos(self):
        response = self.client.get(reverse('cargos:listar_cargos_administrativos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Coordenador')

    def test_detalhe_cargo(self):
        response = self.client.get(reverse('cargos:detalhe_cargo', args=[self.cargo.codigo_cargo]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Coordenador')
        
    def test_criar_cargo(self):
        response = self.client.post(
            reverse('cargos:criar_cargo'),
            {
                'codigo_cargo': 'CARGO002',
                'nome': 'diretor',
                'descricao': 'Responsável pela direção do departamento.'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verifica se o cargo foi criado e se o nome foi capitalizado corretamente
        cargo = CargoAdministrativo.objects.get(codigo_cargo='CARGO002')
        self.assertEqual(cargo.nome, 'Diretor')

    def test_editar_cargo(self):
        response = self.client.post(
            reverse('cargos:editar_cargo', args=[self.cargo.codigo_cargo]),
            {
                'codigo_cargo': 'CARGO001',
                'nome': 'coordenador sênior',
                'descricao': 'Coordenador com experiência avançada.'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verifica se o cargo foi atualizado
        cargo = CargoAdministrativo.objects.get(codigo_cargo='CARGO001')
        self.assertEqual(cargo.nome, 'Coordenador Sênior')
        self.assertEqual(cargo.descricao, 'Coordenador com experiência avançada.')

    def test_excluir_cargo(self):
        response = self.client.post(
            reverse('cargos:excluir_cargo', args=[self.cargo.codigo_cargo])
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
        # Verifica se o cargo foi excluído
        with self.assertRaises(CargoAdministrativo.DoesNotExist):
            CargoAdministrativo.objects.get(codigo_cargo='CARGO001')



