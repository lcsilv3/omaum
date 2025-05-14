# Revisão da Funcionalidade: cursos

## Arquivos forms.py:


### Arquivo: cursos\forms.py

python
from django import forms
from importlib import import_module


def get_curso_model():
    cursos_module = import_module("cursos.models")
    return getattr(cursos_module, "Curso")


class CursoForm(forms.ModelForm):
    class Meta:
        model = get_curso_model()
        fields = ["codigo_curso", "nome", "descricao", "duracao"]
        widgets = {
            "codigo_curso": forms.NumberInput(
                attrs={"class": "form-control", "min": "1"}
            ),
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "duracao": forms.NumberInput(
                attrs={"class": "form-control", "min": "1"}
            ),
        }

    def clean_codigo_curso(self):
        codigo = self.cleaned_data.get("codigo_curso")
        if codigo <= 0:
            raise forms.ValidationError(
                "O código do curso deve ser um número inteiro positivo."
            )
        return codigo

    def clean_nome(self):
        nome = self.cleaned_data.get("nome")
        if len(nome) < 3:
            raise ValidationError(
                "O nome do curso deve ter pelo menos 3 caracteres."
            )
        return nome



## Arquivos views.py:


### Arquivo: cursos\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from importlib import import_module


def get_models():
    cursos_module = import_module("cursos.models")
    return getattr(cursos_module, "Curso")


def get_forms():
    cursos_forms = import_module("cursos.forms")
    return getattr(cursos_forms, "CursoForm")


@login_required
def listar_cursos(request):
    """Lista todos os cursos cadastrados."""
    Curso = get_models()
    cursos = Curso.objects.all()
    return render(request, "cursos/listar_cursos.html", {"cursos": cursos})


@login_required
def criar_curso(request):
    """Cria um novo curso."""
    CursoForm = get_forms()
    if request.method == "POST":
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Curso criado com sucesso!")
            return redirect("cursos:listar_cursos")
    else:
        form = CursoForm()
    return render(request, "cursos/criar_curso.html", {"form": form})


@login_required
def detalhar_curso(request, codigo_curso):
    """Exibe os detalhes de um curso."""
    Curso = get_models()
    curso = get_object_or_404(Curso, codigo_curso=codigo_curso)
    return render(request, "cursos/detalhar_curso.html", {"curso": curso})


@login_required
def editar_curso(request, codigo_curso):
    """Edita um curso existente."""
    Curso = get_models()
    CursoForm = get_forms()
    curso = get_object_or_404(Curso, codigo_curso=codigo_curso)

    if request.method == "POST":
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, "Curso atualizado com sucesso!")
            return redirect("cursos:listar_cursos")
    else:
        form = CursoForm(instance=curso)

    return render(
        request, "cursos/editar_curso.html", {"form": form, "curso": curso}
    )


@login_required
def excluir_curso(request, codigo_curso):
    """Exclui um curso."""
    Curso = get_models()
    curso = get_object_or_404(Curso, codigo_curso=codigo_curso)

    if request.method == "POST":
        curso.delete()
        messages.success(request, "Curso excluído com sucesso!")
        return redirect("cursos:listar_cursos")

    return render(request, "cursos/excluir_curso.html", {"curso": curso})

@login_required
def exportar_cursos(request):
    """Exporta os dados dos cursos para um arquivo CSV."""
    try:
        import csv
        from django.http import HttpResponse
        
        Curso = get_models()
        cursos = Curso.objects.all()
        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="cursos.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Código",
            "Nome",
            "Descrição",
            "Duração (meses)"
        ])
        
        for curso in cursos:
            writer.writerow([
                curso.codigo_curso,
                curso.nome,
                curso.descricao,
                curso.duracao
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar cursos: {str(e)}")
        return redirect("cursos:listar_cursos")

@login_required
def importar_cursos(request):
    """Importa cursos de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            import csv
            from io import TextIOWrapper
            
            Curso = get_models()
            
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            count = 0
            errors = []
            
            for row in reader:
                try:
                    # Processar código do curso
                    codigo_curso = None
                    try:
                        codigo_curso = int(row.get("Código", "").strip())
                    except ValueError:
                        errors.append(f"Código de curso inválido: {row.get('Código', '')}")
                        continue
                    
                    # Verificar se já existe um curso com este código
                    if Curso.objects.filter(codigo_curso=codigo_curso).exists():
                        errors.append(f"Já existe um curso com o código {codigo_curso}")
                        continue
                    
                    # Processar duração
                    duracao = 6  # Valor padrão
                    try:
                        if row.get("Duração (meses)"):
                            duracao = int(row.get("Duração (meses)"))
                    except ValueError:
                        errors.append(f"Duração inválida: {row.get('Duração (meses)', '')}")
                        continue
                    
                    # Criar o curso
                    Curso.objects.create(
                        codigo_curso=codigo_curso,
                        nome=row.get("Nome", "").strip(),
                        descricao=row.get("Descrição", "").strip(),
                        duracao=duracao
                    )
                    
                    count += 1
                except Exception as e:
                    errors.append(f"Erro na linha {count+1}: {str(e)}")
            
            if errors:
                messages.warning(
                    request,
                    f"{count} cursos importados com {len(errors)} erros.",
                )
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(
                        request, f"... e mais {len(errors) - 5} erros."
                    )
            else:
                messages.success(
                    request, f"{count} cursos importados com sucesso!"
                )
            return redirect("cursos:listar_cursos")
        except Exception as e:
            messages.error(request, f"Erro ao importar cursos: {str(e)}")
    
    return render(request, "cursos/importar_cursos.html")



## Arquivos urls.py:


### Arquivo: cursos\urls.py

python
from django.urls import path
from . import views

app_name = "cursos"

urlpatterns = [
    path("", views.listar_cursos, name="listar_cursos"),
    path("criar/", views.criar_curso, name="criar_curso"),
    path("<int:codigo_curso>/", views.detalhar_curso, name="detalhar_curso"),
    path(
        "<int:codigo_curso>/editar/", views.editar_curso, name="editar_curso"
    ),
    path(
        "<int:codigo_curso>/excluir/",
        views.excluir_curso,
        name="excluir_curso",
    ),
    path("exportar/", views.exportar_cursos, name="exportar_cursos"),
    path("importar/", views.importar_cursos, name="importar_cursos"),
]



## Arquivos models.py:


### Arquivo: cursos\models.py

python
from django.db import models
from django.core.validators import MinValueValidator


class Curso(models.Model):
    codigo_curso = models.IntegerField(
        "Código do Curso",
        primary_key=True,
        validators=[MinValueValidator(1)],
        help_text="Digite um número inteiro positivo",
    )
    nome = models.CharField("Nome do Curso", max_length=100)
    descricao = models.TextField("Descrição", blank=True)
    duracao = models.PositiveIntegerField("Duração (meses)", default=6)

    def __str__(self):
        return f"{self.codigo_curso} - {self.nome}"

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["codigo_curso"]



## Arquivos de Template:


### Arquivo: cursos\templates\cursos\criar_curso.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Criar Novo Curso</h1>
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        <!-- Padronizar botões no formulário -->
        <div class="mt-3">
            <button type="submit" class="btn btn-primary">
                <i class="fas fa-save"></i> {% if curso.codigo_curso %}Atualizar{% else %}Criar{% endif %} Curso
            </button>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">
                <i class="fas fa-arrow-left"></i> Voltar
            </a>
            <a href="{% url 'cursos:listar_cursos' %}" class="btn btn-secondary">
                <i class="fas fa-times"></i> Cancelar
            </a>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: cursos\templates\cursos\detalhar_curso.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
  <h1>Detalhes do Curso</h1>
  
  <div class="card">
    <div class="card-header">
      <h2>{{ curso.nome }}</h2>
    </div>
    <div class="card-body">
      <p><strong>Código:</strong> {{ curso.codigo_curso }}</p>
      <p><strong>Descrição:</strong> {{ curso.descricao }}</p>
      <p><strong>Duração:</strong> {{ curso.duracao }} meses</p>
    </div>
    <div class="card-footer">
      <a href="javascript:history.back()" class="btn btn-secondary me-2">
        <i class="fas fa-arrow-left"></i> Voltar
      </a>
      <a href="{% url 'cursos:editar_curso' curso.codigo_curso %}" class="btn btn-warning me-2">
        <i class="fas fa-edit"></i> Editar
      </a>
      <a href="{% url 'cursos:excluir_curso' curso.codigo_curso %}" class="btn btn-danger me-2">
        <i class="fas fa-trash"></i> Excluir
      </a>
      <a href="{% url 'cursos:listar_cursos' %}" class="btn btn-secondary">
        <i class="fas fa-list"></i> Voltar para a lista
      </a>
    </div>
  </div>
</div>
{% endblock %}





### Arquivo: cursos\templates\cursos\editar_curso.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Editar Curso</h1>
    <form method="post">
        {% csrf_token %}
        {% include 'includes/form_errors.html' %}
        {% for field in form %}
            {% include 'includes/form_field.html' %}
        {% endfor %}
        <div class="mt-3">
            <button type="submit" class="btn btn-primary">Atualizar Curso</button>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'cursos:listar_cursos' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: cursos\templates\cursos\excluir_curso.html

html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h1>Excluir Curso</h1>
    <p>Tem certeza que deseja excluir o curso "{{ curso.nome }}"?</p>
    
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Sim, excluir</button>
        <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
        <a href="{% url 'cursos:listar_cursos' %}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}




### Arquivo: cursos\templates\cursos\importar_cursos.html

html
{% extends 'base.html' %}

{% block title %}Importar Cursos{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Importar Cursos</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="mb-3">Faça upload de um arquivo CSV contendo os dados dos cursos.</p>
            
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="csv_file" class="form-label">Arquivo CSV</label>
                    <input type="file" name="csv_file" id="csv_file" class="form-control" accept=".csv" required>
                    <div class="form-text">O arquivo deve ter cabeçalhos: Código, Nome, Descrição, Duração (meses)</div>
                </div>
                
                <div class="d-flex">
                    <button type="submit" class="btn btn-primary me-2">Importar</button>
                    <a href="{% url 'cursos:listar_cursos' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{% url 'cursos:listar_cursos' %}" class="btn btn-link">Voltar para a lista de cursos</a>
    </div>
</div>
{% endblock %}



### Arquivo: cursos\templates\cursos\listar_cursos.html

html
{% extends 'base.html' %}

{% block title %}Lista de Cursos{% endblock %}

{% block content %}
<div class="container mt-4">
  <!-- Padronizar cabeçalho com botões -->
  <div class="d-flex justify-content-between align-items-center mb-3">
      <h1>Lista de Cursos</h1>
      <div>
          <a href="javascript:history.back()" class="btn btn-secondary me-2">
              <i class="fas fa-arrow-left"></i> Voltar
          </a>
          <a href="{% url 'cursos:criar_curso' %}" class="btn btn-primary me-2">
              <i class="fas fa-plus"></i> Novo Curso
          </a>
          <a href="{% url 'cursos:exportar_cursos' %}" class="btn btn-success me-2">
              <i class="fas fa-file-export"></i> Exportar CSV
          </a>
          <a href="{% url 'cursos:importar_cursos' %}" class="btn btn-info">
              <i class="fas fa-file-import"></i> Importar CSV
          </a>
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
                          <th>Código</th>
                          <th>Nome</th>
                          <th>Duração (meses)</th>
                          <th>Ações</th>
                      </tr>
                  </thead>
                  <tbody>
                      {% for curso in cursos %}
                          <tr>
                              <td>{{ curso.codigo_curso }}</td>
                              <td>{{ curso.nome }}</td>
                              <td>{{ curso.duracao }}</td>
                              <td>
                                  <a href="{% url 'cursos:detalhar_curso' curso.codigo_curso %}" class="btn btn-sm btn-info" title="Ver detalhes completos do curso">Detalhes</a>
                                  <a href="{% url 'cursos:editar_curso' curso.codigo_curso %}" class="btn btn-sm btn-warning" title="Editar informações do curso">Editar</a>
                                  <a href="{% url 'cursos:excluir_curso' curso.codigo_curso %}" class="btn btn-sm btn-danger" title="Excluir este curso">Excluir</a>
                              </td>
                          </tr>
                      {% empty %}
                          <tr>
                              <td colspan="4" class="text-center">
                                  <p class="my-3">Nenhum curso cadastrado.</p>
                              </td>
                          </tr>
                      {% endfor %}
                  </tbody>
              </table>
          </div>
      </div>
      <div class="card-footer">
          <p class="text-muted mb-0">Total: {{ cursos.count|default:"0" }} curso(s)</p>
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
</div>
{% endblock %}


