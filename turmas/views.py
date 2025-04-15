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
