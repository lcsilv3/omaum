# Revisão da Funcionalidade: cargos

## Arquivos forms.py:


### Arquivo: cargos\forms.py

python
from django import forms
from .models import CargoAdministrativo
from alunos.models import Aluno


class CargoAdministrativoForm(forms.ModelForm):
    """
    Formulário para criação e edição de Cargos Administrativos.
    """

    class Meta:
        model = CargoAdministrativo
        fields = ["codigo_cargo", "nome", "descricao"]
        widgets = {
            "codigo_cargo": forms.TextInput(attrs={"class": "form-control"}),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }
        labels = {
            "codigo_cargo": "Código do Cargo",
            "nome": "Nome",
            "descricao": "Descrição",
        }
        help_texts = {
            "codigo_cargo": "Código único que identifica o cargo (ex: COORD, DIR, etc.)",
            "nome": "Nome completo do cargo administrativo",
            "descricao": "Descrição detalhada das responsabilidades do cargo",
        }
        error_messages = {
            "codigo_cargo": {
                "unique": "Este código de cargo já está em uso. Por favor, escolha outro.",
                "required": "O código do cargo é obrigatório.",
                "max_length": "O código do cargo não pode ter mais de 10 caracteres.",
            },
            "nome": {
                "required": "O nome do cargo é obrigatório.",
                "max_length": "O nome do cargo não pode ter mais de 100 caracteres.",
            },
        }

    def clean_codigo_cargo(self):
        """
        Validação personalizada para o campo codigo_cargo.
        Converte o código para maiúsculas e remove espaços extras.
        """
        codigo = self.cleaned_data.get("codigo_cargo")
        if codigo:
            return codigo.upper().strip()
        return codigo

    def clean_nome(self):
        """
        Validação personalizada para o campo nome.
        Capitaliza a primeira letra de cada palavra e remove espaços extras.
        """
        nome = self.cleaned_data.get("nome")
        if nome:
            return " ".join(word.capitalize() for word in nome.split())
        return nome


class AtribuirCargoForm(forms.Form):
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        label="Aluno",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    cargo = forms.ModelChoiceField(
        queryset=CargoAdministrativo.objects.all(),
        label="Cargo",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    data_inicio = forms.DateField(
        label="Data de Início",
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
    )
    data_fim = forms.DateField(
        label="Data de Término",
        required=False,
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
    )



## Arquivos views.py:


### Arquivo: cargos\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Importar a função utilitária centralizada
from core.utils import get_model_dynamically, get_form_dynamically

# Importar o formulário diretamente, pois está no mesmo aplicativo
from .forms import AtribuirCargoForm
from .models import AtribuicaoCargo

def get_cargo_administrativo_model():
    """Obtém o modelo CargoAdministrativo dinamicamente."""
    return get_model_dynamically("cargos", "CargoAdministrativo")

def get_cargo_administrativo_form():
    """Obtém o formulário CargoAdministrativoForm dinamicamente."""
    return get_form_dynamically("cargos", "CargoAdministrativoForm")


@login_required
def listar_cargos(request):
    """Lista todos os cargos administrativos."""
    CargoAdministrativo = get_models()
    cargos = CargoAdministrativo.objects.all()
    return render(request, "cargos/listar_cargos.html", {"cargos": cargos})


@login_required
def criar_cargo(request):
    """Cria um novo cargo administrativo."""
    CargoAdministrativoForm = get_forms()

    if request.method == "POST":
        form = CargoAdministrativoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Cargo administrativo criado com sucesso!"
            )
            return redirect("cargos:listar_cargos")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = CargoAdministrativoForm()

    return render(request, "cargos/criar_cargo.html", {"form": form})


@login_required
def detalhar_cargo(request, id):
    """Exibe os detalhes de um cargo administrativo."""
    CargoAdministrativo = get_models()
    cargo = get_object_or_404(CargoAdministrativo, id=id)
    return render(request, "cargos/detalhar_cargo.html", {"cargo": cargo})


@login_required
def editar_cargo(request, id):
    """Edita um cargo administrativo existente."""
    CargoAdministrativo = get_models()
    CargoAdministrativoForm = get_forms()

    cargo = get_object_or_404(CargoAdministrativo, id=id)

    if request.method == "POST":
        form = CargoAdministrativoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Cargo administrativo atualizado com sucesso!"
            )
            return redirect("cargos:listar_cargos")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = CargoAdministrativoForm(instance=cargo)

    return render(
        request, "cargos/editar_cargo.html", {"form": form, "cargo": cargo}
    )


@login_required
def excluir_cargo(request, id):
    """Exclui um cargo administrativo."""
    CargoAdministrativo = get_models()
    cargo = get_object_or_404(CargoAdministrativo, id=id)

    if request.method == "POST":
        cargo.delete()
        messages.success(request, "Cargo administrativo excluído com sucesso!")
        return redirect("cargos:listar_cargos")

    return render(request, "cargos/excluir_cargo.html", {"cargo": cargo})


@login_required
def atribuir_cargo(request):
    if request.method == "POST":
        form = AtribuirCargoForm(request.POST)
        if form.is_valid():
            atribuicao = AtribuicaoCargo(
                aluno=form.cleaned_data["aluno"],
                cargo=form.cleaned_data["cargo"],
                data_inicio=form.cleaned_data["data_inicio"],
                data_fim=form.cleaned_data["data_fim"],
            )
            atribuicao.save()
            messages.success(request, "Cargo atribuído com sucesso!")
            return redirect("cargos:listar_cargos")
    else:
        form = AtribuirCargoForm()

    return render(request, "cargos/atribuir_cargo.html", {"form": form})


@login_required
def remover_atribuicao_cargo(request, id):
    """Remove a atribuição de um cargo a um aluno."""
    # Implementação pendente
    return render(request, "cargos/remover_atribuicao.html")



## Arquivos urls.py:


### Arquivo: cargos\urls.py

python
from django.urls import path
from . import views

app_name = "cargos"

urlpatterns = [
    path("", views.listar_cargos, name="listar_cargos"),
    path("criar/", views.criar_cargo, name="criar_cargo"),
    path("<int:id>/detalhes/", views.detalhar_cargo, name="detalhar_cargo"),
    path("<int:id>/editar/", views.editar_cargo, name="editar_cargo"),
    path("<int:id>/excluir/", views.excluir_cargo, name="excluir_cargo"),
    path("atribuir/", views.atribuir_cargo, name="atribuir_cargo"),
    path(
        "remover-atribuicao/<int:id>/",
        views.remover_atribuicao_cargo,
        name="remover_atribuicao_cargo",
    ),
]



## Arquivos models.py:


### Arquivo: cargos\models.py

python
from django.db import models
from alunos.models import Aluno


class CargoAdministrativo(models.Model):
    """
    Representa um cargo administrativo no sistema. O cargo administrativo possui um código único,
    um nome e uma descrição opcional.
    """

    codigo_cargo = models.CharField(
        max_length=10, unique=True, verbose_name="Código do Cargo"
    )
    nome = models.CharField(max_length=100, verbose_name="Nome")
    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cargo Administrativo"
        verbose_name_plural = "Cargos Administrativos"
        ordering = ["nome"]


class AtribuicaoCargo(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    cargo = models.ForeignKey(CargoAdministrativo, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)

    # Modificar este campo para permitir valores nulos
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.SET_NULL,
        null=True,  # Permitir valores nulos
        blank=True,  # Permitir campo em branco nos formulários
        verbose_name="Turma",
        related_name="atribuicoes_cargo",
    )

    class Meta:
        verbose_name = "Atribuição de Cargo"
        verbose_name_plural = "Atribuições de Cargos"

    def __str__(self):
        return f"{self.aluno.nome} - {self.cargo.nome}"



## Arquivos de Template:


### Arquivo: cargos\templates\cargos\atribuir_cargo.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Atribuir Cargo</h1>
  
  <form method="post">
    {% csrf_token %}
    {% include 'includes/form_errors.html' %}
    
    {% for field in form %}
      <div class="mb-3">
        <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
        {{ field }}
        {% if field.help_text %}
          <small class="form-text text-muted">{{ field.help_text }}</small>
        {% endif %}
      </div>
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Atribuir</button>
    <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}




### Arquivo: cargos\templates\cargos\confirmar_exclusao.html

html
{% extends 'base.html' %}

{% block title %}Confirmar Exclusão{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Confirmar Exclusão</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="lead">Tem certeza que deseja excluir o cargo administrativo "{{ cargo.nome }}"?</p>
            <p class="text-danger">Esta ação não pode ser desfeita.</p>
            
            <form method="post">
                {% csrf_token %}
                <button type="submit" class="btn btn-danger">Sim, excluir</button>
                <a href="{% url 'cargos:listar_cargos_administrativos' %}" class="btn btn-secondary">Cancelar</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: cargos\templates\cargos\criar_cargo.html

html
{% extends 'base.html' %}

{% block title %}Criar Novo Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Criar Novo Cargo Administrativo</h1>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        
        <button type="submit" class="btn btn-primary">Criar Cargo</button>
        <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




### Arquivo: cargos\templates\cargos\detalhar_cargo.html

html
{% extends 'core/base.html' %}

{% block title %}Detalhes do Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes do Cargo Administrativo</h1>
  
  <div class="card">
    <div class="card-header">
      <h2>{{ cargo.nome }}</h2>
    </div>
    <div class="card-body">
      <p><strong>Código:</strong> {{ cargo.codigo_cargo }}</p>
      <p><strong>Descrição:</strong> {{ cargo.descricao|default:"Não informada" }}</p>
    </div>
    <div class="card-footer">
      <a href="{% url 'cargos:editar_cargo' cargo.id %}" class="btn btn-warning">Editar</a>
      <a href="{% url 'cargos:excluir_cargo' cargo.id %}" class="btn btn-danger">Excluir</a>
      <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Voltar</a>
    </div>
  </div>
</div>
{% endblock %}




### Arquivo: cargos\templates\cargos\detalhe_cargo.html

html
{% extends 'base.html' %}

{% block title %}Detalhes do Cargo{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">Detalhes do Cargo Administrativo</h1>
    
    <div class="card">
        <div class="card-body">
            <h2>{{ cargo.nome }}</h2>
            <p><strong>Código:</strong> {{ cargo.codigo_cargo }}</p>
            <p><strong>Descrição:</strong> {{ cargo.descricao }}</p>
            
            <div class="mt-3">
                <a href="{% url 'cargos:editar_cargo' cargo.codigo_cargo %}" class="btn btn-warning">Editar</a>
                <a href="{% url 'cargos:excluir_cargo' cargo.codigo_cargo %}" class="btn btn-danger">Excluir</a>
                <a href="{% url 'cargos:listar_cargos_administrativos' %}" class="btn btn-secondary">Voltar para a Lista</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}




### Arquivo: cargos\templates\cargos\detalhes_cargo.html

html
{% extends 'base.html' %}

{% block title %}Detalhes do Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes do Cargo Administrativo</h1>
  
  <div class="card">
    <div class="card-header">
      <h2>{{ cargo.nome }}</h2>
    </div>
    <div class="card-body">
      <p><strong>Código:</strong> {{ cargo.codigo_cargo }}</p>
      <p><strong>Descrição:</strong> {{ cargo.descricao|default:"Não informada" }}</p>
    </div>
    <div class="card-footer">
      <a href="{% url 'cargos:editar_cargo' cargo.id %}" class="btn btn-warning">Editar</a>
      <a href="{% url 'cargos:excluir_cargo' cargo.id %}" class="btn btn-danger">Excluir</a>
      <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Voltar</a>
    </div>
  </div>
</div>
{% endblock %}




### Arquivo: cargos\templates\cargos\editar_cargo.html

html
{% extends 'base.html' %}

{% block title %}Editar Cargo Administrativo{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Cargo Administrativo</h1>
    
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        
        <button type="submit" class="btn btn-primary">Atualizar Cargo</button>
        <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




### Arquivo: cargos\templates\cargos\excluir_cargo.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Cargo</h1>
  
    <div class="alert alert-danger">
      <p>Tem certeza que deseja excluir o cargo "{{ cargo.nome }}"?</p>
      {% if atribuicoes %}
        <p><strong>Atenção:</strong> Este cargo possui {{ atribuicoes.count }} atribuições. Excluir o cargo removerá todas as atribuições associadas.</p>
      {% endif %}
    </div>
  
    <form method="post">
      {% csrf_token %}
      <button type="submit" class="btn btn-danger">Sim, excluir</button>
      <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




### Arquivo: cargos\templates\cargos\form_cargo.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>{% if cargo.id %}Editar{% else %}Novo{% endif %} Cargo</h1>
  
  <form method="post">
    {% csrf_token %}
    {% include 'includes/form_errors.html' %}
    
    {% for field in form %}
      {% include 'includes/form_field.html' %}
    {% endfor %}
    
    <button type="submit" class="btn btn-primary">Salvar</button>
    <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}




### Arquivo: cargos\templates\cargos\formulario_cargo.html

html
{% extends 'base.html' %}

{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="container">
    <h1 class="my-4">{{ titulo }}</h1>
    
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
            <a href="{% url 'cargos:listar_cargos_administrativos' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}




### Arquivo: cargos\templates\cargos\listar_cargos.html

html
{% extends 'base.html' %}

{% block title %}Lista de Cargos{% endblock %}

{% block content %}
<div class="container mt-4">
  <!-- Cabeçalho com título e botões na mesma linha -->
  <div class="d-flex justify-content-between align-items-center mb-3">
      <h1>Lista de Cargos</h1>
      <div>
          <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
          <a href="{% url 'cargos:criar_cargo' %}" class="btn btn-primary">Novo Cargo</a>
          <a href="{% url 'cargos:atribuir_cargo' %}" class="btn btn-success">Atribuir Cargo</a>
      </div>
  </div>
    
  <!-- Barra de busca e filtros -->
  <div class="card mb-4">
      <div class="card-header">
          <form method="get" class="row g-3">
              <div class="col-md-6">
                  <input type="text" name="q" class="form-control" placeholder="Buscar por nome ou código..." value="{{ query }}">
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
                          <th>Nome</th>
                          <th>Código</th>
                          <th>Descrição</th>
                          <th>Ações</th>
                      </tr>
                  </thead>
                  <tbody>
                      {% for cargo in cargos %}
                          <tr>
                              <td>{{ cargo.nome }}</td>
                              <td>{{ cargo.codigo_cargo }}</td>
                              <td>{{ cargo.descricao|truncatechars:50 }}</td>
                              <td>
                                  <a href="{% url 'cargos:detalhar_cargo' cargo.id %}" class="btn btn-sm btn-info" title="Ver detalhes completos do cargo">Detalhes</a>
                                  <a href="{% url 'cargos:editar_cargo' cargo.id %}" class="btn btn-sm btn-warning" title="Editar informações do cargo">Editar</a>
                                  <a href="{% url 'cargos:excluir_cargo' cargo.id %}" class="btn btn-sm btn-danger" title="Excluir este cargo">Excluir</a>
                              </td>
                          </tr>
                      {% empty %}
                          <tr>
                              <td colspan="4" class="text-center">
                                  <p class="my-3">Nenhum cargo cadastrado.</p>
                              </td>
                          </tr>
                      {% endfor %}
                  </tbody>
              </table>
          </div>
      </div>
      <div class="card-footer">
          <p class="text-muted mb-0">Total: {{ cargos.count|default:"0" }} cargo(s)</p>
          {% if page_obj.has_other_pages %}
              <nav aria-label="Paginação">
                  <ul class="pagination justify-content-center mb-0">
                      {% if page_obj.has_previous %}
                          <li class="page-item">
                              <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ query }}">Anterior</a>
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
                                  <a class="page-link" href="?page={{ num }}&q={{ query }}">{{ num }}</a>
                              </li>
                          {% endif %}
                      {% endfor %}

                      {% if page_obj.has_next %}
                          <li class="page-item">
                              <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ query }}">Próxima</a>
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
    
  <!-- Seção de Atribuições de Cargos -->
  <h2 class="mt-5">Atribuições de Cargos</h2>
  <div class="card mb-4">
      <div class="card-body">
          <div class="table-responsive">
              <table class="table table-striped">
                  <thead>
                      <tr>
                          <th>Aluno</th>
                          <th>Cargo</th>
                          <th>Data de Início</th>
                          <th>Data de Término</th>
                          <th>Ações</th>
                      </tr>
                  </thead>
                  <tbody>
                      {% for atribuicao in atribuicoes %}
                          <tr>
                              <td>{{ atribuicao.aluno.nome }}</td>
                              <td>{{ atribuicao.cargo.nome }}</td>
                              <td>{{ atribuicao.data_inicio|date:"d/m/Y" }}</td>
                              <td>{{ atribuicao.data_fim|date:"d/m/Y"|default:"Atual" }}</td>
                              <td>
                                  <a href="{% url 'cargos:remover_atribuicao_cargo' atribuicao.id %}" class="btn btn-sm btn-danger" title="Remover esta atribuição de cargo">Remover</a>
                              </td>
                          </tr>
                      {% empty %}
                          <tr>
                              <td colspan="5" class="text-center">
                                  <p class="my-3">Nenhuma atribuição de cargo cadastrada.</p>
                              </td>
                          </tr>
                      {% endfor %}
                  </tbody>
              </table>
          </div>
      </div>
  </div>
</div>
{% endblock %}



### Arquivo: cargos\templates\cargos\remover_atribuicao.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Remover Atribuição de Cargo</h1>
  
  <div class="alert alert-danger">
    <p>Tem certeza que deseja remover a atribuição do cargo "{{ atribuicao.cargo.nome }}" para o aluno "{{ atribuicao.aluno.nome }}"?</p>
  </div>
  
  <form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Sim, remover</button>
    <a href="{% url 'cargos:listar_cargos' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}


