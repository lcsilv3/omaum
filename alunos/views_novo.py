from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET


# --- Relatório de Aniversariantes ---
@login_required
@require_http_methods(["GET"])
def relatorio_aniversariantes(request):
    mes = request.GET.get("mes", "").strip()
    export = request.GET.get("export", "").strip()

    alunos_qs = Aluno.objects.all()
    if mes:
        try:
            mes_int = int(mes)
            alunos_qs = alunos_qs.filter(data_nascimento__month=mes_int)
        except Exception:
            pass
    alunos_qs = alunos_qs.order_by("data_nascimento", "nome")

    # Exportação CSV/Excel
    if export in ["csv", "xls"]:
        if export == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                'attachment; filename="aniversariantes.csv"'
            )
            writer = csv.writer(response)
            writer.writerow(["Nome", "CPF", "Data Nasc.", "Email", "Telefone"])
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
        elif export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            wb = xlwt.Workbook()
            ws = wb.add_sheet("Aniversariantes")
            headers = ["Nome", "CPF", "Data Nasc.", "Email", "Telefone"]
            for col, h in enumerate(headers):
                ws.write(0, col, h)
            for row, aluno in enumerate(alunos_qs, start=1):
                ws.write(row, 0, smart_str(aluno.nome))
                ws.write(row, 1, smart_str(aluno.cpf))
                ws.write(row, 2, smart_str(aluno.data_nascimento))
                ws.write(row, 3, smart_str(aluno.email))
                ws.write(row, 4, smart_str(aluno.celular_primeiro_contato or "-"))
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = (
                'attachment; filename="aniversariantes.xls"'
            )
            return response

    # Espaço reservado para integração futura (ex: envio de e-mail)
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

    return render(
        request,
        "alunos/relatorio_aniversariantes.html",
        {
            "alunos": alunos_qs,
            "meses": meses,
            "mes_filtro": mes,
        },
    )


# --- Relatório Demográfico ---
from django.db.models import Count
import json


@login_required
@require_http_methods(["GET"])
def relatorio_demografico(request):
    faixa = request.GET.get("faixa", "").strip()
    cidade = request.GET.get("cidade", "").strip()
    sexo = request.GET.get("sexo", "").strip()
    export = request.GET.get("export", "").strip()

    # Faixas etárias
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
        from datetime import date, timedelta

        hoje = date.today()
        if faixa == "<18":
            data_limite = hoje - timedelta(days=18 * 365)
            alunos_qs = alunos_qs.filter(data_nascimento__gt=data_limite)
        elif faixa == ">60":
            data_limite = hoje - timedelta(days=60 * 365)
            alunos_qs = alunos_qs.filter(data_nascimento__lte=data_limite)
        else:
            ini, fim = faixa.split("-")
            data_ini = hoje - timedelta(days=int(fim) * 365)
            data_fim = hoje - timedelta(days=(int(ini) - 1) * 365)
            alunos_qs = alunos_qs.filter(
                data_nascimento__lte=data_fim, data_nascimento__gt=data_ini
            )
    alunos_qs = alunos_qs.order_by("nome")

    # Exportação CSV/Excel
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
        elif export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            wb = xlwt.Workbook()
            ws = wb.add_sheet("Demográfico")
            headers = ["Nome", "CPF", "Sexo", "Data Nasc.", "Cidade"]
            for col, h in enumerate(headers):
                ws.write(0, col, h)
            for row, aluno in enumerate(alunos_qs, start=1):
                ws.write(row, 0, smart_str(aluno.nome))
                ws.write(row, 1, smart_str(aluno.cpf))
                ws.write(row, 2, dict(Aluno.SEXO_CHOICES).get(aluno.sexo, "-"))
                ws.write(row, 3, smart_str(aluno.data_nascimento))
                ws.write(
                    row,
                    4,
                    smart_str(aluno.cidade_ref.nome if aluno.cidade_ref else "-"),
                )
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = 'attachment; filename="demografico.xls"'
            return response

    # Gráficos
    # Distribuição por sexo
    sexo_data = list(
        alunos_qs.values("sexo").annotate(qtd=Count("id")).order_by("sexo")
    )
    # Distribuição por faixa etária
    hoje = date.today()
    faixa_counts = {k: 0 for k, _ in faixas}
    for aluno in alunos_qs:
        idade = (
            (hoje - aluno.data_nascimento).days // 365 if aluno.data_nascimento else 0
        )
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

    cidades = list(
        Aluno.objects.exclude(cidade_ref=None)
        .values_list("cidade_ref__id", "cidade_ref__nome")
        .distinct()
        .order_by("cidade_ref__nome")
    )

    return render(
        request,
        "alunos/relatorio_demografico.html",
        {
            "alunos": alunos_qs,
            "faixas": faixas,
            "cidades": cidades,
            "sexo_choices": Aluno.SEXO_CHOICES,
            "filtros": {"faixa": faixa, "cidade": cidade, "sexo": sexo},
            "sexo_data": json.dumps(sexo_data),
            "faixa_counts": json.dumps(faixa_counts),
        },
    )


# --- Relatório Auditoria de Dados ---
from django.utils.encoding import smart_str

try:
    import xlwt
except ImportError:
    xlwt = None
from io import BytesIO
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET"])
def relatorio_auditoria_dados(request):
    # Filtros: campos faltantes
    campos = request.GET.getlist("campo")  # Ex: campo=telefone&campo=endereco
    export = request.GET.get("export", "").strip()

    # Campos auditáveis
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
    for campo in campos:
        if campo in auditaveis:
            filtro = {f"{campo}__isnull": True}
            alunos_qs = alunos_qs.filter(Q(**filtro) | Q(**{campo: ""}))
            faltando.append(auditaveis[campo])
    alunos_qs = alunos_qs.distinct().order_by("nome")

    # Exportação CSV/Excel
    if export in ["csv", "xls"]:
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
        elif export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            wb = xlwt.Workbook()
            ws = wb.add_sheet("Auditoria de Dados")
            headers = ["Nome", "CPF"] + faltando
            for col, h in enumerate(headers):
                ws.write(0, col, h)
            for row_idx, aluno in enumerate(alunos_qs, start=1):
                ws.write(row_idx, 0, smart_str(aluno.nome))
                ws.write(row_idx, 1, smart_str(aluno.cpf))
                for col_idx, campo in enumerate(campos, start=2):
                    ws.write(row_idx, col_idx, smart_str(getattr(aluno, campo, "-")))
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = (
                'attachment; filename="auditoria_dados.xls"'
            )
            return response

    return render(
        request,
        "alunos/relatorio_auditoria_dados.html",
        {
            "alunos": alunos_qs,
            "auditaveis": auditaveis,
            "campos_filtros": campos,
        },
    )


# --- Relatório Histórico do Aluno ---
from django.db.models import Q
from django.utils.encoding import smart_str
from alunos.models import RegistroHistorico, Codigo

try:
    import xlwt
except ImportError:
    xlwt = None
from io import BytesIO
from django.views.decorators.http import require_http_methods
from weasyprint import HTML


@login_required
@require_http_methods(["GET"])
def relatorio_historico_aluno(request):
    aluno_id = request.GET.get("aluno", "").strip()
    tipo_evento = request.GET.get("tipo_evento", "").strip()
    data_ini = request.GET.get("data_ini", "").strip()
    data_fim = request.GET.get("data_fim", "").strip()
    export = request.GET.get("export", "").strip()

    historico_qs = RegistroHistorico.objects.select_related("aluno", "codigo").all()
    if aluno_id:
        historico_qs = historico_qs.filter(aluno_id=aluno_id)
    if tipo_evento:
        historico_qs = historico_qs.filter(codigo_id=tipo_evento)
    if data_ini:
        historico_qs = historico_qs.filter(data_os__gte=data_ini)
    if data_fim:
        historico_qs = historico_qs.filter(data_os__lte=data_fim)
    historico_qs = historico_qs.order_by("-data_os")

    # Exportação CSV/Excel/PDF
    if export in ["csv", "xls", "pdf"]:
        if export == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                'attachment; filename="historico_aluno.csv"'
            )
            writer = csv.writer(response)
            writer.writerow(
                ["Aluno", "CPF", "Evento", "Data", "Ordem de Serviço", "Observações"]
            )
            for reg in historico_qs:
                writer.writerow(
                    [
                        smart_str(reg.aluno.nome),
                        smart_str(reg.aluno.cpf),
                        smart_str(reg.codigo.nome),
                        reg.data_os,
                        reg.ordem_servico or "-",
                        reg.observacoes or "-",
                    ]
                )
            return response
        elif export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            wb = xlwt.Workbook()
            ws = wb.add_sheet("Histórico do Aluno")
            headers = [
                "Aluno",
                "CPF",
                "Evento",
                "Data",
                "Ordem de Serviço",
                "Observações",
            ]
            for col, h in enumerate(headers):
                ws.write(0, col, h)
            for row, reg in enumerate(historico_qs, start=1):
                ws.write(row, 0, smart_str(reg.aluno.nome))
                ws.write(row, 1, smart_str(reg.aluno.cpf))
                ws.write(row, 2, smart_str(reg.codigo.nome))
                ws.write(row, 3, smart_str(reg.data_os))
                ws.write(row, 4, smart_str(reg.ordem_servico or "-"))
                ws.write(row, 5, smart_str(reg.observacoes or "-"))
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = (
                'attachment; filename="historico_aluno.xls"'
            )
            return response
        elif export == "pdf":
            from django.template.loader import get_template

            template = get_template("alunos/relatorio_historico_aluno.html")
            html_string = template.render(
                {
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

    alunos = Aluno.objects.all().order_by("nome")
    tipos_evento = Codigo.objects.all().order_by("nome")

    return render(
        request,
        "alunos/relatorio_historico_aluno.html",
        {
            "historico": historico_qs,
            "alunos": alunos,
            "tipos_evento": tipos_evento,
            "filtros": {
                "aluno": aluno_id,
                "tipo_evento": tipo_evento,
                "data_ini": data_ini,
                "data_fim": data_fim,
            },
        },
    )


# --- Relatório Dados Iniciáticos ---
from datetime import timedelta
from django.utils.encoding import smart_str

try:
    import xlwt
except ImportError:
    xlwt = None
from io import BytesIO
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET"])
def relatorio_dados_iniciaticos(request):
    grau = request.GET.get("grau", "").strip()
    situacao = request.GET.get("situacao", "").strip()
    tempo_casa = request.GET.get("tempo_casa", "").strip()  # em anos
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
        except Exception:
            pass
    alunos_qs = alunos_qs.order_by("nome")

    # Exportação CSV/Excel
    if export in ["csv", "xls"]:
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
        elif export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            wb = xlwt.Workbook()
            ws = wb.add_sheet("Dados Iniciaticos")
            headers = [
                "Nome",
                "CPF",
                "Grau Atual",
                "Situação",
                "Tempo de Casa (anos)",
                "Data Ingresso",
            ]
            for col, h in enumerate(headers):
                ws.write(0, col, h)
            for row, aluno in enumerate(alunos_qs, start=1):
                tempo = (
                    (date.today() - aluno.created_at.date()).days // 365
                    if aluno.created_at
                    else "-"
                )
                ws.write(row, 0, smart_str(aluno.nome))
                ws.write(row, 1, smart_str(aluno.cpf))
                ws.write(row, 2, smart_str(getattr(aluno, "grau_atual", "-")))
                ws.write(row, 3, dict(Aluno.SITUACAO_CHOICES).get(aluno.situacao, "-"))
                ws.write(row, 4, tempo)
                ws.write(
                    row,
                    5,
                    smart_str(aluno.created_at.date() if aluno.created_at else "-"),
                )
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = (
                'attachment; filename="dados_iniciaticos.xls"'
            )
            return response

    # Filtros para o template
    graus = (
        Aluno.objects.values_list("grau_atual", flat=True)
        .distinct()
        .order_by("grau_atual")
    )
    situacoes = Aluno.SITUACAO_CHOICES

    return render(
        request,
        "alunos/relatorio_dados_iniciaticos.html",
        {
            "alunos": alunos_qs,
            "graus": graus,
            "situacoes": situacoes,
            "filtros": {"grau": grau, "situacao": situacao, "tempo_casa": tempo_casa},
        },
    )


from datetime import datetime, timedelta, date
from django.db.models import Count, Q, Avg
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import logging
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from .forms import AlunoForm, RegistroHistoricoFormSet, RegistroHistoricoForm
from .models import Aluno, RegistroHistorico
from .services import listar_alunos, buscar_aluno_por_id
from django import forms

logger = logging.getLogger(__name__)


# --- API Painel de Alunos ---
@login_required
@require_GET
def painel_kpis_api(request):
    total_alunos = Aluno.objects.count()
    alunos_ativos = Aluno.objects.filter(situacao="a").count()
    media_idade = Aluno.objects.filter(situacao="a").aggregate(
        m=Avg("data_nascimento")
    )["m"]
    # Qualidade dos dados: % de alunos ativos com telefone, endereço e contato de emergência
    crit = Q(celular_primeiro_contato__isnull=False) & ~Q(celular_primeiro_contato="")
    crit &= Q(rua__isnull=False) & ~Q(rua="")
    crit &= Q(nome_primeiro_contato__isnull=False) & ~Q(nome_primeiro_contato="")
    completos = Aluno.objects.filter(situacao="a").filter(crit).count()
    total_ativos = alunos_ativos or 1
    qualidade = int((completos / total_ativos) * 100)
    if media_idade:
        hoje = datetime.now().date()
        media_idade = int((hoje - media_idade).days // 365)
    else:
        media_idade = "-"
    return JsonResponse(
        {
            "total_alunos": total_alunos,
            "alunos_ativos": alunos_ativos,
            "media_idade": media_idade,
            "qualidade_dados": qualidade,
        }
    )


@login_required
@require_GET
def painel_graficos_api(request):
    # Gráfico de situação
    situacoes = Aluno.objects.values("situacao").annotate(qtd=Count("id"))
    labels = []
    values = []
    mapa = dict(Aluno._meta.get_field("situacao").choices)
    for s in situacoes:
        labels.append(mapa.get(s["situacao"], s["situacao"]))
        values.append(s["qtd"])
    # Gráfico de novos por mês (últimos 12 meses)
    hoje = datetime.now().date()
    meses = [
        (hoje - timedelta(days=30 * i)).replace(day=1) for i in reversed(range(12))
    ]
    labels_mes = [m.strftime("%b/%Y") for m in meses]
    valores_mes = []
    for m in meses:
        prox = (m + timedelta(days=32)).replace(day=1)
        valores_mes.append(
            Aluno.objects.filter(
                created_at__date__gte=m, created_at__date__lt=prox
            ).count()
        )
    return JsonResponse(
        {
            "situacao": {"labels": labels, "values": values},
            "novos_mes": {"labels": labels_mes, "values": valores_mes},
        }
    )


@login_required
@require_GET
def painel_tabela_api(request):
    # Filtros
    nome = request.GET.get("nome", "").strip()
    cpf = request.GET.get("cpf", "").strip()
    situacao = request.GET.get("situacao", "").strip()
    export = request.GET.get("export", "").strip()
    page = int(request.GET.get("page", 1))
    alunos_qs = Aluno.objects.all()
    if nome:
        alunos_qs = alunos_qs.filter(nome__icontains=nome)
    if cpf:
        alunos_qs = alunos_qs.filter(cpf__icontains=cpf)
    if situacao:
        alunos_qs = alunos_qs.filter(situacao=situacao)
    alunos_qs = alunos_qs.order_by("-id")

    # Exportação CSV/Excel
    if export in ["csv", "xls", "pdf"]:
        import csv
        from io import StringIO, BytesIO
        from django.utils.encoding import smart_str

        response = None
        if export == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="alunos.csv"'
            writer = csv.writer(response)
            writer.writerow(["Nome", "CPF", "Email", "Situação"])
            for aluno in alunos_qs:
                writer.writerow(
                    [
                        smart_str(aluno.nome),
                        smart_str(aluno.cpf),
                        smart_str(aluno.email),
                        dict(Aluno.SITUACAO_CHOICES).get(aluno.situacao, "-"),
                    ]
                )
            return response
        elif export == "xls":
            try:
                import xlwt
            except ImportError:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            wb = xlwt.Workbook()
            ws = wb.add_sheet("Alunos")
            headers = ["Nome", "CPF", "Email", "Situação"]
            for col, h in enumerate(headers):
                ws.write(0, col, h)
            for row, aluno in enumerate(alunos_qs, start=1):
                ws.write(row, 0, smart_str(aluno.nome))
                ws.write(row, 1, smart_str(aluno.cpf))
                ws.write(row, 2, smart_str(aluno.email))
                ws.write(row, 3, dict(Aluno.SITUACAO_CHOICES).get(aluno.situacao, "-"))
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = 'attachment; filename="alunos.xls"'
            return response

    # Paginação
    paginator = Paginator(alunos_qs, 15)
    alunos_page = paginator.get_page(page)

    html = render_to_string(
        "alunos/_tabela_alunos_parcial.html", {"alunos": alunos_page}, request=request
    )
    # Renderizar paginação AJAX
    paginacao_html = ""
    if alunos_page.paginator.num_pages > 1:
        paginacao_html = '<ul class="pagination justify-content-center pagination-sm" id="paginacao-alunos">'
        for p in alunos_page.paginator.page_range:
            active = " active" if p == alunos_page.number else ""
            paginacao_html += f'<li class="page-item{active}"><a href="#" class="page-link" data-page="{p}">{p}</a></li>'
        paginacao_html += "</ul>"

    # Retorno padrão: HTML da tabela (com paginação se AJAX)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return HttpResponse(html + paginacao_html)
    else:
        return HttpResponse(html)


# --- Relatório Ficha Cadastral ---
from turmas.models import Turma
from cursos.models import Curso
from django.utils.encoding import smart_str
import csv

try:
    import xlwt
except ImportError:
    xlwt = None
from io import BytesIO
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET"])
def relatorio_ficha_cadastral(request):
    turma_id = request.GET.get("turma", "").strip()
    curso_id = request.GET.get("curso", "").strip()
    situacao = request.GET.get("situacao", "").strip()
    export = request.GET.get("export", "").strip()

    alunos_qs = Aluno.objects.all()
    if turma_id:
        alunos_qs = alunos_qs.filter(matricula__turma_id=turma_id)
    if curso_id:
        alunos_qs = alunos_qs.filter(matricula__turma__curso_id=curso_id)
    if situacao:
        alunos_qs = alunos_qs.filter(situacao=situacao)
    alunos_qs = alunos_qs.distinct().order_by("nome")

    # Exportação CSV/Excel/PDF
    if export in ["csv", "xls"]:
        if export == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                'attachment; filename="ficha_cadastral.csv"'
            )
            writer = csv.writer(response)
            writer.writerow(
                [
                    "Nome",
                    "CPF",
                    "Data Nascimento",
                    "Email",
                    "Situação",
                    "Endereço",
                    "Turma",
                    "Curso",
                ]
            )
            for aluno in alunos_qs:
                endereco = f"{aluno.rua or ''}, {aluno.numero_imovel or ''}, {aluno.bairro_ref or ''}, {aluno.cidade_ref or ''}, {aluno.cep or ''}"
                turma_nome = getattr(
                    getattr(aluno, "matricula_set", None).first(), "turma", None
                )
                curso_nome = getattr(turma_nome, "curso", None)
                writer.writerow(
                    [
                        smart_str(aluno.nome),
                        smart_str(aluno.cpf),
                        smart_str(aluno.data_nascimento),
                        smart_str(aluno.email),
                        dict(Aluno.SITUACAO_CHOICES).get(aluno.situacao, "-"),
                        smart_str(endereco),
                        smart_str(turma_nome.nome if turma_nome else "-"),
                        smart_str(curso_nome.nome if curso_nome else "-"),
                    ]
                )
            return response
        elif export == "xls":
            if not xlwt:
                return HttpResponse("Pacote xlwt não instalado.", status=500)
            wb = xlwt.Workbook()
            ws = wb.add_sheet("Ficha Cadastral")
            headers = [
                "Nome",
                "CPF",
                "Data Nascimento",
                "Email",
                "Situação",
                "Endereço",
                "Turma",
                "Curso",
            ]
            for col, h in enumerate(headers):
                ws.write(0, col, h)
            for row, aluno in enumerate(alunos_qs, start=1):
                endereco = f"{aluno.rua or ''}, {aluno.numero_imovel or ''}, {aluno.bairro_ref or ''}, {aluno.cidade_ref or ''}, {aluno.cep or ''}"
                turma_nome = getattr(
                    getattr(aluno, "matricula_set", None).first(), "turma", None
                )
                curso_nome = getattr(turma_nome, "curso", None)
                ws.write(row, 0, smart_str(aluno.nome))
                ws.write(row, 1, smart_str(aluno.cpf))
                ws.write(row, 2, smart_str(aluno.data_nascimento))
                ws.write(row, 3, smart_str(aluno.email))
                ws.write(row, 4, dict(Aluno.SITUACAO_CHOICES).get(aluno.situacao, "-"))
                ws.write(row, 5, smart_str(endereco))
                ws.write(row, 6, smart_str(turma_nome.nome if turma_nome else "-"))
                ws.write(row, 7, smart_str(curso_nome.nome if curso_nome else "-"))
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            response = HttpResponse(
                output.getvalue(), content_type="application/vnd.ms-excel"
            )
            response["Content-Disposition"] = (
                'attachment; filename="ficha_cadastral.xls"'
            )
            return response
        elif export == "pdf":
            from django.template.loader import get_template
            from weasyprint import HTML

            template = get_template("alunos/relatorio_ficha_cadastral.html")
            html_string = template.render(
                {
                    "alunos": alunos_qs,
                    "turmas": turmas,
                    "cursos": cursos,
                    "situacoes": situacoes,
                    "filtros": {
                        "turma": turma_id,
                        "curso": curso_id,
                        "situacao": situacao,
                    },
                    "is_export_pdf": True,
                }
            )
            pdf_file = HTML(
                string=html_string, base_url=request.build_absolute_uri()
            ).write_pdf()
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = (
                'attachment; filename="ficha_cadastral.pdf"'
            )
            return response

    # Filtros para o template
    turmas = Turma.objects.all().order_by("nome")
    cursos = Curso.objects.all().order_by("nome")
    situacoes = Aluno.SITUACAO_CHOICES

    return render(
        request,
        "alunos/relatorio_ficha_cadastral.html",
        {
            "alunos": alunos_qs,
            "turmas": turmas,
            "cursos": cursos,
            "situacoes": situacoes,
            "filtros": {"turma": turma_id, "curso": curso_id, "situacao": situacao},
        },
    )
