# Revisão da Funcionalidade: iniciacoes

## Arquivos forms.py:


### Arquivo: iniciacoes\forms.py

```python
from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Iniciacao, GrauIniciacao


class IniciacaoForm(forms.ModelForm):
    class Meta:
        model = Iniciacao
        # Remova 'nome' da lista de campos
        fields = ["aluno", "curso", "data_iniciacao", "grau", "observacoes"]
        widgets = {
            "data_iniciacao": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "aluno": forms.Select(attrs={"class": "form-control"}),
            "curso": forms.Select(attrs={"class": "form-control"}),
            "grau": forms.TextInput(attrs={"class": "form-control"}),
            "observacoes": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }
        labels = {
            "aluno": "Aluno",
            "curso": "Curso",
            "data_iniciacao": "Data de Iniciação",
            "grau": "Grau",
            "observacoes": "Observações",
        }
        help_texts = {
            "curso": "Selecione o curso de iniciação",
            "data_iniciacao": "Selecione a data em que o aluno foi iniciado no curso",
        }

    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get("aluno")
        curso = cleaned_data.get("curso")
        data_iniciacao = cleaned_data.get("data_iniciacao")

        # Verifica se já existe uma iniciação para este aluno neste curso
        if aluno and curso:
            # Exclui a instância atual em caso de edição
            instance_id = self.instance.id if self.instance else None

            # Verifica se já existe outra iniciação com o mesmo aluno e curso
            if (
                Iniciacao.objects.filter(aluno=aluno, curso=curso)
                .exclude(id=instance_id)
                .exists()
            ):
                raise ValidationError(
                    f"O aluno {aluno.nome} já possui uma iniciação no curso {curso.nome}."
                )

        return cleaned_data

    def clean_data_iniciacao(self):
        data_iniciacao = self.cleaned_data.get("data_iniciacao")

        if data_iniciacao and data_iniciacao > date.today():
            raise ValidationError(
                "A data de iniciação não pode ser no futuro."
            )

        return data_iniciacao


class GrauIniciacaoForm(forms.ModelForm):
    class Meta:
        model = GrauIniciacao
        fields = ["nome", "descricao", "ordem"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "ordem": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean_ordem(self):
        ordem = self.cleaned_data.get("ordem")
        if ordem <= 0:
            raise ValidationError("A ordem deve ser um número positivo.")
        return ordem

```

## Arquivos views.py:


### Arquivo: iniciacoes\views.py

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Iniciacao, GrauIniciacao  # Add GrauIniciacao here
from .forms import (
    IniciacaoForm,
    GrauIniciacaoForm,
)  # Add GrauIniciacaoForm if it exists
from alunos.models import Aluno
from django.contrib.auth.decorators import login_required


@login_required
def listar_iniciacoes(request):
    # Parâmetros de filtro
    aluno_id = request.GET.get("aluno")
    nome_curso = request.GET.get("curso")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    # Query base
    iniciacoes = Iniciacao.objects.all()

    # Aplicar filtros
    if aluno_id:
        iniciacoes = iniciacoes.filter(aluno_id=aluno_id)

    if nome_curso:
        iniciacoes = iniciacoes.filter(nome_curso__icontains=nome_curso)

    if data_inicio:
        iniciacoes = iniciacoes.filter(data_iniciacao__gte=data_inicio)

    if data_fim:
        iniciacoes = iniciacoes.filter(data_iniciacao__lte=data_fim)

    # Busca geral
    search_query = request.GET.get("search", "")
    if search_query:
        iniciacoes = iniciacoes.filter(
            Q(aluno__nome__icontains=search_query)
            | Q(nome_curso__icontains=search_query)
        )

    # Paginação
    paginator = Paginator(iniciacoes, 10)  # 10 itens por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Lista de alunos para o filtro
    alunos = Aluno.objects.all()

    context = {
        "page_obj": page_obj,
        "alunos": alunos,
        "filtros": {
            "aluno_id": aluno_id,
            "nome_curso": nome_curso,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "search": search_query,
        },
    }

    return render(request, "iniciacoes/listar_iniciacoes.html", context)


@login_required
def criar_iniciacao(request):
    if request.method == "POST":
        form = IniciacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Iniciação criada com sucesso.")
            return redirect("iniciacoes:listar_iniciacoes")
    else:
        form = IniciacaoForm()
    return render(request, "iniciacoes/criar_iniciacao.html", {"form": form})


@login_required
def detalhar_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    return render(
        request, "iniciacoes/detalhar_iniciacao.html", {"iniciacao": iniciacao}
    )


@login_required
def editar_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    if request.method == "POST":
        form = IniciacaoForm(request.POST, instance=iniciacao)
        if form.is_valid():
            form.save()
            messages.success(request, "Iniciação atualizada com sucesso.")
            return redirect("iniciacoes:listar_iniciacoes")
    else:
        form = IniciacaoForm(instance=iniciacao)
    return render(
        request,
        "iniciacoes/editar_iniciacao.html",
        {"form": form, "iniciacao": iniciacao},
    )


@login_required
def excluir_iniciacao(request, id):
    iniciacao = get_object_or_404(Iniciacao, id=id)
    if request.method == "POST":
        iniciacao.delete()
        messages.success(request, "Iniciação excluída com sucesso.")
        return redirect("iniciacoes:listar_iniciacoes")
    return render(
        request, "iniciacoes/excluir_iniciacao.html", {"iniciacao": iniciacao}
    )


import csv
from django.http import HttpResponse


@login_required
def exportar_iniciacoes_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="iniciacoes.csv"'

    # Aplicar os mesmos filtros da listagem
    aluno_id = request.GET.get("aluno")
    nome_curso = request.GET.get("curso")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    search_query = request.GET.get("search", "")

    # Query base
    iniciacoes = Iniciacao.objects.all()

    # Aplicar filtros (mesmo código da view listar_iniciacoes)
    if aluno_id:
        iniciacoes = iniciacoes.filter(aluno_id=aluno_id)

    if nome_curso:
        iniciacoes = iniciacoes.filter(nome_curso__icontains=nome_curso)

    if data_inicio:
        iniciacoes = iniciacoes.filter(data_iniciacao__gte=data_inicio)

    if data_fim:
        iniciacoes = iniciacoes.filter(data_iniciacao__lte=data_fim)

    if search_query:
        iniciacoes = iniciacoes.filter(
            Q(aluno__nome__icontains=search_query)
            | Q(nome_curso__icontains=search_query)
        )

    writer = csv.writer(response)
    writer.writerow(["Aluno", "Curso", "Data de Iniciação", "Observações"])

    for iniciacao in iniciacoes:
        writer.writerow(
            [
                iniciacao.aluno.nome,
                iniciacao.nome_curso,
                iniciacao.data_iniciacao.strftime("%d/%m/%Y"),
                iniciacao.observacoes or "",
            ]
        )

    # Adicionar mensagem de sucesso
    messages.success(
        request,
        f"Arquivo CSV com {iniciacoes.count()} iniciações exportado com sucesso.",
    )

    return response


@login_required
def listar_graus(request):
    """Lista todos os graus de iniciação."""
    graus = GrauIniciacao.objects.all()
    return render(request, "iniciacoes/listar_graus.html", {"graus": graus})


@login_required
def criar_grau(request):
    """Cria um novo grau de iniciação."""
    if request.method == "POST":
        form = GrauIniciacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Grau de iniciação criado com sucesso!")
            return redirect("iniciacoes:listar_graus")
    else:
        form = GrauIniciacaoForm()
    return render(request, "iniciacoes/criar_grau.html", {"form": form})


@login_required
def editar_grau(request, id):
    """Edita um grau de iniciação existente."""
    grau = get_object_or_404(GrauIniciacao, id=id)
    if request.method == "POST":
        form = GrauIniciacaoForm(request.POST, instance=grau)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Grau de iniciação atualizado com sucesso!"
            )
            return redirect("iniciacoes:listar_graus")
    else:
        form = GrauIniciacaoForm(instance=grau)
    return render(
        request, "iniciacoes/editar_grau.html", {"form": form, "grau": grau}
    )


@login_required
def excluir_grau(request, id):
    """Exclui um grau de iniciação."""
    grau = get_object_or_404(GrauIniciacao, id=id)
    if request.method == "POST":
        grau.delete()
        messages.success(request, "Grau de iniciação excluído com sucesso!")
        return redirect("iniciacoes:listar_graus")
    return render(request, "iniciacoes/excluir_grau.html", {"grau": grau})

```

## Arquivos urls.py:


### Arquivo: iniciacoes\urls.py

```python
from django.urls import path
from . import views

app_name = "iniciacoes"

urlpatterns = [
    path("", views.listar_iniciacoes, name="listar_iniciacoes"),
    path("nova/", views.criar_iniciacao, name="criar_iniciacao"),
    path("<int:id>/editar/", views.editar_iniciacao, name="editar_iniciacao"),
    path(
        "<int:id>/excluir/", views.excluir_iniciacao, name="excluir_iniciacao"
    ),
    path(
        "<int:id>/detalhes/",
        views.detalhar_iniciacao,
        name="detalhar_iniciacao",
    ),
    path("graus/", views.listar_graus, name="listar_graus"),
    path("graus/novo/", views.criar_grau, name="criar_grau"),
    path("graus/<int:id>/editar/", views.editar_grau, name="editar_grau"),
    path("graus/<int:id>/excluir/", views.excluir_grau, name="excluir_grau"),
]

```

## Arquivos models.py:


### Arquivo: iniciacoes\models.py

```python
from django.db import models
from importlib import import_module


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_curso_model():
    cursos_module = import_module("cursos.models")
    return getattr(cursos_module, "Curso")


class Iniciacao(models.Model):
    aluno = models.ForeignKey(
        get_aluno_model(),
        on_delete=models.CASCADE,
        verbose_name="Aluno",
        to_field="cpf",  # Especificar que estamos referenciando o campo cpf
    )
    curso = models.ForeignKey(
        get_curso_model(), on_delete=models.CASCADE, verbose_name="Curso"
    )
    data_iniciacao = models.DateField(verbose_name="Data da Iniciação")
    grau = models.CharField(max_length=50, verbose_name="Grau")
    observacoes = models.TextField(
        blank=True, null=True, verbose_name="Observações"
    )

    def __str__(self):
        return f"{self.aluno.nome} - {self.curso.nome} - {self.grau}"

    class Meta:
        verbose_name = "Iniciação"
        verbose_name_plural = "Iniciações"
        ordering = ["-data_iniciacao"]
        unique_together = ["aluno", "curso", "grau"]


class GrauIniciacao(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Grau")
    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )
    ordem = models.PositiveIntegerField(unique=True, verbose_name="Ordem")

    class Meta:
        verbose_name = "Grau de Iniciação"
        verbose_name_plural = "Graus de Iniciação"
        ordering = ["ordem"]

    def __str__(self):
        return self.nome

```

## Arquivos de Template:


### Arquivo: iniciacoes\templates\iniciacoes\criar_grau.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Novo Grau de Iniciação</h1>
  
  <form method="post">
    {% csrf_token %}
    {% include 'includes/form_errors.html' %}
    
    {% for field in form %}
      {% include 'includes/form_field.html' %}
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Criar Grau</button>
    <a href="{% url 'iniciacoes:listar_graus' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}

```


### Arquivo: iniciacoes\templates\iniciacoes\criar_iniciacao.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Nova Iniciação</h1>
  
    <form method="post">
      {% csrf_token %}
      {% include 'includes/form_errors.html' %}
    
      {% for field in form %}
        {% include 'includes/form_field.html' %}
      {% endfor %}
    
      <button type="submit" class="btn btn-primary">Registrar Iniciação</button>
      <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}

```


### Arquivo: iniciacoes\templates\iniciacoes\detalhar_iniciacao.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes da Iniciação</h1>
  
  <div class="card">
    <div class="card-header">
      <h2>Iniciação de {{ iniciacao.aluno.nome }}</h2>
    </div>
    <div class="card-body">
      <p><strong>Aluno:</strong> {{ iniciacao.aluno.nome }}</p>
      <p><strong>Grau:</strong> {{ iniciacao.grau.nome }}</p>
      <p><strong>Data:</strong> {{ iniciacao.data|date:"d/m/Y" }}</p>
      <p><strong>Local:</strong> {{ iniciacao.local }}</p>
      <p>
        <strong>Status:</strong> 
        {% if iniciacao.concluida %}
          <span class="badge bg-success">Concluída</span>
        {% else %}
          <span class="badge bg-warning">Pendente</span>
        {% endif %}
      </p>
      {% if iniciacao.observacoes %}
        <p><strong>Observações:</strong> {{ iniciacao.observacoes }}</p>
      {% endif %}
      <p><strong>Registrado por:</strong> {{ iniciacao.registrado_por.username }}</p>
      <p><strong>Data de registro:</strong> {{ iniciacao.data_registro|date:"d/m/Y H:i" }}</p>
      {% if iniciacao.atualizado_por %}
        <p><strong>Atualizado por:</strong> {{ iniciacao.atualizado_por.username }}</p>
        <p><strong>Data de atualização:</strong> {{ iniciacao.data_atualizacao|date:"d/m/Y H:i" }}</p>
      {% endif %}
    </div>
    <div class="card-footer">
      <a href="{% url 'iniciacoes:editar_iniciacao' iniciacao.id %}" class="btn btn-warning">Editar</a>
      <a href="{% url 'iniciacoes:excluir_iniciacao' iniciacao.id %}" class="btn btn-danger">Excluir</a>
      <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Voltar</a>
    </div>
  </div>
</div>
{% endblock %}

```


### Arquivo: iniciacoes\templates\iniciacoes\editar_grau.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Editar Grau de Iniciação</h1>
  
  <form method="post">
    {% csrf_token %}
    {% include 'includes/form_errors.html' %}
    
    {% for field in form %}
      {% include 'includes/form_field.html' %}
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Atualizar Grau</button>
    <a href="{% url 'iniciacoes:listar_graus' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}

```


### Arquivo: iniciacoes\templates\iniciacoes\editar_iniciacao.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Iniciação</h1>
  
    <form method="post">
      {% csrf_token %}
      {% include 'includes/form_errors.html' %}
    
      {% for field in form %}
        {% include 'includes/form_field.html' %}
      {% endfor %}
    
      <button type="submit" class="btn btn-primary">Atualizar Iniciação</button>
      <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}
```


### Arquivo: iniciacoes\templates\iniciacoes\excluir_grau.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Excluir Grau de Iniciação</h1>
  
  <div class="alert alert-danger">
    <p>Tem certeza que deseja excluir o grau <strong>{{ grau.nome }}</strong>?</p>
    {% if iniciacoes_associadas %}
      <div class="mt-3">
        <p><strong>Atenção:</strong> Existem {{ iniciacoes_associadas }} iniciações associadas a este grau. A exclusão deste grau pode afetar esses registros.</p>
      </div>
    {% endif %}
  </div>
  
  <form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Sim, excluir</button>
    <a href="{% url 'iniciacoes:listar_graus' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}

```


### Arquivo: iniciacoes\templates\iniciacoes\excluir_iniciacao.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Iniciação</h1>
  
    <div class="alert alert-danger">
      <p>Tem certeza que deseja excluir a iniciação de <strong>{{ iniciacao.aluno.nome }}</strong> no grau <strong>{{ iniciacao.grau.nome }}</strong> realizada em <strong>{{ iniciacao.data|date:"d/m/Y" }}</strong>?</p>
    </div>
  
    <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Sim, excluir</button>
      <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}
```


### Arquivo: iniciacoes\templates\iniciacoes\listar_graus.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Graus de Iniciação</h1>
  
  <div class="d-flex justify-content-between mb-3">
    <a href="{% url 'iniciacoes:criar_grau' %}" class="btn btn-primary">Novo Grau</a>
    <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Voltar para Iniciações</a>
  </div>
  
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Nome</th>
        <th>Número</th>
        <th>Descrição</th>
        <th>Requisitos</th>
        <th>Ações</th>
      </tr>
    </thead>
    <tbody>
      {% for grau in graus %}
      <tr>
        <td>{{ grau.nome }}</td>
        <td>{{ grau.numero }}</td>
        <td>{{ grau.descricao|truncatechars:50 }}</td>
        <td>{{ grau.requisitos|truncatechars:50 }}</td>
        <td>
          <a href="{% url 'iniciacoes:editar_grau' grau.id %}" class="btn btn-sm btn-warning">Editar</a>
          <a href="{% url 'iniciacoes:excluir_grau' grau.id %}" class="btn btn-sm btn-danger">Excluir</a>
        </td>
      </tr>
      {% empty %}
      <tr>
        <td colspan="5">Nenhum grau cadastrado.</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}

```


### Arquivo: iniciacoes\templates\iniciacoes\listar_iniciacoes.html

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Iniciações</h1>
  
    <div class="d-flex justify-content-between mb-3">
      <a href="{% url 'iniciacoes:criar_iniciacao' %}" class="btn btn-primary">Nova Iniciação</a>
      <a href="{% url 'iniciacoes:listar_graus' %}" class="btn btn-info">Gerenciar Graus</a>
    </div>
  
    <div class="card mb-4">
      <div class="card-header">
        <h5>Filtros</h5>
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
            <label for="grau" class="form-label">Grau</label>
            <select name="grau" id="grau" class="form-select">
              <option value="">Todos</option>
              {% for grau in graus %}
                <option value="{{ grau.id }}" {% if request.GET.grau == grau.id|stringformat:"i" %}selected{% endif %}>
                  {{ grau.nome }}
                </option>
              {% endfor %}
            </select>
          </div>
          <div class="col-md-4">
            <label for="data" class="form-label">Data</label>
            <input type="date" name="data" id="data" class="form-control" value="{{ request.GET.data }}">
          </div>
          <div class="col-12 mt-3">
            <button type="submit" class="btn btn-primary">Filtrar</button>
            <a href="{% url 'iniciacoes:listar_iniciacoes' %}" class="btn btn-secondary">Limpar Filtros</a>
          </div>
        </form>
      </div>
    </div>
  
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Aluno</th>
          <th>Grau</th>
          <th>Data</th>
          <th>Local</th>
          <th>Status</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        {% for iniciacao in iniciacoes %}
        <tr>
          <td>{{ iniciacao.aluno.nome }}</td>
          <td>{{ iniciacao.grau.nome }}</td>
          <td>{{ iniciacao.data|date:"d/m/Y" }}</td>
          <td>{{ iniciacao.local }}</td>
          <td>
            {% if iniciacao.concluida %}
              <span class="badge bg-success">Concluída</span>
            {% else %}
              <span class="badge bg-warning">Pendente</span>
            {% endif %}
          </td>
          <td>
            <a href="{% url 'iniciacoes:detalhar_iniciacao' iniciacao.id %}" class="btn btn-sm btn-info">Detalhes</a>
            <a href="{% url 'iniciacoes:editar_iniciacao' iniciacao.id %}" class="btn btn-sm btn-warning">Editar</a>
            <a href="{% url 'iniciacoes:excluir_iniciacao' iniciacao.id %}" class="btn btn-sm btn-danger">Excluir</a>
          </td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="6">Nenhuma iniciação encontrada.</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  
    {% if iniciacoes.has_other_pages %}
    <nav aria-label="Paginação">
      <ul class="pagination justify-content-center">
        {% if iniciacoes.has_previous %}
          <li class="page-item">
            <a class="page-link" href="?page=1{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Primeira">
              <span aria-hidden="true">««</span>
            </a>
          </li>
          <li class="page-item">
            <a class="page-link" href="?page={{ iniciacoes.previous_page_number }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Anterior">
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
      
        {% for i in iniciacoes.paginator.page_range %}
          {% if iniciacoes.number == i %}
            <li class="page-item active"><a class="page-link" href="#">{{ i }}</a></li>
          {% elif i > iniciacoes.number|add:'-3' and i < iniciacoes.number|add:'3' %}
            <li class="page-item">
              <a class="page-link" href="?page={{ i }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}">{{ i }}</a>
            </li>
          {% endif %}
        {% endfor %}
      
        {% if iniciacoes.has_next %}
          <li class="page-item">
            <a class="page-link" href="?page={{ iniciacoes.next_page_number }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Próxima">
              <span aria-hidden="true">»</span>
            </a>
          </li>
          <li class="page-item">
            <a class="page-link" href="?page={{ iniciacoes.paginator.num_pages }}{% if request.GET.aluno %}&aluno={{ request.GET.aluno }}{% endif %}{% if request.GET.grau %}&grau={{ request.GET.grau }}{% endif %}{% if request.GET.data %}&data={{ request.GET.data }}{% endif %}" aria-label="Última">
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
{% endblock %}
```
