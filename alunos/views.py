"""
Views relacionadas ao gerenciamento de alunos no sistema.
"""

import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET

from .forms import AlunoForm, RegistroHistoricoFormSet
from .models import Aluno, Curso
from .services import listar_alunos

logger = logging.getLogger(__name__)

@login_required
def listar_alunos_view(request):
    """Lista todos os alunos, com suporte a busca dinâmica (AJAX)."""
    try:
        query = request.GET.get("q", "")
        curso_id = request.GET.get("curso", "")
        page_number = request.GET.get("page")

        alunos_list = listar_alunos(query=query, curso_id=curso_id)
        total_alunos = alunos_list.count()

        paginator = Paginator(alunos_list, 10)
        page_obj = paginator.get_page(page_number)

        cursos_para_filtro = Curso.objects.all().order_by("nome")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            alunos_data = [
                {
                    "id": aluno.id,
                    "nome": aluno.nome,
                    "email": aluno.email,
                    "cpf": aluno.cpf,
                    "foto": aluno.foto.url if aluno.foto else None,
                    "cursos": [
                        matricula.turma.curso.nome
                        for matricula in aluno.matriculas.select_related("turma__curso")
                    ] if aluno.matriculas.exists() else ["Sem curso associado"]
                }
                for aluno in page_obj
            ]
            return JsonResponse({
                "alunos": alunos_data,
                "page": page_obj.number,
                "num_pages": paginator.num_pages
            })

        return render(
            request,
            "alunos/listar_alunos.html",
            {
                "alunos": page_obj,
                "page_obj": page_obj,
                "query": query,
                "cursos": cursos_para_filtro,
                "curso_selecionado": curso_id,
                "total_alunos": total_alunos,
            },
        )
    except Exception as exc:
        logger.error("Erro ao listar alunos: %s", exc)
        return render(
            request,
            "alunos/listar_alunos.html",
            {
                "alunos": [],
                "page_obj": None,
                "query": "",
                "cursos": [],
                "curso_selecionado": "",
                "total_alunos": 0,
                "error_message": f"Erro ao listar alunos: {exc}",
            },
        )

@login_required
@permission_required("alunos.add_aluno", raise_exception=True)
def criar_aluno(request):
    """
    Cria um novo aluno e gerencia seu histórico de registros.
    """
    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES)
        historico_formset = RegistroHistoricoFormSet(request.POST, prefix="historico")

        if form.is_valid() and historico_formset.is_valid():
            try:
                with transaction.atomic():
                    aluno = form.save(commit=False)
                    aluno.cpf = "".join(filter(str.isdigit, str(aluno.cpf)))
                    aluno.save()

                    historico_formset.instance = aluno
                    historico_formset.save()

                messages.success(request, "Aluno criado com sucesso!")
                return redirect("alunos:listar_alunos")
            except Exception as exc:
                logger.error("Erro ao criar aluno: %s", exc)
                messages.error(request, f"Ocorreu um erro ao salvar o aluno: {exc}")
    else:
        form = AlunoForm()
        historico_formset = RegistroHistoricoFormSet(prefix="historico")

    context = {
        "form": form,
        "historico_formset": historico_formset,
        "aluno": None
    }
    return render(request, "alunos/formulario_aluno.html", context)

@login_required
def detalhar_aluno(request, cpf):
    """Exibe os detalhes de um aluno e seu histórico de registros."""
    aluno = listar_alunos(cpf=cpf).first()
    if not aluno:
        messages.error(request, "Aluno não encontrado.")
        return redirect("alunos:listar_alunos")

    historico_list = aluno.historico_set.all()

    context = {
        "aluno": aluno,
        "historico_list": historico_list,
    }
    return render(request, "alunos/detalhar_aluno.html", context)

@login_required
@permission_required("alunos.change_aluno", raise_exception=True)
def editar_aluno(request, cpf):
    """
    Edita um aluno existente e seu histórico de registros.
    """
    aluno = get_object_or_404(Aluno, cpf=cpf)

    if request.method == "POST":
        form = AlunoForm(request.POST, request.FILES, instance=aluno)
        historico_formset = RegistroHistoricoFormSet(
            request.POST, instance=aluno, prefix="historico"
        )

        if form.is_valid() and historico_formset.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    historico_formset.save()

                messages.success(request, "Aluno atualizado com sucesso!")
                return redirect("alunos:listar_alunos")
            except Exception as exc:
                logger.error("Erro ao editar aluno %s: %s", cpf, exc)
                messages.error(request, f"Ocorreu um erro ao atualizar o aluno: {exc}")
    else:
        form = AlunoForm(instance=aluno)
        historico_formset = RegistroHistoricoFormSet(instance=aluno, prefix="historico")

    context = {
        "form": form,
        "historico_formset": historico_formset,
        "aluno": aluno
    }
    return render(request, "alunos/formulario_aluno.html", context)

@login_required
@permission_required("alunos.delete_aluno", raise_exception=True)
def excluir_aluno(request, cpf):
    """Exclui um aluno utilizando a camada de serviço."""
    aluno = listar_alunos(cpf=cpf).first()
    if not aluno:
        messages.error(request, "Aluno não encontrado.")
        return redirect("alunos:listar_alunos")

    if request.method == "POST":
        try:
            aluno.delete()
            messages.success(request, "Aluno excluído com sucesso!")
            return redirect("alunos:listar_alunos")
        except Exception as exc:
            messages.error(request, f"Não foi possível excluir o aluno. Erro: {exc}")
            return redirect("alunos:detalhar_aluno", cpf=cpf)

    context = {
        "aluno": aluno,
    }
    return render(request, "alunos/excluir_aluno.html", context)

@login_required
@require_GET
def search_alunos(request):
    """
    Endpoint para busca dinâmica de alunos.
    Retorna os resultados em formato JSON para requisições AJAX.
    """
    query = request.GET.get("q", "").strip()
    curso_id = request.GET.get("curso", None)

    logger.debug(
        "Requisição recebida para busca dinâmica. Query: %s, Curso ID: %s",
        query,
        curso_id
    )

    try:
        alunos_queryset = listar_alunos(query=query, curso_id=curso_id)
        logger.debug(
            "Query executada: %s, Resultados encontrados: %d",
            query,
            alunos_queryset.count()
        )

        paginator = Paginator(alunos_queryset, 10)
        page_number = request.GET.get("page", 1)
        alunos = paginator.get_page(page_number)

        alunos_data = [
            {
                "cpf": aluno.cpf,
                "nome": aluno.nome,
                "email": aluno.email,
                "numero_iniciatico": aluno.numero_iniciatico,
                "foto": aluno.foto.url if aluno.foto else None,
            }
            for aluno in alunos
        ]

        return JsonResponse(
            {
                "success": True,
                "alunos": alunos_data,
                "page": alunos.number,
                "num_pages": alunos.paginator.num_pages,
            }
        )
    except ValueError as exc:
        logger.error("Erro de valor: %s", exc)
        return JsonResponse({"success": False, "error": str(exc)}, status=400)
    except Exception as exc:
        logger.error("Erro inesperado na busca de alunos: %s", exc)
        return JsonResponse(
            {"success": False, "error": "Erro interno do servidor."}, status=500
        )
