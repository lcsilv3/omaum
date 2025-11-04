"""
Views para relatórios de atividades.
"""

import logging
from typing import Optional
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone

from .utils import get_model_class
from ..services.relatorios_participacao import (
    gerar_relatorio_participacao,
    normalizar_filtros,
    obter_opcoes_filtros_participacao,
)
from ..services.relatorios_instrutores import (
    gerar_relatorio_carga_instrutores,
    normalizar_filtros_instrutores,
    obter_opcoes_filtros_instrutores,
)
from ..services.relatorios_frequencia import (
    gerar_relatorio_frequencia,
    normalizar_filtros_frequencia,
    obter_opcoes_filtros_frequencia,
)
from ..services.relatorios_cronograma import (
    gerar_relatorio_cronograma,
    normalizar_filtros_cronograma,
    obter_opcoes_filtros_cronograma,
)
from ..services.relatorios_historico_aluno import (
    normalizar_filtros_historico,
    gerar_relatorio_historico_aluno,
    obter_opcoes_filtros_historico,
)

# Set up logger
logger = logging.getLogger(__name__)

NOME_ORGANIZACAO_PADRAO = "OMAUM - Ordem Mística de Aspiração Universal ao Mestrado"
NOME_SISTEMA_PADRAO = "Sistema de Gestão Integrada"
TITULO_RELATORIO_PARTICIPACAO = "Relatório de Participação por Atividade"
TITULO_RELATORIO_CARGA = "Relatório de Carga de Instrutores"
TITULO_RELATORIO_FREQUENCIA = "Relatório de Carências e Frequência por Turma"
TITULO_RELATORIO_CRONOGRAMA = "Relatório Cronograma Curso × Turmas"
TITULO_RELATORIO_HISTORICO = "Relatório Histórico de Participação do Aluno"


def _cabecalho_relatorio(titulo: str) -> dict:
    """
    Retorna os metadados padrão utilizados no cabeçalho dos relatórios
    do app Atividades.
    """

    data_emissao = timezone.now().strftime("%d/%m/%Y %H:%M")

    return {
        "titulo": titulo,
        "data_emissao": data_emissao,
        "nome_organizacao": NOME_ORGANIZACAO_PADRAO,
        "nome_sistema": NOME_SISTEMA_PADRAO,
    }


def _gerar_relatorio_participacao(request):
    """Retorna filtros e dados consolidados do relatório de participação."""

    filtros = normalizar_filtros(request.GET)
    relatorio = gerar_relatorio_participacao(filtros)
    return filtros, relatorio


def _gerar_relatorio_carga_instrutores(request):
    """Retorna filtros e dados consolidados do relatório de carga de instrutores."""

    filtros = normalizar_filtros_instrutores(request.GET)
    relatorio = gerar_relatorio_carga_instrutores(filtros)
    return filtros, relatorio


def _gerar_relatorio_cronograma(request):
    """Retorna filtros e dados consolidados do relatório de cronograma."""

    filtros = normalizar_filtros_cronograma(request.GET)
    relatorio = gerar_relatorio_cronograma(filtros)
    return filtros, relatorio


def _gerar_relatorio_frequencia(request):
    """Retorna filtros e dados consolidados do relatório de frequência."""

    filtros = normalizar_filtros_frequencia(request.GET)
    relatorio = gerar_relatorio_frequencia(filtros)
    return filtros, relatorio


def _gerar_relatorio_historico(request):
    """Retorna filtros e dados do relatório histórico de participação do aluno."""

    filtros = normalizar_filtros_historico(request.GET)
    relatorio = gerar_relatorio_historico_aluno(filtros)
    return filtros, relatorio


def _descricao_periodo(filtros):
    """Monta descrição textual para o período filtrado."""

    if filtros.data_inicio and filtros.data_fim:
        inicio = filtros.data_inicio.strftime("%d/%m/%Y")
        fim = filtros.data_fim.strftime("%d/%m/%Y")
        return f"{inicio} a {fim}"
    if filtros.data_inicio:
        inicio = filtros.data_inicio.strftime("%d/%m/%Y")
        return f"A partir de {inicio}"
    if filtros.data_fim:
        fim = filtros.data_fim.strftime("%d/%m/%Y")
        return f"Até {fim}"
    return None


def _montar_descricao_filtros_frequencia(filtros, opcoes):
    """Retorna descrições amigáveis dos filtros de frequência."""

    cursos_map = {item["id"]: item["nome"] for item in opcoes.get("cursos", [])}
    turmas_map = {item["id"]: item["nome"] for item in opcoes.get("turmas", [])}
    meses_map = {item["value"]: item["label"] for item in opcoes.get("meses", [])}
    anos_map = {item["value"]: item["label"] for item in opcoes.get("anos", [])}
    status_map = {item["value"]: item["label"] for item in opcoes.get("status", [])}

    mes_label = meses_map.get(str(filtros.mes)) if filtros.mes is not None else None
    ano_label = anos_map.get(str(filtros.ano)) if filtros.ano is not None else None

    periodo = None
    if mes_label and ano_label:
        periodo = f"{mes_label} / {ano_label}"
    elif ano_label:
        periodo = ano_label

    return {
        "curso": cursos_map.get(filtros.curso_id),
        "turma": turmas_map.get(filtros.turma_id),
        "periodo": periodo,
        "status_carencia": status_map.get(filtros.status_carencia),
    }


def _montar_descricao_filtros_cronograma(filtros, opcoes):
    """Retorna descrições amigáveis para o relatório de cronograma."""

    cursos_map = {item["id"]: item["nome"] for item in opcoes.get("cursos", [])}
    turmas_map = {item["id"]: item["nome"] for item in opcoes.get("turmas", [])}
    status_map = {item["value"]: item["label"] for item in opcoes.get("status", [])}

    return {
        "curso": cursos_map.get(filtros.curso_id),
        "turma": turmas_map.get(filtros.turma_id),
        "status": status_map.get(filtros.status),
        "responsavel": filtros.responsavel,
        "periodo": _descricao_periodo(filtros),
    }


def _montar_descricao_filtros_historico(filtros, opcoes):
    """Retorna descrições amigáveis para o relatório histórico do aluno."""

    alunos_map = {item["id"]: item["nome"] for item in opcoes.get("alunos", [])}
    cursos_map = {item["id"]: item["nome"] for item in opcoes.get("cursos", [])}
    papeis_map = {item["value"]: item["label"] for item in opcoes.get("papeis", [])}

    return {
        "aluno": alunos_map.get(filtros.aluno_id),
        "curso": cursos_map.get(filtros.curso_id),
        "papel": papeis_map.get(filtros.papel),
        "periodo": _descricao_periodo(filtros),
    }


def _montar_descricao_filtros_instrutores(filtros, opcoes):
    """Retorna descrições amigáveis dos filtros aplicados."""

    instrutores_map = {
        item["id"]: item["nome"] for item in opcoes.get("instrutores", [])
    }
    cursos_map = {item["id"]: item["nome"] for item in opcoes.get("cursos", [])}
    status_map = {item["value"]: item["label"] for item in opcoes.get("status", [])}

    return {
        "instrutor": instrutores_map.get(filtros.instrutor_id),
        "curso": cursos_map.get(filtros.curso_id),
        "status_turma": status_map.get(filtros.status_turma),
        "periodo": _descricao_periodo(filtros),
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

    # Cabeçalho clássico (compatível com o restante do projeto)
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
        data_inicio_str = (
            atividade.data_inicio.strftime("%d/%m/%Y") if atividade.data_inicio else ""
        )
        data_fim_str = (
            atividade.data_fim.strftime("%d/%m/%Y")
            if getattr(atividade, "data_fim", None)
            else ""
        )

        writer.writerow(
            [
                atividade.nome,
                atividade.descricao or "",
                data_inicio_str,
                data_fim_str,
                getattr(atividade, "responsavel", "") or "",
                getattr(atividade, "local", "") or "",
                atividade.status or "",
                getattr(atividade, "tipo_atividade", "") or "",
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
                "Data de Início": (
                    atividade.data_inicio.strftime("%d/%m/%Y")
                    if atividade.data_inicio
                    else ""
                ),
                "Data de Término": (
                    atividade.data_fim.strftime("%d/%m/%Y")
                    if getattr(atividade, "data_fim", None)
                    else ""
                ),
                "Responsável": getattr(atividade, "responsavel", "") or "",
                "Local": getattr(atividade, "local", "") or "",
                "Status": atividade.status or "",
                "Tipo de Atividade": getattr(atividade, "tipo_atividade", "") or "",
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
    # Implementação simples para PDF - retorno em HTML (preview)
    from django.template.loader import get_template

    template = get_template("atividades/relatorio_atividades_pdf.html")
    context = {
        **_cabecalho_relatorio("Relatório de Atividades"),
        "atividades": atividades,
        "total_atividades": atividades.count(),
    }

    html = template.render(context)

    # Retorno em HTML para inspeção rápida enquanto o pipeline oficial de PDF é ajustado
    return HttpResponse(html, content_type="text/html")


@login_required
def relatorio_frequencia_turmas(request):
    filtros, relatorio = _gerar_relatorio_frequencia(request)
    opcoes = obter_opcoes_filtros_frequencia(filtros.curso_id, filtros.ano)
    descricao_filtros = _montar_descricao_filtros_frequencia(filtros, opcoes)

    context = {
        **_cabecalho_relatorio(TITULO_RELATORIO_FREQUENCIA),
        "relatorio": relatorio,
        "filtros": filtros,
        "cursos": opcoes["cursos"],
        "turmas": opcoes["turmas"],
        "meses": opcoes["meses"],
        "anos": opcoes["anos"],
        "status_carencia_choices": opcoes["status"],
        "descricao_filtros": descricao_filtros,
        "query_params": request.GET.urlencode(),
    }
    return render(request, "atividades/relatorio_frequencia_turma.html", context)


@login_required
def relatorio_cronograma_curso_turmas(request):
    filtros, relatorio = _gerar_relatorio_cronograma(request)
    opcoes = obter_opcoes_filtros_cronograma(filtros.curso_id)
    descricao_filtros = _montar_descricao_filtros_cronograma(filtros, opcoes)

    context = {
        **_cabecalho_relatorio(TITULO_RELATORIO_CRONOGRAMA),
        "relatorio": relatorio,
        "filtros": filtros,
        "cursos": opcoes["cursos"],
        "turmas": opcoes["turmas"],
        "status_choices": opcoes["status"],
        "responsaveis": opcoes["responsaveis"],
        "descricao_filtros": descricao_filtros,
        "query_params": request.GET.urlencode(),
    }
    return render(request, "atividades/relatorio_cronograma_curso_turmas.html", context)


@login_required
def exportar_relatorio_cronograma(request, formato):
    """Exporta o relatório de cronograma para o formato solicitado."""

    filtros, relatorio = _gerar_relatorio_cronograma(request)
    opcoes = obter_opcoes_filtros_cronograma(filtros.curso_id)
    descricao_filtros = _montar_descricao_filtros_cronograma(filtros, opcoes)

    if formato == "csv":
        return _exportar_cronograma_csv(relatorio)
    if formato == "excel":
        return _exportar_cronograma_excel(relatorio)
    if formato == "pdf":
        return _exportar_cronograma_pdf(relatorio, filtros, descricao_filtros)

    messages.error(request, f"Formato de exportação '{formato}' não suportado.")
    return redirect("atividades:relatorio_cronograma_curso_turmas")


@login_required
def exportar_relatorio_historico_aluno(request, formato):
    """Exporta o relatório histórico do aluno para o formato solicitado."""

    filtros, relatorio = _gerar_relatorio_historico(request)
    opcoes = obter_opcoes_filtros_historico(filtros.aluno_id, filtros.curso_id)
    descricao_filtros = _montar_descricao_filtros_historico(filtros, opcoes)

    if formato == "csv":
        return _exportar_historico_csv(relatorio)
    if formato == "excel":
        return _exportar_historico_excel(relatorio)
    if formato == "pdf":
        return _exportar_historico_pdf(relatorio, filtros, descricao_filtros)

    messages.error(request, f"Formato de exportação '{formato}' não suportado.")
    return redirect("atividades:relatorio_historico_aluno")


@login_required
def relatorio_historico_aluno(request):
    filtros, relatorio = _gerar_relatorio_historico(request)
    opcoes = obter_opcoes_filtros_historico(filtros.aluno_id, filtros.curso_id)
    descricao_filtros = _montar_descricao_filtros_historico(filtros, opcoes)

    context = {
        **_cabecalho_relatorio(TITULO_RELATORIO_HISTORICO),
        "relatorio": relatorio,
        "filtros": filtros,
        "alunos": opcoes["alunos"],
        "cursos": opcoes["cursos"],
        "papeis": opcoes["papeis"],
        "descricao_filtros": descricao_filtros,
        "query_params": request.GET.urlencode(),
    }
    return render(request, "atividades/relatorio_historico_aluno.html", context)


@login_required
def relatorio_participacao_atividades(request):
    """Renderiza o relatório de participação por atividade com filtros dinâmicos."""

    filtros, relatorio = _gerar_relatorio_participacao(request)
    opcoes = obter_opcoes_filtros_participacao(filtros.curso_id)

    context = {
        **_cabecalho_relatorio(TITULO_RELATORIO_PARTICIPACAO),
        "relatorio": relatorio,
        "filtros": filtros,
        "cursos": opcoes["cursos"],
        "turmas": opcoes["turmas"],
        "tipos": opcoes["tipos"],
        "status_choices": opcoes["status"],
        "query_params": request.GET.urlencode(),
    }

    return render(
        request,
        "atividades/relatorio_participacao_atividades.html",
        context,
    )


@login_required
def exportar_relatorio_participacao(request, formato):
    """Exporta o relatório de participação nos formatos CSV, Excel ou PDF."""

    filtros, relatorio = _gerar_relatorio_participacao(request)

    if formato == "csv":
        return _exportar_participacao_csv(relatorio)
    if formato == "excel":
        return _exportar_participacao_excel(relatorio)
    if formato == "pdf":
        return _exportar_participacao_pdf(relatorio, filtros)

    messages.error(request, f"Formato de exportação '{formato}' não suportado.")
    return redirect("atividades:relatorio_participacao_atividades")


@login_required
@require_GET
def ajax_relatorio_participacao_tabela(request):
    """Retorna a tabela consolidada do relatório de participação para AJAX."""

    _, relatorio = _gerar_relatorio_participacao(request)
    return render(
        request,
        "atividades/partials/relatorio_participacao_tabela.html",
        {"relatorio": relatorio},
    )


def _exportar_participacao_csv(relatorio):
    """Gera arquivo CSV do relatório de participação."""

    import csv

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_participacao_atividades.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "Atividade",
            "Curso",
            "Turmas",
            "Data Inicial",
            "Data Final",
            "Status",
            "Tipo",
            "Convocados",
            "Presentes",
            "Faltas",
            "Faltas Justificadas",
            "Voluntários Extra",
            "Voluntários Simples",
            "Percentual Presença (%)",
        ]
    )

    for linha in relatorio.linhas:
        writer.writerow(
            [
                linha.atividade_nome,
                linha.curso_nome or "-",
                "; ".join(linha.turmas) if linha.turmas else "-",
                linha.data_inicio.strftime("%d/%m/%Y") if linha.data_inicio else "-",
                linha.data_fim.strftime("%d/%m/%Y") if linha.data_fim else "-",
                linha.status_atividade,
                linha.tipo_atividade,
                linha.total_convocados,
                linha.total_presentes,
                linha.total_faltas,
                linha.total_faltas_justificadas,
                linha.total_voluntario_extra,
                linha.total_voluntario_simples,
                f"{linha.percentual_presenca:.2f}",
            ]
        )

    writer.writerow([])
    writer.writerow(
        [
            "Totais",
            "-",
            "-",
            "-",
            "-",
            "-",
            "-",
            relatorio.resumo.total_convocados,
            relatorio.resumo.total_presentes,
            relatorio.resumo.total_faltas,
            relatorio.resumo.total_faltas_justificadas,
            relatorio.resumo.total_voluntario_extra,
            relatorio.resumo.total_voluntario_simples,
            f"{relatorio.resumo.percentual_presenca_medio:.2f}",
        ]
    )

    return response


def _exportar_participacao_excel(relatorio):
    """Gera arquivo Excel do relatório de participação."""

    try:
        import pandas as pd
    except ImportError:
        logger.error("Pandas não está instalado")
        return HttpResponse("Erro: Pandas não está instalado", status=500)

    dados = []
    for linha in relatorio.linhas:
        dados.append(
            {
                "Atividade": linha.atividade_nome,
                "Curso": linha.curso_nome or "-",
                "Turmas": "; ".join(linha.turmas) if linha.turmas else "-",
                "Data Inicial": linha.data_inicio.strftime("%d/%m/%Y")
                if linha.data_inicio
                else "-",
                "Data Final": linha.data_fim.strftime("%d/%m/%Y")
                if linha.data_fim
                else "-",
                "Status": linha.status_atividade,
                "Tipo": linha.tipo_atividade,
                "Convocados": linha.total_convocados,
                "Presentes": linha.total_presentes,
                "Faltas": linha.total_faltas,
                "Faltas Justificadas": linha.total_faltas_justificadas,
                "Voluntários Extra": linha.total_voluntario_extra,
                "Voluntários Simples": linha.total_voluntario_simples,
                "Percentual Presença (%)": linha.percentual_presenca,
            }
        )

    dados.append(
        {
            "Atividade": "Totais",
            "Curso": "-",
            "Turmas": "-",
            "Data Inicial": "-",
            "Data Final": "-",
            "Status": "-",
            "Tipo": "-",
            "Convocados": relatorio.resumo.total_convocados,
            "Presentes": relatorio.resumo.total_presentes,
            "Faltas": relatorio.resumo.total_faltas,
            "Faltas Justificadas": relatorio.resumo.total_faltas_justificadas,
            "Voluntários Extra": relatorio.resumo.total_voluntario_extra,
            "Voluntários Simples": relatorio.resumo.total_voluntario_simples,
            "Percentual Presença (%)": relatorio.resumo.percentual_presenca_medio,
        }
    )

    df = pd.DataFrame(dados)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_participacao_atividades.xlsx"'
    )

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Participacao", index=False)

    return response


def _exportar_participacao_pdf(relatorio, filtros):
    """
    Gera saída em PDF (HTML para pré-visualização) para o relatório
    de participação.
    """

    from django.template.loader import get_template

    template = get_template("atividades/relatorio_participacao_atividades_pdf.html")
    context = {
        **_cabecalho_relatorio(TITULO_RELATORIO_PARTICIPACAO),
        "relatorio": relatorio,
        "filtros": filtros,
    }

    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_participacao_atividades.pdf"'
    )

    # Retorno em HTML para inspeção rápida enquanto o pipeline oficial de PDF é ajustado
    return HttpResponse(html, content_type="text/html")


@login_required
def relatorio_carga_instrutores(request):
    """Renderiza o relatório de carga de instrutores."""

    filtros, relatorio = _gerar_relatorio_carga_instrutores(request)
    opcoes = obter_opcoes_filtros_instrutores(filtros.curso_id)
    descricao_filtros = _montar_descricao_filtros_instrutores(filtros, opcoes)

    context = {
        **_cabecalho_relatorio(TITULO_RELATORIO_CARGA),
        "relatorio": relatorio,
        "filtros": filtros,
        "instrutores": opcoes["instrutores"],
        "cursos": opcoes["cursos"],
        "status_turma_choices": opcoes["status"],
        "query_params": request.GET.urlencode(),
        "descricao_filtros": descricao_filtros,
    }

    return render(
        request,
        "atividades/relatorio_carga_instrutores.html",
        context,
    )


@login_required
def exportar_relatorio_carga_instrutores(request, formato):
    """Exporta o relatório de carga de instrutores para o formato desejado."""

    filtros, relatorio = _gerar_relatorio_carga_instrutores(request)

    if formato == "csv":
        return _exportar_carga_instrutores_csv(relatorio)
    if formato == "excel":
        return _exportar_carga_instrutores_excel(relatorio)
    if formato == "pdf":
        opcoes = obter_opcoes_filtros_instrutores(filtros.curso_id)
        descricao_filtros = _montar_descricao_filtros_instrutores(filtros, opcoes)
        return _exportar_carga_instrutores_pdf(relatorio, filtros, descricao_filtros)

    messages.error(request, f"Formato de exportação '{formato}' não suportado.")
    return redirect("atividades:relatorio_carga_instrutores")


@login_required
def exportar_relatorio_frequencia(request, formato):
    """Exporta o relatório de frequência para o formato solicitado."""

    filtros, relatorio = _gerar_relatorio_frequencia(request)
    opcoes = obter_opcoes_filtros_frequencia(filtros.curso_id, filtros.ano)
    descricao_filtros = _montar_descricao_filtros_frequencia(filtros, opcoes)

    if formato == "csv":
        return _exportar_frequencia_csv(relatorio)
    if formato == "excel":
        return _exportar_frequencia_excel(relatorio)
    if formato == "pdf":
        return _exportar_frequencia_pdf(relatorio, filtros, descricao_filtros)

    messages.error(request, f"Formato de exportação '{formato}' não suportado.")
    return redirect("atividades:relatorio_frequencia_turmas")


@login_required
@require_GET
def ajax_relatorio_carga_instrutores_tabela(request):
    """Retorna a tabela do relatório de carga de instrutores para AJAX."""

    filtros, relatorio = _gerar_relatorio_carga_instrutores(request)
    opcoes = obter_opcoes_filtros_instrutores(filtros.curso_id)
    descricao_filtros = _montar_descricao_filtros_instrutores(filtros, opcoes)
    return render(
        request,
        "atividades/partials/relatorio_carga_instrutores_tabela.html",
        {"relatorio": relatorio, "descricao_filtros": descricao_filtros},
    )


@login_required
@require_GET
def ajax_relatorio_frequencia_tabela(request):
    """Retorna a tabela do relatório de frequência para renderização via AJAX."""

    filtros, relatorio = _gerar_relatorio_frequencia(request)
    opcoes = obter_opcoes_filtros_frequencia(filtros.curso_id, filtros.ano)
    descricao_filtros = _montar_descricao_filtros_frequencia(filtros, opcoes)

    return render(
        request,
        "atividades/partials/relatorio_frequencia_tabela.html",
        {
            "relatorio": relatorio,
            "descricao_filtros": descricao_filtros,
        },
    )


@login_required
@require_GET
def ajax_relatorio_frequencia_opcoes(request):
    """Retorna as opções de filtro do relatório de frequência (AJAX)."""

    def _to_int(valor: Optional[str]) -> Optional[int]:
        try:
            return int(valor) if valor else None
        except (TypeError, ValueError):
            return None

    curso_id = _to_int(request.GET.get("curso"))
    ano = _to_int(request.GET.get("ano"))
    opcoes = obter_opcoes_filtros_frequencia(curso_id, ano)
    return JsonResponse(opcoes)


@login_required
@require_GET
def ajax_relatorio_cronograma_tabela(request):
    """Retorna a tabela do relatório de cronograma para renderização via AJAX."""

    filtros, relatorio = _gerar_relatorio_cronograma(request)
    opcoes = obter_opcoes_filtros_cronograma(filtros.curso_id)
    descricao_filtros = _montar_descricao_filtros_cronograma(filtros, opcoes)

    return render(
        request,
        "atividades/partials/relatorio_cronograma_tabela.html",
        {
            "relatorio": relatorio,
            "descricao_filtros": descricao_filtros,
        },
    )


@login_required
@require_GET
def ajax_relatorio_cronograma_opcoes(request):
    """Retorna as opções de filtro do relatório de cronograma (AJAX)."""

    def _to_int(valor: Optional[str]) -> Optional[int]:
        try:
            return int(valor) if valor else None
        except (TypeError, ValueError):
            return None

    curso_id = _to_int(request.GET.get("curso"))
    opcoes = obter_opcoes_filtros_cronograma(curso_id)
    return JsonResponse(opcoes)


@login_required
@require_GET
def ajax_relatorio_historico_tabela(request):
    """Retorna o conteúdo do relatório histórico do aluno para AJAX."""

    filtros, relatorio = _gerar_relatorio_historico(request)
    opcoes = obter_opcoes_filtros_historico(filtros.aluno_id, filtros.curso_id)
    descricao_filtros = _montar_descricao_filtros_historico(filtros, opcoes)

    return render(
        request,
        "atividades/partials/relatorio_historico_aluno_timeline.html",
        {
            "relatorio": relatorio,
            "descricao_filtros": descricao_filtros,
        },
    )


@login_required
@require_GET
def ajax_relatorio_historico_opcoes(request):
    """Retorna opções dinâmicas de filtros para o relatório histórico (AJAX)."""

    def _to_int(valor: Optional[str]) -> Optional[int]:
        try:
            return int(valor) if valor else None
        except (TypeError, ValueError):
            return None

    aluno_id = _to_int(request.GET.get("aluno"))
    curso_id = _to_int(request.GET.get("curso"))
    opcoes = obter_opcoes_filtros_historico(aluno_id, curso_id)
    return JsonResponse(opcoes)


def _exportar_carga_instrutores_csv(relatorio):
    """Gera arquivo CSV da carga de instrutores."""

    import csv

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_carga_instrutores.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "Instrutor",
            "Papel",
            "Cursos",
            "Turmas",
            "Total de Atividades",
            "Total de Horas",
            "Distribuição por Status",
        ]
    )

    for linha in relatorio.linhas:
        status_resumo = "; ".join(
            (
                f"{status}: {quantidade}"
                for status, quantidade in linha.atividades_por_status.items()
            )
        )
        writer.writerow(
            [
                linha.instrutor_nome,
                linha.papel_display,
                "; ".join(linha.cursos) if linha.cursos else "-",
                "; ".join(linha.turmas) if linha.turmas else "-",
                linha.total_atividades,
                f"{linha.total_horas:.2f}",
                status_resumo or "-",
            ]
        )

    writer.writerow([])

    # Distribuição por status (texto resumido)
    resumo_items = relatorio.resumo.atividades_por_status.items()
    distrib_totais = (
        "; ".join((f"{status}: {quantidade}" for status, quantidade in resumo_items))
        or "-"
    )

    writer.writerow(
        [
            "Totais",
            "-",
            "-",
            "-",
            relatorio.resumo.total_atividades,
            f"{relatorio.resumo.total_horas:.2f}",
            distrib_totais,
        ]
    )

    writer.writerow(
        [
            "Instrutores únicos",
            relatorio.resumo.total_instrutores,
            "-",
            "-",
            "-",
            "-",
            "-",
        ]
    )

    return response


def _exportar_carga_instrutores_excel(relatorio):
    """Gera arquivo Excel da carga de instrutores."""

    try:
        import pandas as pd
    except ImportError:
        logger.error("Pandas não está instalado")
        return HttpResponse("Erro: Pandas não está instalado", status=500)

    dados = []
    for linha in relatorio.linhas:
        status_resumo = "; ".join(
            f"{status}: {quantidade}"
            for status, quantidade in linha.atividades_por_status.items()
        )
        dados.append(
            {
                "Instrutor": linha.instrutor_nome,
                "Papel": linha.papel_display,
                "Cursos": "; ".join(linha.cursos) if linha.cursos else "-",
                "Turmas": "; ".join(linha.turmas) if linha.turmas else "-",
                "Total de Atividades": linha.total_atividades,
                "Total de Horas": linha.total_horas,
                "Distribuição por Status": status_resumo or "-",
            }
        )

    resumo_items = relatorio.resumo.atividades_por_status.items()
    distrib_totais = (
        "; ".join((f"{status}: {quantidade}" for status, quantidade in resumo_items))
        or "-"
    )

    dados.append(
        {
            "Instrutor": "Totais",
            "Papel": "-",
            "Cursos": "-",
            "Turmas": "-",
            "Total de Atividades": relatorio.resumo.total_atividades,
            "Total de Horas": relatorio.resumo.total_horas,
            "Distribuição por Status": distrib_totais,
        }
    )

    dados.append(
        {
            "Instrutor": "Instrutores únicos",
            "Papel": relatorio.resumo.total_instrutores,
            "Cursos": "-",
            "Turmas": "-",
            "Total de Atividades": "-",
            "Total de Horas": "-",
            "Distribuição por Status": "-",
        }
    )

    df = pd.DataFrame(dados)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_carga_instrutores.xlsx"'
    )

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="CargaInstrutores", index=False)

    return response


def _exportar_carga_instrutores_pdf(relatorio, filtros, descricao_filtros):
    """Gera saída PDF (HTML) para o relatório de carga de instrutores."""

    from django.template.loader import get_template

    template = get_template("atividades/relatorio_carga_instrutores_pdf.html")
    context = {
        **_cabecalho_relatorio(TITULO_RELATORIO_CARGA),
        "relatorio": relatorio,
        "filtros": filtros,
        "descricao_filtros": descricao_filtros,
    }

    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_carga_instrutores.pdf"'
    )

    return HttpResponse(html, content_type="text/html")


def _exportar_cronograma_csv(relatorio):
    """Gera arquivo CSV do relatório de cronograma."""

    import csv

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_cronograma_curso_turmas.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "Atividade",
            "Curso",
            "Turmas",
            "Data Prevista",
            "Data Final Prevista",
            "Data Realizada",
            "Status",
            "Responsável",
            "Atraso (dias)",
            "Adiantamento (dias)",
        ]
    )

    for linha in relatorio.linhas:
        writer.writerow(
            [
                linha.atividade_nome,
                linha.curso_nome,
                "; ".join(linha.turmas) if linha.turmas else "-",
                linha.data_prevista.strftime("%d/%m/%Y")
                if linha.data_prevista
                else "-",
                linha.data_prevista_fim.strftime("%d/%m/%Y")
                if linha.data_prevista_fim
                else "-",
                linha.data_realizada.strftime("%d/%m/%Y")
                if linha.data_realizada
                else "-",
                linha.status,
                linha.responsavel or "-",
                linha.atraso_dias if linha.atraso_dias is not None else "-",
                linha.adiantamento_dias if linha.adiantamento_dias is not None else "-",
            ]
        )

    writer.writerow([])
    writer.writerow(["Resumo", "", "", "", "", "", "", "", "", ""])
    writer.writerow(
        [
            "Total de atividades",
            relatorio.resumo.total_atividades,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
    )
    writer.writerow(
        [
            "Atividades atrasadas",
            relatorio.resumo.atividades_atrasadas,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
    )
    writer.writerow(
        [
            "Atividades adiantadas",
            relatorio.resumo.atividades_adiantadas,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
    )
    writer.writerow(
        [
            "Atividades no prazo",
            relatorio.resumo.atividades_no_prazo,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
    )

    distribuicao = "; ".join(
        f"{status}: {quantidade}"
        for status, quantidade in relatorio.resumo.atividades_por_status.items()
    )

    writer.writerow(
        [
            "Distribuição por status",
            distribuicao or "-",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
    )

    return response


def _exportar_cronograma_excel(relatorio):
    """Gera arquivo Excel do relatório de cronograma."""

    try:
        import pandas as pd
    except ImportError:
        logger.error("Pandas não está instalado")
        return HttpResponse("Erro: Pandas não está instalado", status=500)

    dados = []
    for linha in relatorio.linhas:
        dados.append(
            {
                "Atividade": linha.atividade_nome,
                "Curso": linha.curso_nome,
                "Turmas": "; ".join(linha.turmas) if linha.turmas else "-",
                "Data Prevista": (
                    linha.data_prevista.strftime("%d/%m/%Y")
                    if linha.data_prevista
                    else "-"
                ),
                "Data Final Prevista": (
                    linha.data_prevista_fim.strftime("%d/%m/%Y")
                    if linha.data_prevista_fim
                    else "-"
                ),
                "Data Realizada": (
                    linha.data_realizada.strftime("%d/%m/%Y")
                    if linha.data_realizada
                    else "-"
                ),
                "Status": linha.status,
                "Responsável": linha.responsavel or "-",
                "Atraso (dias)": linha.atraso_dias,
                "Adiantamento (dias)": linha.adiantamento_dias,
            }
        )

    dados.append(
        {
            "Atividade": "Total de atividades",
            "Curso": relatorio.resumo.total_atividades,
            "Turmas": "-",
            "Data Prevista": "-",
            "Data Final Prevista": "-",
            "Data Realizada": "-",
            "Status": "-",
            "Responsável": "-",
            "Atraso (dias)": "-",
            "Adiantamento (dias)": "-",
        }
    )

    dados.append(
        {
            "Atividade": "Atividades atrasadas",
            "Curso": relatorio.resumo.atividades_atrasadas,
            "Turmas": "-",
            "Data Prevista": "-",
            "Data Final Prevista": "-",
            "Data Realizada": "-",
            "Status": "-",
            "Responsável": "-",
            "Atraso (dias)": "-",
            "Adiantamento (dias)": "-",
        }
    )

    dados.append(
        {
            "Atividade": "Atividades adiantadas",
            "Curso": relatorio.resumo.atividades_adiantadas,
            "Turmas": "-",
            "Data Prevista": "-",
            "Data Final Prevista": "-",
            "Data Realizada": "-",
            "Status": "-",
            "Responsável": "-",
            "Atraso (dias)": "-",
            "Adiantamento (dias)": "-",
        }
    )

    dados.append(
        {
            "Atividade": "Atividades no prazo",
            "Curso": relatorio.resumo.atividades_no_prazo,
            "Turmas": "-",
            "Data Prevista": "-",
            "Data Final Prevista": "-",
            "Data Realizada": "-",
            "Status": "-",
            "Responsável": "-",
            "Atraso (dias)": "-",
            "Adiantamento (dias)": "-",
        }
    )

    distribuicao = "; ".join(
        f"{status}: {quantidade}"
        for status, quantidade in relatorio.resumo.atividades_por_status.items()
    )

    dados.append(
        {
            "Atividade": "Distribuição por status",
            "Curso": distribuicao or "-",
            "Turmas": "-",
            "Data Prevista": "-",
            "Data Final Prevista": "-",
            "Data Realizada": "-",
            "Status": "-",
            "Responsável": "-",
            "Atraso (dias)": "-",
            "Adiantamento (dias)": "-",
        }
    )

    df = pd.DataFrame(dados)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_cronograma_curso_turmas.xlsx"'
    )

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Cronograma", index=False)

    return response


def _exportar_cronograma_pdf(relatorio, filtros, descricao_filtros):
    """Gera saída em HTML para pré-visualização do relatório de cronograma."""

    from django.template.loader import get_template

    template = get_template("atividades/relatorio_cronograma_curso_turmas.html")
    context = {
        **_cabecalho_relatorio(TITULO_RELATORIO_CRONOGRAMA),
        "relatorio": relatorio,
        "filtros": filtros,
        "descricao_filtros": descricao_filtros,
        "cursos": [],
        "turmas": [],
        "status_choices": [],
        "responsaveis": [],
        "query_params": "",
    }

    html = template.render(context)
    response = HttpResponse(html, content_type="text/html")
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_cronograma_curso_turmas.pdf"'
    )
    return response


def _exportar_historico_csv(relatorio):
    """Gera arquivo CSV do relatório histórico de participação do aluno."""

    import csv

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_historico_aluno.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "Data",
            "Papel",
            "Descrição",
            "Atividade",
            "Curso",
            "Turma",
            "Status de Presença",
            "Status da Atividade",
            "Tipo de Atividade",
        ]
    )

    for evento in relatorio.eventos:
        writer.writerow(
            [
                evento.data.strftime("%d/%m/%Y") if evento.data else "-",
                evento.papel_display,
                evento.descricao,
                evento.atividade_nome or "-",
                evento.curso_nome or "-",
                evento.turma_nome or "-",
                evento.status_presenca or "-",
                evento.status_atividade or "-",
                evento.tipo_atividade or "-",
            ]
        )

    writer.writerow([])
    writer.writerow(["Resumo", "", "", "", "", "", "", "", ""])
    writer.writerow(["Total de eventos", relatorio.resumo.total_eventos])
    writer.writerow(
        ["Participações contabilizadas", relatorio.resumo.total_participacoes]
    )
    writer.writerow(["Presenças", relatorio.resumo.total_presencas])
    writer.writerow(["Faltas", relatorio.resumo.total_faltas])
    writer.writerow(["Faltas justificadas", relatorio.resumo.total_justificadas])
    writer.writerow(["Atuações voluntárias", relatorio.resumo.total_voluntarios])
    writer.writerow(["Atuações em instrução", relatorio.resumo.total_instrucao])

    distribuicao = "; ".join(
        f"{papel}: {quantidade}"
        for papel, quantidade in relatorio.resumo.eventos_por_papel.items()
    )
    writer.writerow(["Eventos por papel", distribuicao or "-"])

    return response


def _exportar_historico_excel(relatorio):
    """Gera arquivo Excel do relatório histórico do aluno."""

    try:
        import pandas as pd
    except ImportError:
        logger.error("Pandas não está instalado")
        return HttpResponse("Erro: Pandas não está instalado", status=500)

    dados = []
    for evento in relatorio.eventos:
        dados.append(
            {
                "Data": evento.data.strftime("%d/%m/%Y") if evento.data else "-",
                "Papel": evento.papel_display,
                "Descrição": evento.descricao,
                "Atividade": evento.atividade_nome or "-",
                "Curso": evento.curso_nome or "-",
                "Turma": evento.turma_nome or "-",
                "Status de Presença": evento.status_presenca or "-",
                "Status da Atividade": evento.status_atividade or "-",
                "Tipo de Atividade": evento.tipo_atividade or "-",
            }
        )

    dados.append(
        {
            "Data": "Resumo",
            "Papel": "Total de eventos",
            "Descrição": relatorio.resumo.total_eventos,
            "Atividade": "-",
            "Curso": "-",
            "Turma": "-",
            "Status de Presença": "-",
            "Status da Atividade": "-",
            "Tipo de Atividade": "-",
        }
    )

    dados.append(
        {
            "Data": "Resumo",
            "Papel": "Participações contabilizadas",
            "Descrição": relatorio.resumo.total_participacoes,
            "Atividade": "-",
            "Curso": "-",
            "Turma": "-",
            "Status de Presença": "-",
            "Status da Atividade": "-",
            "Tipo de Atividade": "-",
        }
    )

    dados.append(
        {
            "Data": "Resumo",
            "Papel": "Presenças",
            "Descrição": relatorio.resumo.total_presencas,
            "Atividade": "-",
            "Curso": "-",
            "Turma": "-",
            "Status de Presença": "-",
            "Status da Atividade": "-",
            "Tipo de Atividade": "-",
        }
    )

    dados.append(
        {
            "Data": "Resumo",
            "Papel": "Faltas",
            "Descrição": relatorio.resumo.total_faltas,
            "Atividade": "-",
            "Curso": "-",
            "Turma": "-",
            "Status de Presença": "-",
            "Status da Atividade": "-",
            "Tipo de Atividade": "-",
        }
    )

    dados.append(
        {
            "Data": "Resumo",
            "Papel": "Faltas justificadas",
            "Descrição": relatorio.resumo.total_justificadas,
            "Atividade": "-",
            "Curso": "-",
            "Turma": "-",
            "Status de Presença": "-",
            "Status da Atividade": "-",
            "Tipo de Atividade": "-",
        }
    )

    dados.append(
        {
            "Data": "Resumo",
            "Papel": "Atuações voluntárias",
            "Descrição": relatorio.resumo.total_voluntarios,
            "Atividade": "-",
            "Curso": "-",
            "Turma": "-",
            "Status de Presença": "-",
            "Status da Atividade": "-",
            "Tipo de Atividade": "-",
        }
    )

    dados.append(
        {
            "Data": "Resumo",
            "Papel": "Atuações em instrução",
            "Descrição": relatorio.resumo.total_instrucao,
            "Atividade": "-",
            "Curso": "-",
            "Turma": "-",
            "Status de Presença": "-",
            "Status da Atividade": "-",
            "Tipo de Atividade": "-",
        }
    )

    distribuicao = "; ".join(
        f"{papel}: {quantidade}"
        for papel, quantidade in relatorio.resumo.eventos_por_papel.items()
    )

    dados.append(
        {
            "Data": "Resumo",
            "Papel": "Eventos por papel",
            "Descrição": distribuicao or "-",
            "Atividade": "-",
            "Curso": "-",
            "Turma": "-",
            "Status de Presença": "-",
            "Status da Atividade": "-",
            "Tipo de Atividade": "-",
        }
    )

    df = pd.DataFrame(dados)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_historico_aluno.xlsx"'
    )

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Historico", index=False)

    return response


def _exportar_historico_pdf(relatorio, filtros, descricao_filtros):
    """Gera saída em HTML para pré-visualização do relatório histórico."""

    from django.template.loader import get_template

    template = get_template("atividades/relatorio_historico_aluno_pdf.html")
    context = {
        **_cabecalho_relatorio(TITULO_RELATORIO_HISTORICO),
        "relatorio": relatorio,
        "filtros": filtros,
        "descricao_filtros": descricao_filtros,
    }

    html = template.render(context)
    response = HttpResponse(html, content_type="text/html")
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_historico_aluno.pdf"'
    )
    return response


def _exportar_frequencia_csv(relatorio):
    """Gera arquivo CSV do relatório de frequência."""

    import csv

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_frequencia_turma.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "Aluno",
            "Curso",
            "Turma",
            "Total de Atividades",
            "Presenças",
            "Faltas",
            "Percentual de Presença (%)",
            "Carências",
            "Liberado",
            "Status",
        ]
    )

    for linha in relatorio.linhas:
        writer.writerow(
            [
                linha.aluno_nome,
                linha.curso_nome,
                linha.turma_nome,
                linha.total_atividades,
                linha.presentes,
                linha.faltas,
                f"{linha.percentual_presenca:.2f}",
                linha.numero_carencias,
                "Sim" if linha.liberado else "Não",
                linha.status_carencia or "-",
            ]
        )

    writer.writerow([])
    writer.writerow(
        [
            "Resumo",
            relatorio.resumo.total_alunos,
            relatorio.resumo.alunos_liberados,
            relatorio.resumo.alunos_com_carencia,
            relatorio.resumo.total_atividades,
            relatorio.resumo.total_presencas,
            relatorio.resumo.total_faltas,
            f"{relatorio.resumo.percentual_presenca_medio:.2f}",
            "-",
            "-",
        ]
    )

    return response


def _exportar_frequencia_excel(relatorio):
    """Gera arquivo Excel do relatório de frequência."""

    try:
        import pandas as pd
    except ImportError:
        logger.error("Pandas não está instalado")
        return HttpResponse("Erro: Pandas não está instalado", status=500)

    dados = []
    for linha in relatorio.linhas:
        dados.append(
            {
                "Aluno": linha.aluno_nome,
                "Curso": linha.curso_nome,
                "Turma": linha.turma_nome,
                "Total de Atividades": linha.total_atividades,
                "Presenças": linha.presentes,
                "Faltas": linha.faltas,
                "Percentual de Presença (%)": linha.percentual_presenca,
                "Carências": linha.numero_carencias,
                "Liberado": "Sim" if linha.liberado else "Não",
                "Status": linha.status_carencia or "-",
            }
        )

    dados.append(
        {
            "Aluno": "Resumo",
            "Curso": "Total Alunos",
            "Turma": relatorio.resumo.total_alunos,
            "Total de Atividades": relatorio.resumo.total_atividades,
            "Presenças": relatorio.resumo.total_presencas,
            "Faltas": relatorio.resumo.total_faltas,
            "Percentual de Presença (%)": relatorio.resumo.percentual_presenca_medio,
            "Carências": relatorio.resumo.alunos_com_carencia,
            "Liberado": relatorio.resumo.alunos_liberados,
            "Status": "-",
        }
    )

    df = pd.DataFrame(dados)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_frequencia_turma.xlsx"'
    )

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Frequencia", index=False)

    return response


def _exportar_frequencia_pdf(relatorio, filtros, descricao_filtros):
    """Gera saída em HTML para pré-visualização de PDF do relatório de frequência."""

    from django.template.loader import get_template

    template = get_template("atividades/relatorio_frequencia_turma.html")
    context = {
        **_cabecalho_relatorio(TITULO_RELATORIO_FREQUENCIA),
        "relatorio": relatorio,
        "filtros": filtros,
        "descricao_filtros": descricao_filtros,
        "cursos": [],
        "turmas": [],
        "meses": [],
        "anos": [],
        "status_carencia_choices": [],
        "query_params": "",
    }

    html = template.render(context)
    response = HttpResponse(html, content_type="text/html")
    response["Content-Disposition"] = (
        'attachment; filename="relatorio_frequencia_turma.pdf"'
    )
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
