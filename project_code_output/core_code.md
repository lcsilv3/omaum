# Código da Funcionalidade: core
*Gerado automaticamente*



## core\admin.py

python
from django.contrib import admin
from .models import Aluno, Categoria, Item

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'data_nascimento', 'ativo')
    search_fields = ('nome', 'email', 'telefone')
    list_filter = ('ativo', 'data_cadastro')
    list_editable = ('ativo',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'data_criacao')
    search_fields = ('nome',)
    list_filter = ('data_criacao',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'disponivel', 'data_criacao')
    list_filter = ('categoria', 'disponivel', 'data_criacao')
    search_fields = ('nome', 'descricao')
    list_editable = ('preco', 'disponivel')




## core\apps.py

python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'




## core\forms.py

python
from django import forms
from core.models import Aluno, Curso, Turma, AtividadeAcademica, AtividadeRitualistica
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ('nome', 'matricula', 'curso')

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ('nome', 'descricao')

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ('nome', 'curso', 'data_inicio', 'data_fim', 'vagas')

class AtividadeAcademicaForm(forms.ModelForm):
    class Meta:
        model = AtividadeAcademica
        fields = ('nome', 'descricao', 'data', 'turma')

class AtividadeRitualisticaForm(forms.ModelForm):
    class Meta:
        model = AtividadeRitualistica
        fields = ['nome', 'descricao', 'turma', 'alunos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turma'].queryset = Turma.objects.all()
        self.fields['alunos'].queryset = Aluno.objects.all()
        self.fields['alunos'].widget = forms.CheckboxSelectMultiple()

class AlunoTurmaForm(forms.Form):
    aluno = forms.ModelChoiceField(queryset=Aluno.objects.all(), label="Aluno")

    def __init__(self, *args, **kwargs):
        turma = kwargs.pop('turma', None)
        super().__init__(*args, **kwargs)
        if turma:
            self.fields['aluno'].queryset = Aluno.objects.exclude(turmas=turma)

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



## core\models.py

python
from django.db import models
from django.utils import timezone

class Aluno(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    data_cadastro = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Item(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='itens')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'



## core\tests.py

python
from django.test import TestCase

# Create your tests here.




## core\urls.py

python
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('alunos/', views.lista_alunos, name='lista_alunos'),
    path('alunos/<int:aluno_id>/', views.detalhe_aluno, name='detalhe_aluno'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/<int:categoria_id>/', views.detalhe_categoria, name='detalhe_categoria'),
    path('itens/', views.lista_itens, name='lista_itens'),
    path('itens/<int:item_id>/', views.detalhe_item, name='detalhe_item'),
    path('atividades/', views.academica_lista, name='academica_lista'),
    path('atividades/<int:atividade_id>/', views.academica_detalhe, name='academica_detalhe'),
    path('atividades/ritualistica/', views.ritualistica_lista, name='ritualistica_lista'),
    path('atividades/ritualistica/<int:atividade_id>/', views.ritualistica_detalhe, name='ritualistica_detalhe'),
]



## core\views.py

python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from core.models import Aluno, Curso, Turma
from core.forms import AlunoForm, CursoForm, TurmaForm, AlunoTurmaForm
from django.contrib.auth import login, authenticate
from .forms import RegistroForm

def home(request):
    return render(request, 'core/home.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

# Aluno views
@login_required
def aluno_list(request):
    alunos = Aluno.objects.all()
    return render(request, 'core/listar_alunos.html', {'alunos': alunos})

@login_required
def aluno_create(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:listar_alunos')
    else:
        form = AlunoForm()
    return render(request, 'core/aluno_form.html', {'form': form})

@login_required
def aluno_detail(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request, 'core/aluno_detail.html', {'aluno': aluno})

@login_required
def aluno_update(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('core:listar_alunos')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'core/aluno_form.html', {'form': form})

@login_required
def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        aluno.delete()
        return redirect('core:listar_alunos')
    return render(request, 'core/aluno_confirm_delete.html', {'aluno': aluno})

# Turma views
@login_required
def turma_list(request):
    turmas = Turma.objects.all()
    return render(request, 'core/turma_list.html', {'turmas': turmas})

@login_required
def turma_create(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:listar_turmas')
    else:
        form = TurmaForm()
    return render(request, 'core/turma_form.html', {'form': form})

@login_required
def turma_detail(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    return render(request, 'core/turma_detail.html', {'turma': turma})

@login_required
def turma_update(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return redirect('core:listar_turmas')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'core/turma_form.html', {'form': form})

@login_required
def turma_delete(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        turma.delete()
        return redirect('core:listar_turmas')
    return render(request, 'core/turma_confirm_delete.html', {'turma': turma})

# Presença views
@login_required
def listar_presencas_academicas(request):
    # Adicione a lógica para listar presenças acadêmicas
    pass

# Cargo views
@login_required
def listar_cargos_administrativos(request):
    # Adicione a lógica para listar cargos administrativos
    pass

# Relatório views
@login_required
def relatorio_alunos(request):
    # Adicione a lógica para gerar relatórios de alunos
    pass

# Punição views
@login_required
def listar_punicoes(request):
    # Adicione a lógica para listar punições
    pass

# Iniciação views
@login_required
def listar_iniciacoes(request):
    # Adicione a lógica para listar iniciações
    pass
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        # Forçar a geração do token CSRF
        csrf_token = get_token(request)

        logger.info(f"GET CSRF cookie: {request.META.get('CSRF_COOKIE')}")
        logger.info(f"GET CSRF token: {csrf_token}")
        response = super().get(request, *args, **kwargs)
        response.set_cookie('csrftoken', csrf_token, httponly=False, samesite='Lax')
        return response

    def post(self, request, *args, **kwargs):
        logger.info(f"POST CSRF cookie: {request.META.get('CSRF_COOKIE')}")
        logger.info(f"POST CSRF token: {request.POST.get('csrfmiddlewaretoken')}")
        return super().post(request, *args, **kwargs)

def test_csrf(request):
    csrf_token = get_token(request)
    return HttpResponse(f"CSRF Token: {csrf_token}")
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registro.html'

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Aluno, Categoria, Item

def lista_alunos(request):
    alunos = Aluno.objects.filter(ativo=True)
    return render(request, 'core/lista_alunos.html', {'alunos': alunos})

def detalhe_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    return render(request, 'core/detalhe_aluno.html', {'aluno': aluno})

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'core/lista_categorias.html', {'categorias': categorias})

def detalhe_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    itens = categoria.itens.all()
    return render(request, 'core/detalhe_categoria.html', {
        'categoria': categoria,
        'itens': itens
    })

def lista_itens(request):
    itens = Item.objects.filter(disponivel=True)
    return render(request, 'core/lista_itens.html', {'itens': itens})

def detalhe_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'core/detalhe_item.html', {'item': item})




## core\templates\core\base.html

html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sistema{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Sistema</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'core:lista_categorias' %}">Categorias</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'core:lista_itens' %}">Itens</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>




## core\templates\core\lista_categorias.html

html
{% extends "core/base.html" %}

{% block title %}Categorias{% endblock %}

{% block content %}
    <h1>Categorias</h1>
    
    <div class="row mt-4">
        {% for categoria in categorias %}
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ categoria.nome }}</h5>
                        <p class="card-text">{{ categoria.descricao|truncatewords:20 }}</p>
                        <a href="{% url 'core:detalhe_categoria' categoria.id %}" class="btn btn-primary">Ver detalhes</a>
                    </div>
                </div>
            </div>
        {% empty %}
            <div class="col-12">
                <p>Nenhuma categoria encontrada.</p>
            </div>
        {% endfor %}
    </div>
{% endblock %}


