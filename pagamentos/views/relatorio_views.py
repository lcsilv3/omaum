import datetime
import io
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils import timezone
from django.views.decorators.http import require_GET

import xlsxwriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


# Importação dinâmica para evitar referências circulares
def get_pagamento_model():
    from pagamentos.models import Pagamento

    return Pagamento


@login_required
def relatorio_financeiro(request):
    """
    Exibe um relatório financeiro com dados de pagamentos.
    """
    Pagamento = get_pagamento_model()
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)

    total_pago = Pagamento.objects.filter(status="PAGO").aggregate(
        total=Sum("valor_pago")
    )["total"] or Decimal("0.00")
    total_pendente = Pagamento.objects.filter(status="PENDENTE").aggregate(
        total=Sum("valor")
    )["total"] or Decimal("0.00")
    total_atrasado = Pagamento.objects.filter(status="ATRASADO").aggregate(
        total=Sum("valor")
    )["total"] or Decimal("0.00")
    total_cancelado = Pagamento.objects.filter(status="CANCELADO").aggregate(
        total=Sum("valor")
    )["total"] or Decimal("0.00")
    total_geral = total_pago + total_pendente + total_atrasado + total_cancelado

    pagamentos_mes = Pagamento.objects.filter(
        data_vencimento__gte=primeiro_dia_mes, data_vencimento__lte=hoje
    ).order_by("-data_vencimento")

    pagos_mes = pagamentos_mes.filter(status="PAGO").count()
    pendentes_mes = pagamentos_mes.filter(status="PENDENTE").count()
    atrasados_mes = pagamentos_mes.filter(status="ATRASADO").count()
    cancelados_mes = pagamentos_mes.filter(status="CANCELADO").count()

    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    mes_atual = meses[hoje.month - 1]

    context = {
        "total_pago": total_pago,
        "total_pendente": total_pendente,
        "total_atrasado": total_atrasado,
        "total_cancelado": total_cancelado,
        "total_geral": total_geral,
        "pagamentos_mes": pagamentos_mes,
        "pagos_mes": pagos_mes,
        "pendentes_mes": pendentes_mes,
        "atrasados_mes": atrasados_mes,
        "cancelados_mes": cancelados_mes,
        "mes_atual": mes_atual,
    }
    return render(request, "pagamentos/relatorio_financeiro.html", context)


@login_required
def exportar_pagamentos_excel(request):
    """
    Exporta os pagamentos para um arquivo Excel.
    """
    Pagamento = get_pagamento_model()

    # Obter filtros da requisição
    status = request.GET.get("status", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    # Filtrar pagamentos
    pagamentos = Pagamento.objects.all().order_by("-data_vencimento")

    if status:
        pagamentos = pagamentos.filter(status=status)

    if data_inicio:
        try:
            data_inicio_obj = datetime.datetime.strptime(data_inicio, "%Y-%m-%d").date()
            pagamentos = pagamentos.filter(data_vencimento__gte=data_inicio_obj)
        except ValueError:
            pass

    if data_fim:
        try:
            data_fim_obj = datetime.datetime.strptime(data_fim, "%Y-%m-%d").date()
            pagamentos = pagamentos.filter(data_vencimento__lte=data_fim_obj)
        except ValueError:
            pass

    # Criar arquivo Excel em memória
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Pagamentos")

    # Formatos
    header_format = workbook.add_format(
        {
            "bold": True,
            "bg_color": "#4472C4",
            "color": "white",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        }
    )

    date_format = workbook.add_format({"num_format": "dd/mm/yyyy"})
    money_format = workbook.add_format({"num_format": "R$ #,##0.00"})

    # Cabeçalhos
    headers = [
        "ID",
        "Aluno",
        "CPF",
        "Valor",
        "Vencimento",
        "Status",
        "Data Pagamento",
        "Valor Pago",
        "Método",
    ]

    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)

    # Dados
    for row, pagamento in enumerate(pagamentos, start=1):
        worksheet.write(row, 0, pagamento.id)
        worksheet.write(row, 1, pagamento.aluno.nome)
        worksheet.write(row, 2, pagamento.aluno.cpf)
        worksheet.write(row, 3, float(pagamento.valor), money_format)
        worksheet.write(row, 4, pagamento.data_vencimento, date_format)
        worksheet.write(row, 5, pagamento.get_status_display())

        if pagamento.data_pagamento:
            worksheet.write(row, 6, pagamento.data_pagamento, date_format)
        else:
            worksheet.write(row, 6, "-")

        if pagamento.valor_pago:
            worksheet.write(row, 7, float(pagamento.valor_pago), money_format)
        else:
            worksheet.write(row, 7, "-")

        if pagamento.metodo_pagamento:
            worksheet.write(row, 8, pagamento.get_metodo_pagamento_display())
        else:
            worksheet.write(row, 8, "-")

    # Ajustar largura das colunas
    worksheet.set_column("A:A", 5)  # ID
    worksheet.set_column("B:B", 30)  # Aluno
    worksheet.set_column("C:C", 15)  # CPF
    worksheet.set_column("D:D", 12)  # Valor
    worksheet.set_column("E:E", 12)  # Vencimento
    worksheet.set_column("F:F", 12)  # Status
    worksheet.set_column("G:G", 15)  # Data Pagamento
    worksheet.set_column("H:H", 12)  # Valor Pago
    worksheet.set_column("I:I", 15)  # Método

    workbook.close()

    # Preparar resposta
    output.seek(0)

    hoje = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"pagamentos_{hoje}.xlsx"

    response = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    return response


@login_required
def exportar_pagamentos_pdf(request):
    """
    Exporta os pagamentos para um arquivo PDF.
    """
    Pagamento = get_pagamento_model()

    # Obter filtros da requisição
    status = request.GET.get("status", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    # Filtrar pagamentos
    pagamentos = Pagamento.objects.all().order_by("-data_vencimento")

    if status:
        pagamentos = pagamentos.filter(status=status)

    if data_inicio:
        try:
            data_inicio_obj = datetime.datetime.strptime(data_inicio, "%Y-%m-%d").date()
            pagamentos = pagamentos.filter(data_vencimento__gte=data_inicio_obj)
        except ValueError:
            pass

    if data_fim:
        try:
            data_fim_obj = datetime.datetime.strptime(data_fim, "%Y-%m-%d").date()
            pagamentos = pagamentos.filter(data_vencimento__lte=data_fim_obj)
        except ValueError:
            pass

    # Calcular totais
    total_pago = pagamentos.filter(status="PAGO").aggregate(total=Sum("valor_pago"))[
        "total"
    ] or Decimal("0.00")
    total_pendente = pagamentos.filter(
        Q(status="PENDENTE") | Q(status="ATRASADO")
    ).aggregate(total=Sum("valor"))["total"] or Decimal("0.00")
    total_geral = total_pago + total_pendente

    # Preparar dados para o template
    filtros = {
        "status": dict(Pagamento.STATUS_CHOICES).get(status, "Todos")
        if status
        else "Todos",
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }

    # Renderizar o HTML
    template = get_template("pagamentos/pdf/pagamentos_pdf.html")
    template.render(
        {
            "pagamentos": pagamentos,
            "filtros": filtros,
            "total_pago": total_pago,
            "total_pendente": total_pendente,
            "total_geral": total_geral,
            "data_geracao": timezone.now(),
        }
    )

    # Gerar PDF usando ReportLab
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = 1  # Centralizado

    # Título
    elements.append(Paragraph("Relatório de Pagamentos", title_style))
    elements.append(Spacer(1, 0.25 * inch))

    # Dados para a tabela
    data = [["Aluno", "CPF", "Valor", "Vencimento", "Status", "Data Pagamento"]]

    for pagamento in pagamentos:
        data.append(
            [
                pagamento.aluno.nome,
                pagamento.aluno.cpf,
                f"R$ {pagamento.valor:.2f}",
                pagamento.data_vencimento.strftime("%d/%m/%Y"),
                pagamento.get_status_display(),
                pagamento.data_pagamento.strftime("%d/%m/%Y")
                if pagamento.data_pagamento
                else "-",
            ]
        )

    # Criar tabela
    table = Table(data)  # Estilo da tabela
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (2, 1), (2, -1), "RIGHT"),  # Alinhar valores à direita
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("TOPPADDING", (0, 1), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ]
    )

    # Aplicar estilos alternados para as linhas
    for i in range(1, len(data)):
        if i % 2 == 0:
            table_style.add("BACKGROUND", (0, i), (-1, i), colors.lightgrey)

    table.setStyle(table_style)
    elements.append(table)

    # Adicionar informações de totais
    elements.append(Spacer(1, 0.5 * inch))

    # Estilo para o resumo
    summary_style = ParagraphStyle(
        "Summary",
        parent=styles["Normal"],
        fontSize=12,
        alignment=2,  # Alinhado à direita
        spaceAfter=6,
    )

    elements.append(Paragraph(f"Total Pago: R$ {total_pago:.2f}", summary_style))
    elements.append(
        Paragraph(f"Total Pendente: R$ {total_pendente:.2f}", summary_style)
    )
    elements.append(Paragraph(f"Total Geral: R$ {total_geral:.2f}", summary_style))

    # Adicionar rodapé com data de geração
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.grey,
        alignment=1,  # Centralizado
    )

    data_geracao = timezone.now().strftime("%d/%m/%Y %H:%M:%S")
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(f"Relatório gerado em {data_geracao}", footer_style))

    # Construir o PDF
    doc.build(elements)

    # Preparar resposta
    buffer.seek(0)

    hoje = timezone.now().strftime("%Y%m%d")
    filename = f"pagamentos_{hoje}.pdf"

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    return response


@login_required
@require_GET
def dados_grafico_pagamentos(request):
    """
    Retorna dados para o gráfico de pagamentos.
    """
    Pagamento = get_pagamento_model()

    # Obter período (padrão: últimos 6 meses)
    meses = int(request.GET.get("meses", 6))
    if meses > 12:
        meses = 12  # Limitar a 12 meses

    # Data atual e data inicial
    data_final = timezone.now().date()
    data_inicial = (data_final - datetime.timedelta(days=30 * meses)).replace(day=1)

    # Preparar dados
    labels = []
    dados_pagos = []
    dados_pendentes = []
    dados_atrasados = []

    # Gerar dados para cada mês
    data_atual = data_inicial
    while data_atual <= data_final:
        # Último dia do mês
        if data_atual.month == 12:
            ultimo_dia = data_atual.replace(day=31)
        else:
            ultimo_dia = data_atual.replace(
                month=data_atual.month + 1, day=1
            ) - datetime.timedelta(days=1)

        # Filtrar pagamentos do mês
        pagamentos_mes = Pagamento.objects.filter(
            data_vencimento__gte=data_atual, data_vencimento__lte=ultimo_dia
        )

        # Calcular totais
        total_pago = (
            pagamentos_mes.filter(status="PAGO").aggregate(total=Sum("valor_pago"))[
                "total"
            ]
            or 0
        )
        total_pendente = (
            pagamentos_mes.filter(status="PENDENTE").aggregate(total=Sum("valor"))[
                "total"
            ]
            or 0
        )
        total_atrasado = (
            pagamentos_mes.filter(status="ATRASADO").aggregate(total=Sum("valor"))[
                "total"
            ]
            or 0
        )

        # Adicionar aos dados
        mes_nome = data_atual.strftime("%b/%Y")
        labels.append(mes_nome)
        dados_pagos.append(float(total_pago))
        dados_pendentes.append(float(total_pendente))
        dados_atrasados.append(float(total_atrasado))

        # Avançar para o próximo mês
        if data_atual.month == 12:
            data_atual = data_atual.replace(year=data_atual.year + 1, month=1)
        else:
            data_atual = data_atual.replace(month=data_atual.month + 1)

    # Retornar dados em formato JSON
    return JsonResponse(
        {
            "labels": labels,
            "datasets": [
                {
                    "label": "Pagos",
                    "data": dados_pagos,
                    "backgroundColor": "rgba(40, 167, 69, 0.7)",
                    "borderColor": "rgba(40, 167, 69, 1)",
                    "borderWidth": 1,
                },
                {
                    "label": "Pendentes",
                    "data": dados_pendentes,
                    "backgroundColor": "rgba(255, 193, 7, 0.7)",
                    "borderColor": "rgba(255, 193, 7, 1)",
                    "borderWidth": 1,
                },
                {
                    "label": "Atrasados",
                    "data": dados_atrasados,
                    "backgroundColor": "rgba(220, 53, 69, 0.7)",
                    "borderColor": "rgba(220, 53, 69, 1)",
                    "borderWidth": 1,
                },
            ],
        }
    )


@login_required
def pagamentos_por_turma(request):
    """
    Exibe um relatório de pagamentos agrupados por turma.
    """
    Pagamento = get_pagamento_model()

    # Importar modelo de Turma dinamicamente para evitar referências circulares
    try:
        from turmas.models import Turma
        from matriculas.models import Matricula
    except ImportError:
        messages.error(request, "Módulo de turmas ou matrículas não disponível")
        return redirect("pagamentos:relatorio_financeiro")

    # Obter todas as turmas ativas
    turmas = Turma.objects.filter(ativa=True).order_by("nome")

    # Dados para o relatório
    dados_turmas = []

    for turma in turmas:
        # Obter alunos matriculados nesta turma
        matriculas = Matricula.objects.filter(turma=turma, ativa=True)
        alunos_ids = matriculas.values_list("aluno_id", flat=True)

        # Obter pagamentos destes alunos
        pagamentos = Pagamento.objects.filter(aluno_id__in=alunos_ids)

        # Calcular totais
        total_pago = pagamentos.filter(status="PAGO").aggregate(
            total=Sum("valor_pago")
        )["total"] or Decimal("0.00")
        total_pendente = pagamentos.filter(status="PENDENTE").aggregate(
            total=Sum("valor")
        )["total"] or Decimal("0.00")
        total_atrasado = pagamentos.filter(status="ATRASADO").aggregate(
            total=Sum("valor")
        )["total"] or Decimal("0.00")
        total_cancelado = pagamentos.filter(status="CANCELADO").aggregate(
            total=Sum("valor")
        )["total"] or Decimal("0.00")

        # Adicionar dados da turma
        dados_turmas.append(
            {
                "turma": turma,
                "total_alunos": matriculas.count(),
                "total_pago": total_pago,
                "total_pendente": total_pendente,
                "total_atrasado": total_atrasado,
                "total_cancelado": total_cancelado,
                "total_geral": total_pago
                + total_pendente
                + total_atrasado
                + total_cancelado,
            }
        )

    context = {"dados_turmas": dados_turmas, "data_geracao": timezone.now()}

    return render(request, "pagamentos/relatorio_pagamentos_turma.html", context)


@login_required
@require_GET
def dados_distribuicao_pagamentos(request):
    """
    Retorna dados para o gráfico de distribuição de pagamentos.
    """
    Pagamento = get_pagamento_model()

    # Obter data atual e primeiro dia do mês
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)

    # Obter pagamentos do mês atual
    pagamentos_mes = Pagamento.objects.filter(
        data_vencimento__gte=primeiro_dia_mes, data_vencimento__lte=hoje
    )

    # Contar por status
    pagos = pagamentos_mes.filter(status="PAGO").count()
    pendentes = pagamentos_mes.filter(status="PENDENTE").count()
    atrasados = pagamentos_mes.filter(status="ATRASADO").count()
    cancelados = pagamentos_mes.filter(status="CANCELADO").count()

    # Retornar dados em formato JSON
    return JsonResponse(
        {
            "labels": ["Pagos", "Pendentes", "Atrasados", "Cancelados"],
            "datasets": [
                {
                    "data": [pagos, pendentes, atrasados, cancelados],
                    "backgroundColor": [
                        "rgba(40, 167, 69, 0.7)",  # Verde
                        "rgba(255, 193, 7, 0.7)",  # Amarelo
                        "rgba(220, 53, 69, 0.7)",  # Vermelho
                        "rgba(108, 117, 125, 0.7)",  # Cinza
                    ],
                    "borderColor": [
                        "rgba(40, 167, 69, 1)",
                        "rgba(255, 193, 7, 1)",
                        "rgba(220, 53, 69, 1)",
                        "rgba(108, 117, 125, 1)",
                    ],
                    "borderWidth": 1,
                }
            ],
        }
    )
