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
