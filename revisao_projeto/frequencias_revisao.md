# Revisão da Funcionalidade: frequencias

## Arquivos forms.py:


### Arquivo: frequencias\forms.py

python
from django import forms
from .models import Frequencia
import datetime
from django.core.exceptions import ValidationError


class FrequenciaForm(forms.ModelForm):
    class Meta:
        model = Frequencia
        fields = ["aluno", "turma", "data", "presente", "justificativa"]
        widgets = {
            "aluno": forms.Select(attrs={"class": "form-select"}),
            "turma": forms.Select(attrs={"class": "form-select"}),
            "data": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "presente": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "justificativa": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
        }

    def clean_data(self):
        data = self.cleaned_data.get("data")
        if data and data > datetime.date.today():
            raise ValidationError(
                "A data da frequência não pode ser no futuro."
            )
        return data

    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get("aluno")
        turma = cleaned_data.get("turma")
        data = cleaned_data.get("data")

        # Se for uma atualização (instância existe), precisamos excluir a instância atual da verificação de unicidade
        if self.instance.pk:
            if (
                Frequencia.objects.filter(aluno=aluno, turma=turma, data=data)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise ValidationError(
                    "Já existe um registro de frequência para este aluno nesta turma e data."
                )
        else:
            if aluno and turma and data:
                if Frequencia.objects.filter(
                    aluno=aluno, turma=turma, data=data
                ).exists():
                    raise ValidationError(
                        "Já existe um registro de frequência para este aluno nesta turma e data."
                    )

        return cleaned_data



## Arquivos views.py:


### Arquivo: frequencias\views.py

python
import importlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Frequencia
from alunos.models import Aluno
from atividades.models import AtividadeAcademica


# Função para obter modelos usando importlib
def get_models():
    Frequencia = importlib.import_module("frequencias.models").Frequencia
    Aluno = importlib.import_module("alunos.models").Aluno
    Turma = importlib.import_module("turmas.models").Turma
    return Frequencia, Aluno, Turma


# Função para obter formulários usando importlib
def get_forms():
    FrequenciaForm = importlib.import_module(
        "frequencias.forms"
    ).FrequenciaForm
    return FrequenciaForm


@login_required
@permission_required("frequencias.add_frequencia", raise_exception=True)
def registrar_frequencia(request):
    FrequenciaForm = get_forms()

    if request.method == "POST":
        form = FrequenciaForm(request.POST)
        if form.is_valid():
            frequencia = form.save(commit=False)
            frequencia.registrado_por = request.user
            frequencia.save()
            messages.success(request, "Frequência registrada com sucesso!")
            return redirect("frequencias:listar_frequencias")
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = FrequenciaForm()

    return render(
        request, "frequencias/registrar_frequencia.html", {"form": form}
    )


@login_required
@permission_required("frequencias.add_frequencia", raise_exception=True)
def registrar_frequencia_turma(request, turma_id):
    Frequencia, Aluno, Turma = get_models()

    turma = get_object_or_404(Turma, id=turma_id)
    alunos = Aluno.objects.filter(turmas=turma)

    if request.method == "POST":
        data = request.POST.get("data")
        presentes = request.POST.getlist("presentes")

        # Create or update attendance records
        for aluno in alunos:
            presente = str(aluno.id) in presentes
            justificativa = request.POST.get(f"justificativa_{aluno.id}", "")

            # Check if record exists
            frequencia, created = Frequencia.objects.update_or_create(
                aluno=aluno,
                turma=turma,
                data=data,
                defaults={
                    "presente": presente,
                    "justificativa": justificativa if not presente else "",
                    "registrado_por": request.user,
                },
            )

        messages.success(request, "Frequências registradas com sucesso!")
        return redirect("frequencias:listar_frequencias")

    return render(
        request,
        "frequencias/registrar_frequencia_turma.html",
        {
            "turma": turma,
            "alunos": alunos,
        },
    )


@login_required
@permission_required("frequencias.view_frequencia", raise_exception=True)
def listar_frequencias(request):
    frequencias_list = Frequencia.objects.all().select_related(
        "aluno", "atividade"
    )

    # Filtros
    aluno_id = request.GET.get("aluno")
    atividade_id = request.GET.get("atividade")
    data = request.GET.get("data")

    if aluno_id:
        frequencias_list = frequencias_list.filter(aluno_id=aluno_id)
    if atividade_id:
        frequencias_list = frequencias_list.filter(atividade_id=atividade_id)
    if data:
        frequencias_list = frequencias_list.filter(data=data)

    # Paginação
    paginator = Paginator(frequencias_list, 10)  # 10 itens por página
    page = request.GET.get("page")

    try:
        frequencias = paginator.page(page)
    except PageNotAnInteger:
        frequencias = paginator.page(1)
    except EmptyPage:
        frequencias = paginator.page(paginator.num_pages)

    # Obter listas para os filtros
    alunos = Aluno.objects.all()
    atividades = AtividadeAcademica.objects.all()

    return render(
        request,
        "frequencias/listar_frequencias.html",
        {
            "frequencias": frequencias,
            "alunos": alunos,
            "atividades": atividades,
        },
    )


@login_required
@permission_required("frequencias.change_frequencia", raise_exception=True)
def editar_frequencia(request, id):
    Frequencia = get_models()[0]
    FrequenciaForm = get_forms()

    frequencia = get_object_or_404(Frequencia, id=id)

    if request.method == "POST":
        form = FrequenciaForm(request.POST, instance=frequencia)
        if form.is_valid():
            form.save()
            messages.success(request, "Frequência atualizada com sucesso!")
            return redirect("frequencias:listar_frequencias")
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = FrequenciaForm(instance=frequencia)

    return render(
        request,
        "frequencias/editar_frequencia.html",
        {"form": form, "frequencia": frequencia},
    )


@login_required
@permission_required("frequencias.view_frequencia", raise_exception=True)
def detalhar_frequencia(request, id):
    """Exibe os detalhes de uma frequência."""
    Frequencia = get_models()[0]
    frequencia = get_object_or_404(Frequencia, id=id)
    return render(
        request,
        "frequencias/detalhar_frequencia.html",
        {"frequencia": frequencia},
    )


@login_required
@permission_required("frequencias.delete_frequencia", raise_exception=True)
def excluir_frequencia(request, id):
    Frequencia = get_models()[0]
    frequencia = get_object_or_404(Frequencia, id=id)

    if request.method == "POST":
        frequencia.delete()
        messages.success(request, "Frequência excluída com sucesso!")
        return redirect("frequencias:listar_frequencias")

    return render(
        request,
        "frequencias/excluir_frequencia.html",
        {"frequencia": frequencia},
    )


@login_required
@permission_required("frequencias.view_frequencia", raise_exception=True)
def relatorio_frequencias(request):
    # Implementação pendente
    return render(request, "frequencias/relatorio_frequencias.html")


@login_required
@permission_required("frequencias.view_frequencia", raise_exception=True)
def exportar_frequencias(request):
    # Implementação pendente

    return redirect("frequencias:listar_frequencias")



## Arquivos urls.py:


### Arquivo: frequencias\urls.py

python
from django.urls import path
from . import views

app_name = "frequencias"

urlpatterns = [
    path("", views.listar_frequencias, name="listar_frequencias"),
    path(
        "registrar/", views.registrar_frequencia, name="registrar_frequencia"
    ),
    path(
        "<int:id>/editar/", views.editar_frequencia, name="editar_frequencia"
    ),
    path(
        "<int:id>/excluir/",
        views.excluir_frequencia,
        name="excluir_frequencia",
    ),
    path(
        "<int:id>/detalhes/",
        views.detalhar_frequencia,
        name="detalhar_frequencia",
    ),
    path(
        "relatorio/", views.relatorio_frequencias, name="relatorio_frequencias"
    ),
    path("exportar/", views.exportar_frequencias, name="exportar_frequencias"),
]



## Arquivos models.py:


### Arquivo: frequencias\models.py

python
from django.db import models
from alunos.models import Aluno
from atividades.models import AtividadeAcademica


class Frequencia(models.Model):
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, verbose_name="Aluno"
    )
    atividade = models.ForeignKey(
        AtividadeAcademica, on_delete=models.CASCADE, verbose_name="Atividade"
    )
    data = models.DateField(verbose_name="Data")
    presente = models.BooleanField(default=True, verbose_name="Presente")
    justificativa = models.TextField(
        blank=True, null=True, verbose_name="Justificativa"
    )

    def __str__(self):
        return f"{self.aluno.nome} - {self.atividade.nome} - {self.data}"

    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
        ordering = ["-data"]
        unique_together = ["aluno", "atividade", "data"]



## Arquivos de Template:


### Arquivo: frequencias\templates\frequencias\detalhar_frequencia.html

html
{% extends 'base.html' %}

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
                  <p><strong>Turma:</strong> {{ frequencia.turma.id }}</p>
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




### Arquivo: frequencias\templates\frequencias\editar_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Registro de FrequÃªncia</h1>
  
    <form method="post">
      {% csrf_token %}
      {% include 'includes/form_errors.html' %}
    
      {% for field in form %}
        {% include 'includes/form_field.html' %}
      {% endfor %}
    
      <button type="submit" class="btn btn-primary">Atualizar</button>
      <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\estatisticas_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Estatísticas de Frequência</h1>
   
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
   
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
                    <a href="{% url 'estatisticas_frequencia' %}" class="btn btn-secondary">Limpar Filtros</a>
                </div>
            </form>
        </div>
    </div>
   
    <!-- Resumo Estatístico -->
    <div class="row">
        <div class="col-md-4">
            <div class="card text-white bg-primary mb-4">
                <div class="card-header">Total de Registros</div>
                <div class="card-body">
                    <h5 class="card-title">{{ total }}</h5>
                    <p class="card-text">registros de frequência</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-white bg-success mb-4">
                <div class="card-header">Presenças</div>
                <div class="card-body">
                    <h5 class="card-title">{{ presentes }}</h5>
                    <p class="card-text">alunos presentes ({{ taxa_presenca|floatformat:2 }}%)</p>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card text-white bg-danger mb-4">
                <div class="card-header">Ausências</div>
                <div class="card-body">
                    <h5 class="card-title">{{ ausentes }}</h5>
                    <p class="card-text">alunos ausentes ({{ 100|sub:taxa_presenca|floatformat:2 }}%)</p>
                </div>
            </div>
        </div>
    </div>
   
    <!-- Gráfico (pode ser implementado com Chart.js) -->
    <div class="card mb-4">
        <div class="card-header">
            <h5 class="mb-0">Gráfico de Frequência</h5>
        </div>
        <div class="card-body">
            <canvas id="graficoFrequencia" width="400" height="200"></canvas>
        </div>
    </div>
   
    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
        <a href="{% url 'listar_frequencias' %}" class="btn btn-secondary">Voltar para Lista</a>
    </div>
</div>

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        var ctx = document.getElementById('graficoFrequencia').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Presentes', 'Ausentes'],
                datasets: [{
                    label: 'Frequência',
                    data: [{{ presentes }}, {{ ausentes }}],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        'rgba(40, 167, 69, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Distribuição de Frequência'
                    }
                }
            }
        });
    });
</script>
{% endblock %}
{% endblock %}




### Arquivo: frequencias\templates\frequencias\excluir_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Registro de Frequência</h1>
  
    <div class="alert alert-danger">
      <p>Tem certeza que deseja excluir o registro de frequência de <strong>{{ frequencia.aluno.nome }}</strong> na atividade <strong>{{ frequencia.atividade.nome }}</strong> do dia <strong>{{ frequencia.data|date:"d/m/Y" }}</strong>?</p>
    </div>
  
    <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Sim, excluir</button>
      <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\listar_frequencias.html

html
{% extends 'base.html' %}

{% block title %}Lista de Frequências{% endblock %}

{% block content %}
<div class="container mt-4">
  <!-- Cabeçalho com título e botões na mesma linha -->
  <div class="d-flex justify-content-between align-items-center mb-3">
      <h1>Lista de Frequências</h1>
      <div>
          <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
          <a href="{% url 'frequencias:registrar_frequencia' %}" class="btn btn-primary">Registrar Frequência</a>
          <a href="{% url 'frequencias:relatorio_frequencias' %}" class="btn btn-info">Relatório</a>
      </div>
  </div>
    
  <!-- Barra de busca e filtros -->
  <div class="card mb-4">
      <div class="card-header">
          <form method="get" class="row g-3">
              <div class="col-md-4">
                  <input type="text" name="q" class="form-control" placeholder="Buscar por aluno ou atividade..." value="{{ query }}">
              </div>
              <div class="col-md-3">
                  <select name="atividade" class="form-select">
                      <option value="">Todas as atividades</option>
                      {% for atividade in atividades %}
                          <option value="{{ atividade.id }}" {% if atividade.id|stringformat:"s" == atividade_selecionada %}selected{% endif %}>{{ atividade.nome }}</option>
                      {% endfor %}
                  </select>
              </div>
              <div class="col-md-3">
                  <input type="date" name="data" class="form-control" value="{{ data_selecionada }}">
              </div>
              <div class="col-md-2">
                  <button type="submit" class="btn btn-primary w-100">Filtrar</button>
              </div>
          </form>
      </div>
      <div class="card-body">
          <div class="table-responsive">
              <table class="table table-striped">
                  <thead>
                      <tr>
                          <th>Aluno</th>
                          <th>Atividade</th>
                          <th>Data</th>
                          <th>Presente</th>
                          <th>Ações</th>
                      </tr>
                  </thead>
                  <tbody>
                      {% for frequencia in frequencias %}
                          <tr>
                              <td>{{ frequencia.aluno.nome }}</td>
                              <td>{{ frequencia.atividade.nome }}</td>
                              <td>{{ frequencia.data|date:"d/m/Y" }}</td>
                              <td>
                                  {% if frequencia.presente %}
                                      <span class="badge bg-success">Presente</span>
                                  {% else %}
                                      <span class="badge bg-danger">Ausente</span>
                                  {% endif %}
                              </td>
                              <td>
                                  <a href="{% url 'frequencias:detalhar_frequencia' frequencia.id %}" class="btn btn-sm btn-info" title="Ver detalhes completos da frequência">Detalhes</a>
                                  <a href="{% url 'frequencias:editar_frequencia' frequencia.id %}" class="btn btn-sm btn-warning" title="Editar informações da frequência">Editar</a>
                                  <a href="{% url 'frequencias:excluir_frequencia' frequencia.id %}" class="btn btn-sm btn-danger" title="Excluir este registro de frequência">Excluir</a>
                              </td>
                          </tr>
                      {% empty %}
                          <tr>
                              <td colspan="5" class="text-center">
                                  <p class="my-3">Nenhum registro de frequência encontrado.</p>
                              </td>
                          </tr>
                      {% endfor %}
                  </tbody>
              </table>
          </div>
      </div>
      <div class="card-footer">
          <p class="text-muted mb-0">Total: {{ frequencias.count|default:"0" }} registro(s)</p>
          {% if page_obj.has_other_pages %}
              <nav aria-label="Paginação">
                  <ul class="pagination justify-content-center mb-0">
                      {% if page_obj.has_previous %}
                          <li class="page-item">
                              <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}&atividade={{ atividade_selecionada }}&data={{ data_selecionada }}">Anterior</a>
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
                                  <a class="page-link" href="?page={{ num }}&q={{ query }}&atividade={{ atividade_selecionada }}&data={{ data_selecionada }}">{{ num }}</a>
                              </li>
                          {% endif %}
                      {% endfor %}

                      {% if page_obj.has_next %}
                          <li class="page-item">
                              <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}&atividade={{ atividade_selecionada }}&data={{ data_selecionada }}">Próxima</a>
                          </li>
                      {% else %}
                          <li class="page-item disabled">
                              <span class="page-link">Próxima</span>
                          </li>
                      {% endif %}
                  </ul>
              </nav>
          {% endif %}
      </div>
  </div>
</div>
{% endblock %}



### Arquivo: frequencias\templates\frequencias\registrar_frequencia.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Registrar Frequência</h1>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="card">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
                {% include 'includes/form_errors.html' %}
                
                {% for field in form %}
                    {% include 'includes/form_field.html' %}
                {% endfor %}
                
                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                    <button type="submit" class="btn btn-primary">Registrar Frequência</button>
                    <a href="{% url 'frequencias:listar_frequencias' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\registrar_frequencia_turma.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Registrar Frequência da Turma: {{ turma.id }}</h1>
   
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
   
    <div class="card">
        <div class="card-body">
            <form method="post">
                {% csrf_token %}
               
                <div class="mb-3">
                    <label for="data" class="form-label">Data</label>
                    <input type="date" class="form-control" id="data" name="data" required>
                </div>
               
                <table class="table">
                    <thead>
                        <tr>
                            <th>Aluno</th>
                            <th>Presente</th>
                            <th>Justificativa (se ausente)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for aluno in alunos %}
                        <tr>
                            <td>{{ aluno.nome }}</td>
                            <td>
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" name="presentes" value="{{ aluno.id }}" id="presente_{{ aluno.id }}" checked>
                                    <label class="form-check-label" for="presente_{{ aluno.id }}">
                                        Presente
                                    </label>
                                </div>
                            </td>
                            <td>
                                <textarea class="form-control" name="justificativa_{{ aluno.id }}" rows="2" placeholder="Justificativa para ausência"></textarea>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="3" class="text-center">Nenhum aluno encontrado nesta turma.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
               
                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                    <button type="submit" class="btn btn-primary">Registrar Frequências</button>
                    <a href="{% url 'listar_frequencias' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: frequencias\templates\frequencias\relatorio_frequencias.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Relatório de Frequências</h1>
  
  <div class="card mb-4">
    <div class="card-header">
      <h5>Filtros do Relatório</h5>
    </div>
    <div class="card-body">
      <form method="get" class="row g-3">
        <div class="col-md-4">
          <label for="aluno" class="form-label">Aluno</label>
          <select name="aluno" id="aluno" class="form-select">
            <option value="">Todos</option>
            {% for aluno in alunos %}
              <option value="{{ aluno.id }}" {% if request.GET.aluno == aluno.id|stringformat:"i" %}selected{% endif %}>
                {{ aluno.nome }}
              </option>
            {% endfor %}
          </select>
        </div>
        <div class="col-md-4">
          <label for="atividade" class="form-label">Atividade</label>
          <select name="atividade" id="atividade" class="form-select">
            <option value="">Todas</option>
            {% for atividade in atividades %}
              <option value="{{ atividade.id }}" {% if request.GET.atividade == atividade.id|stringformat:"i" %}selected{% endif %}>
                {{ atividade.nome }}
              </option>
            {% endfor %}
          </select>
        </div>
        <div class="col-md-4">
          <label for="turma" class="form-label">Turma</label>
          <select name="turma" id="turma" class="form-select">
            <option value="">Todas</option>
            {% for turma in turmas %}
              <option value="{{ turma.id }}" {% if request.GET.turma == turma.id|stringformat:"i" %}selected{% endif %}>
                {{ turma.nome }}
              </option>
            {% endfor %}
          </select>
        </div>
        <div class="col-md-4">
          <label for="data_inicio" class="form-label">Data Início</label>
          <input type="date" name="data_inicio" id="data_inicio" class="form-control" value="{{ request.GET.data_inicio }}">
        </div>
        <div class="col-md-4">
          <label for="data_fim" class="form-label">Data Fim</label>
          <input type="date" name="data_fim" id="data_fim" class="form-control" value="{{ request.GET.data_fim }}">
        </div>
        <div class="col-md-4">
          <label for="status" class="form-label">Status</label>
          <select name="status" id="status" class="form-select">
            <option value="">Todos</option>
            <option value="presente" {% if request.GET.status == 'presente' %}selected{% endif %}>Presente</option>
            <option value="ausente" {% if request.GET.status == 'ausente' %}selected{% endif %}>Ausente</option>
          </select>
        </div>
        <div class="col-12 mt-3">
          <button type="submit" class="btn btn-primary">Gerar Relatório</button>
          <a href="{% url 'frequencias:relatorio_frequencias' %}" class="btn btn-secondary">Limpar Filtros</a>
          {% if frequencias %}
            <a href="{% url 'frequencias:exportar_frequencias' %}?{{ request.GET.urlencode }}" class="btn btn-success">Exportar para Excel</a>
          {% endif %}
        </div>
      </form>
    </div>
  </div>
  
  {% if frequencias %}
    <div class="card">
      <div class="card-header">
        <h5>Resultados do Relatório</h5>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Aluno</th>
                <th>Atividade</th>
                <th>Turma</th>
                <th>Data</th>
                <th>Status</th>
                <th>Justificativa</th>
              </tr>
            </thead>
            <tbody>
              {% for frequencia in frequencias %}
              <tr>
                <td>{{ frequencia.aluno.nome }}</td>
                <td>{{ frequencia.atividade.nome }}</td>
                <td>{{ frequencia.atividade.turma.nome }}</td>
                <td>{{ frequencia.data|date:"d/m/Y" }}</td>
                <td>
                  {% if frequencia.presente %}
                    <span class="badge bg-success">Presente</span>
                  {% else %}
                    <span class="badge bg-danger">Ausente</span>
                  {% endif %}
                </td>
                <td>{{ frequencia.justificativa|default:"-" }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        
        <div class="mt-4">
          <h5>Resumo</h5>
          <div class="row">
            <div class="col-md-4">
              <div class="card bg-light">
                <div class="card-body">
                  <h6 class="card-title">Total de Registros</h6>
                  <p class="card-text display-6">{{ frequencias|length }}</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-success text-white">
                <div class="card-body">
                  <h6 class="card-title">Presenças</h6>
                  <p class="card-text display-6">{{ presencas }}</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-danger text-white">
                <div class="card-body">
                  <h6 class="card-title">Ausências</h6>
                  <p class="card-text display-6">{{ ausencias }}</p>
                </div>
              </div>
            </div>
          </div>
          
          {% if taxa_presenca is not None %}
          <div class="mt-3">
            <h6>Taxa de Presença: {{ taxa_presenca }}%</h6>
            <div class="progress">
              <div class="progress-bar bg-success" role="progressbar" style="width: {{ taxa_presenca }}%" aria-valuenow="{{ taxa_presenca }}" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </div>
          {% endif %}
        </div>
      </div>
    </div>
  {% elif request.GET %}
    <div class="alert alert-info">
      Nenhum registro de frequência encontrado com os filtros selecionados.
    </div>
  {% endif %}
</div>
{% endblock %}


