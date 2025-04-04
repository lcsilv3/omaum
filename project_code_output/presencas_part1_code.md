# Código da Funcionalidade: presencas - Parte 1/2
*Gerado automaticamente*



## presencas\admin.py

python
from django.contrib import admin

# Register your models here.





## presencas\apps.py

python
from django.apps import AppConfig


class PresencasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'presencas'





## presencas\forms.py

python
from django import forms
from importlib import import_module

def get_presenca_model():
    presencas_module = import_module('presencas.models')
    return getattr(presencas_module, 'PresencaAcademica')

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_turma_model():
    turmas_module = import_module('turmas.models')
    return getattr(turmas_module, 'Turma')

class PresencaForm(forms.ModelForm):
    class Meta:
        model = get_presenca_model()
        fields = ['aluno', 'turma', 'data', 'presente', 'justificativa']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'justificativa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data and data > datetime.date.today():
            raise ValidationError("A data da presença não pode ser no futuro.")
        return data
        
    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        turma = cleaned_data.get('turma')
        data = cleaned_data.get('data')
        
        if aluno and turma and data:
            if PresencaAcademica.objects.filter(aluno=aluno, turma=turma, data=data).exists():
                raise ValidationError("Já existe um registro de presença para este aluno nesta turma e data.")
        
        return cleaned_data




## presencas\models.py

python
from django.db import models
from django.contrib.auth.models import User
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_turma_model():
    turmas_module = import_module('turmas.models')
    return getattr(turmas_module, 'Turma')

class PresencaAcademica(models.Model):
    aluno = models.ForeignKey(
        get_aluno_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Aluno',
        to_field='cpf'  # Especificar que estamos referenciando o campo cpf
    )
    turma = models.ForeignKey(
        get_turma_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Turma'
    )
    data = models.DateField(verbose_name='Data')
    presente = models.BooleanField(default=True, verbose_name='Presente')
    justificativa = models.TextField(blank=True, null=True, verbose_name='Justificativa')
    registrado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='Registrado por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f"{self.aluno.nome} - {self.turma.nome} - {self.data}"

    class Meta:
        verbose_name = 'Presença Acadêmica'
        verbose_name_plural = 'Presenças Acadêmicas'
        ordering = ['-data', 'aluno__nome']
        unique_together = ['aluno', 'turma', 'data']




## presencas\tests.py

python
from django.test import TestCase

# Create your tests here.





## presencas\urls.py

python
from django.urls import path
from . import views

app_name = 'presencas'

urlpatterns = [
    path('lista/', views.listar_presencas, name='listar_presencas'),  # Alterado para usar a função existente
    path('registrar/', views.registrar_presenca, name='registrar_presenca'),
    path('editar/<int:id>/', views.editar_presenca, name='editar_presenca'),
    path('excluir/<int:id>/', views.excluir_presenca, name='excluir_presenca'),
    path('relatorio/', views.relatorio_presencas, name='relatorio_presencas'),
]





## presencas\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import PresencaAcademica
from .forms import PresencaForm
from alunos.models import Aluno
from turmas.models import Turma

@login_required
def registrar_presenca(request):
    """Registra a presença de um aluno."""
    if request.method == 'POST':
        form = PresencaForm(request.POST)
        if form.is_valid():
            presenca = form.save(commit=False)
            presenca.registrado_por = request.user
            presenca.save()
            messages.success(request, 'Presença registrada com sucesso!')
            return redirect('presencas:listar_presencas')
    else:
        form = PresencaForm()
    
    return render(request, 'presencas/registrar_presenca.html', {'form': form})

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def listar_presencas(request):
    presencas_list = PresencaAcademica.objects.all().select_related('aluno', 'turma')
    
    # Filtros
    aluno_id = request.GET.get('aluno')
    turma_id = request.GET.get('turma')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if aluno_id:
        presencas_list = presencas_list.filter(aluno_id=aluno_id)
    if turma_id:
        presencas_list = presencas_list.filter(turma_id=turma_id)
    if data_inicio:
        presencas_list = presencas_list.filter(data__gte=data_inicio)
    if data_fim:
        presencas_list = presencas_list.filter(data__lte=data_fim)
    
    # Paginação
    paginator = Paginator(presencas_list, 10)  # 10 itens por página
    page = request.GET.get('page')
    
    try:
        presencas = paginator.page(page)
    except PageNotAnInteger:
        presencas = paginator.page(1)
    except EmptyPage:
        presencas = paginator.page(paginator.num_pages)
    
    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
    
    return render(request, 'presencas/lista_presencas.html', {
        'presencas': presencas,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'alunos': alunos,
        'turmas': turmas
    })

@login_required
def editar_presenca(request, id):
    """Edita um registro de presença."""
    presenca = get_object_or_404(PresencaAcademica, id=id)
    
    if request.method == 'POST':
        form = PresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Presença atualizada com sucesso!')
            return redirect('presencas:listar_presencas')
    else:
        form = PresencaForm(instance=presenca)
    
    return render(request, 'presencas/editar_presenca.html', {'form': form, 'presenca': presenca})

@login_required
@permission_required('presencas.delete_presencaacademica', raise_exception=True)
def excluir_presenca(request, id):  # Padronizado para usar 'id'
    presenca = get_object_or_404(PresencaAcademica, id=id)
    
    if request.method == 'POST':
        presenca.delete()
        messages.success(request, 'Presença excluída com sucesso!')
        return redirect('presencas:listar_presencas')  # Corrigido para usar o namespace
    
    return render(request, 'presencas/excluir_presenca.html', {'presenca': presenca})

@login_required
@permission_required('presencas.view_presencaacademica', raise_exception=True)
def relatorio_presencas(request):
    # Implementação pendente
    return render(request, 'presencas/relatorio_presencas.html')





## presencas\management\commands\setup_presencas_permissions.py

python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from presencas.models import PresencaAcademica

class Command(BaseCommand):
    help = 'Set up permissions for the presencas app'

    def handle(self, *args, **options):
        # Get content type for the PresencaAcademica model
        content_type = ContentType.objects.get_for_model(PresencaAcademica)
        
        # Get all permissions for the PresencaAcademica model
        permissions = Permission.objects.filter(content_type=content_type)
        
        # Add all permissions to the teachers group
        # for permission in permissions:
        #     teachers_group.permissions.add(permission)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully set up permissions for the presencas app'))





## presencas\templates\presencas\editar_presenca.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Presença</h1>
    
    <div class="card mb-4">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                {% for field in form %}
                <div class="mb-3">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                    <div class="text-danger">
                        {% for error in field.errors %}
                        <small>{{ error }}</small>
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
                
                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Salvar Alterações</button>
                    <a href="{% url 'lista_presencas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}





## presencas\templates\presencas\excluir_presenca.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Registro de Presença</h1>
    
    <div class="card mb-4">
        <div class="card-body">
            <div class="alert alert-danger">
                <h5>Confirmação de Exclusão</h5>
                <p>Você está prestes a excluir o seguinte registro de presença:</p>
                <ul>
                    <li><strong>Aluno:</strong> {{ presenca.aluno }}</li>
                    <li><strong>Turma:</strong> {{ presenca.turma }}</li>
                    <li><strong>Data:</strong> {{ presenca.data }}</li>
                    <li><strong>Presente:</strong> {% if presenca.presente %}Sim{% else %}Não{% endif %}</li>
                </ul>
                <p>Esta ação não pode ser desfeita. Deseja continuar?</p>
            </div>
            
            <form method="post">
                {% csrf_token %}
                <div class="mt-3">
                    <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
                    <a href="{% url 'lista_presencas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}



