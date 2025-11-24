"""Views relacionadas a relatórios e exportação de dados de Alunos."""

import csv
import json
from datetime import datetime, date, timedelta
from io import BytesIO

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.utils import timezone
from django.utils.encoding import smart_str
from django.views.decorators.http import require_http_methods

# Importação corrigida para buscar modelos de seus respectivos apps
from alunos.models import Aluno, RegistroHistorico, Codigo
from turmas.models import Turma
from cursos.models import Curso
from alunos.services import listar_alunos_para_relatorio

NOME_ORGANIZACAO_PADRAO = "OMAUM - Ordem Mística de Aspiração Universal ao Mestrado"
NOME_SISTEMA_PADRAO = "Sistema de Gestão Integrada"


def _cabecalho_relatorio(titulo: str) -> dict:
    """Retorna o cabeçalho padrão para os relatórios do app Alunos."""

    return {
        "titulo": titulo,
        "data_emissao": timezone.now().strftime("%d/%m/%Y %H:%M"),
        "nome_organizacao": NOME_ORGANIZACAO_PADRAO,
        "nome_sistema": NOME_SISTEMA_PADRAO,
    }


try:
    import xlwt
except ImportError:  # pragma: no cover - dependência opcional
    xlwt = None


@login_required
def painel(request):
    """Renderiza o template base do painel de alunos."""
    return render(request, "alunos/painel.html")


@login_required
def relatorio_ficha_cadastral(request):
    """
    Gera e exibe o relatório de Ficha Cadastral de Alunos, com filtros e opções de exportação.
    """
    # Captura de filtros
    filtros = {
        "aluno_id": request.GET.get("aluno"),
        "turma_id": request.GET.get("turma"),
        "curso_id": request.GET.get("curso"),
        "situacao": request.GET.get("situacao"),
    }
    alunos = listar_alunos_para_relatorio(**filtros)

    # Captura de formato de exportação
    formato_export = request.GET.get("export")

    if formato_export:
        # Lógica de Exportação
        if formato_export == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                'attachment; filename="ficha_cadastral_alunos.csv"'
            )
            writer = csv.writer(response)
            writer.writerow(["Nome", "CPF", "Data Nasc.", "Email", "Situação"])
            for aluno in alunos:
                writer.writerow(
                    [
                        aluno.nome,
                        aluno.cpf,
                        aluno.data_nascimento,
                        aluno.email,
                        aluno.get_situacao_display(),
                    ]
                )
            return response

        elif formato_export == "excel":
            df = pd.DataFrame(
                list(
                    alunos.values("nome", "cpf", "data_nascimento", "email", "situacao")
                )
            )
            df["situacao"] = df["situacao"].apply(
                lambda x: dict(Aluno.SITUACAO_CHOICES).get(x, x)
            )

            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Ficha Cadastral")
            output.seek(0)

            response = HttpResponse(
                output,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = (
                'attachment; filename="ficha_cadastral_alunos.xlsx"'
            )
            return response

        elif formato_export == "pdf":
            from weasyprint import HTML

            template = get_template("alunos/relatorio_ficha_cadastral_pdf.html")
            contexto_pdf = {
                **_cabecalho_relatorio("Relatório de Ficha Cadastral"),
                "alunos": alunos,
            }
            html_string = template.render(contexto_pdf, request)
            pdf_file = HTML(
                string=html_string, base_url=request.build_absolute_uri()
            ).write_pdf()
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = (
                'attachment; filename="ficha_cadastral_alunos.pdf"'
            )
            return response

    # Renderização HTML padrão
    context = {
        **_cabecalho_relatorio("Relatório de Ficha Cadastral"),
        "alunos": alunos,
        "filtros": filtros,
        "todos_alunos": Aluno.objects.all().order_by("nome"),
        "turmas": Turma.objects.all().order_by("nome"),
        "cursos": Curso.objects.all().order_by("nome"),
        "situacoes": Aluno.SITUACAO_CHOICES,
    }
    return render(request, "alunos/relatorio_ficha_cadastral.html", context)


@login_required
@require_http_methods(["GET"])
def relatorio_dados_iniciaticos(request):
    """Exibe o relatório de dados iniciáticos com filtros e exportações CSV/XLS."""

    grau = request.GET.get("grau", "").strip()
    situacao = request.GET.get("situacao", "").strip()
    tempo_casa = request.GET.get("tempo_casa", "").strip()
    export = request.GET.get("export", "").strip()

    alunos_qs = Aluno.objects.all()
    if grau:
        alunos_qs = alunos_qs.filter(grau_atual=grau)
    if situacao:
        alunos_qs = alunos_qs.filter(situacao=situacao)
    if tempo_casa:
        try:
            anos = int(tempo_casa)
            data_limite = date.today() - timedelta(days=anos * 365)
            alunos_qs = alunos_qs.filter(created_at__lte=data_limite)
        except (TypeError, ValueError):
            pass

    alunos_qs = alunos_qs.order_by("nome")

    if export in ["csv", "xls", "pdf"]:
        if export == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                'attachment; filename="dados_iniciaticos.csv"'
            )
            writer = csv.writer(response)
            writer.writerow(
                [
                    "Nome",
                    "CPF",
                    "Grau Atual",
                    "Situação",
                    "Tempo de Casa (anos)",
                    "Data Ingresso",
                ]
            )
            for aluno in alunos_qs:
                tempo = (
                    (date.today() - aluno.created_at.date()).days // 365
                    if aluno.created_at
                    else "-"
                )
                writer.writerow(
                    [
                        smart_str(aluno.nome),
                        smart_str(aluno.cpf),
                        smart_str(getattr(aluno, "grau_atual", "-")),
                        dict(Aluno.SITUACAO_CHOICES).get(aluno.situacao, "-"),
                        tempo,
                        aluno.created_at.date() if aluno.created_at else "-",
                    ]
                )
            return response

        if export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("Dados Iniciáticos")
            headers = [
                "Nome",
                "CPF",
                "Grau Atual",
                "Situação",
                "Tempo de Casa (anos)",
                "Data Ingresso",
            ]
            for col, header in enumerate(headers):
                sheet.write(0, col, header)
            for row, aluno in enumerate(alunos_qs, start=1):
                tempo = (
                    (date.today() - aluno.created_at.date()).days // 365
                    if aluno.created_at
                    else "-"
                )
                sheet.write(row, 0, smart_str(aluno.nome))
                sheet.write(row, 1, smart_str(aluno.cpf))
                sheet.write(row, 2, smart_str(getattr(aluno, "grau_atual", "-")))
                sheet.write(
                    row,
                    3,
                    dict(Aluno.SITUACAO_CHOICES).get(aluno.situacao, "-"),
                )
                sheet.write(row, 4, tempo)
                sheet.write(
                    row,
                    5,
                    smart_str(aluno.created_at.date() if aluno.created_at else "-"),
                )
            output = BytesIO()
            workbook.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = (
                'attachment; filename="dados_iniciaticos.xls"'
            )
            return response

        if export == "pdf":
            from weasyprint import HTML

            template = get_template("alunos/relatorio_dados_iniciaticos_pdf.html")
            contexto_pdf = {
                **_cabecalho_relatorio("Relatório de Dados Iniciáticos"),
                "alunos": alunos_qs,
            }
            html_string = template.render(contexto_pdf, request)
            pdf_file = HTML(
                string=html_string, base_url=request.build_absolute_uri()
            ).write_pdf()
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = (
                'attachment; filename="dados_iniciaticos.pdf"'
            )
            return response

    graus = (
        Aluno.objects.values_list("grau_atual", flat=True)
        .distinct()
        .order_by("grau_atual")
    )

    context = {
        **_cabecalho_relatorio("Relatório de Dados Iniciáticos"),
        "alunos": alunos_qs,
        "graus": graus,
        "situacoes": Aluno.SITUACAO_CHOICES,
        "filtros": {"grau": grau, "situacao": situacao, "tempo_casa": tempo_casa},
    }
    return render(request, "alunos/relatorio_dados_iniciaticos.html", context)


@login_required
@require_http_methods(["GET"])
def relatorio_historico_aluno(request):
    """Lista eventos do histórico iniciático com filtros e exportações."""

    aluno_id = request.GET.get("aluno", "").strip()
    tipo_evento = request.GET.get("tipo_evento", "").strip()
    data_ini = request.GET.get("data_ini", "").strip()
    data_fim = request.GET.get("data_fim", "").strip()
    export = request.GET.get("export", "").strip()

    historico_qs = (
        RegistroHistorico.objects.select_related("aluno", "codigo")
        .all()
        .order_by("-data_os")
    )

    if aluno_id:
        historico_qs = historico_qs.filter(aluno_id=aluno_id)
    if tipo_evento:
        historico_qs = historico_qs.filter(codigo_id=tipo_evento)
    if data_ini:
        historico_qs = historico_qs.filter(data_os__gte=data_ini)
    if data_fim:
        historico_qs = historico_qs.filter(data_os__lte=data_fim)

    if export in ["csv", "xls", "pdf"]:
        if export == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                'attachment; filename="historico_aluno.csv"'
            )
            writer = csv.writer(response)
            writer.writerow(
                [
                    "Aluno",
                    "CPF",
                    "Evento",
                    "Data",
                    "Ordem de Serviço",
                    "Observações",
                ]
            )
            for registro in historico_qs:
                writer.writerow(
                    [
                        smart_str(registro.aluno.nome),
                        smart_str(registro.aluno.cpf),
                        smart_str(registro.codigo.nome),
                        registro.data_os,
                        registro.ordem_servico or "-",
                        registro.observacoes or "-",
                    ]
                )
            return response

        if export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("Histórico do Aluno")
            headers = [
                "Aluno",
                "CPF",
                "Evento",
                "Data",
                "Ordem de Serviço",
                "Observações",
            ]
            for col, header in enumerate(headers):
                sheet.write(0, col, header)
            for row, registro in enumerate(historico_qs, start=1):
                sheet.write(row, 0, smart_str(registro.aluno.nome))
                sheet.write(row, 1, smart_str(registro.aluno.cpf))
                sheet.write(row, 2, smart_str(registro.codigo.nome))
                sheet.write(row, 3, smart_str(registro.data_os))
                sheet.write(row, 4, smart_str(registro.ordem_servico or "-"))
                sheet.write(row, 5, smart_str(registro.observacoes or "-"))
            output = BytesIO()
            workbook.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = (
                'attachment; filename="historico_aluno.xls"'
            )
            return response

        if export == "pdf":
            from weasyprint import (
                HTML,
            )  # import local para evitar dependência obrigatória

            template = get_template("alunos/relatorio_historico_aluno.html")
            html_string = template.render(
                {
                    **_cabecalho_relatorio("Relatório de Histórico do Aluno"),
                    "historico": historico_qs,
                    "alunos": Aluno.objects.all(),
                    "tipos_evento": Codigo.objects.all(),
                    "filtros": {
                        "aluno": aluno_id,
                        "tipo_evento": tipo_evento,
                        "data_ini": data_ini,
                        "data_fim": data_fim,
                    },
                    "is_export_pdf": True,
                }
            )
            pdf_file = HTML(
                string=html_string, base_url=request.build_absolute_uri()
            ).write_pdf()
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = (
                'attachment; filename="historico_aluno.pdf"'
            )
            return response

    context = {
        **_cabecalho_relatorio("Relatório de Histórico do Aluno"),
        "historico": historico_qs,
        "alunos": Aluno.objects.all().order_by("nome"),
        "tipos_evento": Codigo.objects.all().order_by("nome"),
        "filtros": {
            "aluno": aluno_id,
            "tipo_evento": tipo_evento,
            "data_ini": data_ini,
            "data_fim": data_fim,
        },
    }
    return render(request, "alunos/relatorio_historico_aluno.html", context)


@login_required
@require_http_methods(["GET"])
def relatorio_auditoria_dados(request):
    """Realiza auditoria de campos obrigatórios, com exportação CSV/XLS."""

    campos = request.GET.getlist("campo")
    export = request.GET.get("export", "").strip()

    auditaveis = {
        "email": "E-mail",
        "celular_primeiro_contato": "Celular 1º Contato",
        "rua": "Rua",
        "numero_imovel": "Número",
        "bairro_ref": "Bairro",
        "cidade_ref": "Cidade",
        "cep": "CEP",
        "nome_primeiro_contato": "Nome 1º Contato",
    }

    alunos_qs = Aluno.objects.all()
    faltando = []

    texto_fields = (
        models.CharField,
        models.TextField,
        models.EmailField,
        models.SlugField,
        models.URLField,
    )

    for campo in campos:
        if campo not in auditaveis:
            continue

        try:
            campo_model = Aluno._meta.get_field(campo)
        except Exception:
            campo_model = None

        filtros_q = Q(**{f"{campo}__isnull": True})

        if campo_model and isinstance(campo_model, texto_fields):
            filtros_q |= Q(**{f"{campo}__exact": ""})

        alunos_qs = alunos_qs.filter(filtros_q)
        faltando.append(auditaveis[campo])

    alunos_qs = alunos_qs.distinct().order_by("nome")
    alunos_list = list(alunos_qs)

    auditoria_resultados = []
    for aluno in alunos_list:
        faltantes_campos = []
        valores_campos = {}
        for campo in campos:
            valor = getattr(aluno, campo, None)
            valores_campos[campo] = valor
            if not valor:
                faltantes_campos.append(auditaveis.get(campo, campo))
        auditoria_resultados.append(
            {"aluno": aluno, "faltantes": faltantes_campos, "valores": valores_campos}
        )

    if export in ["csv", "xls", "pdf"]:
        if export == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                'attachment; filename="auditoria_dados.csv"'
            )
            writer = csv.writer(response)
            writer.writerow(["Nome", "CPF"] + faltando)
            for aluno in alunos_qs:
                row = [aluno.nome, aluno.cpf]
                for campo in campos:
                    row.append(getattr(aluno, campo, "-"))
                writer.writerow(row)
            return response

        if export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("Auditoria de Dados")
            headers = ["Nome", "CPF"] + faltando
            for col, header in enumerate(headers):
                sheet.write(0, col, header)
            for row_idx, aluno in enumerate(alunos_qs, start=1):
                sheet.write(row_idx, 0, smart_str(aluno.nome))
                sheet.write(row_idx, 1, smart_str(aluno.cpf))
                for col_idx, campo in enumerate(campos, start=2):
                    sheet.write(
                        row_idx,
                        col_idx,
                        smart_str(getattr(aluno, campo, "-")),
                    )
            output = BytesIO()
            workbook.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = (
                'attachment; filename="auditoria_dados.xls"'
            )
            return response

        if export == "pdf":
            from weasyprint import HTML

            template = get_template("alunos/relatorio_auditoria_dados_pdf.html")
            contexto_pdf = {
                **_cabecalho_relatorio("Relatório de Auditoria de Dados"),
                "resultados": auditoria_resultados,
                "campos_selecionados": [
                    auditaveis.get(campo, campo) for campo in campos
                ],
                "auditaveis": auditaveis,
                "campos_filtros": campos,
            }
            html_string = template.render(contexto_pdf, request)
            pdf_file = HTML(
                string=html_string, base_url=request.build_absolute_uri()
            ).write_pdf()
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = (
                'attachment; filename="auditoria_dados.pdf"'
            )
            return response

    context = {
        **_cabecalho_relatorio("Relatório de Auditoria de Dados"),
        "alunos": alunos_list,
        "auditaveis": auditaveis,
        "campos_filtros": campos,
        "auditoria_resultados": auditoria_resultados,
    }
    return render(request, "alunos/relatorio_auditoria_dados.html", context)


@login_required
@require_http_methods(["GET"])
def relatorio_demografico(request):
    """Apresenta distribuição demográfica com filtros e estatísticas."""

    faixa = request.GET.get("faixa", "").strip()
    cidade = request.GET.get("cidade", "").strip()
    sexo = request.GET.get("sexo", "").strip()
    export = request.GET.get("export", "").strip()

    faixas = [
        ("<18", "Menores de 18"),
        ("18-25", "18 a 25"),
        ("26-35", "26 a 35"),
        ("36-45", "36 a 45"),
        ("46-60", "46 a 60"),
        (">60", "Acima de 60"),
    ]

    alunos_qs = Aluno.objects.all()

    if cidade:
        alunos_qs = alunos_qs.filter(cidade_ref_id=cidade)
    if sexo:
        alunos_qs = alunos_qs.filter(sexo=sexo)
    if faixa:
        hoje = date.today()
        if faixa == "<18":
            data_limite = hoje - timedelta(days=18 * 365)
            alunos_qs = alunos_qs.filter(data_nascimento__gt=data_limite)
        elif faixa == ">60":
            data_limite = hoje - timedelta(days=60 * 365)
            alunos_qs = alunos_qs.filter(data_nascimento__lte=data_limite)
        else:
            inicio, fim = faixa.split("-")
            data_fim = hoje - timedelta(days=int(inicio) * 365)
            data_inicio = hoje - timedelta(days=(int(fim) + 1) * 365)
            alunos_qs = alunos_qs.filter(
                data_nascimento__lte=data_fim, data_nascimento__gt=data_inicio
            )

    alunos_qs = alunos_qs.order_by("nome")

    if export in ["csv", "xls"]:
        if export == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="demografico.csv"'
            writer = csv.writer(response)
            writer.writerow(["Nome", "CPF", "Sexo", "Data Nasc.", "Cidade"])
            for aluno in alunos_qs:
                writer.writerow(
                    [
                        smart_str(aluno.nome),
                        smart_str(aluno.cpf),
                        dict(Aluno.SEXO_CHOICES).get(aluno.sexo, "-"),
                        aluno.data_nascimento,
                        smart_str(aluno.cidade_ref.nome if aluno.cidade_ref else "-"),
                    ]
                )
            return response

        if export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet("Demográfico")
            headers = ["Nome", "CPF", "Sexo", "Data Nasc.", "Cidade"]
            for col, header in enumerate(headers):
                sheet.write(0, col, header)
            for row, aluno in enumerate(alunos_qs, start=1):
                sheet.write(row, 0, smart_str(aluno.nome))
                sheet.write(row, 1, smart_str(aluno.cpf))
                sheet.write(
                    row,
                    2,
                    dict(Aluno.SEXO_CHOICES).get(aluno.sexo, "-"),
                )
                sheet.write(row, 3, smart_str(aluno.data_nascimento))
                sheet.write(
                    row,
                    4,
                    smart_str(aluno.cidade_ref.nome if aluno.cidade_ref else "-"),
                )
            output = BytesIO()
            workbook.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = 'attachment; filename="demografico.xls"'
            return response

    hoje = date.today()
    faixa_counts = {codigo: 0 for codigo, _ in faixas}
    for aluno in alunos_qs:
        if not aluno.data_nascimento:
            continue
        idade = (hoje - aluno.data_nascimento).days // 365
        if idade < 18:
            faixa_counts["<18"] += 1
        elif idade <= 25:
            faixa_counts["18-25"] += 1
        elif idade <= 35:
            faixa_counts["26-35"] += 1
        elif idade <= 45:
            faixa_counts["36-45"] += 1
        elif idade <= 60:
            faixa_counts["46-60"] += 1
        else:
            faixa_counts[">60"] += 1

    sexo_data = list(
        alunos_qs.values("sexo").annotate(qtd=Count("id")).order_by("sexo")
    )
    cidades = list(
        Aluno.objects.exclude(cidade_ref=None)
        .values_list("cidade_ref__id", "cidade_ref__nome")
        .distinct()
        .order_by("cidade_ref__nome")
    )

    context = {
        **_cabecalho_relatorio("Relatório Demográfico"),
        "alunos": alunos_qs,
        "faixas": faixas,
        "cidades": cidades,
        "sexo_choices": Aluno.SEXO_CHOICES,
        "filtros": {"faixa": faixa, "cidade": cidade, "sexo": sexo},
        "sexo_data": json.dumps(sexo_data),
        "faixa_counts": json.dumps(faixa_counts),
    }
    return render(request, "alunos/relatorio_demografico.html", context)


@login_required
@require_http_methods(["GET"])
def relatorio_aniversariantes(request):
    """Lista aniversariantes do mês com suporte a exportação CSV/XLS/PDF."""

    mes = request.GET.get("mes", "").strip()
    export = request.GET.get("export", "").strip()

    alunos_qs = Aluno.objects.all()
    if mes:
        try:
            mes_int = int(mes)
            alunos_qs = alunos_qs.filter(data_nascimento__month=mes_int)
        except (TypeError, ValueError):
            pass

    alunos_qs = alunos_qs.order_by("data_nascimento__day", "nome")

    if export in ["csv", "xls", "pdf"]:
        agora = datetime.now()
        header_org = "OM-AUM (Ordem Mística de Aspiração Universal ao Mestrado)"
        header_data = f"Emitido em: {agora.strftime('%d/%m/%Y às %H:%M')}"
        headers = ["Nome", "CPF", "Data Nasc.", "Email", "Telefone"]

        if export == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                'attachment; filename="aniversariantes.csv"'
            )
            writer = csv.writer(response)
            writer.writerow([header_org])
            writer.writerow([header_data])
            writer.writerow([])
            writer.writerow(headers)
            for aluno in alunos_qs:
                writer.writerow(
                    [
                        smart_str(aluno.nome),
                        smart_str(aluno.cpf),
                        aluno.data_nascimento,
                        smart_str(aluno.email),
                        smart_str(aluno.celular_primeiro_contato or "-"),
                    ]
                )
            return response

        if export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            workbook = xlwt.Workbook(encoding="utf-8")
            sheet = workbook.add_sheet("Aniversariantes")
            sheet.write(0, 0, header_org)
            sheet.write(1, 0, header_data)
            for col, header in enumerate(headers):
                sheet.write(3, col, header)
            for row_idx, aluno in enumerate(alunos_qs, start=4):
                sheet.write(row_idx, 0, smart_str(aluno.nome))
                sheet.write(row_idx, 1, smart_str(aluno.cpf))
                sheet.write(row_idx, 2, aluno.data_nascimento)
                sheet.write(row_idx, 3, smart_str(aluno.email))
                sheet.write(
                    row_idx,
                    4,
                    smart_str(aluno.celular_primeiro_contato or "-"),
                )
            output = BytesIO()
            workbook.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = (
                'attachment; filename="aniversariantes.xls"'
            )
            return response

        if export == "pdf":
            from weasyprint import HTML  # import local para dependência opcional

            template = get_template("alunos/relatorio_aniversariantes_pdf.html")
            html_string = template.render(
                {
                    **_cabecalho_relatorio("Relatório de Aniversariantes"),
                    "alunos": alunos_qs,
                },
                request,
            )
            pdf_file = HTML(
                string=html_string, base_url=request.build_absolute_uri()
            ).write_pdf()
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = (
                'attachment; filename="aniversariantes.pdf"'
            )
            return response

    meses = [
        ("1", "Janeiro"),
        ("2", "Fevereiro"),
        ("3", "Março"),
        ("4", "Abril"),
        ("5", "Maio"),
        ("6", "Junho"),
        ("7", "Julho"),
        ("8", "Agosto"),
        ("9", "Setembro"),
        ("10", "Outubro"),
        ("11", "Novembro"),
        ("12", "Dezembro"),
    ]

    context = {
        **_cabecalho_relatorio("Relatório de Aniversariantes"),
        "alunos": alunos_qs,
        "meses": meses,
        "mes_filtro": mes,
    }
    return render(request, "alunos/relatorio_aniversariantes.html", context)
