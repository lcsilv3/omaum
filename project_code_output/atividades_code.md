# Código da Funcionalidade: atividades
*Gerado automaticamente*



## atividades\admin.py

python
from django.contrib import admin
from .models import AtividadeAcademica, AtividadeRitualistica

@admin.register(AtividadeAcademica)
class AtividadeAcademicaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'turma', 'data_inicio', 'data_fim']
    list_filter = ['turma']
    search_fields = ['nome', 'descricao']

@admin.register(AtividadeRitualistica)
class AtividadeRitualisticaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'turma', 'data_inicio', 'data_fim']
    list_filter = ['turma']
    search_fields = ['nome', 'descricao']
    filter_horizontal = ['alunos']




## atividades\apps.py

python
from django.apps import AppConfig


class AtividadesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'atividades'




## atividades\forms.py

python
from django import forms
from django.core.exceptions import ValidationError
import datetime
from .models import AtividadeAcademica, AtividadeRitualistica  # Adicione AtividadeRitualistica aqui

class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = AtividadeAcademica
        fields = ['nome', 'descricao', 'data_inicio', 'data_fim', 'turma']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_data_inicio(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        if data_inicio and data_inicio < datetime.date.today():
            raise ValidationError("A data de início da atividade não pode ser no passado.")
        return data_inicio

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValidationError("A data de fim não pode ser anterior à data de início.")
        return cleaned_data

class AtividadeRitualisticaForm(forms.ModelForm):
    todos_alunos = forms.BooleanField(required=False, label='Todos os Alunos')
    
    class Meta:
        model = AtividadeRitualistica
        fields = ['nome', 'descricao', 'data_inicio', 'data_fim', 'turma', 'alunos']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'alunos': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alunos'].required = False

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        todos_alunos = cleaned_data.get('todos_alunos')
        alunos = cleaned_data.get('alunos')
        
        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValidationError("A data de fim não pode ser anterior à data de início.")

        if not todos_alunos and not alunos:
            raise ValidationError("Selecione alunos específicos ou marque 'Todos os Alunos'.")

        if todos_alunos and alunos:
            raise ValidationError("Você não pode selecionar alunos específicos quando 'Todos os Alunos' está marcado.")
        
        return cleaned_data



## atividades\models.py

python
from django.db import models
from turmas.models import Turma
from django.conf import settings

class AtividadeAcademica(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição')
    data_inicio = models.DateField(verbose_name='Data de Início')
    data_fim = models.DateField(verbose_name='Data de Fim')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name='Turma')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Atividade Acadêmica'
        verbose_name_plural = 'Atividades Acadêmicas'

class AtividadeRitualistica(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    descricao = models.TextField(verbose_name='Descrição')
    data_inicio = models.DateField(verbose_name='Data de Início')
    data_fim = models.DateField(verbose_name='Data de Fim')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name='Turma')
    alunos = models.ManyToManyField('core.Aluno', blank=True, related_name='atividades_ritualisticas', verbose_name='Alunos')
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Atividade Ritualística'
        verbose_name_plural = 'Atividades Ritualísticas'




## atividades\tests.py

python
from django.test import TestCase

# Create your tests here.




## atividades\urls.py

python
from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    # URLs para Atividades Acadêmicas
    path('academicas/', views.AcademicaListaView.as_view(), name='academica_lista'),
    path('academicas/criar/', views.AcademicaCriarView.as_view(), name='academica_criar'),
    path('academicas/<int:pk>/editar/', views.AcademicaEditarView.as_view(), name='academica_editar'),
    path('academicas/<int:pk>/excluir/', views.AcademicaExcluirView.as_view(), name='academica_excluir'),
    
    # URLs para Atividades Ritualísticas
    path('ritualisticas/', views.RitualisticaListaView.as_view(), name='ritualistica_lista'),
    path('ritualisticas/criar/', views.RitualisticaCriarView.as_view(), name='ritualistica_criar'),
    path('ritualisticas/<int:pk>/editar/', views.RitualisticaEditarView.as_view(), name='ritualistica_editar'),
    path('ritualisticas/<int:pk>/excluir/', views.RitualisticaExcluirView.as_view(), name='ritualistica_excluir'),
]



## atividades\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import AtividadeAcademica, AtividadeRitualistica
from .forms import AtividadeAcademicaForm, AtividadeRitualisticaForm
from turmas.models import Turma

# Views para Atividades Acadêmicas
class AcademicaListaView(ListView):
    model = AtividadeAcademica
    template_name = 'atividades/academica_lista.html'
    context_object_name = 'atividades'
    paginate_by = 10  # Número de itens por página
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        
        # Adicionar lista de turmas para o filtro
        context['turmas'] = Turma.objects.all()
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Busca por nome
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(nome__icontains=search_query)
        
        # Filtro por turma
        turma_id = self.request.GET.get('turma', '')
        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
        
        # Filtro por data de início
        data_inicio_min = self.request.GET.get('data_inicio_min', '')
        if data_inicio_min:
            queryset = queryset.filter(data_inicio__gte=data_inicio_min)
        
        # Filtro por data de fim
        data_fim_max = self.request.GET.get('data_fim_max', '')
        if data_fim_max:
            queryset = queryset.filter(data_fim__lte=data_fim_max)
        
        # Ordenação
        order_by = self.request.GET.get('order_by', 'nome')
        order_dir = self.request.GET.get('order_dir', 'asc')
        
        if order_dir == 'desc':
            order_by = f'-{order_by}'
            
        return queryset.order_by(order_by)


class AcademicaCriarView(CreateView):
    model = AtividadeAcademica
    form_class = AtividadeAcademicaForm
    template_name = 'atividades/academica_formulario.html'
    success_url = reverse_lazy('atividades:academica_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Atividade acadêmica criada com sucesso!')
        return super().form_valid(form)


class AcademicaEditarView(UpdateView):
    model = AtividadeAcademica
    form_class = AtividadeAcademicaForm
    template_name = 'atividades/academica_formulario.html'
    success_url = reverse_lazy('atividades:academica_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Atividade acadêmica atualizada com sucesso!')
        return super().form_valid(form)


class AcademicaExcluirView(DeleteView):
    model = AtividadeAcademica
    template_name = 'atividades/academica_confirmar_exclusao.html'
    success_url = reverse_lazy('atividades:academica_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Atividade acadêmica excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


# Views para Atividades Ritualísticas
class RitualisticaListaView(ListView):
    model = AtividadeRitualistica
    template_name = 'atividades/ritualistica_lista.html'
    context_object_name = 'atividades_ritualisticas'
    paginate_by = 10  # Número de itens por página
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        
        # Adicionar lista de turmas para o filtro
        context['turmas'] = Turma.objects.all()
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Busca por nome
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(nome__icontains=search_query)
        
        # Filtro por turma
        turma_id = self.request.GET.get('turma', '')
        if turma_id:
            queryset = queryset.filter(turma_id=turma_id)
        
        # Filtro por data de início
        data_inicio_min = self.request.GET.get('data_inicio_min', '')
        if data_inicio_min:
            queryset = queryset.filter(data_inicio__gte=data_inicio_min)
        
        # Filtro por data de fim
        data_fim_max = self.request.GET.get('data_fim_max', '')
        if data_fim_max:
            queryset = queryset.filter(data_fim__lte=data_fim_max)
        
        # Ordenação
        order_by = self.request.GET.get('order_by', 'nome')
        order_dir = self.request.GET.get('order_dir', 'asc')
        
        if order_dir == 'desc':
            order_by = f'-{order_by}'
            
        return queryset.order_by(order_by)


class RitualisticaCriarView(CreateView):
    model = AtividadeRitualistica
    form_class = AtividadeRitualisticaForm
    template_name = 'atividades/atividade_ritualistica_form.html'
    success_url = reverse_lazy('atividades:ritualistica_lista')
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        # Handle the todos_alunos field logic
        if form.cleaned_data.get('todos_alunos'):
            # Logic to get all students from the selected turma
            turma = form.cleaned_data.get('turma')
            if turma:
                # Save first to create the instance
                instance.save()
                # Then add all students from the turma
                from core.models import Aluno
                alunos = Aluno.objects.filter(turma=turma)
                instance.alunos.set(alunos)
        else:
            instance.save()
            # The many-to-many relationship will be saved by the form
        
        messages.success(self.request, 'Atividade ritualística criada com sucesso!')
        return redirect(self.success_url)


class RitualisticaEditarView(UpdateView):
    model = AtividadeRitualistica
    form_class = AtividadeRitualisticaForm
    template_name = 'atividades/atividade_ritualistica_form.html'
    success_url = reverse_lazy('atividades:ritualistica_lista')
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        # Handle the todos_alunos field logic
        if form.cleaned_data.get('todos_alunos'):
            # Logic to get all students from the selected turma
            turma = form.cleaned_data.get('turma')
            if turma:
                # Save first to create the instance
                instance.save()
                # Then add all students from the turma
                from core.models import Aluno
                alunos = Aluno.objects.filter(turma=turma)
                instance.alunos.set(alunos)
        else:
            instance.save()
            # The many-to-many relationship will be saved by the form
            
        messages.success(self.request, 'Atividade ritualística atualizada com sucesso!')
        return redirect(self.success_url)


class RitualisticaExcluirView(DeleteView):
    model = AtividadeRitualistica
    template_name = 'atividades/ritualistica_confirmar_exclusao.html'
    success_url = reverse_lazy('atividades:ritualistica_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Atividade ritualística excluída com sucesso!')
        return super().delete(request, *args, **kwargs)




## atividades\templates\atividades\academica_confirmar_exclusao.html

html
{% extends "base.html" %}

{% block title %}Confirmar Exclusão{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Confirmar Exclusão</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="lead">Tem certeza que deseja excluir a atividade acadêmica "{{ object.nome }}"?</p>
            <p class="text-danger">Esta ação não pode ser desfeita.</p>
            
            <form method="post">
                {% csrf_token %}
                <button type="submit" class="btn btn-danger">Sim, excluir</button>
                <a href="{% url 'atividades:academica_lista' %}" class="btn btn-secondary">Cancelar</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}




## atividades\templates\atividades\academica_formulario.html

html
{% extends "base.html" %}

{% block title %}
    {% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Acadêmica
{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">
        {% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Acadêmica
    </h1>
    
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
            <a href="{% url 'atividades:academica_lista' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}




## atividades\templates\atividades\academica_lista.html

html
{% extends "base.html" %}

{% block title %}Atividades Acadêmicas{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Atividades Acadêmicas</h1>
    
    <div class="d-flex justify-content-between mb-3">
        <a href="{% url 'atividades:academica_criar' %}" class="btn btn-primary">Nova Atividade</a>
        
        <form class="d-flex" method="get">
            <input class="form-control me-2" type="search" placeholder="Buscar atividades" 
                   name="search" value="{{ search_query }}">
            <button class="btn btn-outline-primary" type="submit">Buscar</button>
        </form>
    </div>
    
    <div class="mb-3">
        <form method="get" class="d-flex flex-wrap gap-2">
            {% if search_query %}
            <input type="hidden" name="search" value="{{ search_query }}">
            {% endif %}
            
            <div class="form-group">
                <label for="turma_filter">Filtrar por Turma:</label>
                <select name="turma" id="turma_filter" class="form-control">
                    <option value="">Todas as Turmas</option>
                    {% for turma in turmas %}
                    <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"i" %}selected{% endif %}>{{ turma.nome }}</option>
                    {% endfor %}
                </select>
            </div>
            
            <div class="form-group">
                <label for="data_inicio_filter">Data de Início (a partir de):</label>
                <input type="date" name="data_inicio_min" id="data_inicio_filter" class="form-control" value="{{ request.GET.data_inicio_min }}">
            </div>
            
            <div class="form-group">
                <label for="data_fim_filter">Data de Fim (até):</label>
                <input type="date" name="data_fim_max" id="data_fim_filter" class="form-control" value="{{ request.GET.data_fim_max }}">
            </div>
            
            <div class="form-group d-flex align-items-end">
                <button type="submit" class="btn btn-primary">Filtrar</button>
                <a href="{% url 'atividades:academica_lista' %}" class="btn btn-secondary ms-2">Limpar Filtros</a>
            </div>
        </form>
    </div>
    
    <div class="card">
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>
                            <a href="?{% if request.GET.order_by == 'nome' and request.GET.order_dir == 'asc' %}order_by=nome&order_dir=desc{% else %}order_by=nome&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}">
                                Nome
                                {% if request.GET.order_by == 'nome' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'turma' and request.GET.order_dir == 'asc' %}order_by=turma&order_dir=desc{% else %}order_by=turma&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}">
                                Turma
                                {% if request.GET.order_by == 'turma' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'data_inicio' and request.GET.order_dir == 'asc' %}order_by=data_inicio&order_dir=desc{% else %}order_by=data_inicio&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}">
                                Data de Início
                                {% if request.GET.order_by == 'data_inicio' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'data_fim' and request.GET.order_dir == 'asc' %}order_by=data_fim&order_dir=desc{% else %}order_by=data_fim&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}">
                                Data de Fim
                                {% if request.GET.order_by == 'data_fim' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {% for atividade in atividades %}
                    <tr>
                        <td>{{ atividade.nome }}</td>
                        <td>{{ atividade.turma }}</td>
                        <td>{{ atividade.data_inicio|date:"d/m/Y" }}</td>
                        <td>{{ atividade.data_fim|date:"d/m/Y" }}</td>
                        <td>
                            <a href="{% url 'atividades:academica_editar' atividade.id %}" class="btn btn-sm btn-warning">Editar</a>
                            <button type="button" class="btn btn-sm btn-danger" 
                                    data-bs-toggle="modal" 
                                    data-bs-target="#deleteModal{{ atividade.id }}">
                                Excluir
                            </button>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center">Nenhuma atividade acadêmica encontrada.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% if is_paginated %}
    <nav aria-label="Paginação">
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page=1{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}" aria-label="Primeira">
                    <span aria-hidden="true">««</span>
                </a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}" aria-label="Anterior">
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
            
            {% for num in page_obj.paginator.page_range %}
                {% if page_obj.number == num %}
                <li class="page-item active"><a class="page-link" href="?page={{ num }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}">{{ num }}</a></li>
                {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                <li class="page-item"><a class="page-link" href="?page={{ num }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}">{{ num }}</a></li>
                {% endif %}
            {% endfor %}
            
            {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}" aria-label="Próxima">
                    <span aria-hidden="true">»</span>
                </a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}" aria-label="Última">
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
{% for atividade in atividades %}
<!-- Modal de confirmação para cada atividade -->
<div class="modal fade" id="deleteModal{{ atividade.id }}" tabindex="-1" aria-labelledby="deleteModalLabel{{ atividade.id }}" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="deleteModalLabel{{ atividade.id }}">Confirmar Exclusão</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
            </div>
            <div class="modal-body">
                <p>Tem certeza que deseja excluir a atividade acadêmica <strong>"{{ atividade.nome }}"</strong>?</p>
                <p class="text-danger">Esta ação não pode ser desfeita.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <a href="{% url 'atividades:academica_excluir' atividade.id %}" class="btn btn-danger">Sim, excluir</a>
            </div>
        </div>
    </div>
</div>
{% endfor %}
{% endblock %}




## atividades\templates\atividades\atividade_ritualistica_form.html

html
{% extends 'base.html' %}

{% block title %}
    {% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Ritualística
{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">
        {% if form.instance.pk %}Editar{% else %}Nova{% endif %} Atividade Ritualística
    </h1>
    
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
            <a href="{% url 'atividades:ritualistica_lista' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        var todosAlunosCheckbox = document.getElementById('id_todos_alunos');
        var alunosField = document.getElementById('id_alunos');

        function toggleAlunosField() {
            alunosField.disabled = todosAlunosCheckbox.checked;
        }

        todosAlunosCheckbox.addEventListener('change', toggleAlunosField);
        toggleAlunosField();
    });
</script>
{% endblock %}



## atividades\templates\atividades\ritualistica_confirmar_exclusao.html

html
{% extends "base.html" %}

{% block title %}Confirmar Exclusão{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Confirmar Exclusão</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="lead">Tem certeza que deseja excluir a atividade ritualística "{{ object.nome }}"?</p>
            <p class="text-danger">Esta ação não pode ser desfeita.</p>
            
            <form method="post">
                {% csrf_token %}
                <button type="submit" class="btn btn-danger">Sim, excluir</button>
                <a href="{% url 'atividades:ritualistica_lista' %}" class="btn btn-secondary">Cancelar</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}




## atividades\templates\atividades\ritualistica_lista.html

html
{% extends 'base.html' %}

{% block title %}Atividades Ritualísticas{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Atividades Ritualísticas</h1>
    
    <div class="d-flex justify-content-between mb-3">
        <a href="{% url 'atividades:ritualistica_criar' %}" class="btn btn-primary">Nova Atividade Ritualística</a>
        
        <form class="d-flex" method="get">
            <input class="form-control me-2" type="search" placeholder="Buscar atividades"
                   name="search" value="{{ search_query }}">
            <button class="btn btn-outline-primary" type="submit">Buscar</button>
        </form>
    </div>
    
    <!-- Filtros adicionais -->
    <div class="mb-3">
        <form method="get" class="d-flex flex-wrap gap-2">
            {% if search_query %}
            <input type="hidden" name="search" value="{{ search_query }}">
            {% endif %}
            
            <div class="form-group me-2">
                <label for="turma_filter">Filtrar por Turma:</label>
                <select name="turma" id="turma_filter" class="form-control">
                    <option value="">Todas as Turmas</option>
                    {% for turma in turmas %}
                    <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"i" %}selected{% endif %}>{{ turma.nome }}</option>
                    {% endfor %}
                </select>
            </div>
            
            <div class="form-group me-2">
                <label for="data_inicio_filter">Data de Início (a partir de):</label>
                <input type="date" name="data_inicio_min" id="data_inicio_filter" class="form-control" value="{{ request.GET.data_inicio_min }}">
            </div>
            
            <div class="form-group me-2">
                <label for="data_fim_filter">Data de Fim (até):</label>
                <input type="date" name="data_fim_max" id="data_fim_filter" class="form-control" value="{{ request.GET.data_fim_max }}">
            </div>
            
            <div class="form-group d-flex align-items-end">
                <button type="submit" class="btn btn-primary">Filtrar</button>
                <a href="{% url 'atividades:ritualistica_lista' %}" class="btn btn-secondary ms-2">Limpar Filtros</a>
            </div>
        </form>
    </div>
    
    <div class="card">
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>
                            <a href="?{% if request.GET.order_by == 'nome' and request.GET.order_dir == 'asc' %}order_by=nome&order_dir=desc{% else %}order_by=nome&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">
                                Nome
                                {% if request.GET.order_by == 'nome' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'turma' and request.GET.order_dir == 'asc' %}order_by=turma&order_dir=desc{% else %}order_by=turma&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">
                                Turma
                                {% if request.GET.order_by == 'turma' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'data_inicio' and request.GET.order_dir == 'asc' %}order_by=data_inicio&order_dir=desc{% else %}order_by=data_inicio&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">
                                Data de Início
                                {% if request.GET.order_by == 'data_inicio' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>
                            <a href="?{% if request.GET.order_by == 'data_fim' and request.GET.order_dir == 'asc' %}order_by=data_fim&order_dir=desc{% else %}order_by=data_fim&order_dir=asc{% endif %}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">
                                Data de Fim
                                {% if request.GET.order_by == 'data_fim' %}
                                    {% if request.GET.order_dir == 'asc' %}
                                        <i class="fas fa-sort-up"></i>
                                    {% else %}
                                        <i class="fas fa-sort-down"></i>
                                    {% endif %}
                                {% endif %}
                            </a>
                        </th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {% for atividade in atividades_ritualisticas %}
                    <tr>
                        <td>{{ atividade.nome }}</td>
                        <td>{{ atividade.turma }}</td>
                        <td>{{ atividade.data_inicio|date:"d/m/Y" }}</td>
                        <td>{{ atividade.data_fim|date:"d/m/Y" }}</td>
                        <td>
                            <a href="{% url 'atividades:ritualistica_editar' atividade.id %}" class="btn btn-sm btn-warning">Editar</a>
                            <a href="{% url 'atividades:ritualistica_excluir' atividade.id %}" 
                               class="btn btn-sm btn-danger"
                               onclick="return confirm('Tem certeza que deseja excluir a atividade ritualística \'{{ atividade.nome }}\'? Esta ação não pode ser desfeita.')">
                                Excluir
                            </a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center">Nenhuma atividade ritualística encontrada.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- Paginação -->
    {% if is_paginated %}
    <nav aria-label="Paginação" class="mt-3">
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page=1{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}" aria-label="Primeira">
                    <span aria-hidden="true">&laquo;&laquo;</span>
                </a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}" aria-label="Anterior">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
            {% else %}
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Primeira">
                    <span aria-hidden="true">&laquo;&laquo;</span>
                </a>
            </li>
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Anterior">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
            {% endif %}
            
            {% for num in page_obj.paginator.page_range %}
                {% if page_obj.number == num %}
                <li class="page-item active"><a class="page-link" href="?page={{ num }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">{{ num }}</a></li>
                {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                <li class="page-item"><a class="page-link" href="?page={{ num }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}">{{ num }}</a></li>
                {% endif %}
            {% endfor %}
            
            {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}" aria-label="Próxima">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}{% if search_query %}&search={{ search_query }}{% endif %}{% if request.GET.order_by %}&order_by={{ request.GET.order_by }}{% endif %}{% if request.GET.order_dir %}&order_dir={{ request.GET.order_dir }}{% endif %}{% if request.GET.turma %}&turma={{ request.GET.turma }}{% endif %}{% if request.GET.data_inicio_min %}&data_inicio_min={{ request.GET.data_inicio_min }}{% endif %}{% if request.GET.data_fim_max %}&data_fim_max={{ request.GET.data_fim_max }}{% endif %}" aria-label="Última">
                    <span aria-hidden="true">&raquo;&raquo;</span>
                </a>
            </li>
            {% else %}
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Próxima">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
            <li class="page-item




## atividades\tests\test_models.py

python
from django.test import TestCase
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from cursos.models import Curso
from datetime import date

class AtividadeAcademicaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        
    def test_criar_atividade(self):
        atividade = AtividadeAcademica.objects.create(
            nome='Aula de Matemática',
            descricao='Aula introdutória sobre álgebra.',
            data_inicio=date(2023, 2, 1),
            data_fim=date(2023, 2, 28),
            turma=self.turma
        )
        
        self.assertEqual(atividade.nome, 'Aula de Matemática')
        self.assertEqual(atividade.descricao, 'Aula introdutória sobre álgebra.')
        self.assertEqual(str(atividade), 'Aula de Matemática')




## atividades\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from cursos.models import Curso
from datetime import date

class AtividadeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            codigo_curso='CUR01',
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        self.atividade = AtividadeAcademica.objects.create(
            nome='Aula de Matemática',
            descricao='Aula introdutória sobre álgebra.',
            data_inicio=date(2023, 2, 1),
            data_fim=date(2023, 2, 28),
            turma=self.turma
        )

    def test_listar_atividades(self):
        response = self.client.get(reverse('atividades:academica_lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aula de Matemática')

    def test_criar_atividade(self):
        response = self.client.get(reverse('atividades:academica_criar'))
        self.assertEqual(response.status_code, 200)


