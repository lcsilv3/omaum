"""
Views para gerenciamento de frequências mensais.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import logging
import json

# Importar funções utilitárias do módulo utils
from frequencias.utils import get_models, get_forms, get_turma_model

logger = logging.getLogger(__name__)


@login_required
def listar_frequencias(request):
    """Lista todas as frequências mensais."""
    try:
        FrequenciaMensal, _ = get_models()

        # Aplicar filtros
        frequencias = FrequenciaMensal.objects.all().select_related("turma")

        # Filtrar por turma
        turma_id = request.GET.get("turma")
        if turma_id:
            frequencias = frequencias.filter(turma_id=turma_id)

        # Filtrar por ano
        ano = request.GET.get("ano")
        if ano:
            frequencias = frequencias.filter(ano=ano)

        # Ordenar
        frequencias = frequencias.order_by("-ano", "-mes", "turma__nome")

        # Paginação
        paginator = Paginator(frequencias, 20)  # 20 itens por página
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Obter turmas para filtro
        Turma = get_turma_model()
        turmas = Turma.objects.filter(status="A")

        # Obter anos disponíveis
        anos = (
            FrequenciaMensal.objects.values_list("ano", flat=True)
            .distinct()
            .order_by("-ano")
        )

        context = {
            "frequencias": page_obj,
            "page_obj": page_obj,
            "turmas": turmas,
            "anos": anos,
            "turma_selecionada": turma_id,
            "ano_selecionado": ano,
        }

        return render(request, "frequencias/listar_frequencias.html", context)

    except Exception as e:
        logger.error(f"Erro ao listar frequências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao listar frequências: {str(e)}")
        return redirect("core:home")


@login_required
def criar_frequencia_mensal(request):
    """Cria uma nova frequência mensal."""
    try:
        FrequenciaMensalForm, _ = get_forms()

        if request.method == "POST":
            form = FrequenciaMensalForm(request.POST)
            if form.is_valid():
                frequencia = form.save()

                # Calcular carências automaticamente
                frequencia.calcular_carencias()

                messages.success(request, "Frequência mensal criada com sucesso!")
                return redirect(
                    "frequencias:detalhar_frequencia_mensal",
                    frequencia_id=frequencia.id,
                )
        else:
            form = FrequenciaMensalForm()

        context = {"form": form, "titulo": "Criar Frequência Mensal"}

        return render(request, "frequencias/formulario_frequencia_mensal.html", context)

    except Exception as e:
        logger.error(f"Erro ao criar frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao criar frequência mensal: {str(e)}")
        return redirect("frequencias:listar_frequencias")


@login_required
def editar_frequencia_mensal(request, frequencia_id):
    """Edita uma frequência mensal existente."""
    try:
        FrequenciaMensal, _ = get_models()
        FrequenciaMensalForm, _ = get_forms()

        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)

        if request.method == "POST":
            form = FrequenciaMensalForm(request.POST, instance=frequencia)
            if form.is_valid():
                frequencia = form.save()

                # Recalcular carências se necessário
                if "recalcular" in request.POST:
                    frequencia.calcular_carencias()
                    messages.success(
                        request,
                        "Frequência mensal atualizada e carências recalculadas!",
                    )
                else:
                    messages.success(
                        request, "Frequência mensal atualizada com sucesso!"
                    )

                return redirect(
                    "frequencias:detalhar_frequencia_mensal",
                    frequencia_id=frequencia.id,
                )
        else:
            form = FrequenciaMensalForm(instance=frequencia)

        context = {
            "form": form,
            "frequencia": frequencia,
            "titulo": "Editar Frequência Mensal",
        }

        return render(request, "frequencias/formulario_frequencia_mensal.html", context)

    except Exception as e:
        logger.error(f"Erro ao editar frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao editar frequência mensal: {str(e)}")
        return redirect("frequencias:listar_frequencias")


@login_required
def excluir_frequencia_mensal(request, frequencia_id):
    """Exclui uma frequência mensal."""
    try:
        FrequenciaMensal, _ = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)

        if request.method == "POST":
            frequencia.delete()
            messages.success(request, "Frequência mensal excluída com sucesso!")
            return redirect("frequencias:listar_frequencias")

        context = {"frequencia": frequencia}

        return render(request, "frequencias/excluir_frequencia_mensal.html", context)

    except Exception as e:
        logger.error(f"Erro ao excluir frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao excluir frequência mensal: {str(e)}")
        return redirect("frequencias:listar_frequencias")


@login_required
def detalhar_frequencia_mensal(request, frequencia_id):
    """Exibe os detalhes de uma frequência mensal."""
    try:
        FrequenciaMensal, Carencia = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)

        # Obter carências
        carencias = Carencia.objects.filter(
            frequencia_mensal=frequencia
        ).select_related("aluno")

        # Ordenar carências
        carencias = carencias.order_by("liberado", "aluno__nome")

        # Preparar dados para gráfico
        alunos_labels = []
        percentuais_presenca = []

        for carencia in carencias:
            alunos_labels.append(carencia.aluno.nome)
            percentuais_presenca.append(float(carencia.percentual_presenca))

        # Calcular total de alunos
        total_alunos = carencias.count()

        context = {
            "frequencia": frequencia,
            "carencias": carencias,
            "total_alunos": total_alunos,
            "alunos_labels": json.dumps(alunos_labels),
            "percentuais_presenca": json.dumps(percentuais_presenca),
        }

        return render(request, "frequencias/detalhar_frequencia_mensal.html", context)

    except Exception as e:
        logger.error(f"Erro ao detalhar frequência mensal: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao detalhar frequência mensal: {str(e)}")
        return redirect("frequencias:listar_frequencias")


@login_required
def recalcular_carencias(request, frequencia_id):
    """Recalcula as carências de uma frequência mensal."""
    try:
        FrequenciaMensal, _ = get_models()
        frequencia = get_object_or_404(FrequenciaMensal, id=frequencia_id)

        # Recalcular carências
        frequencia.calcular_carencias()

        messages.success(request, "Carências recalculadas com sucesso!")
        return redirect(
            "frequencias:detalhar_frequencia_mensal", frequencia_id=frequencia.id
        )

    except Exception as e:
        logger.error(f"Erro ao recalcular carências: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao recalcular carências: {str(e)}")
        return redirect(
            "frequencias:detalhar_frequencia_mensal", frequencia_id=frequencia_id
        )
