# Relatórios extras (placeholders)
def frequencia_por_atividade(request):
    from atividades.models import Atividade
    from turmas.models import Turma

    turmas = Turma.objects.filter(ativo=True)
    atividades = Atividade.objects.filter(ativo=True)
    turma_id = request.GET.get("turma_id")
    atividade_id = request.GET.get("atividade_id")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    resultados = None
    filtros_aplicados = any(
        valor
        for valor in [turma_id, atividade_id, data_inicio, data_fim]
        if valor not in (None, "")
    )
    is_partial = (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.GET.get("partial") == "1"
    )
    formato = request.GET.get("formato")
    if request.GET:
        service = RelatorioPresencaService()
        resultados = service.obter_frequencia_por_atividade(
            turma_id=turma_id or None,
            atividade_id=atividade_id or None,
            data_inicio=data_inicio or None,
            data_fim=data_fim or None,
        )
        if formato == "csv":
            import csv
            from django.http import HttpResponse

            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                "attachment; filename=frequencia_por_atividade.csv"
            )
            writer = csv.writer(response)
            writer.writerow(["Aluno", "Turma", "Atividade", "Presenças", "Faltas"])
            if resultados:
                for r in resultados:
                    writer.writerow(
                        [
                            r["aluno"].nome,
                            r["turma"].nome,
                            r["atividade"].nome,
                            r["presencas"],
                            r["faltas"],
                        ]
                    )
            return response
        if formato == "pdf" and resultados:
            try:
                from weasyprint import HTML
                from django.template.loader import render_to_string

                html_string = render_to_string(
                    "relatorios_presenca/frequencia_por_atividade.html",
                    {
                        "resultados": resultados,
                        "turmas": turmas,
                        "atividades": atividades,
                        "pdf_export": True,
                    },
                )
                pdf = HTML(string=html_string).write_pdf()
                response = HttpResponse(pdf, content_type="application/pdf")
                response["Content-Disposition"] = (
                    "attachment; filename=frequencia_por_atividade.pdf"
                )
                return response
            except ImportError:
                pass
    contexto = {
        "turmas": turmas,
        "atividades": atividades,
        "resultados": resultados,
        "filtros_aplicados": filtros_aplicados,
    }
    if is_partial:
        return render(
            request,
            "relatorios_presenca/partials/_frequencia_por_atividade_tabela.html",
            {
                "resultados": resultados,
                "filtros_aplicados": filtros_aplicados,
            },
        )
    return render(
        request, "relatorios_presenca/frequencia_por_atividade.html", contexto
    )


def relatorio_faltas(request):
    from turmas.models import Turma

    turmas = Turma.objects.filter(ativo=True)
    turma_id = request.GET.get("turma_id")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    resultados = None
    filtros_aplicados = any(
        valor for valor in [turma_id, data_inicio, data_fim] if valor not in (None, "")
    )
    is_partial = (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.GET.get("partial") == "1"
    )
    formato = request.GET.get("formato")

    if request.GET:
        # Simulação: buscar alunos com mais faltas (ajuste para lógica real)
        from presencas.models import PresencaDetalhada
        from alunos.models import Aluno

        filtros = {}
        if turma_id:
            filtros["turma_id"] = turma_id
        if data_inicio:
            filtros["data__gte"] = data_inicio
        if data_fim:
            filtros["data__lte"] = data_fim
        faltas = (
            PresencaDetalhada.objects.filter(**filtros)
            .values("aluno", "turma")
            .annotate(faltas=models.Sum("faltas"))
            .order_by("-faltas")
        )
        resultados = []
        for f in faltas:
            try:
                aluno = Aluno.objects.get(id=f["aluno"])
                turma = Turma.objects.get(id=f["turma"])
            except (Aluno.DoesNotExist, Turma.DoesNotExist):
                continue
            resultados.append(
                {
                    "aluno": aluno,
                    "turma": turma,
                    "faltas": f["faltas"] or 0,
                }
            )

        if formato == "csv" and resultados:
            import csv
            from django.http import HttpResponse

            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                "attachment; filename=relatorio_faltas.csv"
            )
            writer = csv.writer(response)
            writer.writerow(["Aluno", "Turma", "Faltas"])
            for r in resultados:
                writer.writerow([r["aluno"].nome, r["turma"].nome, r["faltas"]])
            return response
        if formato == "pdf" and resultados:
            try:
                from weasyprint import HTML
                from django.template.loader import render_to_string

                html_string = render_to_string(
                    "relatorios_presenca/relatorio_faltas.html",
                    {
                        "resultados": resultados,
                        "turmas": turmas,
                        "pdf_export": True,
                    },
                )
                pdf = HTML(string=html_string).write_pdf()
                response = HttpResponse(pdf, content_type="application/pdf")
                response["Content-Disposition"] = (
                    "attachment; filename=relatorio_faltas.pdf"
                )
                return response
            except ImportError:
                pass

    contexto = {
        "turmas": turmas,
        "resultados": resultados,
        "filtros_aplicados": filtros_aplicados,
    }
    if is_partial:
        return render(
            request,
            "relatorios_presenca/partials/_relatorio_faltas_tabela.html",
            {
                "resultados": resultados,
                "filtros_aplicados": filtros_aplicados,
            },
        )
    return render(request, "relatorios_presenca/relatorio_faltas.html", contexto)


def alunos_com_carencia(request):
    from cursos.models import Curso
    from turmas.models import Turma

    cursos = Curso.objects.filter(ativo=True)
    turmas = Turma.objects.filter(ativo=True)
    curso_id = request.GET.get("curso_id")
    turma_id = request.GET.get("turma_id")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    resultados = None
    filtros_aplicados = any(
        valor
        for valor in [curso_id, turma_id, data_inicio, data_fim]
        if valor not in (None, "")
    )
    is_partial = (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.GET.get("partial") == "1"
    )
    formato = request.GET.get("formato")
    if request.GET:
        service = RelatorioPresencaService()
        resultados = service.obter_alunos_mais_carencias(
            curso_id=curso_id or None,
            turma_id=turma_id or None,
            data_inicio=data_inicio or None,
            data_fim=data_fim or None,
        )
        if formato == "csv" and resultados:
            import csv
            from django.http import HttpResponse

            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                "attachment; filename=alunos_mais_carencias.csv"
            )
            writer = csv.writer(response)
            writer.writerow(["Aluno", "Turma", "Faltas"])
            for r in resultados:
                writer.writerow(
                    [
                        r["aluno"].nome if r["aluno"] else "",
                        r["turma"].nome if r["turma"] else "",
                        r["faltas"],
                    ]
                )
            return response
        if formato == "pdf" and resultados:
            try:
                from weasyprint import HTML
                from django.template.loader import render_to_string

                html_string = render_to_string(
                    "relatorios_presenca/alunos_com_carencia.html",
                    {
                        "resultados": resultados,
                        "cursos": cursos,
                        "turmas": turmas,
                        "pdf_export": True,
                    },
                )
                pdf = HTML(string=html_string).write_pdf()
                response = HttpResponse(pdf, content_type="application/pdf")
                response["Content-Disposition"] = (
                    "attachment; filename=alunos_mais_carencias.pdf"
                )
                return response
            except ImportError:
                pass
    contexto = {
        "cursos": cursos,
        "turmas": turmas,
        "resultados": resultados,
        "filtros_aplicados": filtros_aplicados,
    }
    if is_partial:
        return render(
            request,
            "relatorios_presenca/partials/_alunos_com_carencia_tabela.html",
            {
                "resultados": resultados,
                "filtros_aplicados": filtros_aplicados,
            },
        )
    return render(request, "relatorios_presenca/alunos_com_carencia.html", contexto)


from django.db import models
from django.shortcuts import render


# Dashboard de relatórios
def dashboard_relatorios(request):
    """Exibe o dashboard de relatórios de presença."""
    return render(request, "relatorios_presenca/dashboard_relatorios.html")


from django.views.decorators.http import require_GET

try:
    from weasyprint import HTML

    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
# --- NOVAS VIEWS PARA AJAX ---


@require_GET
def boletim_frequencia_aluno(request):
    """Exibe boletim de frequência mensal do aluno, com exportação CSV/PDF e AJAX."""
    curso_id = request.GET.get("curso_id")
    turma_id = request.GET.get("turma_id")
    aluno_id = request.GET.get("aluno_id")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")
    formato = request.GET.get("formato")
    partial = request.GET.get("partial") == "1"

    # Filtros para combos
    from cursos.models import Curso

    cursos = Curso.objects.filter(ativo=True)

    dados = None
    if aluno_id and mes and ano:
        service = RelatorioPresencaService()
        dados = service.obter_boletim_aluno(aluno_id, mes, ano, turma_id)

    contexto = {
        "cursos": cursos,
        "dados": dados,
        "mes": mes,
        "ano": ano,
        "aluno_id": aluno_id,
        "turma_id": turma_id,
        "curso_id": curso_id,
    }

    if formato == "csv" and dados:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f"attachment; filename=boletim_aluno_{aluno_id}_{mes}-{ano}.csv"
        )
        writer = csv.writer(response)
        writer.writerow(
            [
                "Convocações",
                "Presenças",
                "Faltas",
                "%",
                "V1",
                "V2",
                "Vol",
                "Car",
                "Limite%",
            ]
        )
        row = [
            dados["convocacoes"],
            dados["presencas"],
            dados["faltas"],
            dados["percentual"],
            dados["v1"],
            dados["v2"],
            dados["vol"],
            dados["carencias"],
            dados["limite_percentual"],
        ]
        writer.writerow(row)
        return response

    if formato == "pdf" and dados and WEASYPRINT_AVAILABLE:
        html = render(
            request,
            "relatorios_presenca/_boletim_frequencia_aluno_tabela.html",
            {"dados": dados},
        )
        pdf = HTML(string=html.content.decode("utf-8")).write_pdf()
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = (
            f"attachment; filename=boletim_aluno_{aluno_id}_{mes}-{ano}.pdf"
        )
        return response

    template = (
        "relatorios_presenca/_boletim_frequencia_aluno_tabela.html"
        if partial
        else "relatorios_presenca/boletim_frequencia_aluno.html"
    )
    return render(request, template, contexto)


import datetime
import csv  # Import the csv module
from django.http import JsonResponse, HttpResponse
from .services import RelatorioPresencaService
from .generators.excel import ExcelGenerator
from turmas.models import Turma
from alunos.models import Aluno
from cursos.models import Curso


# View para renderizar o formulário principal
def relatorio_form(request):
    """Exibe o formulário para solicitar a geração de relatórios."""
    cursos = Curso.objects.filter(ativo=True)
    context = {"cursos": cursos}
    return render(request, "relatorios_presenca/gerar_relatorio.html", context)


# View para exportar o relatório consolidado em diferentes formatos
def exportar_relatorio_consolidado(request):
    """Gera e retorna um relatório consolidado em formato Excel ou CSV."""
    if request.method != "POST":
        return HttpResponse("Método não permitido.", status=405)

    turma_id = request.POST.get("turma_id")
    data_inicio_str = request.POST.get("data_inicio", "2025-01-01")
    data_fim_str = request.POST.get("data_fim", "2025-12-31")
    formato = request.POST.get("formato", "excel")  # Get the format from the request

    try:
        data_inicio = datetime.datetime.strptime(data_inicio_str, "%Y-%m-%d").date()
        data_fim = datetime.datetime.strptime(data_fim_str, "%Y-%m-%d").date()
        turma = Turma.objects.get(pk=turma_id)
    except (ValueError, Turma.DoesNotExist, TypeError):
        return HttpResponse("Parâmetros inválidos.", status=400)

    service = RelatorioPresencaService()
    dados = service.obter_dados_consolidado(turma_id, data_inicio, data_fim)

    if formato == "excel":
        generator = ExcelGenerator(template_path=None)
        wb = generator.gerar_consolidado(dados)
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            f"attachment; filename=relatorio_consolidado_{turma.nome}.xlsx"
        )
        wb.save(response)
        return response

    elif formato == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f"attachment; filename=relatorio_consolidado_{turma.nome}.csv"
        )

        writer = csv.writer(response)
        # Write header
        writer.writerow(
            [
                "Aluno",
                "Presentes",
                "Faltas",
                "Justificadas",
                "Voluntário Extra",
                "Voluntário Simples",
                "Percentual Presença",
            ]
        )

        # Write data rows
        for aluno_dados in dados["alunos"]:
            totais = aluno_dados["totais"]
            total_atividades = (
                totais.get("P", 0) + totais.get("F", 0) + totais.get("J", 0)
            )
            percentual_presenca = (
                (totais.get("P", 0) / total_atividades * 100)
                if total_atividades > 0
                else 0
            )

            writer.writerow(
                [
                    aluno_dados["aluno"].nome,
                    totais.get("P", 0),
                    totais.get("F", 0),
                    totais.get("J", 0),
                    totais.get("V1", 0),
                    totais.get("V2", 0),
                    f"{percentual_presenca:.2f}%",
                ]
            )
        return response

    return HttpResponse("Formato não suportado.", status=400)


# --- NOVAS VIEWS PARA AJAX ---


def turmas_por_curso_json(request):
    """Retorna uma lista de turmas em JSON para um curso específico."""
    curso_id = request.GET.get("curso_id")
    if not curso_id:
        return JsonResponse({"turmas": []})

    turmas = Turma.objects.filter(curso_id=curso_id, ativo=True).values("id", "nome")
    return JsonResponse({"turmas": list(turmas)})


def alunos_por_turma_json(request):
    """Retorna uma lista de alunos em JSON para uma turma específica."""
    turma_id = request.GET.get("turma_id")
    if not turma_id:
        return JsonResponse({"alunos": []})

    # Para obter os alunos, precisamos olhar as matrículas da turma
    try:
        turma = Turma.objects.get(pk=turma_id)
        # Acessando alunos através do related_name 'matriculas' que vem do app matriculas
        alunos = Aluno.objects.filter(
            matriculas__turma=turma, matriculas__ativa=True
        ).order_by("nome")
        alunos_data = [{"id": aluno.id, "nome": aluno.nome} for aluno in alunos]
        return JsonResponse({"alunos": alunos_data})
    except Turma.DoesNotExist:
        return JsonResponse({"alunos": []})


def consolidado_tabela_ajax(request):
    """
    Retorna a tabela consolidada de presenças em HTML para atualização via AJAX.
    """
    turma_id = request.GET.get("turma_id")
    data_inicio_str = request.GET.get("data_inicio")
    data_fim_str = request.GET.get("data_fim")

    if not turma_id or not data_inicio_str or not data_fim_str:
        return HttpResponse("Parâmetros de filtro incompletos.", status=400)

    try:
        data_inicio = datetime.datetime.strptime(data_inicio_str, "%Y-%m-%d").date()
        data_fim = datetime.datetime.strptime(data_fim_str, "%Y-%m-%d").date()
        turma = Turma.objects.get(pk=turma_id)
    except (ValueError, Turma.DoesNotExist, TypeError):
        return HttpResponse("Parâmetros inválidos.", status=400)

    service = RelatorioPresencaService()
    dados = service.obter_dados_consolidado(turma_id, data_inicio, data_fim)

    context = {
        "dados": dados,
        "turma": turma,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }
    return render(request, "relatorios_presenca/_consolidado_tabela.html", context)
