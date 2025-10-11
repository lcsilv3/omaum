"""
Views para relatórios de atividades.
"""

import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone

from .utils import get_model_class

# Set up logger
logger = logging.getLogger(__name__)

NOME_ORGANIZACAO_PADRAO = "OMAUM - Ordem Mística de Aspiração Universal ao Mestrado"
NOME_SISTEMA_PADRAO = "Sistema de Gestão Integrada"


def _cabecalho_relatorio(titulo: str) -> dict:
    """Retorna os metadados padrão utilizados no cabeçalho dos relatórios do app Atividades."""

    return {
        "titulo": titulo,
        "data_emissao": timezone.now().strftime("%d/%m/%Y %H:%M"),
        "nome_organizacao": NOME_ORGANIZACAO_PADRAO,
        "nome_sistema": NOME_SISTEMA_PADRAO,
    }


@login_required
def relatorio_atividades(request):
    """Gera um relatório de atividades com base nos filtros aplicados."""
    Atividade = get_model_class("Atividade")

    # Obter parâmetros de filtro
    status = request.GET.get("status", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    # Filtrar atividades
    atividades = Atividade.objects.all()

    if status:
        atividades = atividades.filter(status=status)

    if data_inicio:
        atividades = atividades.filter(data_inicio__gte=data_inicio)

    if data_fim:
        atividades = atividades.filter(data_inicio__lte=data_fim)

    # Calcular totais
    total_atividades = atividades.count()

    context = {
        **_cabecalho_relatorio("Relatório de Atividades"),
        "atividades": atividades,
        "total_atividades": total_atividades,
        "status": status,
        "status_choices": Atividade.STATUS_CHOICES,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    return render(request, "atividades/relatorio_atividades.html", context)


@login_required
def relatorio_atividades_curso_turma(request):
    """Relatório de atividades por curso e turma."""
    Curso = get_model_class("Curso", "cursos")
    Turma = get_model_class("Turma", "turmas")
    Atividade = get_model_class("Atividade")

    # Obter filtros
    curso_id = request.GET.get("curso")
    turma_id = request.GET.get("turma")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    # Filtrar atividades
    atividades = Atividade.objects.all()

    if curso_id:
        atividades = atividades.filter(curso_id=curso_id)
    if turma_id:
        atividades = atividades.filter(turma_id=turma_id)
    if data_inicio:
        atividades = atividades.filter(data_inicio__gte=data_inicio)
    if data_fim:
        atividades = atividades.filter(data_inicio__lte=data_fim)

    # Obter dados para formulário
    cursos = Curso.objects.filter(ativo=True)
    turmas = Turma.objects.filter(status="A")

    if curso_id:
        turmas = turmas.filter(curso_id=curso_id)

    return render(
        request,
        "atividades/relatorio_atividades_curso_turma.html",
        {
            "atividades": atividades,
            "cursos": cursos,
            "turmas": turmas,
            "curso_selecionado": curso_id,
            "turma_selecionada": turma_id,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        },
    )


@login_required
def exportar_atividades(request, formato):
    """Exporta as atividades filtradas para o formato especificado."""
    # Obter os mesmos filtros que no relatório
    status = request.GET.get("status", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    # Obter atividades filtradas
    Atividade = get_model_class("Atividade")

    atividades = Atividade.objects.all()
    if status:
        atividades = atividades.filter(status=status)
    if data_inicio:
        atividades = atividades.filter(data_inicio__gte=data_inicio)
    if data_fim:
        atividades = atividades.filter(data_inicio__lte=data_fim)

    # Exportar para o formato solicitado
    if formato == "csv":
        return exportar_atividades_csv(atividades)
    elif formato == "excel":
        return exportar_atividades_excel(atividades)
    elif formato == "pdf":
        return exportar_atividades_pdf(atividades)
    else:
        messages.error(request, f"Formato de exportação '{formato}' não suportado.")
        return redirect("atividades:relatorio_atividades")


def exportar_atividades_csv(atividades):
    """Exporta as atividades para CSV."""
    import csv

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="atividades.csv"'

    writer = csv.writer(response)

    # Cabeçalho
    writer.writerow(
        [
            "Nome",
            "Descrição",
            "Data de Início",
            "Data de Término",
            "Responsável",
            "Local",
            "Status",
            "Tipo de Atividade",
        ]
    )

    # Dados das atividades
    for atividade in atividades:
        writer.writerow(
            [
                atividade.nome,
                atividade.descricao or "",
                atividade.data_inicio.strftime("%d/%m/%Y")
                if atividade.data_inicio
                else "",
                atividade.data_fim.strftime("%d/%m/%Y") if atividade.data_fim else "",
                atividade.responsavel or "",
                atividade.local or "",
                atividade.status or "",
                atividade.tipo_atividade or "",
            ]
        )

    return response


def exportar_atividades_excel(atividades):
    """Exporta as atividades para Excel."""
    try:
        import pandas as pd
    except ImportError:
        logger.error("Pandas não está instalado")
        return HttpResponse("Erro: Pandas não está instalado", status=500)

    # Criar DataFrame
    data = []
    for atividade in atividades:
        data.append(
            {
                "Nome": atividade.nome,
                "Descrição": atividade.descricao or "",
                "Data de Início": atividade.data_inicio.strftime("%d/%m/%Y")
                if atividade.data_inicio
                else "",
                "Data de Término": atividade.data_fim.strftime("%d/%m/%Y")
                if atividade.data_fim
                else "",
                "Responsável": atividade.responsavel or "",
                "Local": atividade.local or "",
                "Status": atividade.status or "",
                "Tipo de Atividade": atividade.tipo_atividade or "",
            }
        )

    df = pd.DataFrame(data)

    # Criar resposta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="atividades.xlsx"'

    # Escrever para Excel
    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Atividades", index=False)

    return response


def exportar_atividades_pdf(atividades):
    """Exporta as atividades para PDF."""
    # Implementação simples para PDF - pode ser expandida com ReportLab
    from django.template.loader import get_template

    template = get_template("atividades/relatorio_atividades_pdf.html")
    context = {
        "atividades": atividades,
        "total_atividades": atividades.count(),
    }

    html = template.render(context)

    # Para implementação completa, usar WeasyPrint ou ReportLab
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="atividades.pdf"'

    # Implementação básica - retorna HTML por enquanto
    response = HttpResponse(html, content_type="text/html")

    return response


@login_required
@require_GET
def ajax_turmas_por_curso_relatorio(request):
    """Endpoint AJAX que retorna as turmas de um curso em JSON para relatório."""
    curso_id = request.GET.get("curso_id")
    if not curso_id:
        return JsonResponse({"error": "Curso não especificado"}, status=400)

    try:
        Turma = get_model_class("Turma", "turmas")
        turmas = Turma.objects.filter(curso_id=curso_id, status="A")

        turmas_data = []
        for turma in turmas:
            turmas_data.append(
                {
                    "id": turma.id,
                    "nome": turma.nome,
                    "descricao": turma.descricao or "",
                }
            )

        return JsonResponse({"turmas": turmas_data})
    except Exception as e:
        logger.error(f"Erro ao buscar turmas: {e}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)


@login_required
@require_GET
def ajax_atividades_filtradas_relatorio(request):
    """Endpoint AJAX que retorna atividades filtradas por curso/turma para relatório."""
    curso_id = request.GET.get("curso_id")
    turma_id = request.GET.get("turma_id")

    try:
        Atividade = get_model_class("Atividade")
        atividades = Atividade.objects.all()

        if curso_id:
            atividades = atividades.filter(curso_id=curso_id)
        if turma_id:
            atividades = atividades.filter(turma_id=turma_id)

        # Retorna HTML parcial da tabela
        return render(
            request,
            "atividades/partials/tabela_atividades.html",
            {"atividades": atividades},
        )
    except Exception as e:
        logger.error(f"Erro ao buscar atividades: {e}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)
