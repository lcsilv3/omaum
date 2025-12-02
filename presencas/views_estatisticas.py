"""
Views para estatísticas de presença usando o CalculadoraEstatisticas.
"""

import logging
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils import timezone

from .services.calculadora_estatisticas import CalculadoraEstatisticas
from .models import PresencaDetalhada, ConfiguracaoPresenca
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET"])
def consolidado_aluno(request, aluno_id):
    """
    FASE 3B: Retorna consolidado de presença com cache inteligente.

    Parâmetros GET:
    - turma_id: ID da turma (opcional)
    - atividade_id: ID da atividade (opcional)
    - periodo_inicio: Data início (YYYY-MM-DD)
    - periodo_fim: Data fim (YYYY-MM-DD)
    - formato: 'json' ou 'html' (padrão: json)
    """
    try:
        # Cache baseado nos parâmetros da requisição
        params = request.GET.copy()
        cache_key = f"consolidado_aluno_{aluno_id}_{hash(str(sorted(params.items())))}"

        cached_result = cache.get(cache_key)
        if cached_result:
            logger.debug(f"Cache hit para consolidado_aluno: {cache_key}")
            if params.get("formato") == "html":
                return render(
                    request,
                    "presencas/consolidado_aluno.html",
                    cached_result["context"],
                )
            return JsonResponse(cached_result["data"])

        # Verificar se aluno existe com query otimizada
        aluno = get_object_or_404(Aluno.objects.select_related("curso"), id=aluno_id)

        # Obter parâmetros da requisição
        turma_id = request.GET.get("turma_id")
        atividade_id = request.GET.get("atividade_id")
        periodo_inicio = request.GET.get("periodo_inicio")
        periodo_fim = request.GET.get("periodo_fim")
        formato = request.GET.get("formato", "json")

        # Converter datas
        if periodo_inicio:
            periodo_inicio = datetime.strptime(periodo_inicio, "%Y-%m-%d").date()
        if periodo_fim:
            periodo_fim = datetime.strptime(periodo_fim, "%Y-%m-%d").date()

        # Calcular consolidado
        consolidado = CalculadoraEstatisticas.calcular_consolidado_aluno(
            aluno_id=aluno_id,
            turma_id=int(turma_id) if turma_id else None,
            atividade_id=int(atividade_id) if atividade_id else None,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
        )

        # Retornar resposta
        if formato == "html":
            return render(
                request,
                "presencas/consolidado_aluno.html",
                {
                    "consolidado": consolidado,
                    "aluno": aluno,
                    "titulo": f"Consolidado de Presença - {aluno.nome}",
                },
            )
        else:
            return JsonResponse(consolidado, safe=False)

    except ValidationError as e:
        logger.error(f"Erro de validação no consolidado do aluno {aluno_id}: {str(e)}")
        return JsonResponse({"erro": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro no consolidado do aluno {aluno_id}: {str(e)}")
        return JsonResponse({"erro": "Erro interno do servidor"}, status=500)


@login_required
@require_http_methods(["GET"])
def tabela_consolidada(request):
    """
    Gera tabela consolidada de presença (replicando Excel).

    Parâmetros GET:
    - turma_id: ID da turma (opcional)
    - atividade_id: ID da atividade (opcional)
    - periodo_inicio: Data início (YYYY-MM-DD)
    - periodo_fim: Data fim (YYYY-MM-DD)
    - ordenar_por: 'nome', 'percentual', 'carencias' (padrão: nome)
    - formato: 'json' ou 'html' (padrão: json)
    """
    try:
        # Obter parâmetros
        turma_id = request.GET.get("turma_id")
        atividade_id = request.GET.get("atividade_id")
        periodo_inicio = request.GET.get("periodo_inicio")
        periodo_fim = request.GET.get("periodo_fim")
        ordenar_por = request.GET.get("ordenar_por", "nome")
        formato = request.GET.get("formato", "json")

        # Validar ordenação
        if ordenar_por not in ["nome", "percentual", "carencias"]:
            ordenar_por = "nome"

        # Converter datas
        if periodo_inicio:
            periodo_inicio = datetime.strptime(periodo_inicio, "%Y-%m-%d").date()
        if periodo_fim:
            periodo_fim = datetime.strptime(periodo_fim, "%Y-%m-%d").date()

        # Gerar tabela
        tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
            turma_id=int(turma_id) if turma_id else None,
            atividade_id=int(atividade_id) if atividade_id else None,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
            ordenar_por=ordenar_por,
        )

        # Retornar resposta
        if formato == "html":
            # Obter dados para o template
            turma = None
            atividade = None

            if turma_id:
                turma = get_object_or_404(Turma, id=turma_id)
            if atividade_id:
                atividade = get_object_or_404(Atividade, id=atividade_id)

            return render(
                request,
                "presencas/tabela_consolidada.html",
                {
                    "tabela": tabela,
                    "turma": turma,
                    "atividade": atividade,
                    "filtros": {
                        "turma_id": turma_id,
                        "atividade_id": atividade_id,
                        "periodo_inicio": periodo_inicio,
                        "periodo_fim": periodo_fim,
                        "ordenar_por": ordenar_por,
                    },
                    "titulo": "Tabela Consolidada de Presença",
                },
            )
        else:
            return JsonResponse(tabela, safe=False)

    except ValidationError as e:
        logger.error(f"Erro de validação na tabela consolidada: {str(e)}")
        return JsonResponse({"erro": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro na tabela consolidada: {str(e)}")
        return JsonResponse({"erro": "Erro interno do servidor"}, status=500)


@login_required
@require_http_methods(["GET"])
def estatisticas_turma(request, turma_id):
    """
    Retorna estatísticas consolidadas de uma turma.

    Parâmetros GET:
    - periodo_inicio: Data início (YYYY-MM-DD)
    - periodo_fim: Data fim (YYYY-MM-DD)
    - formato: 'json' ou 'html' (padrão: json)
    """
    try:
        # Verificar se turma existe
        turma = get_object_or_404(Turma, id=turma_id)

        # Obter parâmetros
        periodo_inicio = request.GET.get("periodo_inicio")
        periodo_fim = request.GET.get("periodo_fim")
        formato = request.GET.get("formato", "json")

        # Converter datas
        if periodo_inicio:
            periodo_inicio = datetime.strptime(periodo_inicio, "%Y-%m-%d").date()
        if periodo_fim:
            periodo_fim = datetime.strptime(periodo_fim, "%Y-%m-%d").date()

        # Calcular estatísticas
        estatisticas = CalculadoraEstatisticas.calcular_estatisticas_turma(
            turma_id=turma_id, periodo_inicio=periodo_inicio, periodo_fim=periodo_fim
        )

        # Retornar resposta
        if formato == "html":
            return render(
                request,
                "presencas/estatisticas_turma.html",
                {
                    "estatisticas": estatisticas,
                    "turma": turma,
                    "titulo": f"Estatísticas da Turma - {turma.nome}",
                },
            )
        else:
            return JsonResponse(estatisticas, safe=False)

    except ValidationError as e:
        logger.error(
            f"Erro de validação nas estatísticas da turma {turma_id}: {str(e)}"
        )
        return JsonResponse({"erro": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro nas estatísticas da turma {turma_id}: {str(e)}")
        return JsonResponse({"erro": "Erro interno do servidor"}, status=500)


@login_required
@require_http_methods(["POST"])
def recalcular_carencias(request):
    """
    Recalcula carências para um conjunto de presenças.

    Parâmetros POST:
    - turma_id: ID da turma (opcional)
    - atividade_id: ID da atividade (opcional)
    - periodo_inicio: Data início (YYYY-MM-DD)
    - periodo_fim: Data fim (YYYY-MM-DD)
    - presenca_ids: Lista de IDs de presenças específicas (opcional)
    """
    try:
        # Obter parâmetros
        turma_id = request.POST.get("turma_id")
        atividade_id = request.POST.get("atividade_id")
        periodo_inicio = request.POST.get("periodo_inicio")
        periodo_fim = request.POST.get("periodo_fim")
        presenca_ids = request.POST.getlist("presenca_ids")

        # Converter datas
        if periodo_inicio:
            periodo_inicio = datetime.strptime(periodo_inicio, "%Y-%m-%d").date()
        if periodo_fim:
            periodo_fim = datetime.strptime(periodo_fim, "%Y-%m-%d").date()

        # Recalcular carências específicas
        if presenca_ids:
            resultados = []
            for presenca_id in presenca_ids:
                try:
                    resultado = CalculadoraEstatisticas.calcular_carencias(
                        int(presenca_id), forcar_recalculo=True
                    )
                    resultados.append(resultado)
                except Exception as e:
                    resultados.append({"presenca_id": presenca_id, "erro": str(e)})

            return JsonResponse(
                {
                    "sucesso": True,
                    "resultados": resultados,
                    "total_processados": len(presenca_ids),
                }
            )

        # Recalcular todas as carências com filtros
        else:
            resultado = CalculadoraEstatisticas.recalcular_todas_carencias(
                turma_id=int(turma_id) if turma_id else None,
                atividade_id=int(atividade_id) if atividade_id else None,
                periodo_inicio=periodo_inicio,
                periodo_fim=periodo_fim,
            )

            return JsonResponse({"sucesso": True, "resultado": resultado})

    except ValidationError as e:
        logger.error(f"Erro de validação no recálculo de carências: {str(e)}")
        return JsonResponse({"erro": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro no recálculo de carências: {str(e)}")
        return JsonResponse({"erro": "Erro interno do servidor"}, status=500)


@login_required
@require_http_methods(["GET"])
def dashboard_presencas(request):
    """
    Dashboard com visão geral das presenças.
    """
    try:
        # Obter parâmetros
        turma_id = request.GET.get("turma_id")

        # Estatísticas gerais
        estatisticas_gerais = {}

        if turma_id:
            # Estatísticas da turma específica
            get_object_or_404(Turma, id=turma_id)
            estatisticas_gerais = CalculadoraEstatisticas.calcular_estatisticas_turma(
                turma_id=turma_id
            )
        else:
            # Estatísticas de todas as turmas
            turmas = Turma.objects.all()
            estatisticas_gerais = {
                "total_turmas": turmas.count(),
                "total_presencas": PresencaDetalhada.objects.count(),
                "total_alunos": Aluno.objects.count(),
                "total_atividades": Atividade.objects.count(),
                "data_calculo": timezone.now(),
            }

        # Últimas presenças registradas
        ultimas_presencas = PresencaDetalhada.objects.select_related(
            "aluno", "turma", "atividade"
        ).order_by("-data_atualizacao")[:10]

        # Configurações de presença
        configuracoes = ConfiguracaoPresenca.objects.select_related(
            "turma", "atividade"
        ).filter(ativo=True)[:10]

        return render(
            request,
            "presencas/dashboard.html",
            {
                "estatisticas_gerais": estatisticas_gerais,
                "ultimas_presencas": ultimas_presencas,
                "configuracoes": configuracoes,
                "turma_selecionada": turma_id,
                "titulo": "Dashboard de Presenças",
            },
        )

    except Exception as e:
        logger.error(f"Erro no dashboard de presenças: {str(e)}")
        return render(
            request,
            "presencas/dashboard.html",
            {"erro": "Erro ao carregar dashboard", "titulo": "Dashboard de Presenças"},
        )


@login_required
@require_http_methods(["GET"])
def exportar_consolidado(request):
    """
    Exporta consolidado de presença em formato CSV.
    """
    try:
        import csv
        from django.utils.text import slugify

        # Obter parâmetros (mesmo que tabela_consolidada)
        turma_id = request.GET.get("turma_id")
        atividade_id = request.GET.get("atividade_id")
        periodo_inicio = request.GET.get("periodo_inicio")
        periodo_fim = request.GET.get("periodo_fim")
        ordenar_por = request.GET.get("ordenar_por", "nome")

        # Converter datas
        if periodo_inicio:
            periodo_inicio = datetime.strptime(periodo_inicio, "%Y-%m-%d").date()
        if periodo_fim:
            periodo_fim = datetime.strptime(periodo_fim, "%Y-%m-%d").date()

        # Gerar tabela
        tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
            turma_id=int(turma_id) if turma_id else None,
            atividade_id=int(atividade_id) if atividade_id else None,
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
            ordenar_por=ordenar_por,
        )

        # Criar resposta CSV
        response = HttpResponse(content_type="text/csv")

        # Nome do arquivo
        nome_arquivo = "consolidado_presenca"
        if turma_id:
            turma = get_object_or_404(Turma, id=turma_id)
            nome_arquivo += f"_{slugify(turma.nome)}"
        if periodo_inicio:
            nome_arquivo += f"_{periodo_inicio.strftime('%Y%m%d')}"
        if periodo_fim:
            nome_arquivo += f"_{periodo_fim.strftime('%Y%m%d')}"

        response["Content-Disposition"] = f'attachment; filename="{nome_arquivo}.csv"'

        # Escrever CSV
        writer = csv.writer(response)

        # Cabeçalho
        writer.writerow(
            [
                "Aluno",
                "CPF",
                "Turma",
                "Convocações",
                "Presenças",
                "Faltas",
                "Percentual",
                "Voluntários Extra",
                "Voluntários Simples",
                "Total Voluntários",
                "Carências",
                "Status",
            ]
        )

        # Dados
        for linha in tabela["linhas"]:
            writer.writerow(
                [
                    linha["aluno"]["nome"],
                    linha["aluno"]["cpf"],
                    linha["turma"]["nome"] if linha["turma"] else "",
                    linha["totais"]["convocacoes"],
                    linha["totais"]["presencas"],
                    linha["totais"]["faltas"],
                    f"{linha['percentual_geral']:.2f}%",
                    linha["totais"]["voluntario_extra"],
                    linha["totais"]["voluntario_simples"],
                    linha["total_voluntarios"],
                    linha["totais"]["carencias"],
                    linha["status"],
                ]
            )

        # Estatísticas gerais
        writer.writerow([])
        writer.writerow(["ESTATÍSTICAS GERAIS"])
        writer.writerow(
            ["Total de Alunos", tabela["estatisticas_gerais"]["total_alunos"]]
        )
        writer.writerow(
            [
                "Percentual Médio",
                f"{tabela['estatisticas_gerais']['percentual_medio']:.2f}%",
            ]
        )
        writer.writerow(
            ["Total Convocações", tabela["estatisticas_gerais"]["total_convocacoes"]]
        )
        writer.writerow(
            ["Total Presenças", tabela["estatisticas_gerais"]["total_presencas"]]
        )
        writer.writerow(
            ["Total Carências", tabela["estatisticas_gerais"]["total_carencias"]]
        )

        return response

    except Exception as e:
        logger.error(f"Erro na exportação: {str(e)}")
        return JsonResponse({"erro": "Erro na exportação"}, status=500)
