# Revisão da Funcionalidade: relatorios

## Arquivos forms.py:


### Arquivo: relatorios\forms.py

python
from django import forms
from .models import Relatorio


class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ["titulo", "conteudo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "conteudo": forms.Textarea(attrs={"class": "form-control"}),
        }



## Arquivos views.py:


### Arquivo: relatorios\views.py

python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Relatorio
from .forms import RelatorioForm
from django.contrib.auth.decorators import login_required


@login_required
def listar_relatorios(request):
    """Lista todos os relatórios disponíveis."""
    relatorios = Relatorio.objects.all()
    return render(
        request,
        "relatorios/index.html",
        {"relatorios": relatorios},
    )


@login_required
def detalhar_relatorio(request, relatorio_id):
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    return render(
        request, "relatorios/detalhar_relatorio.html", {"relatorio": relatorio}
    )


@login_required
def criar_relatorio(request):
    if request.method == "POST":
        form = RelatorioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("relatorios:listar_relatorios")
    else:
        form = RelatorioForm()
    return render(request, "relatorios/form_relatorio.html", {"form": form})


@login_required
def editar_relatorio(request, relatorio_id):
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    if request.method == "POST":
        form = RelatorioForm(request.POST, instance=relatorio)
        if form.is_valid():
            form.save()
            return redirect("relatorios:listar_relatorios")
    else:
        form = RelatorioForm(instance=relatorio)
    return render(request, "relatorios/form_relatorio.html", {"form": form})


@login_required
def excluir_relatorio(request, relatorio_id):
    relatorio = get_object_or_404(Relatorio, id=relatorio_id)
    if request.method == "POST":
        relatorio.delete()
        return redirect("relatorios:listar_relatorios")
    return render(
        request, "relatorios/confirmar_exclusao.html", {"relatorio": relatorio}
    )


@login_required
def relatorio_alunos(request):
    # Logic to generate the student report
    return render(request, "relatorios/relatorio_alunos.html")


@login_required
def relatorio_presencas(request):
    # Logic to generate the attendance report
    return render(request, "relatorios/relatorio_presencas.html")


@login_required
def relatorio_punicoes(request):
    # Logic to generate the punishment report
    return render(request, "relatorios/relatorio_punicoes.html")


@login_required
def relatorio_alunos_pdf(request):
    # Logic to generate the PDF report for students
    # This might involve rendering a template to PDF or using a library like ReportLab
    return render(request, "relatorios/relatorio_alunos_pdf.html")



## Arquivos urls.py:


### Arquivo: relatorios\urls.py

python
from django.urls import path
from . import views

app_name = "relatorios"

urlpatterns = [
    path(
        "", views.listar_relatorios, name="listar_relatorios"
    ),  # Alterado de 'index' para 'listar_relatorios'
    path("alunos/", views.relatorio_alunos, name="relatorio_alunos"),
    path(
        "alunos/pdf/", views.relatorio_alunos_pdf, name="relatorio_alunos_pdf"
    ),
    path("presencas/", views.relatorio_presencas, name="relatorio_presencas"),
    path("punicoes/", views.relatorio_punicoes, name="relatorio_punicoes"),
]



## Arquivos models.py:


### Arquivo: relatorios\models.py

python
from django.db import models


class Relatorio(models.Model):
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo



## Arquivos de Template:


### Arquivo: relatorios\templates\relatorios\gerar_relatorio.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}




### Arquivo: relatorios\templates\relatorios\listar_relatorios.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Relatórios do Sistema</h1>
    
    <div class="row mt-4">
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Relatório de Alunos</h5>
                </div>
                <div class="card-body">
                    <p class="card-text">Gere relatórios completos dos alunos cadastrados no sistema, com opções de filtros por nome e data de nascimento.</p>
                </div>
                <div class="card-footer">
                    <a href="{% url 'relatorios:relatorio_alunos' %}" class="btn btn-primary">Acessar</a>
                </div>
            </div>
        </div>

        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Relatório de Presenças</h5>
                </div>
                <div class="card-body">
                    <p class="card-text">Acompanhe o registro de presenças dos alunos, com filtros por aluno, turma e período.</p>
                </div>
                <div class="card-footer">
                    <a href="{% url 'relatorios:relatorio_presencas' %}" class="btn btn-success">Acessar</a>
                </div>
            </div>
        </div>

        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-header bg-danger text-white">
                    <h5 class="mb-0">Relatório de Punições</h5>
                </div>
                <div class="card-body">
                    <p class="card-text">Visualize as punições registradas no sistema, com filtros por aluno, tipo de punição e período.</p>
                </div>
                <div class="card-footer">
                    <a href="{% url 'relatorios:relatorio_punicoes' %}" class="btn btn-danger">Acessar</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: relatorios\templates\relatorios\relatorio_alunos.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Relatório de Alunos</h1>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Filtros</h5>
        </div>
        <div class="card-body">
            <form method="get" class="row g-3">
                <div class="col-md-4">
                    <label for="nome" class="form-label">Nome:</label>
                    <input type="text" id="nome" name="nome" class="form-control" value="{{ nome }}">
                </div>
                <div class="col-md-3">
                    <label for="data_inicio" class="form-label">Data de Nascimento (Início):</label>
                    <input type="date" id="data_inicio" name="data_inicio" class="form-control" value="{{ data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data de Nascimento (Fim):</label>
                    <input type="date" id="data_fim" name="data_fim" class="form-control" value="{{ data_fim }}">
                </div>
                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Botões de ação -->
    <div class="mb-3">
        <a href="{% url 'relatorios:relatorio_alunos_pdf' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-danger">
            <i class="fas fa-file-pdf"></i> Baixar PDF
        </a>
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
                        <th>Nome</th>
                        <th>CPF</th>
                        <th>Email</th>
                        <th>Data de Nascimento</th>
                        <!-- Adicione mais colunas conforme necessário -->
                    </tr>
                </thead>
                <tbody>
                    {% for aluno in alunos %}
                    <tr>
                        <td>{{ aluno.nome }}</td>
                        <td>{{ aluno.cpf }}</td>
                        <td>{{ aluno.email }}</td>
                        <td>{{ aluno.data_nascimento|date:"d/m/Y" }}</td>
                        <!-- Adicione mais campos conforme necessário -->
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="4" class="text-center">Nenhum aluno encontrado com os filtros selecionados.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: relatorios\templates\relatorios\relatorio_presencas.html

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
                    <label for="data_inicio" class="form-label">Data Início:</label>
                    <input type="date" id="data_inicio" name="data_inicio" class="form-control" value="{{ data_inicio }}">
                </div>
                <div class="col-md-3">
                    <label for="data_fim" class="form-label">Data Fim:</label>
                    <input type="date" id="data_fim" name="data_fim" class="form-control" value="{{ data_fim }}">
                </div>
                <div class="col-md-3 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Botões de ação -->
    <div class="mb-3">
        <a href="{% url 'relatorios:relatorio_presencas_pdf' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-danger">
            <i class="fas fa-file-pdf"></i> Baixar PDF
        </a>
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
                    </tr>
                </thead>
                <tbody>
                    {% for presenca in presencas %}
                    <tr>
                        <td>{{ presenca.aluno.nome }}</td>
                        <td>{{ presenca.turma.nome }}</td>
                        <td>{{ presenca.data|date:"d/m/Y" }}</td>
                        <td>
                            {% if presenca.presente %}
                                <span class="badge bg-success">Presente</span>
                            {% else %}
                                <span class="badge bg-danger">Ausente</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="4" class="text-center">Nenhuma presença encontrada com os filtros selecionados.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: relatorios\templates\relatorios\relatorio_punicoes.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Relatório de Punições</h1>
    
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
                    <label for="tipo_punicao" class="form-label">Tipo de Punição:</label>
                    <select name="tipo_punicao" id="tipo_punicao" class="form-select">
                        <option value="">Todos</option>
                        {% for tipo in tipos_punicao %}
                            <option value="{{ tipo }}" {% if tipo_punicao == tipo %}selected{% endif %}>{{ tipo }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <label for="data_inicio" class="form-label">Data Início:</label>
                    <input type="date" id="data_inicio" name="data_inicio" class="form-control" value="{{ data_inicio }}">
                </div>
                <div class="col-md-2">
                    <label for="data_fim" class="form-label">Data Fim:</label>
                    <input type="date" id="data_fim" name="data_fim" class="form-control" value="{{ data_fim }}">
                </div>
                <div class="col-md-2 d-flex align-items-end">
                    <button type="submit" class="btn btn-primary">Filtrar</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Botões de ação -->
    <div class="mb-3">
        <a href="{% url 'relatorios:relatorio_punicoes_pdf' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}" class="btn btn-danger">
            <i class="fas fa-file-pdf"></i> Baixar PDF
        </a>
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
                        <th>Tipo de Punição</th>
                        <th>Data</th>
                        <th>Descrição</th>
                    </tr>
                </thead>
                <tbody>
                    {% for punicao in punicoes %}
                    <tr>
                        <td>{{ punicao.aluno.nome }}</td>
                        <td>{{ punicao.tipo_punicao }}</td>
                        <td>{{ punicao.data|date:"d/m/Y" }}</td>
                        <td>{{ punicao.descricao|truncatechars:50 }}</td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="4" class="text-center">Nenhuma punição encontrada com os filtros selecionados.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}


