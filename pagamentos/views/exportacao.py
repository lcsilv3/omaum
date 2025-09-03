from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from importlib import import_module
import logging
import csv

logger = logging.getLogger(__name__)


def get_models():
    """Obtém os modelos dinamicamente."""
    try:
        pagamentos_module = import_module("pagamentos.models")
        AtividadeAcademica = getattr(pagamentos_module, "AtividadeAcademica", None)
        AtividadeRitualistica = getattr(
            pagamentos_module, "AtividadeRitualistica", None
        )
        return AtividadeAcademica, AtividadeRitualistica
    except ImportError:
        return None, None


@login_required
def exportar_atividades(request, formato):
    """Exporta as atividades para um arquivo no formato especificado."""
    AtividadeAcademica, AtividadeRitualistica = get_models()

    # Obter parâmetros de filtro
    tipo = request.GET.get("tipo", "todas")
    status = request.GET.get("status", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    # Filtrar atividades acadêmicas
    atividades_academicas = AtividadeAcademica.objects.all()
    if status:
        atividades_academicas = atividades_academicas.filter(status=status)
    if data_inicio:
        atividades_academicas = atividades_academicas.filter(
            data_inicio__gte=data_inicio
        )
    if data_fim:
        atividades_academicas = atividades_academicas.filter(data_inicio__lte=data_fim)

    # Filtrar atividades ritualísticas
    atividades_ritualisticas = AtividadeRitualistica.objects.all()
    if data_inicio:
        atividades_ritualisticas = atividades_ritualisticas.filter(
            data__gte=data_inicio
        )
    if data_fim:
        atividades_ritualisticas = atividades_ritualisticas.filter(data__lte=data_fim)

    # Aplicar filtro por tipo
    if tipo == "academicas":
        atividades_ritualisticas = AtividadeRitualistica.objects.none()
    elif tipo == "ritualisticas":
        atividades_academicas = AtividadeAcademica.objects.none()

    # Exportar para CSV
    if formato == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="atividades.csv"'

        writer = csv.writer(response)
        writer.writerow(
            ["Tipo", "Nome", "Descrição", "Data", "Local", "Status", "Turma(s)"]
        )

        # Adicionar atividades acadêmicas
        for atividade in atividades_academicas:
            turmas = ", ".join([t.nome for t in atividade.turmas.all()])
            writer.writerow(
                [
                    "Acadêmica",
                    atividade.nome,
                    atividade.descricao,
                    atividade.data_inicio.strftime("%d/%m/%Y"),
                    atividade.local,
                    atividade.get_status_display(),
                    turmas,
                ]
            )

        # Adicionar atividades ritualísticas
        for atividade in atividades_ritualisticas:
            writer.writerow(
                [
                    "Ritualística",
                    atividade.nome,
                    atividade.descricao,
                    atividade.data.strftime("%d/%m/%Y"),
                    atividade.local,
                    "N/A",  # Atividades ritualísticas não têm status
                    atividade.turma.nome,
                ]
            )

        return response

    # Exportar para Excel
    elif formato == "excel":
        try:
            import xlwt

            response = HttpResponse(content_type="application/ms-excel")
            response["Content-Disposition"] = 'attachment; filename="atividades.xls"'

            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("Atividades")

            # Estilos
            header_style = xlwt.easyxf(
                "font: bold on; align: wrap on, vert centre, horiz center"
            )
            date_style = xlwt.easyxf(
                "align: wrap on, vert centre, horiz left", num_format_str="DD/MM/YYYY"
            )

            # Cabeçalho
            row_num = 0
            columns = [
                "Tipo",
                "Nome",
                "Descrição",
                "Data",
                "Local",
                "Status",
                "Turma(s)",
            ]

            for col_num, column_title in enumerate(columns):
                ws.write(row_num, col_num, column_title, header_style)

            # Adicionar atividades acadêmicas
            for atividade in atividades_academicas:
                row_num += 1
                turmas = ", ".join([t.nome for t in atividade.turmas.all()])

                ws.write(row_num, 0, "Acadêmica")
                ws.write(row_num, 1, atividade.nome)
                ws.write(row_num, 2, atividade.descricao)
                ws.write(row_num, 3, atividade.data_inicio, date_style)
                ws.write(row_num, 4, atividade.local)
                ws.write(row_num, 5, atividade.get_status_display())
                ws.write(row_num, 6, turmas)

            # Adicionar atividades ritualísticas
            for atividade in atividades_ritualisticas:
                row_num += 1

                ws.write(row_num, 0, "Ritualística")
                ws.write(row_num, 1, atividade.nome)
                ws.write(row_num, 2, atividade.descricao)
                ws.write(row_num, 3, atividade.data, date_style)
                ws.write(row_num, 4, atividade.local)
                ws.write(row_num, 5, "N/A")  # Atividades ritualísticas não têm status
                ws.write(row_num, 6, atividade.turma.nome)

            wb.save(response)
            return response
        except ImportError:
            messages.error(
                request,
                "A biblioteca xlwt não está instalada. Instale-a para exportar para Excel.",
            )
            return redirect("atividades:relatorio_atividades")

    # Exportar para PDF
    elif formato == "pdf":
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter, landscape
            from reportlab.platypus import (
                SimpleDocTemplate,
                Table,
                TableStyle,
                Paragraph,
            )
            from reportlab.lib.styles import getSampleStyleSheet
            from io import BytesIO

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
            elements = []

            # Estilos
            styles = getSampleStyleSheet()
            title_style = styles["Heading1"]

            # Título
            elements.append(Paragraph("Relatório de Atividades", title_style))

            # Dados da tabela
            data = [
                ["Tipo", "Nome", "Descrição", "Data", "Local", "Status", "Turma(s)"]
            ]

            # Adicionar atividades acadêmicas
            for atividade in atividades_academicas:
                turmas = ", ".join([t.nome for t in atividade.turmas.all()])
                data.append(
                    [
                        "Acadêmica",
                        atividade.nome,
                        atividade.descricao,
                        atividade.data_inicio.strftime("%d/%m/%Y"),
                        atividade.local,
                        atividade.get_status_display(),
                        turmas,
                    ]
                )

            # Adicionar atividades ritualísticas
            for atividade in atividades_ritualisticas:
                data.append(
                    [
                        "Ritualística",
                        atividade.nome,
                        atividade.descricao,
                        atividade.data.strftime("%d/%m/%Y"),
                        atividade.local,
                        "N/A",  # Atividades ritualísticas não têm status
                        atividade.turma.nome,
                    ]
                )

            # Criar tabela
            table = Table(data)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )

            elements.append(table)

            # Gerar PDF
            doc.build(elements)

            # Retornar resposta
            buffer.seek(0)
            response = HttpResponse(buffer, content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="atividades.pdf"'

            return response
        except ImportError:
            messages.error(
                request,
                "As bibliotecas necessárias para gerar PDF não estão instaladas.",
            )
            return redirect("atividades:relatorio_atividades")

    # Formato não suportado
    else:
        messages.error(request, f"Formato de exportação '{formato}' não suportado.")
        return redirect("atividades:relatorio_atividades")
