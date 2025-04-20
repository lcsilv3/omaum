from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ValidationError
from importlib import import_module


def get_model(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
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
