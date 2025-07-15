import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from importlib import import_module
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET

from .utils import (
    get_models,
    get_form_class,
    get_model_class,
    get_cursos,
    get_turmas,
    get_atividades_academicas,
)

logger = logging.getLogger(__name__)


@login_required
def listar_atividades_academicas(request):
    query = request.GET.get("q", "")
    curso_id = request.GET.get("curso", "")
    turma_id = request.GET.get("turma", "")

    atividades = (
        get_atividades_academicas().select_related("curso").prefetch_related("turmas")
    )
    cursos = get_cursos()
    turmas = get_turmas()

    if curso_id:
        atividades = atividades.filter(curso_id=curso_id)
        turmas = turmas.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turmas__id=turma_id)
    if query:
        atividades = atividades.filter(nome__icontains=query)

    # Adicionando paginação
    paginator = Paginator(atividades.distinct(), 15)  # 15 por página
    page = request.GET.get("page")
    try:
        atividades_paginadas = paginator.page(page)
    except PageNotAnInteger:
        atividades_paginadas = paginator.page(1)
    except EmptyPage:
        atividades_paginadas = paginator.page(paginator.num_pages)

    context = {
        "atividades": atividades_paginadas,
        "page_obj": atividades_paginadas,
        "cursos": cursos,
        "turmas": turmas,
        "curso_selecionado": curso_id,
        "turma_selecionada": turma_id,
        "query": query,
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(
            request, "atividades/academicas/partials/atividades_tabela.html", context
        )
    return render(
        request, "atividades/academicas/listar_atividades_academicas.html", context
    )


@require_GET
@login_required
def ajax_turmas_por_curso(request):
    curso_id = request.GET.get("curso") or request.GET.get("curso_id")
    models = get_models()
    Turma = models["Turma"]
    if curso_id:
        turmas = Turma.objects.filter(curso_id=curso_id)
    else:
        turmas = Turma.objects.all()
    data = [{"id": turma.id, "nome": turma.nome} for turma in turmas]
    return JsonResponse({"turmas": data})


@require_GET
@login_required
def ajax_atividades_filtradas(request):
    return listar_atividades_academicas(request)


@login_required
def criar_atividade_academica(request):
    try:
        AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
        if request.method == "POST":
            form = AtividadeAcademicaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Atividade acadêmica criada com sucesso!")
                return redirect("atividades:listar_atividades")
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = AtividadeAcademicaForm()
        return render(
            request,
            "atividades/academicas/criar_atividade_academica.html",  # <-- Corrija aqui
            {"form": form},
        )
    except Exception as e:
        logger.error(f"Erro ao criar atividade acadêmica: {str(e)}", exc_info=True)
        messages.error(request, f"Ocorreu um erro ao criar a atividade: {str(e)}")
        return redirect("atividades:listar_atividades")


@login_required
def editar_atividade_academica(request, id):
    try:
        models = get_models()
        AtividadeAcademica = models["AtividadeAcademica"]
        AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
        atividade = get_object_or_404(AtividadeAcademica, id=id)
        if request.method == "POST":
            form = AtividadeAcademicaForm(request.POST, instance=atividade)
            if form.is_valid():
                form.save()
                messages.success(request, "Atividade acadêmica atualizada com sucesso!")
                return redirect("atividades:listar_atividades")
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = AtividadeAcademicaForm(instance=atividade)
        return render(
            request,
            "atividades/academicas/editar_atividade_academica.html",
            {"form": form, "atividade": atividade},
        )
    except Exception as e:
        logger.error(
            f"Erro ao editar atividade acadêmica {id}: {str(e)}", exc_info=True
        )
        messages.error(request, f"Ocorreu um erro ao editar a atividade: {str(e)}")
        return redirect("atividades:listar_atividades")


@login_required
def detalhar_atividade_academica(request, id):
    try:
        models = get_models()
        AtividadeAcademica = models["AtividadeAcademica"]
        atividade = get_object_or_404(
            AtividadeAcademica.objects.select_related("curso").prefetch_related(
                "turmas"
            ),
            id=id,
        )
        return render(
            request,
            "atividades/academicas/detalhar_atividade_academica.html",
            {"atividade": atividade},
        )
    except Exception as e:
        logger.error(
            f"Erro ao detalhar atividade acadêmica {id}: {str(e)}", exc_info=True
        )
        messages.error(
            request, f"Ocorreu um erro ao exibir os detalhes da atividade: {str(e)}"
        )
        return redirect("atividades:listar_atividades")


@login_required
def excluir_atividade_academica(request, id):
    try:
        models = get_models()
        AtividadeAcademica = models["AtividadeAcademica"]
        atividade = get_object_or_404(AtividadeAcademica, id=id)

        # Buscar dependências
        from presencas.models import Presenca, ObservacaoPresenca

        presencas = list(Presenca.objects.filter(atividade=atividade))
        observacoes = list(
            ObservacaoPresenca.objects.filter(atividade_academica=atividade)
        )
        # Se houver outros vínculos relevantes, adicionar aqui
        dependencias = {
            "presencas": presencas,
            "observacoes": observacoes,
        }

        if request.method == "POST":
            if any(len(lst) > 0 for lst in dependencias.values()):
                messages.error(
                    request,
                    "Não é possível excluir a atividade pois existem registros vinculados (presenças, observações, etc.). Remova as dependências antes de tentar novamente.",
                    extra_tags="safe",
                )
                return redirect(
                    "atividades:excluir_atividade_academica", id=atividade.id
                )
            atividade.delete()
            messages.success(request, "Atividade acadêmica excluída com sucesso!")
            return redirect("atividades:listar_atividades")
        return render(
            request,
            "atividades/academicas/excluir_atividade_academica.html",
            {"atividade": atividade, "dependencias": dependencias},
        )
    except Exception as e:
        logger.error(
            f"Erro ao excluir atividade acadêmica {id}: {str(e)}", exc_info=True
        )
        messages.error(request, f"Ocorreu um erro ao excluir a atividade: {str(e)}")
        return redirect("atividades:listar_atividades")


@login_required
def confirmar_exclusao_academica(request, pk):
    try:
        AtividadeAcademica = get_model_class("AtividadeAcademica")
        atividade = get_object_or_404(AtividadeAcademica, pk=pk)
        return_url = request.GET.get(
            "return_url", reverse("atividades:listar_atividades")
        )
        if request.method == "POST":
            try:
                nome_atividade = atividade.nome
                atividade.delete()
                messages.success(
                    request,
                    f"Atividade acadêmica '{nome_atividade}' excluída com sucesso.",
                )
                return redirect(return_url)
            except (AtividadeAcademica.DoesNotExist, ValueError) as e:
                logger.error(
                    f"Erro ao excluir atividade acadêmica: {str(e)}", exc_info=True
                )
                messages.error(
                    request, f"Erro ao excluir atividade acadêmica: {str(e)}"
                )
                return redirect("atividades:detalhar_atividade_academica", pk=pk)
        return render(
            request,
            "atividades/confirmar_exclusao_academica.html",
            {"atividade": atividade, "return_url": return_url},
        )
    except Exception as e:
        logger.error(
            f"Erro ao processar confirmação de exclusão: {str(e)}", exc_info=True
        )
        messages.error(request, f"Ocorreu um erro ao processar a solicitação: {str(e)}")
        return redirect("atividades:listar_atividades")


@login_required
def copiar_atividade_academica(request, id):
    try:
        AtividadeAcademica = get_model_class("AtividadeAcademica")
        AtividadeAcademicaForm = get_form_class("AtividadeAcademicaForm")
        atividade_original = get_object_or_404(AtividadeAcademica, id=id)
        if request.method == "POST":
            form = AtividadeAcademicaForm(request.POST)
            if form.is_valid():
                nova_atividade = form.save(commit=False)
                # Se quiser copiar algum campo fixo da original, faça aqui
                nova_atividade.save()
                form.save_m2m()
                messages.success(request, "Atividade copiada com sucesso!")
                return redirect("atividades:listar_atividades")
        else:
            # Pré-preenche o formulário com os dados da atividade original
            form = AtividadeAcademicaForm(instance=atividade_original)
            form.initial["nome"] = f"Cópia de {atividade_original.nome}"
        return render(
            request,
            "atividades/academicas/copiar_atividade_academica.html",
            {
                "form": form,
                "atividade_original": atividade_original,
            },
        )
    except (ImportError, AttributeError, ValueError) as e:
        logger.error(
            "Erro ao copiar atividade acadêmica %s: %s", id, str(e), exc_info=True
        )
        messages.error(request, f"Ocorreu um erro ao copiar a atividade: {str(e)}")
        return redirect("atividades:listar_atividades")
    except ObjectDoesNotExist as e:
        logger.error(
            "Objeto não encontrado ao copiar atividade acadêmmica %s: %s",
            id,
            str(e),
            exc_info=True,
        )
        messages.error(request, f"Atividade acadêmica não encontrada: {str(e)}")
        return redirect("atividades:listar_atividades")


@login_required
def alunos_por_turma(request, turma_id):
    try:
        Matricula = import_module("matriculas.models").Matricula
        alunos = Matricula.objects.filter(turma_id=turma_id).select_related("aluno")
        data = [
            {
                "nome": m.aluno.nome,
                "foto": m.aluno.foto.url if m.aluno.foto else None,
                "cpf": m.aluno.cpf,
            }
            for m in alunos
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        logger.error(
            "Erro ao obter alunos da turma %s: %s", turma_id, str(e), exc_info=True
        )
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def api_get_turmas_por_curso(request):
    try:
        curso_id = request.GET.get("curso") or request.GET.get("curso_id")
        models = get_models()
        Turma = models["Turma"]
        if curso_id:
            try:
                curso_id = int(curso_id)
                turmas = Turma.objects.filter(curso_id=curso_id)
            except ValueError:
                return JsonResponse(
                    {"error": "ID do curso inválido. Deve ser um número inteiro."},
                    status=400,
                )
        else:
            turmas = Turma.objects.all()
        data = [
            {
                "id": turma.id,
                "nome": turma.nome,
                "codigo": turma.codigo if hasattr(turma, "codigo") else None,
            }
            for turma in turmas
        ]
        return JsonResponse({"turmas": data})
    except Exception as e:
        logger.error("Erro ao obter turmas por curso: %s", str(e), exc_info=True)
        return JsonResponse(
            {"error": "Erro ao processar a solicitação. Tente novamente."}, status=500
        )


@login_required
def api_get_cursos_por_turma(request):
    try:
        turma_id = request.GET.get("turma_id")
        if not turma_id:
            models = get_models()
            Curso = models["Curso"]
            cursos = Curso.objects.all()
            data = [
                {
                    "id": curso.id,
                    "nome": curso.nome,
                    "codigo_curso": (
                        curso.codigo_curso if hasattr(curso, "codigo_curso") else None
                    ),
                }
                for curso in cursos
            ]
            return JsonResponse({"cursos": data})
        try:
            turma_id = int(turma_id)
        except ValueError:
            return JsonResponse(
                {"error": "ID da turma inválido. Deve ser um número inteiro."},
                status=400,
            )
        models = get_models()
        Turma = models["Turma"]
        try:
            turma = Turma.objects.get(id=turma_id)
            curso = turma.curso
            if curso:
                data = {
                    "id": curso.id,
                    "nome": curso.nome,
                    "codigo_curso": (
                        curso.codigo_curso if hasattr(curso, "codigo_curso") else None
                    ),
                }
                return JsonResponse({"cursos": [data]})
            else:
                return JsonResponse({"cursos": []})
        except Turma.DoesNotExist:
            return JsonResponse({"error": "Turma não encontrada."}, status=404)
    except Exception as e:
        logger.error("Erro ao obter cursos por turma: %s", str(e), exc_info=True)
        return JsonResponse(
            {"error": "Erro ao processar a solicitação. Tente novamente."}, status=500
        )
