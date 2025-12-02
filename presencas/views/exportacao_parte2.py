"""
Continuação das views de exportação avançada.
Implementa CSV, PDF e agendamento.
"""

import csv
import tempfile
import os
import io
from typing import Dict, Any, List
from datetime import datetime
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from celery import shared_task
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table as RLTable,
    TableStyle,
    Spacer,
)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
import logging

# Importações da parte 1
from .exportacao import ProcessarExportacaoView, ExcelAvancadoExporter

logger = logging.getLogger(__name__)


class CSVExporter:
    """
    Classe para exportação em formato CSV.
    """

    def gerar_csv_consolidado(
        self, dados: Dict[str, Any], config: Dict[str, Any]
    ) -> HttpResponse:
        """Gera arquivo CSV do consolidado."""

        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = (
            'attachment; filename="consolidado_presencas.csv"'
        )

        # Adicionar BOM para Excel
        response.write("\ufeff")

        writer = csv.writer(response, delimiter=";")  # Usar ; para Excel brasileiro

        # Cabeçalho com informações
        writer.writerow(
            [f"Relatório gerado em: {timezone.now().strftime('%d/%m/%Y %H:%M')}"]
        )
        writer.writerow([])

        # Filtros aplicados
        filtros = dados["filtros_aplicados"]
        if filtros:
            writer.writerow(["Filtros aplicados:"])
            for chave, valor in filtros.items():
                if valor:
                    writer.writerow([f"{chave}: {valor}"])
            writer.writerow([])

        # Estatísticas resumo
        stats = dados["estatisticas"]
        writer.writerow(["ESTATÍSTICAS GERAIS"])
        writer.writerow(["Total de Alunos", stats["total_alunos"]])
        writer.writerow(["Total de Atividades", stats["total_atividades"]])
        writer.writerow(["Total de Presenças", stats["total_presencas"]])
        writer.writerow(["Total de Faltas", stats["total_faltas"]])
        writer.writerow(["Percentual Médio", f"{stats['percentual_medio']:.2f}%"])
        writer.writerow([])

        # Cabeçalhos da tabela principal
        headers = ["Aluno", "Turma"]
        atividades = dados["atividades"]

        for atividade in atividades:
            headers.extend(
                [
                    f"{atividade.nome} - Convocações",
                    f"{atividade.nome} - Presenças",
                    f"{atividade.nome} - Faltas",
                    f"{atividade.nome} - Percentual",
                ]
            )

        headers.extend(
            ["Total Convocações", "Total Presenças", "Total Faltas", "Percentual Médio"]
        )
        writer.writerow(headers)

        # Dados consolidados
        excel_exporter = ExcelAvancadoExporter()
        dados_por_aluno = excel_exporter._agrupar_dados_por_aluno(
            dados["presencas_detalhadas"], atividades
        )

        for aluno_dados in dados_por_aluno.values():
            row = [aluno_dados["aluno"].nome, aluno_dados["turma"].nome]

            # Dados por atividade
            for atividade in atividades:
                presenca = aluno_dados["atividades"].get(atividade.id)
                if presenca:
                    row.extend(
                        [
                            presenca.convocacoes,
                            presenca.presencas,
                            presenca.faltas,
                            f"{float(presenca.percentual_presenca):.2f}%",
                        ]
                    )
                else:
                    row.extend([0, 0, 0, "0.00%"])

            # Totais
            totais = aluno_dados["totais"]
            perc_medio = (
                totais["presencas"] / totais["convocacoes"] * 100
                if totais["convocacoes"] > 0
                else 0
            )

            row.extend(
                [
                    totais["convocacoes"],
                    totais["presencas"],
                    totais["faltas"],
                    f"{perc_medio:.2f}%",
                ]
            )

            writer.writerow(row)

        return response

    def gerar_csv_por_turma(
        self, dados: Dict[str, Any], config: Dict[str, Any]
    ) -> HttpResponse:
        """Gera CSV agrupado por turma."""

        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = (
            'attachment; filename="presencas_por_turma.csv"'
        )
        response.write("\ufeff")

        writer = csv.writer(response, delimiter=";")

        # Cabeçalho
        writer.writerow(
            [f"Relatório por Turma - {timezone.now().strftime('%d/%m/%Y %H:%M')}"]
        )
        writer.writerow([])

        # Dados por turma
        for turma_data in dados["dados_por_turma"].values():
            turma = turma_data["turma"]
            stats = turma_data["estatisticas"]

            writer.writerow([f"TURMA: {turma.nome}"])
            writer.writerow(["Total de Alunos", stats["total_alunos"]])
            writer.writerow(["Total de Presenças", stats["total_presencas"]])
            writer.writerow(["Total de Faltas", stats["total_faltas"]])
            writer.writerow(["Percentual Médio", f"{stats['percentual_medio']:.2f}%"])
            writer.writerow([])

            # Dados detalhados da turma
            writer.writerow(
                ["Aluno", "Atividade", "Data", "Presenças", "Faltas", "Percentual"]
            )

            for presenca in turma_data["presencas"]:
                writer.writerow(
                    [
                        presenca.aluno.nome,
                        presenca.atividade.nome,
                        presenca.atividade.data.strftime("%d/%m/%Y"),
                        presenca.presencas,
                        presenca.faltas,
                        f"{float(presenca.percentual_presenca):.2f}%",
                    ]
                )

            writer.writerow([])
            writer.writerow(["-" * 50])
            writer.writerow([])

        return response


class PDFExporter:
    """
    Classe para exportação em formato PDF.
    """

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()

    def _configurar_estilos(self):
        """Configura estilos personalizados para PDF."""

        # Estilo de título
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Title"],
                fontSize=18,
                spaceAfter=30,
                alignment=1,  # Center
                textColor=colors.darkblue,
            )
        )

        # Estilo de subtítulo
        self.styles.add(
            ParagraphStyle(
                name="CustomSubtitle",
                parent=self.styles["Heading2"],
                fontSize=14,
                spaceAfter=12,
                textColor=colors.darkblue,
            )
        )

        # Estilo de texto normal
        self.styles.add(
            ParagraphStyle(
                name="CustomNormal",
                parent=self.styles["Normal"],
                fontSize=10,
                spaceAfter=6,
            )
        )

    def gerar_pdf_consolidado(
        self, dados: Dict[str, Any], config: Dict[str, Any]
    ) -> HttpResponse:
        """Gera PDF do relatório consolidado."""

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Elementos do documento
        story = []

        # Título
        titulo = config.get(
            "titulo_personalizado", "Relatório Consolidado de Presenças"
        )
        story.append(Paragraph(titulo, self.styles["CustomTitle"]))
        story.append(Spacer(1, 12))

        # Informações do relatório
        info_texto = (
            f"<b>Gerado em:</b> {datetime.now().strftime('%d/%m/%Y às %H:%M')}<br/>"
        )

        filtros = dados["filtros_aplicados"]
        if filtros:
            info_texto += "<b>Filtros aplicados:</b><br/>"
            for chave, valor in filtros.items():
                if valor:
                    info_texto += f"• {chave}: {valor}<br/>"

        story.append(Paragraph(info_texto, self.styles["CustomNormal"]))
        story.append(Spacer(1, 20))

        # Estatísticas gerais
        self._adicionar_estatisticas_pdf(story, dados["estatisticas"])

        # Tabela de dados consolidados
        if config.get("incluir_dados_detalhados", True):
            self._adicionar_tabela_consolidado_pdf(story, dados)

        # Gráficos (se solicitados)
        if config.get("incluir_graficos"):
            self._adicionar_graficos_pdf(story, dados)

        # Gerar PDF
        doc.build(story)
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = (
            'attachment; filename="consolidado_presencas.pdf"'
        )

        return response

    def _adicionar_estatisticas_pdf(self, story: List, stats: Dict[str, Any]):
        """Adiciona seção de estatísticas ao PDF."""

        story.append(Paragraph("Estatísticas Gerais", self.styles["CustomSubtitle"]))

        # Dados da tabela de estatísticas
        data = [
            ["Estatística", "Valor"],
            ["Total de Alunos", str(stats["total_alunos"])],
            ["Total de Atividades", str(stats["total_atividades"])],
            ["Total de Presenças", str(stats["total_presencas"])],
            ["Total de Faltas", str(stats["total_faltas"])],
            ["Percentual Médio", f"{stats['percentual_medio']:.2f}%"],
            ["Total de Voluntários", str(stats.get("voluntarios_total", 0))],
        ]

        # Criar tabela
        table = RLTable(data)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 10),
                ]
            )
        )

        story.append(table)
        story.append(Spacer(1, 20))

    def _adicionar_tabela_consolidado_pdf(self, story: List, dados: Dict[str, Any]):
        """Adiciona tabela de dados consolidados ao PDF."""

        story.append(
            Paragraph("Dados Consolidados por Aluno", self.styles["CustomSubtitle"])
        )

        # Preparar dados da tabela (versão simplificada para PDF)
        excel_exporter = ExcelAvancadoExporter()
        dados_por_aluno = excel_exporter._agrupar_dados_por_aluno(
            dados["presencas_detalhadas"], dados["atividades"]
        )

        # Cabeçalhos simplificados
        data = [
            ["Aluno", "Turma", "Total Conv.", "Total Pres.", "Total Faltas", "% Médio"]
        ]

        # Dados dos alunos
        for aluno_dados in dados_por_aluno.values():
            totais = aluno_dados["totais"]
            perc_medio = (
                totais["presencas"] / totais["convocacoes"] * 100
                if totais["convocacoes"] > 0
                else 0
            )

            data.append(
                [
                    aluno_dados["aluno"].nome[:20],  # Limitar nome para PDF
                    aluno_dados["turma"].nome[:15],
                    str(totais["convocacoes"]),
                    str(totais["presencas"]),
                    str(totais["faltas"]),
                    f"{perc_medio:.1f}%",
                ]
            )

        # Criar tabela
        table = RLTable(data)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 8),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.lightgrey],
                    ),
                ]
            )
        )

        story.append(table)
        story.append(Spacer(1, 20))

    def _adicionar_graficos_pdf(self, story: List, dados: Dict[str, Any]):
        """Adiciona gráficos ao PDF."""

        story.append(Paragraph("Análise Gráfica", self.styles["CustomSubtitle"]))

        stats = dados["estatisticas"]

        # Gráfico de barras - Presenças vs Faltas
        drawing = Drawing(400, 200)

        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300

        chart.data = [[stats["total_presencas"], stats["total_faltas"]]]
        chart.categoryAxis.categoryNames = ["Presenças", "Faltas"]
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = (
            max(stats["total_presencas"], stats["total_faltas"]) * 1.1
        )

        chart.bars[0].fillColor = colors.green
        chart.bars[1].fillColor = colors.red

        drawing.add(chart)
        story.append(drawing)
        story.append(Spacer(1, 20))

        # Gráfico de pizza - Distribuição percentual
        pie_drawing = Drawing(400, 200)

        pie = Pie()
        pie.x = 150
        pie.y = 50
        pie.width = 100
        pie.height = 100

        total_conv = stats["total_presencas"] + stats["total_faltas"]
        if total_conv > 0:
            pie.data = [stats["total_presencas"], stats["total_faltas"]]
            pie.labels = ["Presenças", "Faltas"]
            pie.slices[0].fillColor = colors.green
            pie.slices[1].fillColor = colors.red

        pie_drawing.add(pie)
        story.append(pie_drawing)


class AgendadorRelatorios:
    """
    Classe para agendamento de relatórios automáticos.
    """

    @shared_task
    def processar_relatorio_agendado(agendamento_id: int):
        """Task do Celery para processar relatório agendado."""

        try:
            from ..models import AgendamentoRelatorio

            agendamento = AgendamentoRelatorio.objects.get(id=agendamento_id)

            # Configurar parâmetros
            config = {
                "formato": agendamento.formato,
                "template": agendamento.template,
                "periodo": agendamento.periodo,
                "data_inicio": agendamento.data_inicio,
                "data_fim": agendamento.data_fim,
                "turma_id": agendamento.turma_id,
                "curso": agendamento.curso,
                "incluir_graficos": agendamento.incluir_graficos,
                "incluir_estatisticas": agendamento.incluir_estatisticas,
                "titulo_personalizado": agendamento.titulo_personalizado,
            }

            # Processar exportação
            processor = ProcessarExportacaoView()
            dados = processor._obter_dados(agendamento.template, config)

            # Gerar arquivo
            arquivo_temp = None

            if agendamento.formato.startswith("excel"):
                exporter = ExcelAvancadoExporter()
                response = exporter.gerar_excel_consolidado_geral(dados, config)
                arquivo_temp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)

            elif agendamento.formato == "csv":
                exporter = CSVExporter()
                response = exporter.gerar_csv_consolidado(dados, config)
                arquivo_temp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)

            elif agendamento.formato.startswith("pdf"):
                exporter = PDFExporter()
                response = exporter.gerar_pdf_consolidado(dados, config)
                arquivo_temp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)

            if arquivo_temp:
                arquivo_temp.write(response.content)
                arquivo_temp.close()

                # Enviar por email
                AgendadorRelatorios._enviar_email_relatorio(
                    agendamento, arquivo_temp.name
                )

                # Limpar arquivo temporário
                os.unlink(arquivo_temp.name)

            # Atualizar última execução
            agendamento.ultima_execucao = timezone.now()
            agendamento.save()

            logger.info(f"Relatório agendado {agendamento_id} processado com sucesso")

        except Exception as e:
            logger.error(
                f"Erro ao processar relatório agendado {agendamento_id}: {str(e)}"
            )
            raise

    @staticmethod
    def _enviar_email_relatorio(agendamento, arquivo_path: str):
        """Envia relatório por email."""

        try:
            # Preparar email
            assunto = f"Relatório Automático - {agendamento.nome}"

            corpo = f"""
            Relatório gerado automaticamente.
            
            Nome: {agendamento.nome}
            Template: {agendamento.get_template_display()}
            Formato: {agendamento.get_formato_display()}
            Data de geração: {timezone.now().strftime("%d/%m/%Y %H:%M")}
            
            Atenciosamente,
            Sistema de Presenças OMAUM
            """

            # Criar email
            email = EmailMessage(
                subject=assunto,
                body=corpo,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=agendamento.emails_destino.split(","),
            )

            # Anexar arquivo
            with open(arquivo_path, "rb") as arquivo:
                nome_arquivo = f"relatorio_{agendamento.nome}_{timezone.now().strftime('%Y%m%d_%H%M')}"
                if arquivo_path.endswith(".xlsx"):
                    nome_arquivo += ".xlsx"
                elif arquivo_path.endswith(".csv"):
                    nome_arquivo += ".csv"
                elif arquivo_path.endswith(".pdf"):
                    nome_arquivo += ".pdf"

                email.attach(nome_arquivo, arquivo.read())

            # Enviar
            email.send()

            logger.info(f"Email enviado para: {agendamento.emails_destino}")

        except Exception as e:
            logger.error(f"Erro ao enviar email: {str(e)}")
            raise


class GerenciarAgendamentosView(LoginRequiredMixin, TemplateView):
    """
    View para gerenciar agendamentos de relatórios.
    """

    template_name = "presencas/exportacao/gerenciar_agendamentos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from ..models import AgendamentoRelatorio

        context["agendamentos"] = AgendamentoRelatorio.objects.filter(
            usuario=self.request.user, ativo=True
        ).order_by("-criado_em")

        return context


# Completar implementação da exportação avançada
class ProcessarExportacaoView(ProcessarExportacaoView):
    """
    Extensão da classe ProcessarExportacaoView com métodos de geração.
    """

    def _gerar_excel(
        self, formato: str, template: str, dados: Dict[str, Any], config: Dict[str, Any]
    ):
        """Gera arquivo Excel conforme formato solicitado."""

        exporter = ExcelAvancadoExporter()

        if formato == "excel_basico":
            # Versão básica sem formatação avançada
            config["formatacao_profissional"] = False
            config["incluir_graficos"] = False
            config["multiplas_abas"] = False

        elif formato == "excel_avancado":
            # Versão com formatação profissional
            config["formatacao_profissional"] = True
            config["multiplas_abas"] = True

        elif formato == "excel_graficos":
            # Versão com gráficos embarcados
            config["formatacao_profissional"] = True
            config["incluir_graficos"] = True
            config["multiplas_abas"] = True

        if template == "consolidado_geral":
            return exporter.gerar_excel_consolidado_geral(dados, config)
        elif template == "por_turma":
            return exporter.gerar_excel_por_turma(dados, config)
        elif template == "estatisticas_executivas":
            return exporter.gerar_excel_estatisticas_executivas(dados, config)
        else:
            return {"erro": f"Template Excel não implementado: {template}"}

    def _gerar_csv(self, template: str, dados: Dict[str, Any], config: Dict[str, Any]):
        """Gera arquivo CSV conforme template."""

        exporter = CSVExporter()

        if template == "consolidado_geral":
            return exporter.gerar_csv_consolidado(dados, config)
        elif template == "por_turma":
            return exporter.gerar_csv_por_turma(dados, config)
        else:
            return {"erro": f"Template CSV não implementado: {template}"}

    def _gerar_pdf(
        self, formato: str, template: str, dados: Dict[str, Any], config: Dict[str, Any]
    ):
        """Gera arquivo PDF conforme formato e template."""

        exporter = PDFExporter()

        if formato == "pdf_simples":
            config["incluir_graficos"] = False
            config["incluir_dados_detalhados"] = False

        elif formato == "pdf_completo":
            config["incluir_graficos"] = True
            config["incluir_dados_detalhados"] = True

        if template in ["consolidado_geral", "por_turma", "estatisticas_executivas"]:
            return exporter.gerar_pdf_consolidado(dados, config)
        else:
            return {"erro": f"Template PDF não implementado: {template}"}
