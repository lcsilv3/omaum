# Código da Funcionalidade: cargos - Parte 1/3
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
    path('criar/', views.criar_cargo, name='criar_cargo'),
    path('<int:id>/detalhes/', views.detalhar_cargo, name='detalhar_cargo'),
    path('<int:id>/editar/', views.editar_cargo, name='editar_cargo'),
    path('<int:id>/excluir/', views.excluir_cargo, name='excluir_cargo'),
    path('atribuir/', views.atribuir_cargo, name='atribuir_cargo'),
    path('remover-atribuicao/<int:id>/', views.remover_atribuicao_cargo, name='remover_atribuicao_cargo'),
]




## cargos\views.py

python
import importlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Função para obter modelos usando importlib
def get_models():
    CargoAdministrativo = importlib.import_module('cargos.models').CargoAdministrativo
    return CargoAdministrativo

# Função para obter formulários usando importlib
def get_forms():
    CargoAdministrativoForm = importlib.import_module('cargos.formulario_cargo').CargoAdministrativoForm
    return CargoAdministrativoForm

@login_required
def listar_cargos(request):
    """Lista todos os cargos administrativos."""
    CargoAdministrativo = get_models()
    cargos = CargoAdministrativo.objects.all()
    return render(request, 'cargos/listar_cargos.html', {'cargos': cargos})

@login_required
def criar_cargo(request):
    """Cria um novo cargo administrativo."""
    CargoAdministrativoForm = get_forms()
    
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

@login_required
def detalhar_cargo(request, id):
    """Exibe os detalhes de um cargo administrativo."""
    CargoAdministrativo = get_models()
    cargo = get_object_or_404(CargoAdministrativo, id=id)
    return render(request, 'cargos/detalhar_cargo.html', {'cargo': cargo})

@login_required
def editar_cargo(request, id):
    """Edita um cargo administrativo existente."""
    CargoAdministrativo = get_models()
    CargoAdministrativoForm = get_forms()
    
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

@login_required
def excluir_cargo(request, id):
    """Exclui um cargo administrativo."""
    CargoAdministrativo = get_models()
    cargo = get_object_or_404(CargoAdministrativo, id=id)
    
    if request.method == 'POST':
        cargo.delete()
        messages.success(request, 'Cargo administrativo excluído com sucesso!')
        return redirect('cargos:listar_cargos')
    
    return render(request, 'cargos/excluir_cargo.html', {'cargo': cargo})

@login_required
def atribuir_cargo(request):
    """Atribui um cargo a um aluno."""
    # Implementação pendente
    return render(request, 'cargos/atribuir_cargo.html')

@login_required
def remover_atribuicao_cargo(request, id):
    """Remove a atribuição de um cargo a um aluno."""
    # Implementação pendente
    return render(request, 'cargos/remover_atribuicao.html')





## cargos\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-04-03 20:26

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



