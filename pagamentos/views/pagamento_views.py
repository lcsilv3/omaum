"""Views relacionadas às operações básicas de pagamentos (CRUD, exportação e importação)."""

import csv
import datetime
import logging
from io import TextIOWrapper

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_GET

from pagamentos.models import Pagamento  # ajuste o import conforme seu projeto
from ..forms import PagamentoForm, PagamentoRapidoForm
from .base import get_pagamento_model, get_aluno_model
from turmas.models import Turma
from cursos.models import Curso  # ajuste o import conforme seu projeto

logger = logging.getLogger(__name__)


@login_required
def listar_pagamentos(request):
    """Lista todos os pagamentos com filtros e exportação."""
    try:
        Pagamento = get_pagamento_model()

        # Obter parâmetros de filtro
        query = request.GET.get("q", "")
        status = request.GET.get("status", "")
        data_inicio = request.GET.get("data_inicio", "")
        data_fim = request.GET.get("data_fim", "")
        request.GET.get("exportar", "")  # 'csv', 'excel', 'pdf'

        # Filtrar pagamentos
        pagamentos = Pagamento.objects.all()

        if query:
            pagamentos = pagamentos.filter(
                Q(aluno__nome__icontains=query)
                | Q(aluno__cpf__icontains=query)
                | Q(observacoes__icontains=query)
            )

        if status:
            pagamentos = pagamentos.filter(status=status)

        if data_inicio:
            pagamentos = pagamentos.filter(data_vencimento__gte=data_inicio)

        if data_fim:
            pagamentos = pagamentos.filter(data_vencimento__lte=data_fim)

        # Totais filtrados
        total_pago = (
            pagamentos.filter(status="PAGO").aggregate(total=Sum("valor"))["total"] or 0
        )
        total_pendente = (
            pagamentos.filter(status="PENDENTE").aggregate(total=Sum("valor"))["total"]
            or 0
        )
        total_atrasado = (
            pagamentos.filter(status="ATRASADO").aggregate(total=Sum("valor"))["total"]
            or 0
        )
        total_cancelados = (
            pagamentos.filter(status="CANCELADO").aggregate(total=Sum("valor"))["total"]
            or 0
        )
        total_geral = pagamentos.aggregate(total=Sum("valor"))["total"] or 0

        # Paginação
        paginator = Paginator(pagamentos, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "pagamentos": page_obj,
            "total_pago": total_pago,
            "total_pendente": total_pendente,
            "total_atrasado": total_atrasado,
            "total_cancelados": total_cancelados,
            "total_geral": total_geral,
            "query": query,
            "status": status,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        }

        return render(request, "pagamentos/listar_pagamentos.html", context)

    except Exception as e:
        logger.error(f"Erro ao listar pagamentos: {str(e)}")
        messages.error(request, f"Erro ao listar pagamentos: {str(e)}")
        return render(request, "pagamentos/listar_pagamentos.html", {"pagamentos": []})


@login_required
def criar_pagamento(request):
    """Cria um novo pagamento."""
    get_pagamento_model()
    Aluno = get_aluno_model()

    cursos = Curso.objects.all().order_by("nome")

    if request.method == "POST":
        form = PagamentoForm(request.POST)
        # Defina o queryset de alunos mesmo em POST
        form.fields["aluno"].queryset = Aluno.objects.all()
        if form.is_valid():
            pagamento = form.save()
            messages.success(request, "Pagamento criado com sucesso!")
            return redirect("pagamentos:detalhar_pagamento", pagamento_id=pagamento.id)
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = PagamentoForm()
        form.fields["aluno"].queryset = Aluno.objects.all()

    return render(
        request, "pagamentos/criar_pagamento.html", {"form": form, "cursos": cursos}
    )


@login_required
def editar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    try:
        if request.method == "POST":
            form = PagamentoForm(request.POST, request.FILES, instance=pagamento)
            if form.is_valid():
                form.save()
                messages.success(request, "Pagamento atualizado com sucesso!")
                return redirect(
                    "pagamentos:detalhar_pagamento", pagamento_id=pagamento.id
                )
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = PagamentoForm(instance=pagamento)
        return render(
            request,
            "pagamentos/editar_pagamento.html",
            {"form": form, "pagamento": pagamento},
        )
    except Exception as e:
        logger.error("Erro ao editar pagamento: %s", str(e))
        messages.error(request, f"Erro ao editar pagamento: {str(e)}")
        return redirect("pagamentos:listar_pagamentos")


@login_required
def excluir_pagamento(request, pagamento_id):
    """Exclui um pagamento com padrão de exclusão segura."""
    Pagamento = get_pagamento_model()
    try:
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        # Buscar dependências (exemplo: notas, recibos, etc. - atualmente não há)
        dependencias = {}
        # Se no futuro houver dependências, adicionar aqui
        if request.method == "POST":
            if any(len(lst) > 0 for lst in dependencias.values()):
                messages.error(
                    request,
                    "Não é possível excluir o pagamento pois existem registros vinculados. Remova as dependências antes de tentar novamente.",
                    extra_tags="safe",
                )
                return redirect(
                    "pagamentos:excluir_pagamento", pagamento_id=pagamento.id
                )
            pagamento.delete()
            messages.success(request, "Pagamento excluído com sucesso!")
            return redirect("pagamentos:listar_pagamentos")
        return render(
            request,
            "pagamentos/excluir_pagamento.html",
            {"pagamento": pagamento, "dependencias": dependencias},
        )
    except Exception as e:
        logger.error("Erro ao excluir pagamento: %s", str(e))
        messages.error(request, f"Erro ao excluir pagamento: {str(e)}")
        return redirect("pagamentos:listar_pagamentos")


@login_required
def pagamentos_aluno(request, cpf):
    """Exibe os pagamentos de um aluno específico."""
    try:
        Aluno = get_aluno_model()
        Pagamento = get_pagamento_model()
        aluno = get_object_or_404(Aluno, cpf=cpf)

        status = request.GET.get("status", "")
        data_inicio = request.GET.get("data_inicio", "")
        data_fim = request.GET.get("data_fim", "")

        pagamentos = Pagamento.objects.filter(aluno=aluno)

        if status:
            pagamentos = pagamentos.filter(status=status)
        if data_inicio:
            try:
                data_inicio_dt = datetime.datetime.strptime(
                    data_inicio, "%Y-%m-%d"
                ).date()
                pagamentos = pagamentos.filter(data_vencimento__gte=data_inicio_dt)
            except ValueError:
                pass
        if data_fim:
            try:
                data_fim_dt = datetime.datetime.strptime(data_fim, "%Y-%m-%d").date()
                pagamentos = pagamentos.filter(data_vencimento__lte=data_fim_dt)
            except ValueError:
                pass

        pagamentos = pagamentos.order_by("-data_vencimento")

        total_pago = (
            pagamentos.filter(status="PAGO").aggregate(Sum("valor"))["valor__sum"] or 0
        )
        total_pendente = (
            pagamentos.filter(status="PENDENTE").aggregate(Sum("valor"))["valor__sum"]
            or 0
        )
        total_atrasado = (
            pagamentos.filter(status="ATRASADO").aggregate(Sum("valor"))["valor__sum"]
            or 0
        )

        paginator = Paginator(pagamentos, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "aluno": aluno,
            "pagamentos": page_obj,
            "page_obj": page_obj,
            "status": status,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "total_pago": total_pago,
            "total_pendente": total_pendente,
            "total_atrasado": total_atrasado,
            "total_geral": total_pago + total_pendente + total_atrasado,
        }

        return render(request, "pagamentos/pagamentos_aluno.html", context)
    except Exception as e:
        logger.error(f"Erro ao listar pagamentos do aluno {cpf}: {str(e)}")
        messages.error(request, f"Erro ao listar pagamentos do aluno: {str(e)}")
        return redirect("pagamentos:listar_pagamentos")


@login_required
def registrar_pagamento_rapido(request, cpf):
    Aluno = get_aluno_model()
    aluno = get_object_or_404(Aluno, cpf=cpf)
    if request.method == "POST":
        form = PagamentoRapidoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.aluno = aluno
            pagamento.save()
            messages.success(request, "Pagamento registrado com sucesso!")
            return redirect("pagamentos:pagamentos_aluno", cpf=aluno.cpf)
    else:
        form = PagamentoRapidoForm()
    return render(
        request,
        "pagamentos/registrar_pagamento_rapido.html",
        {"form": form, "aluno": aluno},
    )


@login_required
def importar_pagamentos_csv(request):
    """
    Importa pagamentos a partir de um arquivo CSV enviado pelo usuário.
    Espera um arquivo com cabeçalhos: aluno_cpf, valor, data_vencimento, status, observacoes
    """
    Pagamento = get_pagamento_model()
    Aluno = get_aluno_model()
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        try:
            # Decodifica o arquivo para leitura universal
            decoded_file = TextIOWrapper(csv_file.file, encoding="utf-8")
            reader = csv.DictReader(decoded_file)
            criados = 0
            erros = []
            for idx, row in enumerate(
                reader, start=2
            ):  # start=2 para considerar o cabeçalho
                try:
                    aluno_cpf = row.get("aluno_cpf")
                    valor = float(row.get("valor", 0))
                    data_vencimento = datetime.datetime.strptime(
                        row.get("data_vencimento"), "%Y-%m-%d"
                    ).date()
                    status = row.get("status", "PENDENTE")
                    observacoes = row.get("observacoes", "")

                    aluno = Aluno.objects.get(cpf=aluno_cpf)
                    Pagamento.objects.create(
                        aluno=aluno,
                        valor=valor,
                        data_vencimento=data_vencimento,
                        status=status,
                        observacoes=observacoes,
                    )
                    criados += 1
                except Exception as e:
                    erros.append(f"Linha {idx}: {str(e)}")
            if criados:
                messages.success(
                    request, f"{criados} pagamentos importados com sucesso!"
                )
            if erros:
                messages.warning(
                    request, "Algumas linhas não foram importadas:\n" + "\n".join(erros)
                )
            return redirect("pagamentos:listar_pagamentos")
        except Exception as e:
            logger.error(f"Erro ao importar pagamentos CSV: {str(e)}")
            messages.error(request, f"Erro ao importar pagamentos: {str(e)}")
    return render(request, "pagamentos/importar_pagamentos.html")


def exportar_pagamentos_csv(pagamentos_queryset):
    """Exporta pagamentos para CSV."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="pagamentos.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "Aluno",
            "Valor",
            "Vencimento",
            "Status",
            "Data Pagamento",
            "Método",
            "Observações",
        ]
    )
    for p in pagamentos_queryset:
        writer.writerow(
            [
                p.aluno.nome,
                f"{p.valor:.2f}",
                p.data_vencimento.strftime("%d/%m/%Y"),
                p.get_status_display(),
                p.data_pagamento.strftime("%d/%m/%Y") if p.data_pagamento else "",
                p.get_metodo_pagamento_display()
                if hasattr(p, "get_metodo_pagamento_display") and p.metodo_pagamento
                else "",
                p.observacoes or "",
            ]
        )
    return response


def exportar_pagamentos_excel(pagamentos_queryset):
    """Exporta pagamentos para Excel (formato CSV para compatibilidade)."""
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="pagamentos.xls"'
    writer = csv.writer(response, delimiter="\t")
    writer.writerow(
        [
            "Aluno",
            "Valor",
            "Vencimento",
            "Status",
            "Data Pagamento",
            "Método",
            "Observações",
        ]
    )
    for p in pagamentos_queryset:
        writer.writerow(
            [
                p.aluno.nome,
                f"{p.valor:.2f}",
                p.data_vencimento.strftime("%d/%m/%Y"),
                p.get_status_display(),
                p.data_pagamento.strftime("%d/%m/%Y") if p.data_pagamento else "",
                p.get_metodo_pagamento_display()
                if hasattr(p, "get_metodo_pagamento_display") and p.metodo_pagamento
                else "",
                p.observacoes or "",
            ]
        )
    return response


@login_required
def exportar_pagamentos_pdf(request):
    """View para exportar pagamentos filtrados para PDF."""
    Pagamento = get_pagamento_model()

    # Obter filtros da query string
    query = request.GET.get("q", "")
    status = request.GET.get("status", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    pagamentos = Pagamento.objects.all().select_related("aluno")

    if query:
        pagamentos = pagamentos.filter(
            Q(aluno__nome__icontains=query)
            | Q(aluno__cpf__icontains=query)
            | Q(observacoes__icontains=query)
        )
    if status:
        pagamentos = pagamentos.filter(status=status)
    if data_inicio:
        try:
            data_inicio_dt = datetime.datetime.strptime(data_inicio, "%Y-%m-%d").date()
            pagamentos = pagamentos.filter(data_vencimento__gte=data_inicio_dt)
        except ValueError:
            data_inicio_dt = ""
    else:
        data_inicio_dt = ""
    if data_fim:
        try:
            data_fim_dt = datetime.datetime.strptime(data_fim, "%Y-%m-%d").date()
            pagamentos = pagamentos.filter(data_vencimento__lte=data_fim_dt)
        except ValueError:
            data_fim_dt = ""
    else:
        data_fim_dt = ""

    # Totais
    total_pago = (
        pagamentos.filter(status="PAGO").aggregate(Sum("valor"))["valor__sum"] or 0
    )
    total_pendente = (
        pagamentos.filter(status="PENDENTE").aggregate(Sum("valor"))["valor__sum"] or 0
    )
    total_geral = total_pago + total_pendente

    context = {
        "pagamentos": pagamentos,
        "data_geracao": timezone.now(),
        "total_pago": total_pago,
        "total_pendente": total_pendente,
        "total_geral": total_geral,
        "filtros": {
            "status": dict(Pagamento.STATUS_CHOICES).get(status) if status else "Todos",
            "data_inicio": data_inicio_dt,
            "data_fim": data_fim_dt,
        },
    }
    return exportar_pagamentos_pdf_util(pagamentos, context)


# Renomeie a função utilitária para evitar conflito de nomes:
def exportar_pagamentos_pdf_util(pagamentos_queryset, context):
    """Exporta pagamentos para PDF usando um template HTML."""
    from django.template.loader import render_to_string

    html = render_to_string("pagamentos/pdf/pagamentos_pdf.html", context)
    return HttpResponse(html)


@login_required
def detalhar_pagamento(request, pagamento_id):
    """Exibe os detalhes de um pagamento."""
    Pagamento = get_pagamento_model()
    try:
        pagamento = get_object_or_404(Pagamento, id=pagamento_id)
        return render(
            request, "pagamentos/detalhar_pagamento.html", {"pagamento": pagamento}
        )
    except Exception as e:
        logger.error("Erro ao detalhar pagamento: %s", str(e))
        messages.error(request, f"Erro ao detalhar pagamento: {str(e)}")
        return redirect("pagamentos:listar_pagamentos")


def turmas_por_curso(request):
    curso_id = request.GET.get("curso_id")
    turmas = []
    if curso_id:
        turmas = list(Turma.objects.filter(curso_id=curso_id).values("id", "nome"))
    return JsonResponse(turmas, safe=False)


@require_GET
@login_required
def buscar_alunos(request):
    termo = request.GET.get("q", "").strip()
    Aluno = get_aluno_model()
    alunos = []
    if termo and len(termo) >= 2:
        alunos = Aluno.objects.filter(
            Q(nome__icontains=termo) | Q(cpf__icontains=termo)
        ).values("cpf", "nome")[:10]  # <-- Corrigido aqui!
    return JsonResponse(list(alunos), safe=False)
