"""
Views do aplicativo Presenças.
"""

import logging
from datetime import date
from calendar import monthrange
from importlib import import_module

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from presencas.models import RegistroPresenca
from alunos.services import (
    listar_alunos as listar_alunos_service,
    buscar_aluno_por_cpf as buscar_aluno_por_cpf_service,
)
from presencas.forms import TotaisAtividadesPresencaForm


def _get_model(app_name: str, model_name: str):
    """Importa modelo dinamicamente para evitar circularidade."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


Atividade = _get_model("atividades", "Atividade")
Turma = _get_model("turmas", "Turma")

logger = logging.getLogger(__name__)


@login_required
def listar_presencas_academicas(request):
    aluno_id = request.GET.get("aluno", "")
    turma_id = request.GET.get("turma", "")
    atividade_id = request.GET.get("atividade", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    presencas = RegistroPresenca.objects.all().select_related("aluno", "turma", "atividade")
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

    alunos = listar_alunos_service()
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

    alunos = listar_alunos_service()
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
    presenca = get_object_or_404(RegistroPresenca, pk=pk)

    if request.method == "POST":
        presenca.delete()
        messages.success(request, "Presença excluída com sucesso!")
        return redirect("presencas:listar_presencas_academicas")

    context = {"presenca": presenca}
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
    observacoes = (
        RegistroPresenca.objects.exclude(justificativa__isnull=True)
        .exclude(justificativa__exact="")
        .order_by("-data_registro")
    )
    context = {"observacoes": observacoes}
    return render(request, "presencas/listar_observacoes_presenca.html", context)


@login_required
def registrar_presenca_dados_basicos(request):
    turmas = Turma.objects.all()
    anos = list(range(2020, 2030))
    meses = [
        {"numero": 1, "nome": "Janeiro"},
        {"numero": 2, "nome": "Fevereiro"},
        {"numero": 3, "nome": "Março"},
        {"numero": 4, "nome": "Abril"},
        {"numero": 5, "nome": "Maio"},
        {"numero": 6, "nome": "Junho"},
        {"numero": 7, "nome": "Julho"},
        {"numero": 8, "nome": "Agosto"},
        {"numero": 9, "nome": "Setembro"},
        {"numero": 10, "nome": "Outubro"},
        {"numero": 11, "nome": "Novembro"},
        {"numero": 12, "nome": "Dezembro"},
    ]

    if request.method == "POST":
        turma_id = request.POST.get("turma")
        ano = request.POST.get("ano")
        mes = request.POST.get("mes")

        if not all([turma_id, ano, mes]):
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect("presencas:registrar_presenca_dados_basicos")

        # Salvar dados na sessão
        request.session["presenca_turma_id"] = turma_id
        request.session["presenca_ano"] = ano
        request.session["presenca_mes"] = mes

        messages.success(request, "Dados básicos registrados com sucesso!")
        return redirect("presencas:registrar_presenca_totais_atividades")

    context = {
        "turmas": turmas,
        "anos": anos,
        "meses": meses,
        "breadcrumb": [
            {"etapa": "Dados Básicos", "ativa": True},
            {"etapa": "Totais de Atividades", "ativa": False},
            {"etapa": "Dias de Atividades", "ativa": False},
            {"etapa": "Alunos", "ativa": False},
        ],
        "titulo_pagina": "Registrar Presença - Dados Básicos",
        "descricao_pagina": "Selecione a turma, ano e mês para iniciar o registro de presenças.",
    }
    return render(request, "presencas/registrar_presenca_dados_basicos.html", context)


@login_required
def registrar_presenca_totais_atividades(request):
    turma_id = request.session.get("presenca_turma_id")
    ano = request.session.get("presenca_ano")
    mes = request.session.get("presenca_mes")
    turma = Turma.objects.get(id=turma_id) if turma_id else None
    curso = turma.curso if turma else None
    atividades = []
    if turma and ano and mes:
        primeiro_dia = date(int(ano), int(mes), 1)
        ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
        atividades = (
            Atividade.objects.filter(turmas__id=turma.id)
            .filter(data_inicio__range=[primeiro_dia, ultimo_dia])
            .distinct()
        )

    form = TotaisAtividadesPresencaForm()

    if request.method == "POST":
        form = TotaisAtividadesPresencaForm(request.POST)
        if form.is_valid():
            # Salvar totais de atividades (não persiste mais em modelo; guarda na sessão)
            totais_valores = {}
            for atividade in atividades:
                total_field = f"total_{atividade.id}"
                total_value = form.cleaned_data.get(total_field, 0)
                totais_valores[str(atividade.id)] = int(total_value or 0)

            # Salvar dados na sessão
            request.session["presenca_atividades_totais"] = True
            request.session["presenca_totais_valores"] = totais_valores
            messages.success(request, "Totais de atividades registrados com sucesso!")
            return redirect("presencas:registrar_presenca_dias_atividades")

    context = {
        "form": form,
        "turma": turma,
        "curso": curso,
        "ano": ano,
        "mes": mes,
        "atividades": atividades,
        "breadcrumb": [
            {"etapa": "Dados Básicos", "ativa": False},
            {"etapa": "Totais de Atividades", "ativa": True},
            {"etapa": "Dias de Atividades", "ativa": False},
            {"etapa": "Alunos", "ativa": False},
        ],
        "titulo_pagina": "Registrar Presença - Totais de Atividades",
        "descricao_pagina": "Informe o total de atividades realizadas no mês.",
    }
    return render(
        request, "presencas/registrar_presenca_totais_atividades.html", context
    )


@login_required
def registrar_presenca_dias_atividades(request):
    turma_id = request.session.get("presenca_turma_id")
    ano = request.session.get("presenca_ano")
    mes = request.session.get("presenca_mes")

    if not all([turma_id, ano, mes]):
        messages.error(request, "Dados básicos não encontrados. Reinicie o processo.")
        return redirect("presencas:registrar_presenca_dados_basicos")

    turma = Turma.objects.get(id=turma_id)

    if request.method == "POST":
        # Processar dados do formulário - Agora redireciona diretamente para a lista
        request.session["presenca_dias_atividades"] = True
        messages.success(request, "Registro de presenças finalizado com sucesso!")
        # Limpa dados da sessão
        session_keys = [
            "presenca_turma_id",
            "presenca_ano",
            "presenca_mes",
            "presenca_totais_atividades",
        ]
        for key in session_keys:
            if key in request.session:
                del request.session[key]
        return redirect("presencas:listar_presencas_academicas")

    context = {
        "turma": turma,
        "ano": ano,
        "mes": mes,
        "breadcrumb": [
            {"etapa": "Dados Básicos", "ativa": False},
            {"etapa": "Totais de Atividades", "ativa": False},
            {"etapa": "Dias de Atividades", "ativa": True},
            {"etapa": "Alunos", "ativa": False},
        ],
        "titulo_pagina": "Registrar Presença - Dias de Atividades",
        "descricao_pagina": "Marque os dias em que houve atividades.",
    }
    return render(request, "presencas/registrar_presenca_dias_atividades.html", context)


@login_required
def registrar_presenca_alunos(request):
    turma_id = request.session.get("presenca_turma_id")
    ano = request.session.get("presenca_ano")
    mes = request.session.get("presenca_mes")

    if not all([turma_id, ano, mes]):
        messages.error(request, "Dados básicos não encontrados. Reinicie o processo.")
        return redirect("presencas:registrar_presenca_dados_basicos")

    turma = Turma.objects.get(id=turma_id)

    if request.method == "POST":
        # Processar dados do formulário
        request.session["presenca_alunos"] = True
        messages.success(request, "Presenças dos alunos registradas com sucesso!")
        return redirect("presencas:registrar_presenca_confirmar")

    context = {
        "turma": turma,
        "ano": ano,
        "mes": mes,
        "breadcrumb": [
            {"etapa": "Dados Básicos", "ativa": False},
            {"etapa": "Totais de Atividades", "ativa": False},
            {"etapa": "Dias de Atividades", "ativa": False},
            {"etapa": "Alunos", "ativa": True},
        ],
        "titulo_pagina": "Registrar Presença - Alunos",
        "descricao_pagina": "Registre as presenças dos alunos.",
    }
    return render(request, "presencas/registrar_presenca_alunos.html", context)


@login_required
def registrar_presenca_confirmar(request):
    turma_id = request.session.get("presenca_turma_id")
    ano = request.session.get("presenca_ano")
    mes = request.session.get("presenca_mes")

    if not all([turma_id, ano, mes]):
        messages.error(request, "Dados básicos não encontrados. Reinicie o processo.")
        return redirect("presencas:registrar_presenca_dados_basicos")

    turma = Turma.objects.get(id=turma_id)

    if request.method == "POST":
        # Finalizar o registro
        # Limpar dados da sessão
        keys_to_remove = [
            "presenca_turma_id",
            "presenca_ano",
            "presenca_mes",
            "presenca_atividades_totais",
            "presenca_dias_atividades",
            "presenca_alunos",
        ]
        for key in keys_to_remove:
            request.session.pop(key, None)

        messages.success(request, "Registro de presença finalizado com sucesso!")
        return redirect("presencas:listar_presencas_academicas")

    context = {
        "turma": turma,
        "ano": ano,
        "mes": mes,
        "breadcrumb": [
            {"etapa": "Dados Básicos", "ativa": False},
            {"etapa": "Totais de Atividades", "ativa": False},
            {"etapa": "Dias de Atividades", "ativa": False},
            {"etapa": "Alunos", "ativa": False},
            {"etapa": "Confirmar", "ativa": True},
        ],
        "titulo_pagina": "Registrar Presença - Confirmar",
        "descricao_pagina": "Revise e confirme os dados antes de finalizar.",
    }
    return render(request, "presencas/registrar_presenca_confirmar.html", context)


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
