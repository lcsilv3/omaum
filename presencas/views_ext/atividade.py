from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from importlib import import_module


def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


def get_form_dynamically(app_name, form_name):
    """Obtém um formulário dinamicamente."""
    module = import_module(f"{app_name}.forms")
    return getattr(module, form_name)


@login_required
def registrar_presencas_atividade(request):
    """Registra presenças para uma atividade específica."""
    AtividadeAcademica = get_model_dynamically("atividades", "AtividadeAcademica")
    get_model_dynamically("alunos", "Aluno")
    Presenca = get_model_dynamically("presencas", "Presenca")

    if request.method == "POST":
        atividade_id = request.POST.get("atividade")
        data = request.POST.get("data")

        if not atividade_id or not data:
            messages.error(request, "Atividade e data são obrigatórios.")
            return redirect("presencas:registrar_presencas_atividade")

        atividade = get_object_or_404(AtividadeAcademica, id=atividade_id)

        # Processar presenças
        presentes = request.POST.getlist("presentes", [])

        # Obter alunos da atividade
        alunos = []
        for turma in atividade.turmas.all():
            # Obter alunos matriculados na turma
            Matricula = get_model_dynamically("matriculas", "Matricula")
            matriculas = Matricula.objects.filter(turma=turma, status="A")
            alunos.extend([m.aluno for m in matriculas])

        # Remover duplicatas
        alunos = list(set(alunos))

        # Registrar presenças
        for aluno in alunos:
            presente = aluno.cpf in presentes
            justificativa = (
                request.POST.get(f"justificativa_{aluno.cpf}", "")
                if not presente
                else ""
            )

            # Verificar se já existe registro
            presenca, created = Presenca.objects.update_or_create(
                aluno=aluno,
                atividade=atividade,
                data=data,
                defaults={
                    "presente": presente,
                    "justificativa": justificativa,
                    "registrado_por": request.user,
                },
            )

        messages.success(request, "Presenças registradas com sucesso!")
        return redirect("presencas:listar_presencas")
    else:
        # Obter atividades para o formulário
        atividades = AtividadeAcademica.objects.all().order_by("-data_inicio")

        context = {
            "atividades": atividades,
            "data_hoje": timezone.now().date().strftime("%Y-%m-%d"),
        }

        return render(request, "presencas/registrar_presencas_atividade.html", context)


@login_required
def editar_presenca(request, presenca_id):
    """Edita um registro de presença existente."""
    Presenca = get_model_dynamically("presencas", "Presenca")
    PresencaForm = get_form_dynamically("presencas", "PresencaForm")

    presenca = get_object_or_404(Presenca, id=presenca_id)

    if request.method == "POST":
        form = PresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            form.save()
            messages.success(request, "Presença atualizada com sucesso!")
            return redirect("presencas:listar_presencas")
    else:
        form = PresencaForm(instance=presenca)

    context = {"form": form, "presenca": presenca}

    return render(request, "presencas/editar_presenca.html", context)
