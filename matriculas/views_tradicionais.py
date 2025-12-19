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

    # Choices para status (corrigido: era STATUS_CHOICES, correto é OPCOES_STATUS)
    status_choices = Matricula.OPCOES_STATUS

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
    # M10: Pré-selecionar turma se vier via GET parameter
    turma_id = request.GET.get('turma', None)
    
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
        # Pré-selecionar turma se vier do botão "Matricular Alunos"
        initial_data = {}
        if turma_id:
            initial_data['turma'] = turma_id
        form = MatriculaForm(initial=initial_data)

    context = {
        "form": form,
        "titulo": "Nova Matrícula",
        "turma_id": turma_id,  # Passar para o template
    }

    return render(request, "matriculas/formulario_matricula.html", context)


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

    return render(request, "matriculas/formulario_matricula.html", context)


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


@login_required
def cancelar_matricula(request, matricula_id):
    """Cancela uma matrícula ativa."""
    matricula = get_object_or_404(Matricula, id=matricula_id)

    if matricula.status != "A":
        messages.info(
            request,
            "Apenas matrículas ativas podem ser canceladas.",
        )
        return redirect("matriculas:detalhar_matricula", matricula_id=matricula.id)

    if request.method == "POST":
        try:
            matricula.status = "C"  # ativa vira False automaticamente via property
            matricula.save(update_fields=["status"])
            messages.success(request, "Matrícula cancelada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao cancelar matrícula: {str(e)}")

        return redirect("matriculas:detalhar_matricula", matricula_id=matricula.id)

    context = {
        "matricula": matricula,
        "titulo": f"Cancelar Matrícula #{matricula.id}",
    }

    return render(
        request,
        "matriculas/confirmar_cancelamento_matricula.html",
        context,
    )


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


# M7: Endpoint para info da turma em tempo real
@login_required
def turma_info(request, turma_id):
    """Retorna informações da turma em JSON para exibição dinâmica."""
    try:
        Turma = import_module("turmas.models").Turma
        turma = get_object_or_404(Turma, id=turma_id)
        
        # Calcular vagas disponíveis
        matriculas_ativas = turma.matriculas.filter(status="A").count()
        vagas_disponiveis = turma.vagas - matriculas_ativas
        percentual_ocupacao = int((matriculas_ativas / turma.vagas * 100)) if turma.vagas > 0 else 0
        
        # Informações do instrutor
        instrutor_nome = turma.instrutor.nome if turma.instrutor else "Não definido"
        
        data = {
            "id": turma.id,
            "nome": turma.nome,
            "status": turma.status,
            "status_display": turma.get_status_display(),
            "vagas_total": turma.vagas,
            "vagas_ocupadas": matriculas_ativas,
            "vagas_disponiveis": vagas_disponiveis,
            "percentual_ocupacao": percentual_ocupacao,
            "horario": turma.horario or "Não definido",
            "dia_semana": turma.get_dias_semana_display() if turma.dias_semana else "Não definido",
            "instrutor": instrutor_nome,
            "curso": turma.curso.nome if turma.curso else "Não definido",
            "local": turma.local or "Não definido",
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# M8: Endpoint para info do aluno em tempo real
@login_required
def aluno_info(request, aluno_id):
    """Retorna informações do aluno em JSON para exibição dinâmica."""
    try:
        Aluno = import_module("alunos.models").Aluno
        aluno = get_object_or_404(Aluno, id=aluno_id)
        
        # Buscar turmas ativas do aluno
        matriculas_ativas = Matricula.objects.filter(
            aluno=aluno,
            status="A",
            turma__status="A"
        ).select_related("turma")
        
        turmas_ativas_lista = [
            {
                "id": m.turma.id,
                "nome": m.turma.nome,
                "data_matricula": m.data_matricula.strftime("%d/%m/%Y")
            }
            for m in matriculas_ativas
        ]
        
        data = {
            "id": aluno.id,
            "nome": aluno.nome,
            "cpf": aluno.cpf or "Não informado",
            "grau_atual": aluno.grau_atual or "Não definido",
            "status": "Ativo" if aluno.ativo else "Inativo",
            "turmas_ativas": turmas_ativas_lista,
            "tem_turmas_ativas": len(turmas_ativas_lista) > 0,
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Aliases para compatibilidade
realizar_matricula = criar_matricula
