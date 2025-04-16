# Revisão da Funcionalidade: turmas

## Arquivos forms.py:


### Arquivo: turmas\forms.py

```python
from django import forms
from .models import Turma
from django.core.exceptions import ValidationError
from django.utils import timezone
from importlib import import_module  # Add this import


def get_aluno_model():
    """Obtém o modelo Aluno dinamicamente."""
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = [
            "nome",
            "curso",
            "vagas",
            "status",
            "data_inicio",
            "data_fim",
            "instrutor",
            "instrutor_auxiliar",
            "auxiliar_instrucao",
            "dias_semana",
            "local",
            "horario",
            "descricao",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "curso": forms.Select(attrs={"class": "form-select"}),
            "vagas": forms.NumberInput(
                attrs={"class": "form-control", "min": "1"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "instrutor": forms.Select(attrs={"class": "form-control"}),
            "instrutor_auxiliar": forms.Select(
                attrs={"class": "form-control"}
            ),
            "auxiliar_instrucao": forms.Select(
                attrs={"class": "form-control"}
            ),
            "dias_semana": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "horario": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }
        help_texts = {
            "vagas": "Número máximo de alunos que podem ser matriculados na turma.",
            "data_inicio": "Data de início das aulas.",
            "data_fim": "Data prevista para o término das aulas.",
            "status": "Status atual da turma.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert date format for display in the form
        if self.instance and self.instance.pk:
            if self.instance.data_inicio:
                self.initial[
                    "data_inicio"
                ] = self.instance.data_inicio.strftime("%Y-%m-%d")
            if self.instance.data_fim:
                self.initial["data_fim"] = self.instance.data_fim.strftime(
                    "%Y-%m-%d"
                )

        # Tornar os campos de instrutores opcionais
        self.fields["instrutor"].required = False
        self.fields["instrutor_auxiliar"].required = False
        self.fields["auxiliar_instrucao"].required = False

        # Configurar os querysets para mostrar apenas alunos elegíveis
        Aluno = get_aluno_model()
        alunos_elegíveis = Aluno.objects.filter(situacao="A")

        # Filtrar alunos que podem ser instrutores
        alunos_instrutores = [
            aluno for aluno in alunos_elegíveis if aluno.pode_ser_instrutor
        ]

        self.fields["instrutor"].queryset = Aluno.objects.filter(
            cpf__in=[a.cpf for a in alunos_instrutores]
        )
        self.fields["instrutor_auxiliar"].queryset = Aluno.objects.filter(
            cpf__in=[a.cpf for a in alunos_instrutores]
        )
        self.fields["auxiliar_instrucao"].queryset = Aluno.objects.filter(
            cpf__in=[a.cpf for a in alunos_instrutores]
        )

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_fim = cleaned_data.get("data_fim")

        # Validar que a data de início é anterior à data de fim
        if data_inicio and data_fim and data_inicio > data_fim:
            raise ValidationError(
                "A data de início não pode ser posterior à data de fim."
            )

        # Validar que a data de início não é no passado (para novas turmas)
        if (
            not self.instance.pk
            and data_inicio
            and data_inicio < timezone.now().date()
        ):
            raise ValidationError(
                "A data de início não pode ser no passado para novas turmas."
            )

        # Verificar se os instrutores são diferentes entre si
        instrutor = cleaned_data.get("instrutor")
        instrutor_auxiliar = cleaned_data.get("instrutor_auxiliar")
        auxiliar_instrucao = cleaned_data.get("auxiliar_instrucao")

        if (
            instrutor
            and instrutor_auxiliar
            and instrutor == instrutor_auxiliar
        ):
            self.add_error(
                "instrutor_auxiliar",
                "O instrutor auxiliar deve ser diferente do instrutor principal.",
            )

        if (
            instrutor
            and auxiliar_instrucao
            and instrutor == auxiliar_instrucao
        ):
            self.add_error(
                "auxiliar_instrucao",
                "O auxiliar de instrução deve ser diferente do instrutor principal.",
            )

        if (
            instrutor_auxiliar
            and auxiliar_instrucao
            and instrutor_auxiliar == auxiliar_instrucao
        ):
            self.add_error(
                "auxiliar_instrucao",
                "O auxiliar de instrução deve ser diferente do instrutor auxiliar.",
            )

        return cleaned_data

    def clean_nome(self):
        nome = self.cleaned_data.get("nome")
        if nome:
            # Verificar se já existe uma turma com o mesmo nome (ignorando case)
            instance_id = getattr(self.instance, "id", None)
            turmas_existentes = Turma.objects.filter(nome__iexact=nome)

            if instance_id:
                turmas_existentes = turmas_existentes.exclude(id=instance_id)

            if turmas_existentes.exists():
                raise ValidationError(
                    "Já existe uma turma com este nome. Por favor, escolha um nome diferente."
                )

            # Opcional: normalizar o nome (por exemplo, primeira letra maiúscula)
            nome = nome.strip().capitalize()

        return nome

```

## Arquivos views.py:


### Arquivo: turmas\views.py

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from importlib import import_module
from django.core.exceptions import ValidationError

# Import your Turma model
from .models import Turma


# Define functions to get models dynamically
def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_matricula_model():
    matriculas_module = import_module("matriculas.models")
    return getattr(matriculas_module, "Matricula")


@login_required
def listar_turmas(request):
    """Lista todas as turmas cadastradas."""
    turmas = Turma.objects.all()
    return render(request, "turmas/listar_turmas.html", {"turmas": turmas})


@login_required
def criar_turma(request):
    """Cria uma nova turma."""
    # Implementation here
    pass


@login_required
def detalhar_turma(request, id):
    """Exibe os detalhes de uma turma."""
    # Implementation here
    pass


@login_required
def editar_turma(request, id):
    """Edita uma turma existente."""
    # Implementation here
    pass


@login_required
def excluir_turma(request, id):
    """Exclui uma turma."""
    # Implementation here
    pass


@login_required
def dashboard_turmas(request):
    """Exibe o dashboard de turmas."""
    # Implementation here
    pass


@login_required
def listar_alunos_matriculados(request, id):
    """Lista os alunos matriculados em uma turma."""
    # Implementation here
    pass

```

## Arquivos urls.py:


### Arquivo: turmas\urls.py

```python
from django.urls import path
from . import views

app_name = "turmas"

urlpatterns = [
    path("", views.listar_turmas, name="listar_turmas"),
    path("criar/", views.criar_turma, name="criar_turma"),
    path("<int:id>/", views.detalhar_turma, name="detalhar_turma"),
    path("<int:id>/editar/", views.editar_turma, name="editar_turma"),
    path("<int:id>/excluir/", views.excluir_turma, name="excluir_turma"),
    path(
        "<int:id>/adicionar-aluno/",
        views.adicionar_aluno_turma,
        name="matricular_aluno",
    ),
    path(
        "<int:id>/matricular-aluno/",
        views.adicionar_aluno_turma,
        name="matricular_aluno",
    ),
    path(
        "<int:turma_id>/remover-aluno/<str:aluno_id>/",
        views.remover_aluno_turma,
        name="remover_aluno_turma",
    ),
    path("dashboard/", views.dashboard_turmas, name="dashboard"),
    path(
        "<int:id>/alunos/",
        views.listar_alunos_matriculados,
        name="listar_alunos_matriculados",
    ),
]

```

## Arquivos models.py:


### Arquivo: turmas\models.py

```python
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Turma(models.Model):
    """
    Modelo para representar uma turma no sistema OMAUM.
    """

    STATUS_CHOICES = [
        ("A", "Ativa"),
        ("I", "Inativa"),
        ("C", "Concluída"),
    ]

    # Informações básicas
    nome = models.CharField(max_length=100, verbose_name="Nome da Turma")
    curso = models.ForeignKey(
        "cursos.Curso",
        on_delete=models.CASCADE,
        verbose_name="Curso",
        related_name="turmas",
    )
    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )

    # Datas
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Término")

    # Informações de agendamento
    dias_semana = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Dias da Semana"
    )
    local = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Local"
    )
    horario = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Horário"
    )

    # Capacidade e status
    vagas = models.PositiveIntegerField(
        default=20,
        validators=[MinValueValidator(1)],
        verbose_name="Número de Vagas",
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default="A",
        verbose_name="Status",
    )

    # Instrutores
    instrutor = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="turmas_como_instrutor",
        verbose_name="Instrutor Principal",
    )
    instrutor_auxiliar = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="turmas_como_instrutor_auxiliar",
        verbose_name="Instrutor Auxiliar",
    )
    auxiliar_instrucao = models.ForeignKey(
        "alunos.Aluno",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="turmas_como_auxiliar_instrucao",
        verbose_name="Auxiliar de Instrução",
    )

    # Metadados
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Criado em"
    )
    updated_at = models.DateTimeField(
        default=timezone.now, verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ["-data_inicio"]

    def __str__(self):
        return f"{self.nome} - {self.curso.nome}"

    @property
    def vagas_disponiveis(self):
        """Retorna o número de vagas disponíveis na turma."""
        vagas_ocupadas = self.matriculas.filter(status="A").count()
        return self.vagas - vagas_ocupadas

    @property
    def esta_ativa(self):
        """Verifica se a turma está ativa."""
        return self.status == "A"

    @property
    def esta_em_andamento(self):
        """Verifica se a turma está em andamento (começou mas não terminou)."""
        hoje = timezone.now().date()
        return self.data_inicio <= hoje <= self.data_fim and self.status == "A"

    def clean(self):
        super().clean()

        # Verificar se já existe uma turma com o mesmo nome (ignorando case)
        if self.nome:
            turmas_existentes = Turma.objects.filter(nome__iexact=self.nome)

            # Excluir a própria instância se estiver editando
            if self.pk:
                turmas_existentes = turmas_existentes.exclude(pk=self.pk)

            if turmas_existentes.exists():
                raise ValidationError(
                    {
                        "nome": "Já existe uma turma com este nome. Por favor, escolha um nome diferente."
                    }
                )

```

## Arquivos de Template:


### Arquivo: turmas\templates\turmas\adicionar_aluno.html

```html
{% extends 'base.html' %}

{% block title %}Adicionar Aluno à Turma{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Adicionar Aluno à Turma: {{ turma.nome }}</h1>
        <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Voltar para Turma</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Selecione um Aluno</h5>
        </div>
        <div class="card-body">
            {% if alunos %}
                <form method="post" class="mb-4">
                    {% csrf_token %}
                    
                    <div class="mb-3">
                        <label for="id_aluno" class="form-label">Aluno</label>
                        <select name="aluno" id="id_aluno" class="form-select" required>
                            <option value="">Selecione um aluno</option>
                            {% for aluno in alunos %}
                                <option value="{{ aluno.cpf }}">{{ aluno.nome }} (CPF: {{ aluno.cpf }})</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="d-flex justify-content-between">
                        <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
                        <button type="submit" class="btn btn-primary">Adicionar Aluno</button>
                    </div>
                </form>
                
                <div class="mt-3">
                    <p><strong>Informações da Turma:</strong></p>
                    <ul>
                        <li><strong>Nome:</strong> {{ turma.nome }}</li>
                        <li><strong>Curso:</strong> {{ turma.curso }}</li>
                        <li><strong>Vagas Disponíveis:</strong> {{ turma.vagas_disponiveis }}</li>
                        <li><strong>Status:</strong> {{ turma.get_status_display }}</li>
                    </ul>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <p>Não há alunos disponíveis para matricular nesta turma.</p>
                    <p>Possíveis razões:</p>
                    <ul>
                        <li>Todos os alunos já estão matriculados nesta turma</li>
                        <li>Não há alunos cadastrados no sistema</li>
                    </ul>
                </div>
                <a href="{% url 'alunos:criar_aluno' %}" class="btn btn-primary">Cadastrar Novo Aluno</a>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Add select2 for better search experience if available
        if (typeof $.fn.select2 !== 'undefined') {
            $('#id_aluno').select2({
                placeholder: 'Selecione um aluno',
                width: '100%'
            });
        }
    });
</script>
{% endblock %}

```


### Arquivo: turmas\templates\turmas\cancelar_matricula.html

```html
{% extends 'base.html' %}

{% block title %}Cancelar Matrícula{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Cancelar Matrícula</h1>
    
    <div class="alert alert-warning">
        <p>Você está prestes a cancelar a matrícula do aluno <strong>{{ aluno.nome }}</strong> na turma <strong>{{ turma.nome }}</strong>.</p>
        <p>Esta ação não pode ser desfeita. Deseja continuar?</p>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Confirmar Cancelamento</button>
        <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Voltar</a>
    </form>
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
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Criar Nova Turma</h1>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Voltar para Lista</a>
    </div>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}

    <form method="post">
        {% csrf_token %}
        
        <div class="row">
            <!-- Informações Básicas -->
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Informações Básicas</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="{{ form.nome.id_for_label }}" class="form-label">{{ form.nome.label }}</label>
                            {{ form.nome }}
                            {% if form.nome.errors %}
                                <div class="text-danger">{{ form.nome.errors }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.curso.id_for_label }}" class="form-label">{{ form.curso.label }}</label>
                            {{ form.curso }}
                            {% if form.curso.errors %}
                                <div class="text-danger">{{ form.curso.errors }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.vagas.id_for_label }}" class="form-label">{{ form.vagas.label }}</label>
                            {{ form.vagas }}
                            {% if form.vagas.errors %}
                                <div class="text-danger">{{ form.vagas.errors }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.status.id_for_label }}" class="form-label">{{ form.status.label }}</label>
                            {{ form.status }}
                            {% if form.status.errors %}
                                <div class="text-danger">{{ form.status.errors }}</div>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Datas e Horários -->
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0">Datas e Horários</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="{{ form.data_inicio.id_for_label }}" class="form-label">{{ form.data_inicio.label }}</label>
                                {{ form.data_inicio }}
                                {% if form.data_inicio.errors %}
                                    <div class="text-danger">{{ form.data_inicio.errors }}</div>
                                {% endif %}
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label for="{{ form.data_fim.id_for_label }}" class="form-label">{{ form.data_fim.label }}</label>
                                {{ form.data_fim }}
                                {% if form.data_fim.errors %}
                                    <div class="text-danger">{{ form.data_fim.errors }}</div>
                                {% endif %}
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.horario.id_for_label }}" class="form-label">{{ form.horario.label }}</label>
                            {{ form.horario }}
                            {% if form.horario.errors %}
                                <div class="text-danger">{{ form.horario.errors }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.dias_semana.id_for_label }}" class="form-label">{{ form.dias_semana.label }}</label>
                            {{ form.dias_semana }}
                            {% if form.dias_semana.errors %}
                                <div class="text-danger">{{ form.dias_semana.errors }}</div>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Instrutores -->
        <div class="card mb-3">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0">Instrutores</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4 mb-3">
                        <label for="search-instrutor" class="form-label">Instrutor Principal</label>
                        <input type="text" id="search-instrutor" class="form-control" 
                               placeholder="Digite parte do CPF, nome ou número iniciático..." 
                               autocomplete="off">
                        <div id="search-results-instrutor" class="list-group mt-2" style="display: none;"></div>
                        <div id="selected-instrutor-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-instrutor-info">Nenhum instrutor selecionado</div>
                        </div>
                        {{ form.instrutor }}
                        {% if form.instrutor.errors %}
                            <div class="text-danger">{{ form.instrutor.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-4 mb-3">
                        <label for="search-instrutor-auxiliar" class="form-label">Instrutor Auxiliar</label>
                        <input type="text" id="search-instrutor-auxiliar" class="form-control" 
                               placeholder="Digite parte do CPF, nome ou número iniciático..." 
                               autocomplete="off">
                        <div id="search-results-instrutor-auxiliar" class="list-group mt-2" style="display: none;"></div>
                        <div id="selected-instrutor-auxiliar-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-instrutor-auxiliar-info">Nenhum instrutor selecionado</div>
                        </div>
                        {{ form.instrutor_auxiliar }}
                        {% if form.instrutor_auxiliar.errors %}
                            <div class="text-danger">{{ form.instrutor_auxiliar.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-4 mb-3">
                        <label for="search-auxiliar-instrucao" class="form-label">Auxiliar de Instrução</label>
                        <input type="text" id="search-auxiliar-instrucao" class="form-control" 
                               placeholder="Digite parte do CPF, nome ou número iniciático..." 
                               autocomplete="off">
                        <div id="search-results-auxiliar-instrucao" class="list-group mt-2" style="display: none;"></div>
                        <div id="selected-auxiliar-instrucao-container" class="p-3 border rounded mt-2 d-none">
                            <div id="selected-auxiliar-instrucao-info">Nenhum instrutor selecionado</div>
                        </div>
                        {{ form.auxiliar_instrucao }}
                        {% if form.auxiliar_instrucao.errors %}
                            <div class="text-danger">{{ form.auxiliar_instrucao.errors }}</div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Informações Adicionais -->
        <div class="card mb-3">
            <div class="card-header bg-secondary text-white">
                <h5 class="mb-0">Informações Adicionais</h5>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <label for="{{ form.descricao.id_for_label }}" class="form-label">{{ form.descricao.label }}</label>
                    {{ form.descricao }}
                    {% if form.descricao.errors %}
                        <div class="text-danger">{{ form.descricao.errors }}</div>
                    {% endif %}
                </div>
                
                <div class="mb-3">
                    <label for="{{ form.local.id_for_label }}" class="form-label">{{ form.local.label }}</label>
                    {{ form.local }}
                    {% if form.local.errors %}
                        <div class="text-danger">{{ form.local.errors }}</div>
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between">
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Criar Turma</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Esconder os campos select originais
        document.getElementById('{{ form.instrutor.id_for_label }}').style.display = 'none';
        document.getElementById('{{ form.instrutor_auxiliar.id_for_label }}').style.display = 'none';
        document.getElementById('{{ form.auxiliar_instrucao.id_for_label }}').style.display = 'none';
        
        // Configurar busca para Instrutor Principal
        setupInstructorSearch(
            'search-instrutor',
            'search-results-instrutor',
            'selected-instrutor-container',
            'selected-instrutor-info',
            '{{ form.instrutor.id_for_label }}'
        );
        
        // Configurar busca para Instrutor Auxiliar
        setupInstructorSearch(
            'search-instrutor-auxiliar',
            'search-results-instrutor-auxiliar',
            'selected-instrutor-auxiliar-container',
            'selected-instrutor-auxiliar-info',
            '{{ form.instrutor_auxiliar.id_for_label }}'
        );
        
        // Configurar busca para Auxiliar de Instrução
        setupInstructorSearch(
            'search-auxiliar-instrucao',
            'search-results-auxiliar-instrucao',
            'selected-auxiliar-instrucao-container',
            'selected-auxiliar-instrucao-info',
            '{{ form.auxiliar_instrucao.id_for_label }}'
        );
        
        // Inicializar valores selecionados se estiver editando
        initializeSelectedInstructors();
    });
    
    function setupInstructorSearch(searchId, resultsId, containerId, infoId, selectId) {
        const searchInput = document.getElementById(searchId);
        const searchResults = document.getElementById(resultsId);
        const selectedContainer = document.getElementById(containerId);
        const selectedInfo = document.getElementById(infoId);
        const selectElement = document.getElementById(selectId);
        
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            const query = this.value.trim();
            
            // Clear results if query is too short
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
                return;
            }
            
            // Set a timeout to avoid making too many requests
            searchTimeout = setTimeout(function() {
                // Show loading indicator
                searchResults.innerHTML = '<div class="list-group-item text-muted">Buscando...</div>';
                searchResults.style.display = 'block';
                
                // Get CSRF token
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                
                fetch(`/alunos/search/?q=${encodeURIComponent(query)}`, {
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    searchResults.innerHTML = '';
                    
                    if (data.error) {
                        // Handle error response
                        searchResults.innerHTML = `<div class="list-group-item text-danger">Erro ao buscar alunos: ${data.error}</div>`;
                        return;
                    }
                    
                    if (data.length === 0) {
                        searchResults.innerHTML = '<div class="list-group-item">Nenhum aluno encontrado</div>';
                        return;
                    }
                    
                    // Display results
                    data.forEach(aluno => {
                        const item = document.createElement('a');
                        item.href = '#';
                        item.className = 'list-group-item list-group-item-action';
                        item.innerHTML = `
                            <div class="d-flex justify-content-between">
                                <div>${aluno.nome}</div>
                                <div class="text-muted">
                                    <small>CPF: ${aluno.cpf}</small>
                                    ${aluno.numero_iniciatico !== "N/A" ? `<small class="ms-2">Nº: ${aluno.numero_iniciatico}</small>` : ''}
                                </div>
                            </div>
                        `;
                        
                        // Add click event to select this aluno
                        item.addEventListener('click', function(e) {
                            e.preventDefault();
                            selectInstructor(aluno, searchInput, searchResults, selectedContainer, selectedInfo, selectElement);
                        });
                        
                        searchResults.appendChild(item);
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                    searchResults.innerHTML = '<div class="list-group-item text-danger">Erro ao buscar alunos</div>';
                });
            }, 300);
        });
        
        // Hide results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
        
        // Function to select an aluno
        function selectInstructor(aluno, searchInput, searchResults, selectedContainer, selectedInfo, selectElement) {
            // Update the hidden select with the selected aluno's CPF
            selectElement.value = aluno.cpf;
            
            // Update the search input with the selected aluno's name
            searchInput.value = aluno.nome;
            
            // Show the selected aluno info
            selectedInfo.innerHTML = `
                <strong>${aluno.nome}</strong><br>
                CPF: ${aluno.cpf}<br>
                ${aluno.numero_iniciatico !== "N/A" ? `Número Iniciático: ${aluno.numero_iniciatico}` : ''}
            `;
            
            // Show the container
            selectedContainer.classList.remove('d-none');
            
            // Hide the search results
            searchResults.style.display = 'none';
        }
        
        function initializeSelectedInstructors() {
            // Verificar se há valores pré-selecionados (útil para edição)
            const instrutorSelect = document.getElementById('{{ form.instrutor.id_for_label }}');
            const instrutorAuxiliarSelect = document.getElementById('{{ form.instrutor_auxiliar.id_for_label }}');
            const auxiliarInstrucaoSelect = document.getElementById('{{ form.auxiliar_instrucao.id_for_label }}');
            
            // Inicializar instrutor principal se já estiver selecionado
            if (instrutorSelect.value) {
                fetchInstructorData(instrutorSelect.value, function(aluno) {
                    document.getElementById('search-instrutor').value = aluno.nome;
                    document.getElementById('selected-instrutor-info').innerHTML = `
                        <strong>${aluno.nome}</strong><br>
                        CPF: ${aluno.cpf}<br>
                        ${aluno.numero_iniciatico !== "N/A" ? `Número Iniciático: ${aluno.numero_iniciatico}` : ''}
                    `;
                    document.getElementById('selected-instrutor-container').classList.remove('d-none');
                });
            }
            
            // Inicializar instrutor auxiliar se já estiver selecionado
            if (instrutorAuxiliarSelect.value) {
                fetchInstructorData(instrutorAuxiliarSelect.value, function(aluno) {
                    document.getElementById('search-instrutor-auxiliar').value = aluno.nome;
                    document.getElementById('selected-instrutor-auxiliar-info').innerHTML = `
                        <strong>${aluno.nome}</strong><br>
                        CPF: ${aluno.cpf}<br>
                        ${aluno.numero_iniciatico !== "N/A" ? `Número Iniciático: ${aluno.numero_iniciatico}` : ''}
                    `;
                    document.getElementById('selected-instrutor-auxiliar-container').classList.remove('d-none');
                });
            }
            
            // Inicializar auxiliar de instrução se já estiver selecionado
            if (auxiliarInstrucaoSelect.value) {
                fetchInstructorData(auxiliarInstrucaoSelect.value, function(aluno) {
                    document.getElementById('search-auxiliar-instrucao').value = aluno.nome;
                    document.getElementById('selected-auxiliar-instrucao-info').innerHTML = `
                        <strong>${aluno.nome}</strong><br>
                        CPF: ${aluno.cpf}<br>
                        ${aluno.numero_iniciatico !== "N/A" ? `Número Iniciático: ${aluno.numero_iniciatico}` : ''}
                    `;
                    document.getElementById('selected-auxiliar-instrucao-container').classList.remove('d-none');
                });
            }
        }
        
        function fetchInstructorData(cpf, callback) {
            // Get CSRF token
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(`/alunos/get-aluno/${cpf}/`, {
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    callback(data.aluno);
                }
            })
            .catch(error => {
                console.error('Error fetching instructor data:', error);
            });
        }
    }
</script>
{% endblock %}

```


### Arquivo: turmas\templates\turmas\detalhar_turma.html

```html
{% extends 'base.html' %}

{% block title %}Detalhes da Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Cabeçalho com título e botões de ação -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Detalhes da Turma: {{ turma.nome }}</h1>
        <div>
            <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-warning me-2">
                <i class="fas fa-edit"></i> Editar
            </a>
            {% if not matriculas %}
                <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-danger">
                    <i class="fas fa-trash"></i> Excluir
                </a>
            {% endif %}
        </div>
    </div>
    
    <!-- Card de informações da turma com layout em colunas -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="card-title mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <!-- Coluna 1 -->
                <div class="col-md-4">
                    <div class="mb-3">
                        <h6 class="text-muted">Curso</h6>
                        <p class="fs-5">{{ turma.curso }}</p>
                    </div>
                    <div class="mb-3">
                        <h6 class="text-muted">Status</h6>
                        <p>
                            {% if turma.status == 'A' %}
                                <span class="badge bg-success">{{ turma.get_status_display }}</span>
                            {% elif turma.status == 'I' %}
                                <span class="badge bg-warning">{{ turma.get_status_display }}</span>
                            {% else %}
                                <span class="badge bg-secondary">{{ turma.get_status_display }}</span>
                            {% endif %}
                        </p>
                    </div>
                </div>
                
                <!-- Coluna 2 -->
                <div class="col-md-4">
                    <div class="mb-3">
                        <h6 class="text-muted">Data de Início</h6>
                        <p>{{ turma.data_inicio|date:"d/m/Y" }}</p>
                    </div>
                    <div class="mb-3">
                        <h6 class="text-muted">Data de Término</h6>
                        <p>{{ turma.data_fim|date:"d/m/Y" }}</p>
                    </div>
                </div>
                
                <!-- Coluna 3 - Estatísticas -->
                <div class="col-md-4">
                    <div class="card bg-light">
                        <div class="card-body text-center">
                            <h6 class="text-muted">Ocupação</h6>
                            <div class="d-flex justify-content-around mb-2">
                                <div>
                                    <h3 class="mb-0">{{ alunos_matriculados_count }}</h3>
                                    <small class="text-muted">Matriculados</small>
                                </div>
                                <div>
                                    <h3 class="mb-0">{{ turma.vagas }}</h3>
                                    <small class="text-muted">Total</small>
                                </div>
                                <div>
                                    <h3 class="mb-0">{{ vagas_disponiveis }}</h3>
                                    <small class="text-muted">Disponíveis</small>
                                </div>
                            </div>
                            
                            <!-- Barra de progresso -->
                            <div class="progress" style="height: 10px;">
                                <div class="progress-bar bg-primary" role="progressbar" 
                                     style="width: {% widthratio alunos_matriculados_count turma.vagas 100 %}%;" 
                                     aria-valuenow="{{ alunos_matriculados_count }}" 
                                     aria-valuemin="0" 
                                     aria-valuemax="{{ turma.vagas }}">
                                </div>
                            </div>
                            <small class="text-muted">{% widthratio alunos_matriculados_count turma.vagas 100 %}% ocupado</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Descrição em linha separada -->
            {% if turma.descricao %}
            <div class="row mt-3">
                <div class="col-12">
                    <h6 class="text-muted">Descrição</h6>
                    <p>{{ turma.descricao }}</p>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Card de instrutores -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="card-title mb-0">Instrutores</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <!-- Instrutor Principal -->
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-header bg-light">
                            <h6 class="mb-0">Instrutor Principal</h6>
                        </div>
                        <div class="card-body text-center">
                            {% if turma.instrutor %}
                                <div class="mb-3">
                                    {% if turma.instrutor.foto %}
                                        <img src="{{ turma.instrutor.foto.url }}" alt="Foto de {{ turma.instrutor.nome }}" 
                                             class="rounded-circle" style="width: 100px; height: 100px; object-fit: cover;">
                                    {% else %}
                                        <div class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center mx-auto" 
                                             style="width: 100px; height: 100px; font-size: 36px;">
                                            {{ turma.instrutor.nome|first|upper }}
                                        </div>
                                    {% endif %}
                                </div>
                                <h5>{{ turma.instrutor.nome }}</h5>
                                <p class="text-muted">{{ turma.instrutor.numero_iniciatico|default:"" }}</p>
                                <a href="{% url 'alunos:detalhar_aluno' turma.instrutor.cpf %}" class="btn btn-sm btn-primary">
                                    Ver Perfil
                                </a>
                            {% else %}
                                <div class="text-muted py-4">
                                    <i class="fas fa-user-slash fa-3x mb-3"></i>
                                    <p>Nenhum instrutor designado</p>
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <!-- Instrutor Auxiliar -->
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-header bg-light">
                            <h6 class="mb-0">Instrutor Auxiliar</h6>
                        </div>
                        <div class="card-body text-center">
                            {% if turma.instrutor_auxiliar %}
                                <div class="mb-3">
                                    {% if turma.instrutor_auxiliar.foto %}
                                        <img src="{{ turma.instrutor_auxiliar.foto.url }}" alt="Foto de {{ turma.instrutor_auxiliar.nome }}" 
                                             class="rounded-circle" style="width: 100px; height: 100px; object-fit: cover;">
                                    {% else %}
                                        <div class="rounded-circle bg-info text-white d-flex align-items-center justify-content-center mx-auto" 
                                             style="width: 100px; height: 100px; font-size: 36px;">
                                            {{ turma.instrutor_auxiliar.nome|first|upper }}
                                        </div>
                                    {% endif %}
                                </div>
                                <h5>{{ turma.instrutor_auxiliar.nome }}</h5>
                                <p class="text-muted">{{ turma.instrutor_auxiliar.numero_iniciatico|default:"" }}</p>
                                <a href="{% url 'alunos:detalhar_aluno' turma.instrutor_auxiliar.cpf %}" class="btn btn-sm btn-info">
                                    Ver Perfil
                                </a>
                            {% else %}
                                <div class="text-muted py-4">
                                    <i class="fas fa-user-slash fa-3x mb-3"></i>
                                    <p>Nenhum instrutor designado</p>
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Card de alunos matriculados -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Alunos Matriculados</h5>
            <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary">Matricular Aluno</a>
        </div>
        <div class="card-body">
            {% if matriculas %}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Nome</th>
                                <th>CPF</th>
                                <th>Nº Iniciático</th>
                                <th class="text-end">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for matricula in matriculas %}
                            <tr>
                                <td>
                                    <div class="d-flex align-items-center">
                                        <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2" 
                                             style="width: 32px; height: 32px; font-size: 14px;">
                                            {{ matricula.aluno.nome|first|upper }}
                                        </div>
                                        {{ matricula.aluno.nome }}
                                    </div>
                                </td>
                                <td>{{ matricula.aluno.cpf }}</td>
                                <td>{{ matricula.aluno.numero_iniciatico|default:"N/A" }}</td>
                                <td class="text-end">
                                    <a href="{% url 'alunos:detalhar_aluno' matricula.aluno.cpf %}" class="btn btn-sm btn-info">
                                        <i class="fas fa-eye"></i> Ver
                                    </a>
                                    <a href="{% url 'turmas:cancelar_matricula' turma.id matricula.aluno.cpf %}" 
                                       class="btn btn-sm btn-danger"
                                       onclick="return confirm('Tem certeza que deseja cancelar esta matrícula?');">
                                        <i class="fas fa-times"></i> Cancelar
                                    </a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i> Nenhum aluno matriculado nesta turma.
                </div>
                <a href="{% url 'turmas:matricular_aluno' turma.id %}" class="btn btn-primary">
                    <i class="fas fa-user-plus"></i> Matricular Primeiro Aluno
                </a>
            {% endif %}
        </div>
        {% if matriculas %}
        <div class="card-footer text-muted">
            <small>Total: {{ alunos_matriculados_count }} aluno(s)</small>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block extra_css %}
<style>
    .bg-gradient-primary {
        background: linear-gradient(to right, #0d6efd, #0a58ca);
    }

    .bg-primary.bg-opacity-10 {
        background-color: rgba(13, 110, 253, 0.1) !important;
    }

    .bg-success.bg-opacity-10 {
        background-color: rgba(25, 135, 84, 0.1) !important;
    }

    .bg-info.bg-opacity-10 {
        background-color: rgba(13, 202, 240, 0.1) !important;
    }

    .rounded-circle {
        border-radius: 50% !important;
    }

    .progress {
        overflow: hidden;
        background-color: #e9ecef;
    }

    .card {
        transition: all 0.3s ease;
    }

    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 .5rem 1rem rgba(0,0,0,.15) !important;
    }
</style>
{% endblock %}

{% block extra_js %}
<script>
    // Adicione aqui qualquer JavaScript específico para esta página
</script>
{% endblock %}

```


### Arquivo: turmas\templates\turmas\editar_turma.html

```html
{% extends 'base.html' %}

{% block title %}Editar Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Editar Turma: {{ turma.nome }}</h1>
        <a href="{% url 'turmas:listar_turmas' %}" class="btn btn-secondary">Voltar para Lista</a>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Informações Básicas</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <!-- Nome da Turma -->
                        <div class="form-group mb-3">
                            <label for="{{ form.nome.id_for_label }}">{{ form.nome.label }}</label>
                            {{ form.nome }}
                            {% if form.nome.help_text %}
                                <small class="form-text text-muted">{{ form.nome.help_text }}</small>
                            {% endif %}
                            {% for error in form.nome.errors %}
                                <div class="alert alert-danger mt-1">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <!-- Curso -->
                        <div class="form-group mb-3">
                            <label for="{{ form.curso.id_for_label }}">{{ form.curso.label }}</label>
                            {{ form.curso }}
                            {% if form.curso.help_text %}
                                <small class="form-text text-muted">{{ form.curso.help_text }}</small>
                            {% endif %}
                            {% for error in form.curso.errors %}
                                <div class="alert alert-danger mt-1">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-3">
                        <!-- Data de Início -->
                        <div class="form-group mb-3">
                            <label for="{{ form.data_inicio.id_for_label }}">{{ form.data_inicio.label }}</label>
                            {{ form.data_inicio }}
                            {% if form.data_inicio.help_text %}
                                <small class="form-text text-muted">{{ form.data_inicio.help_text }}</small>
                            {% endif %}
                            {% for error in form.data_inicio.errors %}
                                <div class="alert alert-danger mt-1">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                    <div class="col-md-3">
                        <!-- Data de Fim -->
                        <div class="form-group mb-3">
                            <label for="{{ form.data_fim.id_for_label }}">{{ form.data_fim.label }}</label>
                            {{ form.data_fim }}
                            {% if form.data_fim.help_text %}
                                <small class="form-text text-muted">{{ form.data_fim.help_text }}</small>
                            {% endif %}
                            {% for error in form.data_fim.errors %}
                                <div class="alert alert-danger mt-1">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                    <div class="col-md-3">
                        <!-- Vagas -->
                        <div class="form-group mb-3">
                            <label for="{{ form.vagas.id_for_label }}">{{ form.vagas.label }}</label>
                            {{ form.vagas }}
                            {% if form.vagas.help_text %}
                                <small class="form-text text-muted">{{ form.vagas.help_text }}</small>
                            {% endif %}
                            {% for error in form.vagas.errors %}
                                <div class="alert alert-danger mt-1">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                    <div class="col-md-3">
                        <!-- Status -->
                        <div class="form-group mb-3">
                            <label for="{{ form.status.id_for_label }}">{{ form.status.label }}</label>
                            {{ form.status }}
                            {% if form.status.help_text %}
                                <small class="form-text text-muted">{{ form.status.help_text }}</small>
                            {% endif %}
                            {% for error in form.status.errors %}
                                <div class="alert alert-danger mt-1">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <!-- Local -->
                        <div class="form-group mb-3">
                            <label for="{{ form.local.id_for_label }}">{{ form.local.label }}</label>
                            {{ form.local }}
                            {% if form.local.help_text %}
                                <small class="form-text text-muted">{{ form.local.help_text }}</small>
                            {% endif %}
                            {% for error in form.local.errors %}
                                <div class="alert alert-danger mt-1">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <!-- Horário -->
                        <div class="form-group mb-3">
                            <label for="{{ form.horario.id_for_label }}">{{ form.horario.label }}</label>
                            {{ form.horario }}
                            {% if form.horario.help_text %}
                                <small class="form-text text-muted">{{ form.horario.help_text }}</small>
                            {% endif %}
                            {% for error in form.horario.errors %}
                                <div class="alert alert-danger mt-1">{{ error }}</div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                
                <!-- Descrição -->
                <div class="form-group mb-3">
                    <label for="{{ form.descricao.id_for_label }}">{{ form.descricao.label }}</label>
                    {{ form.descricao }}
                    {% if form.descricao.help_text %}
                        <small class="form-text text-muted">{{ form.descricao.help_text }}</small>
                    {% endif %}
                    {% for error in form.descricao.errors %}
                        <div class="alert alert-danger mt-1">{{ error }}</div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="mb-0">Instrutores</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        <!-- Instrutor Principal -->
                        <div class="form-group mb-3">
                            <label for="id_instrutor">Instrutor Principal</label>
                            <select name="instrutor" class="form-select" id="id_instrutor">
                                <option value="">---------</option>
                                {% for aluno in alunos %}
                                    <option value="{{ aluno.cpf }}" {% if turma.instrutor and turma.instrutor.cpf == aluno.cpf %}selected{% endif %}>
                                        {{ aluno.nome }}
                                    </option>
                                {% endfor %}
                            </select>
                            {% if form.instrutor.errors %}
                                {% for error in form.instrutor.errors %}
                                    <div class="alert alert-danger mt-1">{{ error }}</div>
                                {% endfor %}
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-4">
                        <!-- Instrutor Auxiliar -->
                        <div class="form-group mb-3">
                            <label for="id_instrutor_auxiliar">Instrutor Auxiliar</label>
                            <select name="instrutor_auxiliar" class="form-select" id="id_instrutor_auxiliar">
                                <option value="">---------</option>
                                {% for aluno in alunos %}
                                    <option value="{{ aluno.cpf }}" {% if turma.instrutor_auxiliar and turma.instrutor_auxiliar.cpf == aluno.cpf %}selected{% endif %}>
                                        {{ aluno.nome }}
                                    </option>
                                {% endfor %}
                            </select>
                            {% if form.instrutor_auxiliar.errors %}
                                {% for error in form.instrutor_auxiliar.errors %}
                                    <div class="alert alert-danger mt-1">{{ error }}</div>
                                {% endfor %}
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-4">
                        <!-- Auxiliar de Instrução -->
                        <div class="form-group mb-3">
                            <label for="id_auxiliar_instrucao">Auxiliar de Instrução</label>
                            <select name="auxiliar_instrucao" class="form-select" id="id_auxiliar_instrucao">
                                <option value="">---------</option>
                                {% for aluno in alunos %}
                                    <option value="{{ aluno.cpf }}" {% if turma.auxiliar_instrucao and turma.auxiliar_instrucao.cpf == aluno.cpf %}selected{% endif %}>
                                        {{ aluno.nome }}
                                    </option>
                                {% endfor %}
                            </select>
                            {% if form.auxiliar_instrucao.errors %}
                                {% for error in form.auxiliar_instrucao.errors %}
                                    <div class="alert alert-danger mt-1">{{ error }}</div>
                                {% endfor %}
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between">
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
            <button type="submit" class="btn btn-primary">Atualizar Turma</button>
        </div>
    </form>
</div>
{% endblock %}

{% block extra_js %}
<!-- JavaScript adicional para o formulário de edição de turma -->
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Transformar os selects em select2 para melhor experiência de busca
        if (typeof $.fn.select2 !== 'undefined') {
            $('#id_instrutor, #id_instrutor_auxiliar, #id_auxiliar_instrucao').select2({
                placeholder: 'Selecione um instrutor',
                allowClear: true,
                width: '100%'
            });
            
            $('#id_curso').select2({
                placeholder: 'Selecione um curso',
                width: '100%'
            });
        }
        
        // Validação de datas
        const dataInicio = document.getElementById('{{ form.data_inicio.id_for_label }}');
        const dataFim = document.getElementById('{{ form.data_fim.id_for_label }}');
        
        if (dataInicio && dataFim) {
            dataInicio.addEventListener('change', function() {
                if (dataFim.value && new Date(dataInicio.value) > new Date(dataFim.value)) {
                    alert('A data de início não pode ser posterior à data de fim.');
                    dataInicio.value = '';
                }
            });
            
            dataFim.addEventListener('change', function() {
                if (dataInicio.value && new Date(dataInicio.value) > new Date(dataFim.value)) {
                    alert('A data de fim não pode ser anterior à data de início.');
                    dataFim.value = '';
                }
            });
        }
    });
</script>
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

{% block title %}Alunos Matriculados - {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Alunos Matriculados - {{ turma.nome }}</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary me-2">Detalhes da Turma</a>
            <a href="{% url 'turmas:adicionar_aluno_turma' turma.id %}" class="btn btn-primary">Adicionar Aluno</a>
        </div>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card">
        <div class="card-header bg-light">
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Total de Alunos: {{ total_alunos }}</h5>
                <div>
                    <form method="get" class="d-flex">
                        <input type="text" name="q" class="form-control me-2" placeholder="Buscar aluno..." value="{{ query }}">
                        <button type="submit" class="btn btn-outline-primary">Buscar</button>
                    </form>
                </div>
            </div>
        </div>
        <div class="card-body">
            {% if alunos %}
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Nome</th>
                                <th>CPF</th>
                                <th>Email</th>
                                <th>Data de Matrícula</th>
                                <th>Status</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for matricula in matriculas %}
                                <tr>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            {% if matricula.aluno.foto %}
                                                <img src="{{ matricula.aluno.foto.url }}" alt="Foto de {{ matricula.aluno.nome }}" 
                                                     class="rounded-circle me-2" width="40" height="40" 
                                                     style="object-fit: cover;">
                                            {% else %}
                                                <div class="rounded-circle bg-secondary me-2 d-flex align-items-center justify-content-center" 
                                                     style="width: 40px; height: 40px; color: white;">
                                                    {{ matricula.aluno.nome|first|upper }}
                                                </div>
                                            {% endif %}
                                            {{ matricula.aluno.nome }}
                                        </div>
                                    </td>
                                    <td>{{ matricula.aluno.cpf }}</td>
                                    <td>{{ matricula.aluno.email }}</td>
                                    <td>{{ matricula.data_matricula|date:"d/m/Y" }}</td>
                                    <td>
                                        {% if matricula.status == 'A' %}
                                            <span class="badge bg-success">Ativa</span>
                                        {% elif matricula.status == 'C' %}
                                            <span class="badge bg-danger">Cancelada</span>
                                        {% elif matricula.status == 'F' %}
                                            <span class="badge bg-info">Finalizada</span>
                                        {% else %}
                                            <span class="badge bg-secondary">{{ matricula.get_status_display }}</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'alunos:detalhar_aluno' matricula.aluno.cpf %}" class="btn btn-sm btn-info">Detalhes</a>
                                        <a href="{% url 'turmas:remover_aluno_turma' turma.id matricula.aluno.cpf %}" class="btn btn-sm btn-danger">Remover</a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                {% if page_obj.has_other_pages %}
                    <nav aria-label="Paginação">
                        <ul class="pagination justify-content-center mt-3">
                            {% if page_obj.has_previous %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}{% if query %}&q={{ query }}{% endif %}">Anterior</a>
                                </li>
                            {% else %}
                                <li class="page-item disabled">
                                    <span class="page-link">Anterior</span>
                                </li>
                            {% endif %}

                            {% for num in page_obj.paginator.page_range %}
                                {% if page_obj.number == num %}
                                    <li class="page-item active">
                                        <span class="page-link">{{ num }}</span>
                                    </li>
                                {% else %}
                                    <li class="page-item">
                                        <a class="page-link" href="?page={{ num }}{% if query %}&q={{ query }}{% endif %}">{{ num }}</a>
                                    </li>
                                {% endif %}
                            {% endfor %}

                            {% if page_obj.has_next %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ page_obj.next_page_number }}{% if query %}&q={{ query }}{% endif %}">Próxima</a>
                                </li>
                            {% else %}
                                <li class="page-item disabled">
                                    <span class="page-link">Próxima</span>
                                </li>
                            {% endif %}
                        </ul>
                    </nav>
                {% endif %}
            {% else %}
                <div class="alert alert-info text-center">
                    <p class="mb-0">Nenhum aluno matriculado nesta turma.</p>
                </div>
            {% endif %}
        </div>
    </div>
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
                <th>Vagas</th>
                <th>Matrículas</th>
                <th>Disponíveis</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for turma_info in turmas_com_info %}
            {% with turma=turma_info.turma %}
            <tr {% if turma.alerta_instrutor %}class="table-warning"{% endif %}>
                <td>{{ turma.nome }}</td>
                <td>{{ turma.curso }}</td>
                <td>{{ turma.data_inicio|date:"d/m/Y" }}</td>
                <td>{{ turma.data_fim|date:"d/m/Y" }}</td>
                <td>
                    {% if turma.status == 'A' %}
                        <span class="badge bg-success">{{ turma.get_status_display }}</span>
                    {% elif turma.status == 'I' %}
                        <span class="badge bg-warning">{{ turma.get_status_display }}</span>
                    {% else %}
                        <span class="badge bg-secondary">{{ turma.get_status_display }}</span>
                    {% endif %}
                    
                    {% if turma.alerta_instrutor %}
                        <span class="badge bg-danger ms-1" data-bs-toggle="tooltip" title="{{ turma.alerta_mensagem }}">
                            <i class="fas fa-exclamation-triangle"></i>
                        </span>
                    {% endif %}
                </td>
                <td>{{ turma.vagas }}</td>
                <td>{{ turma_info.total_alunos }}</td>
                <td>{{ turma_info.vagas_disponiveis }}</td>
                <td>
                    <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-sm btn-info">Detalhes</a>
                    <a href="{% url 'turmas:editar_turma' turma.id %}" class="btn btn-sm btn-warning">Editar</a>
                    <a href="{% url 'turmas:excluir_turma' turma.id %}" class="btn btn-sm btn-danger">Excluir</a>
                </td>
            </tr>
            {% endwith %}
            {% empty %}
            <tr>
                <td colspan="9" class="text-center">Nenhuma turma encontrada.</td>
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
{% load static %}

{% block title %}Matricular Aluno na Turma: {{ turma.nome }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Matricular Aluno na Turma: {{ turma.nome }}</h1>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <p><strong>Nome da Turma:</strong> {{ turma.nome }}</p>
            <p><strong>Curso:</strong> {{ turma.curso.nome }}</p>
            <p><strong>Período:</strong> {{ turma.data_inicio|date:"d/m/Y" }} a {{ turma.data_fim|date:"d/m/Y" }}</p>
            <p><strong>Vagas Disponíveis:</strong> {{ vagas_disponiveis }}</p>
        </div>
    </div>
    
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Selecionar Aluno para Matrícula</h5>
        </div>
        <div class="card-body">
            <!-- Search input with autocomplete -->
            <div class="mb-4">
                {% csrf_token %}  <!-- Make sure you have this for AJAX requests -->
                <label for="search-aluno" class="form-label">Buscar Aluno:</label>
                <input type="text" id="search-aluno" class="form-control"
                       placeholder="Digite parte do CPF, nome ou número iniciático..."
                       autocomplete="off">
                <div id="search-results" class="list-group mt-2">
                    <!-- Results will be populated here dynamically -->
                </div>
            </div>
            
            <form method="post" id="matricula-form">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="aluno" class="form-label">Aluno Selecionado:</label>
                    <div id="selected-aluno-container" class="p-3 border rounded mb-2 d-none">
                        <div id="selected-aluno-info">Nenhum aluno selecionado</div>
                    </div>
                    <input type="hidden" name="aluno" id="aluno-id" required>
                </div>
                <button type="submit" class="btn btn-primary" id="submit-btn" disabled>Matricular</button>
                <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary">Cancelar</a>
            </form>
        </div>
    </div>
    
    <a href="{% url 'turmas:detalhar_turma' turma.id %}" class="btn btn-secondary mt-3">Voltar para Detalhes da Turma</a>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('search-aluno');
        const searchResults = document.getElementById('search-results');
        const selectedAlunoContainer = document.getElementById('selected-aluno-container');
        const selectedAlunoInfo = document.getElementById('selected-aluno-info');
        const alunoIdField = document.getElementById('aluno-id');
        const submitBtn = document.getElementById('submit-btn');
        
        let searchTimeout;
        
        // Get CSRF token
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // Add CSRF token to all fetch requests
        const originalFetch = window.fetch;
        window.fetch = function(url, options = {}) {
            if (url.startsWith('/')) {
                options.headers = options.headers || {};
                options.headers['X-CSRFToken'] = csrftoken;
            }
            return originalFetch(url, options);
        };
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            const query = this.value.trim();
            
            // Clear results if query is too short
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.classList.add('d-none');
                return;
            }
            
            // Set a timeout to avoid making too many requests
            searchTimeout = setTimeout(function() {
                // Show loading indicator
                searchResults.innerHTML = '<div class="list-group-item text-muted">Buscando...</div>';
                searchResults.classList.remove('d-none');
                
                fetch(`/alunos/search/?q=${encodeURIComponent(query)}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Erro na requisição');
                        }
                        return response.json();
                    })
                    .then(data => {
                        searchResults.innerHTML = '';
                        
                        if (data.error) {
                            // Handle error response
                            searchResults.innerHTML = `<div class="list-group-item text-danger">${data.error}</div>`;
                            return;
                        }
                        
                        if (data.length === 0) {
                            searchResults.innerHTML = '<div class="list-group-item">Nenhum aluno encontrado</div>';
                            return;
                        }
                        
                        // Display results
                        data.forEach(aluno => {
                            const item = document.createElement('a');
                            item.href = '#';
                            item.className = 'list-group-item list-group-item-action';
                            item.innerHTML = `
                                <div class="d-flex justify-content-between">
                                    <div>${aluno.nome}</div>
                                    <div class="text-muted">
                                        <small>CPF: ${aluno.cpf}</small>
                                        ${aluno.numero_iniciatico !== "N/A" ? `<small class="ms-2">Nº: ${aluno.numero_iniciatico}</small>` : ''}
                                    </div>
                                </div>
                            `;
                            
                            // Add click event to select this aluno
                            item.addEventListener('click', function(e) {
                                e.preventDefault();
                                selectAluno(aluno);
                                searchResults.classList.add('d-none');
                            });
                            
                            searchResults.appendChild(item);
                        });
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        searchResults.innerHTML = '<div class="list-group-item text-danger">Erro ao buscar alunos</div>';
                    });
            }, 300);
        });
        
        // Hide results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.add('d-none');
            }
        });
        
        // Function to select an aluno
        function selectAluno(aluno) {
            // Update the hidden input with the selected aluno's CPF
            alunoIdField.value = aluno.cpf;
            
            // Update the search input with the selected aluno's name
            searchInput.value = aluno.nome;
            
            // Show the selected aluno info
            selectedAlunoInfo.innerHTML = `
                <strong>${aluno.nome}</strong><br>
                CPF: ${aluno.cpf}<br>
                ${aluno.numero_iniciatico !== "N/A" ? `Número Iniciático: ${aluno.numero_iniciatico}` : ''}
            `;
            
            // Show the container and enable the submit button
            selectedAlunoContainer.classList.remove('d-none');
            submitBtn.disabled = false;
        }
    });
</script>
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
