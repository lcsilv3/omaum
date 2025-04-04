# Código da Funcionalidade: frequencias - Parte 1/2
*Gerado automaticamente*



## frequencias\admin.py

python
from django.contrib import admin
from .models import Frequencia

@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'data']  # Remove fields that don't exist
    list_filter = ['data']  # Remove fields that don't exist
    search_fields = ('aluno__nome', 'turma__codigo_turma', 'justificativa')
    date_hierarchy = 'data'
    readonly_fields = []  # Remove fields that don't exist
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('aluno', 'turma', 'data', 'presente')
        }),
        ('Justificativa', {
            'fields': ('justificativa',),
            'classes': ('collapse',),
        }),
        ('Informações de Registro', {
            'fields': ('registrado_por', 'data_registro', 'data_atualizacao'),
            'classes': ('collapse',),
        }),
    )





## frequencias\api.py

python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Frequencia
from .serializers import FrequenciaSerializer

class FrequenciaViewSet(viewsets.ModelViewSet):
    queryset = Frequencia.objects.all()
    serializer_class = FrequenciaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Frequencia.objects.all()
        aluno_id = self.request.query_params.get('aluno')
        turma_id = self.request.query_params.get('turma')
        
        if aluno_id:
            queryset = queryset.filter(aluno_id=aluno_id)
        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
            
        return queryset





## frequencias\apps.py

python
from django.apps import AppConfig

class FrequenciasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'frequencias'
    verbose_name = 'Frequências'





## frequencias\forms.py

python
from django import forms
from .models import Frequencia
import datetime
from django.core.exceptions import ValidationError

class FrequenciaForm(forms.ModelForm):
    class Meta:
        model = Frequencia
        fields = ['aluno', 'turma', 'data', 'presente', 'justificativa']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'turma': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'justificativa': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
       
    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data and data > datetime.date.today():
            raise ValidationError("A data da frequência não pode ser no futuro.")
        return data
       
    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        turma = cleaned_data.get('turma')
        data = cleaned_data.get('data')
        
        # Se for uma atualização (instância existe), precisamos excluir a instância atual da verificação de unicidade
        if self.instance.pk:
            if Frequencia.objects.filter(aluno=aluno, turma=turma, data=data).exclude(pk=self.instance.pk).exists():
                raise ValidationError("Já existe um registro de frequência para este aluno nesta turma e data.")
        else:
            if aluno and turma and data:
                if Frequencia.objects.filter(aluno=aluno, turma=turma, data=data).exists():
                    raise ValidationError("Já existe um registro de frequência para este aluno nesta turma e data.")
       
        return cleaned_data





## frequencias\models.py

python
from django.db import models
from importlib import import_module

def get_aluno_model():
    alunos_module = import_module('alunos.models')
    return getattr(alunos_module, 'Aluno')

def get_atividade_model():
    atividades_module = import_module('atividades.models')
    return getattr(atividades_module, 'AtividadeAcademica')

class Frequencia(models.Model):
    aluno = models.ForeignKey(
        get_aluno_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Aluno',
        to_field='cpf'  # Especificar que estamos referenciando o campo cpf
    )
    atividade = models.ForeignKey(
        get_atividade_model(), 
        on_delete=models.CASCADE, 
        verbose_name='Atividade'
    )
    data = models.DateField(verbose_name='Data')
    presente = models.BooleanField(default=True, verbose_name='Presente')
    justificativa = models.TextField(blank=True, null=True, verbose_name='Justificativa')
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.atividade.nome} - {self.data}"
    
    class Meta:
        verbose_name = 'Frequência'
        verbose_name_plural = 'Frequências'
        ordering = ['-data']
        unique_together = ['aluno', 'atividade', 'data']





## frequencias\urls.py

python
from django.urls import path
from . import views

app_name = 'frequencias'

urlpatterns = [
    path('', views.listar_frequencias, name='listar_frequencias'),
    path('registrar/', views.registrar_frequencia, name='registrar_frequencia'),
    path('<int:id>/editar/', views.editar_frequencia, name='editar_frequencia'),
    path('<int:id>/excluir/', views.excluir_frequencia, name='excluir_frequencia'),
    path('<int:id>/detalhes/', views.detalhar_frequencia, name='detalhar_frequencia'),
    path('relatorio/', views.relatorio_frequencias, name='relatorio_frequencias'),
    path('exportar/', views.exportar_frequencias, name='exportar_frequencias'),
]





## frequencias\views.py

python
import importlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Função para obter modelos usando importlib
def get_models():
    Frequencia = importlib.import_module('frequencias.models').Frequencia
    Aluno = importlib.import_module('alunos.models').Aluno
    Turma = importlib.import_module('turmas.models').Turma
    return Frequencia, Aluno, Turma

# Função para obter formulários usando importlib
def get_forms():
    FrequenciaForm = importlib.import_module('frequencias.forms').FrequenciaForm
    return FrequenciaForm

@login_required
@permission_required('frequencias.add_frequencia', raise_exception=True)
def registrar_frequencia(request):
    FrequenciaForm = get_forms()
    
    if request.method == 'POST':
        form = FrequenciaForm(request.POST)
        if form.is_valid():
            frequencia = form.save(commit=False)
            frequencia.registrado_por = request.user
            frequencia.save()
            messages.success(request, 'Frequência registrada com sucesso!')
            return redirect('frequencias:listar_frequencias')
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = FrequenciaForm()
   
    return render(request, 'frequencias/registrar_frequencia.html', {'form': form})

@login_required
@permission_required('frequencias.add_frequencia', raise_exception=True)
def registrar_frequencia_turma(request, turma_id):
    Frequencia, Aluno, Turma = get_models()
    
    turma = get_object_or_404(Turma, id=turma_id)
    alunos = Aluno.objects.filter(turmas=turma)
    
    if request.method == 'POST':
        data = request.POST.get('data')
        presentes = request.POST.getlist('presentes')
        
        # Create or update attendance records
        for aluno in alunos:
            presente = str(aluno.id) in presentes
            justificativa = request.POST.get(f'justificativa_{aluno.id}', '')
            
            # Check if record exists
            frequencia, created = Frequencia.objects.update_or_create(
                aluno=aluno,
                turma=turma,
                data=data,
                defaults={
                    'presente': presente,
                    'justificativa': justificativa if not presente else '',
                    'registrado_por': request.user
                }
            )
        
        messages.success(request, 'Frequências registradas com sucesso!')
        return redirect('frequencias:listar_frequencias')
    
    return render(request, 'frequencias/registrar_frequencia_turma.html', {
        'turma': turma,
        'alunos': alunos,
    })

@login_required
@permission_required('frequencias.view_frequencia', raise_exception=True)
def listar_frequencias(request):
    Frequencia, Aluno, Turma = get_models()
    
    frequencias_list = Frequencia.objects.all().select_related('aluno', 'turma')
   
    # Filtros
    aluno_id = request.GET.get('aluno')
    turma_id = request.GET.get('turma')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    status = request.GET.get('status')
   
    if aluno_id:
        frequencias_list = frequencias_list.filter(aluno_id=aluno_id)
    if turma_id:
        frequencias_list = frequencias_list.filter(turma_id=turma_id)
    if data_inicio:
        frequencias_list = frequencias_list.filter(data__gte=data_inicio)
    if data_fim:
        frequencias_list = frequencias_list.filter(data__lte=data_fim)
    if status:
        presente = status == 'presente'
        frequencias_list = frequencias_list.filter(presente=presente)
   
    # Paginação
    paginator = Paginator(frequencias_list, 10)  # 10 itens por página
    page = request.GET.get('page')
   
    try:
        frequencias = paginator.page(page)
    except PageNotAnInteger:
        frequencias = paginator.page(1)
    except EmptyPage:
        frequencias = paginator.page(paginator.num_pages)
   
    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    turmas = Turma.objects.all()
   
    return render(request, 'frequencias/listar_frequencias.html', {
        'frequencias': frequencias,
        'aluno_id': aluno_id,
        'turma_id': turma_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'status': status,
        'alunos': alunos,
        'turmas': turmas
    })

@login_required
@permission_required('frequencias.change_frequencia', raise_exception=True)
def editar_frequencia(request, id):
    Frequencia = get_models()[0]
    FrequenciaForm = get_forms()
    
    frequencia = get_object_or_404(Frequencia, id=id)
   
    if request.method == 'POST':
        form = FrequenciaForm(request.POST, instance=frequencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Frequência atualizada com sucesso!')
            return redirect('frequencias:listar_frequencias')
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = FrequenciaForm(instance=frequencia)
   
    return render(request, 'frequencias/editar_frequencia.html', {'form': form, 'frequencia': frequencia})

@login_required
@permission_required('frequencias.view_frequencia', raise_exception=True)
def detalhar_frequencia(request, id):
    """Exibe os detalhes de uma frequência."""
    Frequencia = get_models()[0]
    frequencia = get_object_or_404(Frequencia, id=id)
    return render(request, 'frequencias/detalhar_frequencia.html', {'frequencia': frequencia})

@login_required
@permission_required('frequencias.delete_frequencia', raise_exception=True)
def excluir_frequencia(request, id):
    Frequencia = get_models()[0]
    frequencia = get_object_or_404(Frequencia, id=id)
   
    if request.method == 'POST':
        frequencia.delete()
        messages.success(request, 'Frequência excluída com sucesso!')
        return redirect('frequencias:listar_frequencias')
   
    return render(request, 'frequencias/excluir_frequencia.html', {'frequencia': frequencia})

@login_required
@permission_required('frequencias.view_frequencia', raise_exception=True)
def relatorio_frequencias(request):
    # Implementação pendente
    return render(request, 'frequencias/relatorio_frequencias.html')

@login_required
@permission_required('frequencias.view_frequencia', raise_exception=True)
def exportar_frequencias(request):
    # Implementação pendente
    return redirect('frequencias:listar_frequencias')





## frequencias\migrations\0001_initial.py

python
# Generated by Django 5.1.7 on 2025-04-03 20:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alunos', '0001_initial'),
        ('atividades', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frequencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data')),
                ('presente', models.BooleanField(default=True, verbose_name='Presente')),
                ('justificativa', models.TextField(blank=True, null=True, verbose_name='Justificativa')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alunos.aluno', verbose_name='Aluno')),
                ('atividade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atividades.atividadeacademica', verbose_name='Atividade')),
            ],
            options={
                'verbose_name': 'Frequência',
                'verbose_name_plural': 'Frequências',
                'ordering': ['-data'],
                'unique_together': {('aluno', 'atividade', 'data')},
            },
        ),
    ]





## frequencias\static\js\frequencia_form.js

javascript
// Show/hide justification field based on presence checkbox
document.addEventListener('DOMContentLoaded', function() {
    const presenteCheckbox = document.getElementById('id_presente');
    const justificativaField = document.getElementById('id_justificativa').closest('.mb-3');
    
    function toggleJustificativa() {
        if (presenteCheckbox.checked) {
            justificativaField.style.display = 'none';
        } else {
            justificativaField.style.display = 'block';
        }
    }
    
    if (presenteCheckbox) {
        toggleJustificativa();
        presenteCheckbox.addEventListener('change', toggleJustificativa);
    }
});





## frequencias\templates\frequencias\detalhar_frequencia.html

html
{% extends 'core/base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes da Frequência</h1>
    
  {% if messages %}
      {% for message in messages %}
          <div class="alert alert-{{ message.tags }}">
              {{ message }}
          </div>
      {% endfor %}
  {% endif %}
    
  <div class="card">
      <div class="card-header">
          <h5 class="mb-0">Informações da Frequência</h5>
      </div>
      <div class="card-body">
          <div class="row mb-3">
              <div class="col-md-6">
                  <p><strong>Aluno:</strong> {{ frequencia.aluno.nome }}</p>
                  <p><strong>Turma:</strong> {{ frequencia.turma.codigo_turma }}</p>
                  <p><strong>Data:</strong> {{ frequencia.data }}</p>
              </div>
              <div class="col-md-6">
                  <p>
                      <strong>Status:</strong> 
                      {% if frequencia.presente %}
                          <span class="badge bg-success">Presente</span>
                      {% else %}
                          <span class="badge bg-danger">Ausente</span>
                      {% endif %}
                  </p>
                  <p><strong>Registrado por:</strong> {{ frequencia.registrado_por|default:"Não informado" }}</p>
                  <p><strong>Data de registro:</strong> {{ frequencia.data_registro }}</p>
              </div>
          </div>
            
          {% if not frequencia.presente %}
          <div class="mb-3">
              <h6>Justificativa:</h6>
              <div class="p-3 bg-light rounded">
                  {% if frequencia.justificativa %}
                      {{ frequencia.justificativa|linebreaks }}
                  {% else %}
                      <em>Nenhuma justificativa fornecida.</em>
                  {% endif %}
              </div>
          </div>
          {% endif %}
            
          <div class="d-grid gap-2 d-md-flex justify-content-md-end">
              <a href="{% url 'frequencias:editar_frequencia' frequencia.id %}" class="btn btn-warning">Editar</a>
              <a href="{% url 'frequencias:excluir_frequencia' frequencia.id %}" class="btn btn-danger">Excluir</a>
              <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Voltar</a>
          </div>
      </div>
  </div>
</div>
{% endblock %}



