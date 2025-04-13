# Revisão da Funcionalidade: turmas

## Arquivos forms.py:


### Arquivo: turmas\forms.py

```python
from django import forms
from importlib import import_module  # Add this import
from .models import Turma, Matricula  # Importe os modelos necessários


def get_matricula_model():
    """Obtém o modelo Matricula dinamicamente."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Matricula")


def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_curso_model():
    cursos_module = import_module("cursos.models")
    return getattr(cursos_module, "Curso")


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = [
            "nome",
            "curso",
            "data_inicio",
            "data_fim",
            "capacidade",
            "status",
            "descricao",
        ]
        widgets = {
            "data_inicio": forms.DateInput(attrs={"type": "date"}),
            "data_fim": forms.DateInput(attrs={"type": "date"}),
            "descricao": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["curso"].queryset = get_curso_model().objects.all()

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")
        if data_inicio and data_fim and data_inicio >= data_fim:
            raise forms.ValidationError(
                "A data de início deve ser anterior à data de fim."
            )
        return cleaned_data


class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula  # or get_matricula_model() if you're using dynamic imports
        fields = ["aluno", "turma"]  # Make sure 'data_matricula' is NOT in this list
        widgets = {
            "aluno": forms.Select(attrs={"class": "form-control"}),
            "turma": forms.Select(attrs={"class": "form-control"}),
            # Make sure there's NO line for 'data_matricula' here
        }

    def __init__(self, *args, **kwargs):
        turma = kwargs.pop("turma", None)
        super().__init__(*args, **kwargs)

        if turma:
            # Filtra alunos pelo curso da turma
            self.fields["aluno"].queryset = get_aluno_model().objects.filter(
                curso=turma.curso
            )
            self.fields["aluno"].queryset = self.fields["aluno"].queryset.filter(
                curso=turma.curso
            )

```

## Arquivos views.py:


### Arquivo: turmas\views.py

```python
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
```

## Arquivos urls.py:


### Arquivo: turmas\urls.py

```python
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

```

## Arquivos models.py:


### Arquivo: turmas\models.py

```python
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone  # Adicione esta linha
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
```

## Arquivos de Template:


### Arquivo: turmas\templates\turmas\cancelar_matricula.html

```html
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

```


### Arquivo: turmas\templates\turmas\confirmar_cancelamento_matricula.html

```html
{% extends 'base.html' %}

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

```


### Arquivo: turmas\templates\turmas\criar_turma.html

```html
{% extends 'base.html' %}

{% block title %}Criar Nova Turma{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Criar Nova Turma</h1>

    <form method="post">
        {% csrf_token %}

        {% for field in form %}
            <div class="form-group">
                <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                {{ field }}
                {% if field.help_text %}
                    <small class="form-text text-muted">{{ field.help_text }}</small>
                {% endif %}
                {% for error in field.errors %}
                    <div class="alert alert-danger">{{ error }}</div>
                {% endfor %}
            </div>
        {% endfor %}

        <button type="submit" class="btn btn-primary">Salvar</button>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}


```


### Arquivo: turmas\templates\turmas\detalhar_turma.html

```html
{% extends 'base.html' %}

{% block title %}Detalhes da Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Detalhes da Turma: {{ turma.nome }}</h1>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    <div class="card mb-4">
        <div class="card-body">
            <h5 class="card-title">Informações da Turma</h5>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Data de Início:</strong> {{ turma.data_inicio|date:"d/m/Y" }}</p>
            <p><strong>Data de Fim:</strong> {{ turma.data_fim|date:"d/m/Y" }}</p>
            <p><strong>Status:</strong> {{ turma.get_status_display }}</p>
            <p><strong>Capacidade:</strong> {{ turma.capacidade }}</p>
            <p><strong>Alunos Matriculados:</strong> {{ total_matriculas }}</p>
            <p><strong>Vagas Disponíveis:</strong> {{ vagas_disponiveis }}</p>
            <p><strong>Descrição:</strong> {{ turma.descricao|default:"Não informada" }}</p>
        </div>
    </div>

    <h2>Alunos Matriculados</h2>
    <div class="table-responsive">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Matrícula</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for matricula in matriculas %}
                <tr>
                    <td>{{ matricula.aluno.nome }}</td>
                    <td>{{ matricula.aluno.matricula }}</td>
                    <td>
                        <a href="{% url 'turmas:cancelar_matricula' turma.id matricula.aluno.id %}" class="btn btn-sm btn-danger">Cancelar Matrícula</a>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="3" class="text-center">Nenhum aluno matriculado nesta turma.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="mt-4">
        <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary">Matricular Novo Aluno</a>
        <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-warning">Editar Turma</a>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Voltar para Lista de Turmas</a>
    </div>
</div>
{% endblock %}


```


### Arquivo: turmas\templates\turmas\detalhes_turma.html

```html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}

```


### Arquivo: turmas\templates\turmas\editar_turma.html

```html
{% extends 'base.html' %}

{% block title %}Editar Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Turma: {{ turma.nome }}</h1>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    <form method="post">
        {% csrf_token %}

        {% for field in form %}
            <div class="form-group">
                <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                {{ field }}
                {% if field.help_text %}
                    <small class="form-text text-muted">{{ field.help_text }}</small>
                {% endif %}
                {% for error in field.errors %}
                    <div class="alert alert-danger">{{ error }}</div>
                {% endfor %}
            </div>
        {% endfor %}

        <div class="mt-4">
            <button type="submit" class="btn btn-primary">Salvar Alterações</button>
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}


```


### Arquivo: turmas\templates\turmas\excluir_turma.html

```html
{% extends 'base.html' %}

{% block title %}Excluir Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Turma: {{ turma.nome }}</h1>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    <div class="alert alert-danger">
        <p>Você tem certeza que deseja excluir esta turma?</p>
        <p><strong>Atenção:</strong> Esta ação não pode ser desfeita.</p>
    </div>

    <form method="post">
        {% csrf_token %}
        <div class="mt-4">
            <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}


```


### Arquivo: turmas\templates\turmas\listar_alunos_matriculados.html

```html
{% extends 'base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>{{ titulo }}</h1>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome da Turma:</strong> {{ turma.nome }}</p>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Período:</strong> {{ turma.data_inicio|date:"d/m/Y" }} a {{ turma.data_fim|date:"d/m/Y" }}</p>
            <p><strong>Total de Alunos:</strong> {{ turma.total_alunos }} de {{ turma.vagas }}</p>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Alunos Matriculados</h5>
            <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary btn-sm">
                <i class="fas fa-plus"></i> Matricular Aluno
            </a>
        </div>
        <div class="card-body">
            {% if alunos %}
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Nome</th>
                                <th>Matrícula</th>
                                <th>Curso</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for aluno in alunos %}
                                <tr>
                                    <td>{{ aluno.nome }}</td>
                                    <td>{{ aluno.matricula }}</td>
                                    <td>{{ aluno.curso.nome }}</td>
                                    <td>
                                        <a href="{% url 'alunos:detalhar_aluno' aluno.id %}" class="btn btn-info btn-sm">
                                            <i class="fas fa-eye"></i>
                                        </a>
                                        <a href="{% url 'turmas:cancelar_matricula' turma.id aluno.id %}" class="btn btn-danger btn-sm">
                                            <i class="fas fa-times"></i> Cancelar Matrícula
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <p>Nenhum aluno matriculado nesta turma.</p>
            {% endif %}
        </div>
    </div>
    
    <a href="{% url 'turmas:detalhes_turma' turma.id %}" class="btn btn-secondary mt-3">Voltar para Detalhes da Turma</a>
</div>
{% endblock %}

```


### Arquivo: turmas\templates\turmas\listar_turmas.html

```html
{% extends 'base.html' %}

{% block title %}Lista de Turmas{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Lista de Turmas</h1>

    <form method="get" class="mb-3">
        <div class="row">
            <div class="col-md-4">
                <input type="text" name="q" class="form-control" placeholder="Buscar turmas..." value="{{ query }}">
            </div>
            <div class="col-md-3">
                <select name="curso" class="form-control">
                    <option value="">Todos os cursos</option>
                    {% for curso in cursos %}
                        <option value="{{ curso.codigo_curso }}" {% if curso.codigo_curso|stringformat:"s" == curso_selecionado %}selected{% endif %}>
                            {{ curso.nome }}
                        </option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-3">
                <select name="status" class="form-control">
                    <option value="">Todos os status</option>
                    {% for status_value, status_label in opcoes_status %}
                        <option value="{{ status_value }}" {% if status_value == status_selecionado %}selected{% endif %}>
                            {{ status_label }}
                        </option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-2">
                <button type="submit" class="btn btn-primary">Filtrar</button>
            </div>
        </div>
    </form>

    <table class="table table-striped">
        <thead>
            <tr>
                <th>Nome</th>
                <th>Curso</th>
                <th>Data de Início</th>
                <th>Data de Fim</th>
                <th>Status</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for turma in turmas %}
            <tr>
                <td>{{ turma.nome }}</td>
                <td>{{ turma.curso.nome }}</td>
                <td>{{ turma.data_inicio|date:"d/m/Y" }}</td>
                <td>{{ turma.data_fim|date:"d/m/Y" }}</td>
                <td>{{ turma.get_status_display }}</td>
                <td>
                    <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-sm btn-info">Detalhes</a>
                    <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-sm btn-warning">Editar</a>
                    <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-sm btn-danger">Excluir</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="6">Nenhuma turma encontrada.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    {% if turmas.has_other_pages %}
    <nav>
        <ul class="pagination">
            {% if turmas.has_previous %}
                <li class="page-item"><a class="page-link" href="?page={{ turmas.previous_page_number }}">Anterior</a></li>
            {% endif %}

            {% for i in turmas.paginator.page_range %}
                {% if turmas.number == i %}
                    <li class="page-item active"><span class="page-link">{{ i }}</span></li>
                {% else %}
                    <li class="page-item"><a class="page-link" href="?page={{ i }}">{{ i }}</a></li>
                {% endif %}
            {% endfor %}

            {% if turmas.has_next %}
                <li class="page-item"><a class="page-link" href="?page={{ turmas.next_page_number }}">Próxima</a></li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}

    <a href="{% url 'turmas:criar_turma' %}" class="btn btn-primary">Criar Nova Turma</a>
</div>
{% endblock %}


```


### Arquivo: turmas\templates\turmas\matricular_aluno.html

```html
{% extends 'base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>{{ titulo }}</h1>
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome da Turma:</strong> {{ turma.nome }}</p>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Período:</strong> {{ turma.data_inicio|date:"d/m/Y" }} a {{ turma.data_fim|date:"d/m/Y" }}</p>
            <p><strong>Vagas Disponíveis:</strong> {{ turma.vagas_disponiveis }} de {{ turma.vagas }}</p>
        </div>
    </div>
    
    <div class="card mt-4">
        <div class="card-header">
            <h5 class="mb-0">Selecionar Aluno</h5>
        </div>
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="{{ form.aluno.id_for_label }}" class="form-label">Aluno</label>
                    {{ form.aluno }}
                    {% if form.aluno.errors %}
                        <div class="text-danger">{{ form.aluno.errors }}</div>
                    {% endif %}
                </div>
                
                <div class="d-flex justify-content-between">
                    <a href="{% url 'turmas:detalhes_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Matricular</button>
                </div>
            </form>
        </div>
    </div>
    
    <a href="javascript:history.back()" class="btn btn-secondary mt-3">Voltar</a>
</div>
{% endblock %}

```


### Arquivo: turmas\templates\turmas\turma_form.html

```html
{% extends 'base.html' %}

{% block content %}
  <h1>Criar Turma</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Criar</button>
  </form>
{% endblock %}
```
