# Revisão da Funcionalidade: matriculas

## Arquivos views.py:


### Arquivo: matriculas\views.py

python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ValidationError
from importlib import import_module
from django.urls import reverse


def get_model(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    from importlib import import_module
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


@login_required
def listar_matriculas(request):
    """Lista todas as matrículas."""
    Matricula = get_model("matriculas", "Matricula")
    matriculas = Matricula.objects.all().select_related("aluno", "turma")
    return render(
        request,
        "matriculas/listar_matriculas.html",
        {"matriculas": matriculas},
    )


@login_required
def detalhar_matricula(request, id):
    """Exibe os detalhes de uma matrícula."""
    Matricula = get_model("matriculas", "Matricula")
    matricula = get_object_or_404(Matricula, id=id)
    return render(
        request, "matriculas/detalhar_matricula.html", {"matricula": matricula}
    )


@login_required
def realizar_matricula(request):
    """Realiza uma nova matrícula."""
    Aluno = get_model("alunos", "Aluno")
    Turma = get_model("turmas", "Turma")
    Matricula = get_model("matriculas", "Matricula")

    if request.method == "POST":
        aluno_id = request.POST.get("aluno")
        turma_id = request.POST.get("turma")

        if not aluno_id or not turma_id:
            messages.error(request, "Selecione um aluno e uma turma.")
            return redirect("matriculas:realizar_matricula")

        aluno = get_object_or_404(Aluno, cpf=aluno_id)
        turma = get_object_or_404(Turma, id=turma_id)
        # Verificar se já existe matrícula
        if Matricula.objects.filter(aluno=aluno, turma=turma).exists():
            messages.warning(
                request,
                f"O aluno {aluno.nome} já está matriculado nesta turma.",
            )
            return redirect("matriculas:listar_matriculas")

        try:
            matricula = Matricula(
                aluno=aluno,
                turma=turma,
                data_matricula=timezone.now().date(),
                ativa=True,
                status="A",  # Ativa
            )
            matricula.full_clean()  # Valida o modelo
            matricula.save()
            messages.success(
                request,
                f"Matrícula realizada com sucesso para {aluno.nome} na turma {turma.nome}.",
            )
            return redirect("matriculas:listar_matriculas")
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        except Exception as e:
            messages.error(request, f"Erro ao realizar matrícula: {str(e)}")

    # Para o método GET, exibir o formulário
    alunos = Aluno.objects.all()
    turmas = Turma.objects.filter(status="A")  # Apenas turmas ativas
    return render(
        request,
        "matriculas/realizar_matricula.html",
        {"alunos": alunos, "turmas": turmas},
    )


@login_required
def cancelar_matricula(request, id):
    """Cancela uma matrícula existente."""
    Matricula = get_model("matriculas", "Matricula")
    matricula = get_object_or_404(Matricula, id=id)

    if request.method == "POST":
        matricula.status = "C"  # Cancelada
        matricula.save()
        messages.success(
            request,
            f"Matrícula de {matricula.aluno.nome} na turma {matricula.turma.nome} cancelada com sucesso.",
        )
        return redirect("matriculas:listar_matriculas")

    return render(
        request, "matriculas/cancelar_matricula.html", {"matricula": matricula}
    )


@login_required
def cancelar_matricula_por_turma_aluno(request, turma_id, aluno_cpf):
    """Cancela uma matrícula identificada pela turma e pelo CPF do aluno."""
    Matricula = get_model("matriculas", "Matricula")
    Aluno = get_model("alunos", "Aluno")
    Turma = get_model("turmas", "Turma")
    
    # Obter os objetos necessários
    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
    turma = get_object_or_404(Turma, id=turma_id)
    matricula = get_object_or_404(Matricula, aluno=aluno, turma=turma)
    
    if request.method == "POST":
        matricula.status = "C"  # Cancelada
        matricula.save()
        messages.success(
            request,
            f"Matrícula de {aluno.nome} na turma {turma.nome} cancelada com sucesso."
        )
        return redirect("turmas:detalhar_turma", turma_id=turma_id)
    
    # Para requisições GET, exibir página de confirmação
    return render(
        request, 
        "matriculas/cancelar_matricula.html", 
        {
            "matricula": matricula,
            "return_url": reverse("turmas:detalhar_turma", args=[turma_id])
        }
    )


@login_required
def exportar_matriculas(request):
    """Exporta os dados das matrículas para um arquivo CSV."""
    try:
        import csv
        from django.http import HttpResponse
        
        Matricula = get_model("matriculas", "Matricula")
        matriculas = Matricula.objects.all().select_related('aluno', 'turma', 'turma__curso')
        
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="matriculas.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "ID",
            "Aluno (CPF)",
            "Aluno (Nome)",
            "Turma",
            "Curso",
            "Data da Matrícula",
            "Status"
        ])
        
        for matricula in matriculas:
            writer.writerow([
                matricula.id,
                matricula.aluno.cpf,
                matricula.aluno.nome,
                matricula.turma.nome,
                matricula.turma.curso.nome if matricula.turma.curso else "",
                matricula.data_matricula,
                matricula.get_status_display()
            ])
        
        return response
    except Exception as e:
        messages.error(request, f"Erro ao exportar matrículas: {str(e)}")
        return redirect("matriculas:listar_matriculas")

@login_required
def importar_matriculas(request):
    """Importa matrículas de um arquivo CSV."""
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            import csv
            from io import TextIOWrapper
            from django.utils import timezone
            
            Matricula = get_model("matriculas", "Matricula")
            Aluno = get_model("alunos", "Aluno")
            Turma = get_model("turmas", "Turma")
            
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding="utf-8")
            reader = csv.DictReader(csv_file)
            count = 0
            errors = []
            
            for row in reader:
                try:
                    # Buscar aluno pelo CPF
                    aluno = None
                    aluno_cpf = row.get("Aluno (CPF)", "").strip()
                    if aluno_cpf:
                        try:
                            aluno = Aluno.objects.get(cpf=aluno_cpf)
                        except Aluno.DoesNotExist:
                            errors.append(f"Aluno não encontrado com CPF: {aluno_cpf}")
                            continue
                    else:
                        errors.append("CPF do aluno não especificado")
                        continue
                    
                    # Buscar turma pelo nome ou ID
                    turma = None
                    turma_nome = row.get("Turma", "").strip()
                    if turma_nome:
                        try:
                            turma = Turma.objects.get(nome=turma_nome)
                        except Turma.DoesNotExist:
                            try:
                                turma = Turma.objects.get(id=turma_nome)
                            except (Turma.DoesNotExist, ValueError):
                                errors.append(f"Turma não encontrada: {turma_nome}")
                                continue
                    else:
                        errors.append("Turma não especificada")
                        continue
                    
                    # Verificar se já existe matrícula
                    if Matricula.objects.filter(aluno=aluno, turma=turma).exists():
                        errors.append(f"O aluno {aluno.nome} já está matriculado na turma {turma.nome}")
                        continue
                    
                    # Processar data da matrícula
                    data_matricula = timezone.now().date()
                    try:
                        if row.get("Data da Matrícula"):
                            data_matricula = timezone.datetime.strptime(
                                row.get("Data da Matrícula"), "%d/%m/%Y"
                            ).date()
                    except ValueError as e:
                        errors.append(f"Erro no formato de data: {str(e)}")
                        continue
                    
                    # Processar status
                    status = "A"  # Ativa por padrão
                    status_texto = row.get("Status", "").strip()
                    if status_texto:
                        status_map = {"Ativa": "A", "Cancelada": "C", "Finalizada": "F"}
                        status = status_map.get(status_texto, "A")
                    
                    # Criar a matrícula
                    matricula = Matricula(
                        aluno=aluno,
                        turma=turma,
                        data_matricula=data_matricula,
                        ativa=(status == "A"),
                        status=status
                    )
                    
                    # Validar o modelo
                    matricula.full_clean()
                    matricula.save()
                    
                    count += 1
                except Exception as e:
                    errors.append(f"Erro na linha {count+1}: {str(e)}")
            
            if errors:
                messages.warning(
                    request,
                    f"{count} matrículas importadas com {len(errors)} erros.",
                )
                for error in errors[:5]:  # Mostrar apenas os 5 primeiros erros
                    messages.error(request, error)
                if len(errors) > 5:
                    messages.error(
                        request, f"... e mais {len(errors) - 5} erros."
                    )
            else:
                messages.success(
                    request, f"{count} matrículas importadas com sucesso!"
                )
            return redirect("matriculas:listar_matriculas")
        except Exception as e:
            messages.error(request, f"Erro ao importar matrículas: {str(e)}")
    
    return render(request, "matriculas/importar_matriculas.html")



## Arquivos urls.py:


### Arquivo: matriculas\urls.py

python
from django.urls import path
from . import views

app_name = "matriculas"

urlpatterns = [
    path("", views.listar_matriculas, name="listar_matriculas"),
    path("<int:id>/detalhes/", views.detalhar_matricula, name="detalhar_matricula"),
    path("realizar/", views.realizar_matricula, name="realizar_matricula"),
    path("<int:id>/cancelar/", views.cancelar_matricula, name="cancelar_matricula"),
    # Nova URL para cancelar matr√≠cula a partir da turma
    path("turma/<int:turma_id>/aluno/<str:aluno_cpf>/cancelar/", 
         views.cancelar_matricula_por_turma_aluno, 
         name="cancelar_matricula_por_turma_aluno"),
    path("exportar/", views.exportar_matriculas, name="exportar_matriculas"),
    path("importar/", views.importar_matriculas, name="importar_matriculas"),
]



## Arquivos models.py:


### Arquivo: matriculas\models.py

python
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _


class Matricula(models.Model):
    OPCOES_STATUS = [
        ("A", "Ativa"),
        ("C", "Cancelada"),
        ("F", "Finalizada"),
    ]

    aluno = models.ForeignKey(
        "alunos.Aluno", on_delete=models.CASCADE, verbose_name="Aluno"
    )
    turma = models.ForeignKey(
        "turmas.Turma",
        on_delete=models.CASCADE,
        verbose_name="Turma",
        related_name="matriculas",
    )
    data_matricula = models.DateField(verbose_name="Data da Matrícula")
    ativa = models.BooleanField(default=True, verbose_name="Matrícula Ativa")
    status = models.CharField(
        "Status", max_length=1, choices=OPCOES_STATUS, default="A"
    )

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        ordering = ["-data_matricula"]
        unique_together = ["aluno", "turma"]

    def __str__(self):
        return f"{self.aluno.nome} - {self.turma.nome}"

    def clean(self):
        # Check if class is active
        if self.turma.status != "A":
            raise ValidationError(
                {
                    "turma": _(
                        "Não é possível matricular em uma turma inativa ou concluída."
                    )
                }
            )

        # Check if there are available spots
        if (
            not self.pk and self.turma.vagas_disponiveis <= 0
        ):  # Only for new enrollments
            raise ValidationError(
                {"turma": _("Não há vagas disponíveis nesta turma.")}
            )



## Arquivos de Template:


### Arquivo: matriculas\templates\matriculas\cancelar_matricula.html

html
{% extends 'base.html' %}

{% block title %}Cancelar Matrícula{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Cancelar Matrícula</h1>
    
    <div class="alert alert-warning">
        <p>Você está prestes a cancelar a matrícula do aluno <strong>{{ matricula.aluno.nome }}</strong> na turma <strong>{{ matricula.turma.nome }}</strong>.</p>
        <p>Esta ação não pode ser desfeita. Deseja continuar?</p>
    </div>
    
    <!-- Padronizar botões de confirmação -->
    <form method="post">
        {% csrf_token %}
        <div class="d-flex justify-content-between">
            <a href="{{ return_url|default:'/matriculas/' }}" class="btn btn-secondary">
                <i class="fas fa-times"></i> Cancelar
            </a>
            <button type="submit" class="btn btn-danger">
                <i class="fas fa-ban"></i> Confirmar Cancelamento
            </button>
        </div>
    </form>
</div>
{% endblock %}



### Arquivo: matriculas\templates\matriculas\detalhar_matricula.html

html
{% extends 'base.html' %}

{% block title %}Detalhes da Matrícula{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Detalhes da Matrícula</h1>
        <div>
            <a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>
            <a href="{% url 'matriculas:listar_matriculas' %}" class="btn btn-secondary">Lista de Matrículas</a>
        </div>
    </div>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <!-- Informações do Aluno -->
    <div class="card mb-4">
        <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Informações do Aluno</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-8">
                    <div class="d-flex align-items-center">
                        {% if matricula.aluno.foto %}
                            <img src="{{ matricula.aluno.foto.url }}" alt="Foto de {{ matricula.aluno.nome }}" 
                                 class="rounded-circle me-3" width="60" height="60" style="object-fit: cover;">
                        {% else %}
                            <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3"
                                 style="width: 60px; height: 60px; color: white; font-size: 1.5rem;">
                                {{ matricula.aluno.nome|first|upper }}
                            </div>
                        {% endif %}
                        <div>
                            <h5 class="mb-1">{{ matricula.aluno.nome }}</h5>
                            <p class="mb-0">CPF: {{ matricula.aluno.cpf }}</p>
                            <p class="mb-0">Email: {{ matricula.aluno.email }}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 text-md-end">
                    <a href="{% url 'alunos:detalhar_aluno' matricula.aluno.cpf %}" class="btn btn-outline-primary">
                        <i class="fas fa-user"></i> Ver Perfil Completo
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Informações da Turma -->
    <div class="card mb-4">
        <div class="card-header bg-info text-white">
            <h5 class="mb-0">Informações da Turma</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-8">
                    <p><strong>Turma:</strong> {{ matricula.turma.nome }}</p>
                    <p><strong>Curso:</strong> {{ matricula.turma.curso.nome }}</p>
                    <p><strong>Instrutor:</strong> {{ matricula.turma.instrutor.nome|default:"Não definido" }}</p>
                    <p><strong>Período:</strong> {{ matricula.turma.data_inicio|date:"d/m/Y" }} a {{ matricula.turma.data_fim|date:"d/m/Y"|default:"Em andamento" }}</p>
                    <p><strong>Horário:</strong> {{ matricula.turma.horario|default:"Não definido" }}</p>
                    <p><strong>Local:</strong> {{ matricula.turma.local|default:"Não definido" }}</p>
                </div>
                <div class="col-md-4 text-md-end">
                    <a href="{% url 'turmas:detalhar_turma' matricula.turma.id %}" class="btn btn-outline-info">
                        <i class="fas fa-users"></i> Ver Detalhes da Turma
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Informações da Matrícula -->
    <div class="card mb-4">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Informações da Matrícula</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Data da Matrícula:</strong> {{ matricula.data_matricula|date:"d/m/Y" }}</p>
                    <p>
                        <strong>Status:</strong> 
                        {% if matricula.status == 'A' %}
                            <span class="badge bg-success">Ativa</span>
                        {% elif matricula.status == 'C' %}
                            <span class="badge bg-danger">Cancelada</span>
                        {% elif matricula.status == 'F' %}
                            <span class="badge bg-secondary">Finalizada</span>
                        {% endif %}
                    </p>
                </div>
                <div class="col-md-6">
                    <p>
                        <strong>Matrícula Ativa:</strong> 
                        {% if matricula.ativa %}
                            <span class="badge bg-success">Sim</span>
                        {% else %}
                            <span class="badge bg-danger">Não</span>
                        {% endif %}
                    </p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Frequência e Desempenho (se disponível) -->
    {% if frequencias %}
    <div class="card mb-4">
        <div class="card-header bg-warning text-dark">
            <h5 class="mb-0">Frequência e Desempenho</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <h6>Frequência</h6>
                    <div class="progress mb-3" style="height: 25px;">
                        <div class="progress-bar {% if percentual_presenca < 75 %}bg-danger{% else %}bg-success{% endif %}" 
                             role="progressbar" style="width: {{ percentual_presenca }}%;" 
                             aria-valuenow="{{ percentual_presenca }}" aria-valuemin="0" aria-valuemax="100">
                            {{ percentual_presenca|floatformat:1 }}%
                        </div>
                    </div>
                    <p><strong>Total de Presenças:</strong> {{ total_presencas }} de {{ total_aulas }}</p>
                </div>
                <div class="col-md-6">
                    <h6>Desempenho</h6>
                    {% if notas %}
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th>Avaliação</th>
                                    <th>Nota</th>
                                    <th>Data</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for nota in notas %}
                                <tr>
                                    <td>{{ nota.avaliacao }}</td>
                                    <td>{{ nota.valor }}</td>
                                    <td>{{ nota.data|date:"d/m/Y" }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    {% else %}
                        <p class="text-muted">Nenhuma nota registrada.</p>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
    {% endif %}
    
    <!-- Ações -->
    <div class="card mb-4">
        <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Ações</h5>
        </div>
        <div class="card-body">
            <div class="d-flex flex-wrap gap-2">
                {% if matricula.status == 'A' %}
                    <a href="{% url 'matriculas:cancelar_matricula' matricula.id %}" class="btn btn-danger">
                        <i class="fas fa-times-circle"></i> Cancelar Matrícula
                    </a>
                {% endif %}
                
                <a href="{% url 'alunos:detalhar_aluno' matricula.aluno.cpf %}" class="btn btn-primary">
                    <i class="fas fa-user"></i> Ver Perfil do Aluno
                </a>
                
                <a href="{% url 'turmas:detalhar_turma' matricula.turma.id %}" class="btn btn-info">
                    <i class="fas fa-users"></i> Ver Turma
                </a>
                
                {% if frequencias %}
                    <a href="{% url 'frequencias:historico_frequencia' matricula.aluno.cpf %}" class="btn btn-warning">
                        <i class="fas fa-calendar-check"></i> Ver Histórico de Frequência
                    </a>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}



### Arquivo: matriculas\templates\matriculas\detalhes_matricula.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}




### Arquivo: matriculas\templates\matriculas\importar_matriculas.html

html
{% extends 'base.html' %}

{% block title %}Importar Matrículas{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Importar Matrículas</h1>
    
    <div class="card">
        <div class="card-body">
            <p class="mb-3">Faça upload de um arquivo CSV contendo os dados das matrículas.</p>
            
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="csv_file" class="form-label">Arquivo CSV</label>
                    <input type="file" name="csv_file" id="csv_file" class="form-control" accept=".csv" required>
                    <div class="form-text">O arquivo deve ter cabeçalhos: Aluno (CPF), Turma, Data da Matrícula, Status</div>
                </div>
                
                <div class="d-flex">
                    <button type="submit" class="btn btn-primary me-2">Importar</button>
                    <a href="{% url 'matriculas:listar_matriculas' %}" class="btn btn-secondary">Cancelar</a>
                </div>
            </form>
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{% url 'matriculas:listar_matriculas' %}" class="btn btn-link">Voltar para a lista de matrículas</a>
    </div>
</div>
{% endblock %}



### Arquivo: matriculas\templates\matriculas\listar_matriculas.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Padronizar cabeçalho com botões -->
<div class="d-flex justify-content-between align-items-center mb-3">
    <h1>Lista de Matrículas</h1>
    <div>
        <a href="javascript:history.back()" class="btn btn-secondary me-2">
            <i class="fas fa-arrow-left"></i> Voltar
        </a>
        <a href="{% url 'matriculas:realizar_matricula' %}" class="btn btn-primary me-2">
            <i class="fas fa-plus"></i> Nova Matrícula
        </a>
        <a href="{% url 'matriculas:exportar_matriculas' %}" class="btn btn-success me-2">
            <i class="fas fa-file-export"></i> Exportar CSV
        </a>
        <a href="{% url 'matriculas:importar_matriculas' %}" class="btn btn-info">
            <i class="fas fa-file-import"></i> Importar CSV
        </a>
    </div>
</div>

<!-- Padronizar botões de ação na tabela -->
<td>
    <div class="table-actions">
        <a href="{% url 'matriculas:detalhar_matricula' matricula.id %}" class="btn btn-sm btn-info" title="Ver detalhes da matrícula">
            <i class="fas fa-eye"></i> Detalhes
        </a>
        {% if matricula.status == 'A' %}
        <a href="{% url 'matriculas:cancelar_matricula' matricula.id %}" class="btn btn-sm btn-danger" title="Cancelar matrícula">
            <i class="fas fa-ban"></i> Cancelar
        </a>
        {% endif %}
    </div>
</td>
{% endblock %}




### Arquivo: matriculas\templates\matriculas\realizar_matricula.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}


