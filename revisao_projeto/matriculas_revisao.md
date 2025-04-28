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
    
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Confirmar Cancelamento</button>
        <a href="{% url 'matriculas:listar_matriculas' %}" class="btn btn-secondary">Voltar</a>
    </form>
</div>
{% endblock %}



### Arquivo: matriculas\templates\matriculas\detalhes_matricula.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}




### Arquivo: matriculas\templates\matriculas\listar_matriculas.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}




### Arquivo: matriculas\templates\matriculas\realizar_matricula.html

html
{% extends 'base.html' %}

{% block content %}
<!-- Existing content -->

<a href="javascript:history.back()" class="back-button">Voltar</a>
{% endblock %}


