# Revisão da Funcionalidade: presencas

## Arquivos forms.py:


### Arquivo: presencas\forms.py

python
from django import forms
from .models import Presenca


class PresencaForm(forms.ModelForm):
    class Meta:
        model = Presenca
        fields = ["aluno", "turma", "data", "status"]
        widgets = {
            "data": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "aluno": "Aluno",
            "turma": "Turma",
            "data": "Data",
            "status": "Status",
        }
        help_texts = {
            "status": "Selecione o status de presen√ßa do aluno.",
        }



## Arquivos views.py:


### Arquivo: presencas\views.py

python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from importlib import import_module
from .forms import PresencaForm


def get_model(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


@login_required
def listar_presencas(request):
    """Lista todas as presenças registradas."""
    Presenca = get_model("presencas", "Presenca")
    presencas = Presenca.objects.all()
    return render(
        request, "presencas/listar_presencas.html", {"presencas": presencas}
    )


@login_required
def detalhar_presenca(request, presenca_id):
    """Exibe os detalhes de uma presença específica."""
    Presenca = get_model("presencas", "Presenca")
    presenca = get_object_or_404(Presenca, id=presenca_id)
    return render(
        request, "presencas/detalhar_presenca.html", {"presenca": presenca}
    )


@login_required
def criar_presenca(request):
    """Cria uma nova presença."""
    if request.method == "POST":
        form = PresencaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Presença registrada com sucesso!")
            return redirect("presencas:listar_presencas")
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = PresencaForm()
    return render(request, "presencas/form_presenca.html", {"form": form})


@login_required
def editar_presenca(request, presenca_id):
    """Edita uma presença existente."""
    Presenca = get_model("presencas", "Presenca")
    presenca = get_object_or_404(Presenca, id=presenca_id)
    if request.method == "POST":
        form = PresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            messages.success(request, "Presença atualizada com sucesso!")
            return redirect("presencas:listar_presencas")
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = PresencaForm(instance=presenca)
    return render(request, "presencas/form_presenca.html", {"form": form})


@login_required
def excluir_presenca(request, presenca_id):
    """Exclui uma presença."""
    Presenca = get_model("presencas", "Presenca")
    presenca = get_object_or_404(Presenca, id=presenca_id)
    if request.method == "POST":
        presenca.delete()
        messages.success(request, "Presença excluída com sucesso!")
        return redirect("presencas:listar_presencas")
    return render(
        request, "presencas/confirmar_exclusao.html", {"presenca": presenca}
    )


@login_required
def relatorio_presencas(request):
    """Gera um relatório de presenças."""
    Presenca = get_model("presencas", "Presenca")
    presencas = Presenca.objects.all()
    return render(
        request, "presencas/relatorio_presencas.html", {"presencas": presencas}
    )



## Arquivos urls.py:


### Arquivo: presencas\urls.py

python
from django.urls import path
from . import views

app_name = "presencas"

urlpatterns = [
    path("", views.listar_presencas, name="listar_presencas"),
    path(
        "<int:presenca_id>/", views.detalhar_presenca, name="detalhar_presenca"
    ),
    path("criar/", views.criar_presenca, name="criar_presenca"),
    path(
        "<int:presenca_id>/editar/",
        views.editar_presenca,
        name="editar_presenca",
    ),
    path(
        "<int:presenca_id>/excluir/",
        views.excluir_presenca,
        name="excluir_presenca",
    ),
    path("relatorio/", views.relatorio_presencas, name="relatorio_presencas"),
]



## Arquivos models.py:


### Arquivo: presencas\models.py

python
from django.db import models
from alunos.models import Aluno
from turmas.models import Turma


class Presenca(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("presente", "Presente"),
            ("ausente", "Ausente"),
            ("justificado", "Justificado"),
        ],
    )

    def __str__(self):
        return f"Presen√ßa de {self.aluno} em {self.turma} na data {self.data}"



## Arquivos de Template:


### Arquivo: presencas\templates\presencas\detalhar_presenca.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Detalhes da Presença</h1>
    
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Informações do Registro</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Aluno:</strong> {{ presenca.aluno.nome }}</p>
                    <p><strong>Turma:</strong> {{ presenca.turma.nome }}</p>
                    <p><strong>Data:</strong> {{ presenca.data|date:"d/m/Y" }}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Status:</strong> {% if presenca.presente %}Presente{% else %}Ausente{% endif %}</p>
                    <p><strong>Registrado por:</strong> {{ presenca.registrado_por.username }}</p>
                    <p><strong>Data de Registro:</strong> {{ presenca.data_registro|date:"d/m/Y H:i" }}</p>
                </div>
            </div>

            {% if presenca.justificativa %}
            <div class="mt-3">
                <h6>Justificativa:</h6>
                <div class="p-3 bg-light rounded">
                    {{ presenca.justificativa }}
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <div class="mt-3">
        <a href="{% url 'presencas:editar_presenca' presenca.id %}" class="btn btn-warning">Editar</a>
        <a href="{% url 'presencas:excluir_presenca' presenca.id %}" class="btn btn-danger">Excluir</a>
        <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Voltar para Lista</a>
    </div>
</div>
{% endblock %}



### Arquivo: presencas\templates\presencas\editar_presenca.html

html
{% extends 'base.html' %}

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
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: presencas\templates\presencas\excluir_presenca.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Registro de Presença</h1>
    
    <div class="card mb-4">
        <div class="card-body">
            <div class="alert alert-danger">
                <h5>Confirmação de Exclusão</h5>
                <p>Você está prestes a excluir o seguinte registro de presença:</p>
                <ul>
                    <li><strong>Aluno:</strong> {{ presenca.aluno.nome }}</li>
                    <li><strong>Turma:</strong> {{ presenca.turma.nome }}</li>
                    <li><strong>Data:</strong> {{ presenca.data|date:"d/m/Y" }}</li>
                    <li><strong>Status:</strong> {% if presenca.presente %}Presente{% else %}Ausente{% endif %}</li>
                </ul>
                <p>Esta ação não pode ser desfeita. Deseja continuar?</p>
            </div>
            
            <form method="post">
                {% csrf_token %}
                <div class="mt-3">
                    <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: presencas\templates\presencas\listar_presencas.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Lista de Presenças</h1>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="aluno" class="form-label">Aluno</label>
                    <select name="aluno" id="aluno" class="form-select">
                        <option value="">Todos</option>
                        {% for aluno in alunos %}
                            <option value="{{ aluno.id }}" {% if aluno_id == aluno.id|stringformat:"s" %}selected{% endif %}>{{ aluno.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma</label>
                    <select name="turma" id="turma" class="form-select">
                        <option value="">Todas</option>
                        {% for turma in turmas %}
                            <option value="{{ turma.id }}" {% if turma_id == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.id }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data Início</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data Fim</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ data_fim }}">
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary">Limpar Filtros</a>
                </div>
            </form>
        </div>
    </div>

    <table class="table">
        <thead>
            <tr>
                <th>Aluno</th>
                <th>Turma</th>
                <th>Data</th>
                <th>Presente</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>
            {% for presenca in presencas %}
            <tr>
                <td>{{ presenca.aluno.nome }}</td>
                <td>{{ presenca.turma.nome }}</td>
                <td>{{ presenca.data|date:"d/m/Y" }}</td>
                <td>{% if presenca.presente %}Sim{% else %}Não{% endif %}</td>
                <td>
                    <a href="{% url 'presencas:editar_presenca' presenca.id %}" class="btn btn-sm btn-warning">Editar</a>
                    <a href="{% url 'presencas:excluir_presenca' presenca.id %}" class="btn btn-sm btn-danger">Excluir</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5">Nenhuma presença registrada.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <!-- Paginação -->
    {% if presencas.paginator.num_pages > 1 %}
    <nav aria-label="Navegação de página">
        <ul class="pagination justify-content-center">
            {% if presencas.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page=1{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Primeira">
                        <span aria-hidden="true">««</span>
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ presencas.previous_page_number }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Anterior">
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

            {% for i in presencas.paginator.page_range %}
                {% if presencas.number == i %}
                    <li class="page-item active"><a class="page-link" href="#">{{ i }}</a></li>
                {% elif i > presencas.number|add:'-3' and i < presencas.number|add:'3' %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ i }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}">{{ i }}</a>
                    </li>
                {% endif %}
            {% endfor %}

            {% if presencas.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ presencas.next_page_number }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Próxima">
                        <span aria-hidden="true">»</span>
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ presencas.paginator.num_pages }}{% if aluno_id %}&aluno={{ aluno_id }}{% endif %}{% if turma_id %}&turma={{ turma_id }}{% endif %}{% if data_inicio %}&data_inicio={{ data_inicio }}{% endif %}{% if data_fim %}&data_fim={{ data_fim }}{% endif %}" aria-label="Última">
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

    <div class="mt-3">
        <a href="{% url 'presencas:registrar_presenca' %}" class="btn btn-primary">Registrar Nova Presença</a>
        <a href="{% url 'presencas:relatorio_presencas' %}" class="btn btn-info">Gerar Relatório</a>
    </div>
</div>
{% endblock %}




### Arquivo: presencas\templates\presencas\registrar_presenca.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Registrar Presen√ßa</h1>

    <div class="card mb-4">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}

                {% for field in form %}
                <div class="mb-3">
                    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                        <div class="invalid-feedback">
                            {{ field.errors }}
                        </div>
                    {% endif %}
                </div>
                {% endfor %}
                <button type="submit" class="btn btn-primary">Registrar</button>
            </form>
        </div>
    </div>
    <a href="{% url 'presencas:listar_presencas' %}" class="btn btn-secondary mt-2">Voltar</a>
</div>
{% endblock %}




### Arquivo: presencas\templates\presencas\relatorio_presencas.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Relatório de Presenças</h1>

    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-3">
                    <label for="aluno" class="form-label">Aluno:</label>
                    <select name="aluno" id="aluno" class="form-select">
                        <option value="">Todos</option>
                        {% for aluno in alunos %}
                            <option value="{{ aluno.id }}" {% if aluno_id == aluno.id|stringformat:"s" %}selected{% endif %}>{{ aluno.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="turma" class="form-label">Turma:</label>
                    <select name="turma" id="turma" class="form-select">
                        <option value="">Todas</option>
                        {% for turma in turmas %}
                            <option value="{{ turma.id }}" {% if turma_id == turma.id|stringformat:"s" %}selected{% endif %}>{{ turma.nome }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <label for="data_inicio" class="form-label">Data Início:</label>
                    <input type="date" class="form-control" id="data_inicio" name="data_inicio" value="{{ data_inicio }}">
                </div>
                <div class="col-md-2">
                    <label for="data_fim" class="form-label">Data Fim:</label>
                    <input type="date" class="form-control" id="data_fim" name="data_fim" value="{{ data_fim }}">
                </div>
                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Botões de ação -->
    <div class="mb-3">
        <a href="{% url 'presencas:relatorio_presencas_pdf' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-danger">
            <i class="fas fa-file-pdf"></i> Baixar PDF
        </a>
        <a href="{% url 'presencas:relatorio_presencas_excel' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-success">
            <i class="fas fa-file-excel"></i> Baixar Excel
        </a>
    </div>

    <!-- Estatísticas -->
    <div class="mt-4 mb-4">
        <h5>Estatísticas</h5>
        <div class="row">
            <div class="col-md-4">
                <div class="card bg-light">
                    <div class="card-body">
                        <h6 class="card-title">Total de Registros</h6>
                        <p class="card-text display-6">{{ presencas.count }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card bg-success text-white">
                    <div class="card-body">
                        <h6 class="card-title">Presenças</h6>
                        <p class="card-text display-6">{{ presencas_count.presentes }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card bg-danger text-white">
                    <div class="card-body">
                        <h6 class="card-title">Ausências</h6>
                        <p class="card-text display-6">{{ presencas_count.ausentes }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Tabela de resultados -->
    <div class="card">
        <div class="card-header">
            <h5 class="mb-0">Resultados</h5>
        </div>
        <div class="card-body">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Aluno</th>
                        <th>Turma</th>
                        <th>Data</th>
                        <th>Status</th>
                        <th>Justificativa</th>
                    </tr>
                </thead>
                <tbody>
                    {% for presenca in presencas %}
                    <tr>
                        <td>{{ presenca.aluno.nome }}</td>
                        <td>{{ presenca.turma.nome|default:"N/A" }}</td>
                        <td>{{ presenca.data|date:"d/m/Y" }}</td>
                        <td>
                            {% if presenca.presente %}
                                <span class="badge bg-success">Presente</span>
                            {% else %}
                                <span class="badge bg-danger">Ausente</span>
                            {% endif %}
                        </td>
                        <td>{{ presenca.justificativa|default:"-"|truncatechars:50 }}</td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center">Nenhuma presença encontrada com os filtros selecionados.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}

