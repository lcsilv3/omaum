"""
Views do aplicativo Presenças.
"""

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from atividades.models import Atividade
from presencas.models import RegistroPresenca
from alunos.services import (
    listar_alunos as listar_alunos_service,
    buscar_aluno_por_cpf as buscar_aluno_por_cpf_service,
)
from turmas.models import Turma

logger = logging.getLogger(__name__)


@login_required
def listar_presencas_academicas(request):
    aluno_id = request.GET.get("aluno", "")
    turma_id = request.GET.get("turma", "")
    atividade_id = request.GET.get("atividade", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    # Query otimizada com relacionamentos
    presencas = RegistroPresenca.objects.select_related(
        "aluno", "turma__curso", "atividade"
    ).all()

    if aluno_id:
        presencas = presencas.filter(aluno__cpf=aluno_id)
    if turma_id:
        presencas = presencas.filter(turma__id=turma_id)
    if atividade_id:
        presencas = presencas.filter(atividade__id=atividade_id)
    if data_inicio:
        presencas = presencas.filter(data__gte=data_inicio)
    if data_fim:
        presencas = presencas.filter(data__lte=data_fim)

    # Ordenação consistente
    presencas = presencas.order_by("-data", "aluno__nome")

    try:
        alunos_queryset = listar_alunos_service()
        # listar_alunos_service agora retorna um queryset, não um objeto paginado
        alunos = list(alunos_queryset) if alunos_queryset else []
    except Exception as e:
        logger.error(f"Erro ao listar alunos: {str(e)}")
        alunos = []

    turmas = Turma.objects.all()
    atividades = Atividade.objects.all()

    context = {
        "presencas": presencas,
        "alunos": alunos,
        "turmas": turmas,
        "atividades": atividades,
        "filtros": {
            "aluno": aluno_id,
            "turma": turma_id,
            "atividade": atividade_id,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        },
    }
    return render(
        request, "presencas/academicas/listar_presencas_academicas.html", context
    )


@login_required
def registrar_presenca_academica(request):
    if request.method == "POST":
        aluno_id = request.POST.get("aluno")
        turma_id = request.POST.get("turma")
        atividade_id = request.POST.get("atividade")
        data = request.POST.get("data")
        presente = request.POST.get("presente") == "on"
        observacao = request.POST.get("observacao", "")
        try:
            aluno = buscar_aluno_por_cpf_service(aluno_id)
            turma = Turma.objects.get(id=turma_id)
            atividade = Atividade.objects.get(id=atividade_id)
            if not aluno:
                messages.error(request, f"Aluno com CPF {aluno_id} não encontrado.")
                return redirect("presencas:listar_presencas_academicas")

            # Mapear presente->status
            status = "P" if presente else "F"

            presenca, created = RegistroPresenca.objects.get_or_create(
                aluno=aluno,
                turma=turma,
                atividade=atividade,
                data=data,
                defaults={
                    "status": status,
                    "justificativa": observacao or "",
                    "registrado_por": request.user.username,
                    "data_registro": timezone.now(),
                },
            )
            if not created:
                presenca.status = status
                if observacao:
                    presenca.justificativa = observacao
                presenca.registrado_por = request.user.username
                presenca.data_registro = timezone.now()
            presenca.save()
            messages.success(request, "Presença registrada com sucesso!")
            return redirect("presencas:listar_presencas_academicas")
        except Exception as e:
            messages.error(request, f"Erro ao registrar presença: {str(e)}")
            return redirect("presencas:listar_presencas_academicas")

    try:
        alunos_queryset = listar_alunos_service()
        # listar_alunos_service agora retorna um queryset, não um objeto paginado
        alunos = list(alunos_queryset) if alunos_queryset else []
    except Exception as e:
        logger.error(f"Erro ao listar alunos: {str(e)}")
        alunos = []

    turmas = Turma.objects.all()
    atividades = Atividade.objects.all()

    context = {
        "alunos": alunos,
        "turmas": turmas,
        "atividades": atividades,
        "data_hoje": timezone.now().date(),
    }
    return render(
        request, "presencas/academicas/registrar_presenca_academica.html", context
    )


@login_required
def editar_presenca_academica(request, pk):
    presenca = get_object_or_404(RegistroPresenca, pk=pk)

    if request.method == "POST":
        # Lógica de edição
        presente = request.POST.get("presente") == "on"
        request.POST.get("observacao", "")

        presenca.status = "P" if presente else "F"
        presenca.save()

        messages.success(request, "Presença atualizada com sucesso!")
        return redirect("presencas:listar_presencas_academicas")

    context = {"presenca": presenca, "data_hoje": timezone.now().date()}
    return render(
        request, "presencas/academicas/editar_presenca_academica.html", context
    )


@login_required
def excluir_presenca_academica(request, pk):
    from presencas.permissions import PresencaPermissionEngine
    from django.contrib import messages

    presenca = get_object_or_404(RegistroPresenca, pk=pk)

    # Verificar permissões de exclusão
    pode_excluir, motivo_exclusao = PresencaPermissionEngine.pode_excluir_presenca(
        presenca, request.user
    )

    if not pode_excluir:
        messages.error(
            request, f"Não é possível excluir esta presença: {motivo_exclusao}"
        )
        return redirect("presencas:detalhar_presenca_dados_basicos", pk=pk)

    if request.method == "POST":
        # Confirmar exclusão
        confirmar = request.POST.get("confirmar_exclusao")
        motivo = request.POST.get("motivo_exclusao", "").strip()

        if confirmar == "sim":
            if not motivo:
                messages.error(request, "Motivo da exclusão é obrigatório.")
                context = {
                    "presenca": presenca,
                    "pode_excluir": pode_excluir,
                    "motivo_exclusao": motivo_exclusao if not pode_excluir else None,
                }
                return render(
                    request,
                    "presencas/academicas/excluir_presenca_academica.html",
                    context,
                )

            # Registrar motivo da exclusão antes de excluir
            presenca.registrado_por = f"{presenca.registrado_por} (excluído por {request.user.username}: {motivo})"
            presenca.save()
            presenca.delete()

            messages.success(request, "Presença excluída com sucesso!")
            return redirect("presencas:listar_presencas_academicas")
        else:
            messages.info(request, "Exclusão cancelada.")
            return redirect("presencas:detalhar_presenca_dados_basicos", pk=pk)

    context = {
        "presenca": presenca,
        "pode_excluir": pode_excluir,
        "motivo_exclusao": motivo_exclusao if not pode_excluir else None,
    }
    return render(
        request, "presencas/academicas/excluir_presenca_academica.html", context
    )


@login_required
def detalhar_presenca_academica(request, pk):
    presenca = get_object_or_404(RegistroPresenca, pk=pk)
    context = {"presenca": presenca}
    return render(
        request, "presencas/academicas/detalhar_presenca_academica.html", context
    )


@login_required
def exportar_presencas_academicas(request):
    return render(request, "presencas/academicas/exportar_presencas_academicas.html")


@login_required
def importar_presencas_academicas(request):
    return render(request, "presencas/academicas/importar_presencas_academicas.html")


@login_required
def listar_observacoes_presenca(request):
    # Observações agora são a justificativa dos registros de presença
    observacoes = (
        RegistroPresenca.objects.exclude(justificativa__isnull=True)
        .exclude(justificativa__exact="")
        .order_by("-data_registro")
    )
    context = {"observacoes": observacoes}
    return render(request, "presencas/listar_observacoes_presenca.html", context)


# Stubs para views ritualísticas (removidas)
@login_required
def listar_presencas_ritualisticas(request):
    messages.warning(request, "Presenças ritualísticas não estão mais disponíveis.")
    return redirect("presencas:listar_presencas_academicas")


@login_required
def registrar_presenca_ritualistica(request):
    messages.warning(request, "Presenças ritualísticas não estão mais disponíveis.")
    return redirect("presencas:listar_presencas_academicas")


@login_required
def editar_presenca_ritualistica(request, pk):
    messages.warning(request, "Presenças ritualísticas não estão mais disponíveis.")
    return redirect("presencas:listar_presencas_academicas")


@login_required
def excluir_presenca_ritualistica(request, pk):
    messages.warning(request, "Presenças ritualísticas não estão mais disponíveis.")
    return redirect("presencas:listar_presencas_academicas")


@login_required
def detalhar_presenca_ritualistica(request, pk):
    messages.warning(request, "Presenças ritualísticas não estão mais disponíveis.")
    return redirect("presencas:listar_presencas_academicas")


@login_required
def exportar_presencas_ritualisticas(request):
    messages.warning(request, "Presenças ritualísticas não estão mais disponíveis.")
    return redirect("presencas:listar_presencas_academicas")


@login_required
def importar_presencas_ritualisticas(request):
    messages.warning(request, "Presenças ritualísticas não estão mais disponíveis.")
    return redirect("presencas:listar_presencas_academicas")


# ===== FUNÇÕES PLACEHOLDER TEMPORÁRIAS =====


@login_required
def excluir_presenca_academica(request, pk):
    """Placeholder: função de exclusão será implementada conforme demanda."""
    from django.http import HttpResponse

    return HttpResponse("Função de exclusão em desenvolvimento")


@login_required
def exportar_presencas_academicas(request):
    """Placeholder: função de exportação será implementada conforme demanda."""
    from django.http import HttpResponse

    return HttpResponse("Função de exportação em desenvolvimento")


@login_required
def importar_presencas_academicas(request):
    """Placeholder: função de importação será implementada conforme demanda."""
    from django.http import HttpResponse

    return HttpResponse("Função de importação em desenvolvimento")


@login_required
def listar_observacoes_presenca(request):
    """Placeholder: função de observações será implementada conforme demanda."""
    from django.http import HttpResponse

    return HttpResponse("Função de observações em desenvolvimento")
