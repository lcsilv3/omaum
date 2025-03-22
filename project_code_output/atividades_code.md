# Código da Funcionalidade: atividades
*Gerado automaticamente*



## atividades\admin.py

python
from django.contrib import admin
from .models import AtividadeAcademica, AtividadeRitualistica

@admin.register(AtividadeAcademica)
class AtividadeAcademicaAdmin(admin.ModelAdmin):
    list_display = ['nome']  # Ajuste conforme os campos do seu modelo

@admin.register(AtividadeRitualistica)
class AtividadeRitualisticaAdmin(admin.ModelAdmin):
    list_display = ['nome']  # Ajuste conforme os campos do seu modelo




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

# Views para Atividades Acadêmicas
class AcademicaListaView(ListView):
    model = AtividadeAcademica
    template_name = 'atividades/academica_lista.html'
    context_object_name = 'atividades'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(nome__icontains=search_query)
        return queryset

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

# Add these missing views
class RitualisticaEditarView(UpdateView):
    model = AtividadeRitualistica
    form_class = AtividadeRitualisticaForm
    template_name = 'atividades/atividade_ritualistica_form.html'
    success_url = reverse_lazy('atividades:ritualistica_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Atividade ritualística atualizada com sucesso!')
        return super().form_valid(form)

class RitualisticaExcluirView(DeleteView):
    model = AtividadeRitualistica
    template_name = 'atividades/academica_confirmar_exclusao.html'  # Reuse the same template
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




## atividades\templates\atividades\academica_lista.html

html
{% extends "base.html" %}

{% block title %}Nova Atividade Acadêmica{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Nova Atividade Acadêmica</h1>
    
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
            <a href="{% url 'atividades:academica_criar' %}" class="btn btn-primary">Nova Atividade</a>
        </div>
    </form>
</div>
{% endblock %}




## atividades\templates\atividades\atividade_ritualistica_form.html

html
{% extends 'base.html' %}

{% block content %}
<h1>Criar Atividade Ritualística</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Salvar</button>
</form>
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



## atividades\templates\atividades\cadastrar_turma.html

html
{% extends "base.html" %}

{% block content %}
<h1>Cadastrar Turma</h1>
<!-- Your form and other content here -->
{% endblock %}




## atividades\templates\atividades\editar_atividade_academica.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Atividade Acadêmica</h1>
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        <button type="submit" class="btn btn-primary">Atualizar Atividade Acadêmica</button>
        <a href="{% url 'atividades:academica_lista' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




## atividades\templates\atividades\editar_atividade_ritualistica.html

html
{% extends 'base.html' %}

{% block content %}
<h1>Editar Atividade Ritualística</h1>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Salvar</button>
</form>
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



## atividades\templates\atividades\formulario_atividade_academica.html

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




## atividades\templates\atividades\ritualistica_confirmar_exclusao.html

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




## atividades\templates\atividades\ritualistica_lista.html

html
{% extends 'base.html' %}

{% block content %}
<h1>Atividades Ritualísticas</h1>
<a href="{% url 'atividades:ritualistica_criar' %}">Criar Nova Atividade Ritualística</a>
<ul>{% for atividade in object_list %}<li>
    {{ atividade.nome }} - {{ atividade.turma }}
    <a href="{% url 'atividades:ritualistica_editar' atividade.pk %}">Editar</a>
</li>{% empty %}<li>Nenhuma atividade ritualística encontrada.</li>{% endfor %}</ul>
{% endblock %}




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
from atividades.models import AtividadeAcademica, Atividade

class AtividadeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.atividade = AtividadeAcademica.objects.create(
            codigo_atividade='ATV001',
            nome='Aula de Matemática',
            descricao='Aula introdutória sobre álgebra.'
        )

    def test_listar_atividades(self):
        response = self.client.get(reverse('listar_atividades_academicas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aula de Matemática')
        self.assertContains(response, 'ATV001')

    def test_detalhe_atividade(self):
        response = self.client.get(reverse('detalhe_atividade', args=[self.atividade.codigo_atividade]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.atividade.nome)
        self.assertContains(response, self.atividade.descricao)

class RitualisticaExcluirView(DeleteView):
    model = AtividadeRitualistica
    template_name = 'atividades/ritualistica_confirmar_exclusao.html'  # Change this line
    success_url = reverse_lazy('atividades:ritualistica_lista')


