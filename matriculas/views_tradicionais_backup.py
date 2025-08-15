"""
Views tradicionais para o aplicativo de Matrículas.
Seguindo o padrão tradicional do Django.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from importlib import import_module
from .models import Matricula
from .forms import MatriculaForm


@login_required
def listar_matriculas(request):
    """Lista todas as matrículas com filtros."""
    # Importação dinâmica para evitar problemas de dependência circular
    try:
        Turma = import_module("turmas.models").Turma
    except ImportError:
        Turma = None

    # Filtros
    search = request.GET.get("search", "")
    turma_id = request.GET.get("turma", "")
    status = request.GET.get("status", "")

    # Base queryset
    matriculas = Matricula.objects.select_related(
        "aluno", "turma", "turma__curso"
    ).all()

    # Aplicar filtros
    if search:
        matriculas = matriculas.filter(
            Q(aluno__nome__icontains=search) | Q(aluno__cpf__icontains=search)
        )

    if turma_id:
        matriculas = matriculas.filter(turma_id=turma_id)

    if status:
        matriculas = matriculas.filter(status=status)

    # Ordenação
    matriculas = matriculas.order_by("-data_matricula")

    # Paginação
    paginator = Paginator(matriculas, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Buscar turmas para o filtro
    turmas = []
    if Turma:
        turmas = Turma.objects.all().order_by("nome")

    # Choices para status
    status_choices = Matricula.STATUS_CHOICES

    context = {
        "page_obj": page_obj,
        "search": search,
        "turma_id": turma_id,
        "status": status,
        "turmas": turmas,
        "status_choices": status_choices,
        "titulo": "Matrículas",
    }

    return render(request, "matriculas/listar_matriculas.html", context)


@login_required
def criar_matricula(request):
    """Cria uma nova matrícula."""
    if request.method == "POST":
        form = MatriculaForm(request.POST)
        if form.is_valid():
            try:
                matricula = form.save()
                messages.success(request, "Matrícula criada com sucesso!")
                return redirect(
                    "matriculas:detalhar_matricula", matricula_id=matricula.id
                )
            except Exception as e:
                messages.error(request, f"Erro ao criar matrícula: {str(e)}")
        else:
            messages.error(request, "Erro ao criar matrícula. Verifique os dados.")
    else:
        form = MatriculaForm()

    context = {
        "form": form,
        "titulo": "Nova Matrícula",
    }

    return render(request, "matriculas/realizar_matricula.html", context)


@login_required
def detalhar_matricula(request, matricula_id):
    """Detalha uma matrícula específica."""
    matricula = get_object_or_404(Matricula, id=matricula_id)

    context = {
        "matricula": matricula,
        "titulo": f"Matrícula #{matricula.id}",
    }

    return render(request, "matriculas/detalhar_matricula.html", context)


@login_required
def editar_matricula(request, matricula_id):
    """Edita uma matrícula existente."""
    matricula = get_object_or_404(Matricula, id=matricula_id)

    if request.method == "POST":
        form = MatriculaForm(request.POST, instance=matricula)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Matrícula atualizada com sucesso!")
                return redirect(
                    "matriculas:detalhar_matricula", matricula_id=matricula.id
                )
            except Exception as e:
                messages.error(request, f"Erro ao atualizar matrícula: {str(e)}")
        else:
            messages.error(request, "Erro ao atualizar matrícula. Verifique os dados.")
    else:
        form = MatriculaForm(instance=matricula)

    context = {
        "form": form,
        "matricula": matricula,
        "titulo": f"Editar Matrícula #{matricula.id}",
    }

    return render(request, "matriculas/realizar_matricula.html", context)


@login_required
def excluir_matricula(request, matricula_id):
    """Exclui uma matrícula."""
    matricula = get_object_or_404(Matricula, id=matricula_id)

    if request.method == "POST":
        try:
            matricula.delete()
            messages.success(request, "Matrícula excluída com sucesso!")
            return redirect("matriculas:listar_matriculas")
        except Exception as e:
            messages.error(request, f"Erro ao excluir matrícula: {str(e)}")

    context = {
        "matricula": matricula,
        "titulo": f"Excluir Matrícula #{matricula.id}",
    }

    return render(request, "matriculas/confirmar_exclusao_matricula.html", context)


# Views AJAX
@login_required
def buscar_turmas(request):
    """Busca turmas via AJAX."""
    try:
        Turma = import_module("turmas.models").Turma
        turmas = Turma.objects.all().values("id", "nome")
        return JsonResponse({"turmas": list(turmas)})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def buscar_alunos(request):
    """Busca alunos via AJAX."""
    try:
        Aluno = import_module("alunos.models").Aluno
        search = request.GET.get("search", "")

        alunos = Aluno.objects.all()
        if search:
            alunos = alunos.filter(Q(nome__icontains=search) | Q(cpf__icontains=search))

        alunos = alunos.values("id", "nome", "cpf")[:10]
        return JsonResponse({"alunos": list(alunos)})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def exportar_matriculas(request):
    """Exporta matrículas para CSV."""
    from django.http import HttpResponse
    import csv

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="matriculas.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ["ID", "Aluno", "CPF", "Turma", "Curso", "Data Matrícula", "Status"]
    )

    matriculas = Matricula.objects.select_related(
        "aluno", "turma", "turma__curso"
    ).all()
    for matricula in matriculas:
        writer.writerow(
            [
                matricula.id,
                matricula.aluno.nome,
                matricula.aluno.cpf,
                matricula.turma.nome,
                matricula.turma.curso.nome,
                matricula.data_matricula.strftime("%d/%m/%Y"),
                matricula.get_status_display(),
            ]
        )

    return response


@login_required
def importar_matriculas(request):
    """Importa matrículas de CSV."""
    if request.method == "POST":
        messages.info(request, "Funcionalidade de importação em desenvolvimento.")
        return redirect("matriculas:listar_matriculas")

    context = {
        "titulo": "Importar Matrículas",
    }

    return render(request, "matriculas/importar_matriculas.html", context)


# Aliases para compatibilidade
realizar_matricula = criar_matricula
