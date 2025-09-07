# c:/omaum/presencas/views_reports.py
from importlib import import_module
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
import csv


def _get_reporting_service():
    """ObtÃƒÂ©m o mÃƒÂ³dulo de serviÃƒÂ§os de relatÃƒÂ³rios."""
    try:
        return import_module("presencas.services.reporting")
    except ImportError:
        # Fallback para desenvolvimento/testes
        class MockReporting:
            def get_boletim_frequencia_aluno(self, *args, **kwargs):
                return {"alunos": [], "estatisticas": {}, "sucesso": False}

            def csv_boletim_frequencia_aluno(self, *args, **kwargs):
                return "Aluno,Turma,PresenÃƒÂ§a\nSem dados,Sem dados,0"

            def get_consolidado_frequencia_turma(self, *args, **kwargs):
                return {"turmas": [], "estatisticas": {}, "sucesso": False}

            def csv_consolidado_frequencia_turma(self, *args, **kwargs):
                return "Turma,Total,Presentes\nSem dados,0,0"

            def get_alunos_em_risco(self, *args, **kwargs):
                return {"alunos": [], "estatisticas": {}, "sucesso": False}

            def csv_alunos_em_risco(self, *args, **kwargs):
                return "Aluno,Risco\nSem dados,0"

        return MockReporting()


def _get_analytics_service():
    """ObtÃƒÂ©m o mÃƒÂ³dulo de serviÃƒÂ§os de analytics (Categoria 4)."""
    try:
        return import_module("presencas.services.analytics")
    except ImportError:
        # Fallback para desenvolvimento/testes
        class MockAnalytics:
            def get_previsao_evasao(self, *args, **kwargs):
                return {"alunos": [], "estatisticas": {}, "sucesso": False}

            def csv_previsao_evasao(self, *args, **kwargs):
                return "Aluno,Turma,Score Risco\nSem dados,Sem dados,0"

            def get_intervencoes_automaticas(self, *args, **kwargs):
                return {"intervencoes": {}, "estatisticas": {}, "sucesso": False}

            def csv_intervencoes_automaticas(self, *args, **kwargs):
                return "Categoria,Aluno,AÃƒÂ§ÃƒÂ£o\nSem dados,Sem dados,Sem dados"

            def get_correlacao_presenca_desempenho(self, *args, **kwargs):
                return {"correlacoes": [], "estatisticas": {}, "sucesso": False}

            def csv_correlacao_presenca_desempenho(self, *args, **kwargs):
                return "Aluno,PresenÃƒÂ§a,Desempenho\nSem dados,0,0"

        return MockAnalytics()


def _get_administrative_service():
    """ObtÃƒÂ©m o mÃƒÂ³dulo de serviÃƒÂ§os administrativos (Categoria 5)."""
    try:
        return import_module("presencas.services.administrative")
    except ImportError:
        # Fallback para desenvolvimento/testes
        class MockAdministrative:
            def get_dashboard_coordenacao(self, *args, **kwargs):
                return {"estatisticas_gerais": {}, "dados_turmas": [], "sucesso": False}

            def csv_dashboard_coordenacao(self, *args, **kwargs):
                return "Turma,Curso,Alunos\nSem dados,Sem dados,0"

            def get_dashboard_direcao(self, *args, **kwargs):
                return {
                    "estatisticas_institucionais": {},
                    "dados_cursos": [],
                    "sucesso": False,
                }

            def csv_dashboard_direcao(self, *args, **kwargs):
                return "Curso,Alunos,Performance\nSem dados,0,0"

            def get_metricas_professor(self, *args, **kwargs):
                return {
                    "estatisticas_professor": {},
                    "dados_turmas": [],
                    "sucesso": False,
                }

            def csv_metricas_professor(self, *args, **kwargs):
                return "Turma,Alunos,PresenÃƒÂ§a\nSem dados,0,0"

            def get_indicadores_qualidade(self, *args, **kwargs):
                return {
                    "indicadores_principais": {},
                    "indices_qualidade": {},
                    "sucesso": False,
                }

            def csv_indicadores_qualidade(self, *args, **kwargs):
                return "Indicador,Valor,Meta\nSem dados,0,0"

        return MockAdministrative()


# ===== CATEGORIA 5: RELATÃƒâ€œRIOS ADMINISTRATIVOS =====


def listar_dashboard_coordenacao(request):
    """Dashboard executivo para coordenaÃƒÂ§ÃƒÂ£o acadÃƒÂªmica."""
    try:
        admin = _get_administrative_service()
        contexto = admin.get_dashboard_coordenacao(
            turma_id=request.GET.get("turma_id"),
            curso_id=request.GET.get("curso_id"),
            periodo=request.GET.get("periodo"),
        )
        contexto["titulo"] = "Dashboard de CoordenaÃƒÂ§ÃƒÂ£o"
        return render(request, "presencas/dashboard_coordenacao.html", contexto)
    except Exception as e:
        contexto = {
            "titulo": "Dashboard de CoordenaÃƒÂ§ÃƒÂ£o",
            "erro": f"Erro ao carregar dados: {str(e)}",
            "estatisticas_gerais": {},
            "dados_turmas": [],
        }
        return render(request, "presencas/dashboard_coordenacao.html", contexto)


def filtrar_dashboard_coordenacao(request):
    """Filtro AJAX para dashboard de coordenaÃƒÂ§ÃƒÂ£o."""
    try:
        admin = _get_administrative_service()
        dados = admin.get_dashboard_coordenacao(
            turma_id=request.GET.get("turma_id"),
            curso_id=request.GET.get("curso_id"),
            periodo=request.GET.get("periodo"),
        )
        return JsonResponse(dados)
    except Exception as e:
        return JsonResponse(
            {"erro": str(e), "estatisticas_gerais": {}, "dados_turmas": []}
        )


def exportar_csv_dashboard_coordenacao(request):
    """Exporta dashboard de coordenaÃƒÂ§ÃƒÂ£o para CSV."""
    try:
        admin = _get_administrative_service()
        contexto = admin.get_dashboard_coordenacao(
            turma_id=request.GET.get("turma_id"),
            curso_id=request.GET.get("curso_id"),
            periodo=request.GET.get("periodo"),
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="dashboard_coordenacao.csv"'
        )

        csv_content = admin.csv_dashboard_coordenacao(contexto)
        response.write(csv_content)
        return response
    except Exception as e:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="dashboard_coordenacao_erro.csv"'
        )
        response.write(f"Erro,{str(e)}")
        return response


def listar_dashboard_direcao(request):
    """Dashboard executivo para direÃƒÂ§ÃƒÂ£o institucional."""
    try:
        admin = _get_administrative_service()
        contexto = admin.get_dashboard_direcao(
            curso_id=request.GET.get("curso_id"), ano=request.GET.get("ano")
        )
        contexto["titulo"] = "Dashboard de DireÃƒÂ§ÃƒÂ£o"
        return render(request, "presencas/dashboard_direcao.html", contexto)
    except Exception as e:
        contexto = {
            "titulo": "Dashboard de DireÃƒÂ§ÃƒÂ£o",
            "erro": f"Erro ao carregar dados: {str(e)}",
            "estatisticas_institucionais": {},
            "dados_cursos": [],
        }
        return render(request, "presencas/dashboard_direcao.html", contexto)


def filtrar_dashboard_direcao(request):
    """Filtro AJAX para dashboard de direÃƒÂ§ÃƒÂ£o."""
    try:
        admin = _get_administrative_service()
        dados = admin.get_dashboard_direcao(
            curso_id=request.GET.get("curso_id"), ano=request.GET.get("ano")
        )
        return JsonResponse(dados)
    except Exception as e:
        return JsonResponse(
            {"erro": str(e), "estatisticas_institucionais": {}, "dados_cursos": []}
        )


def exportar_csv_dashboard_direcao(request):
    """Exporta dashboard de direÃƒÂ§ÃƒÂ£o para CSV."""
    try:
        admin = _get_administrative_service()
        contexto = admin.get_dashboard_direcao(
            curso_id=request.GET.get("curso_id"), ano=request.GET.get("ano")
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="dashboard_direcao.csv"'

        csv_content = admin.csv_dashboard_direcao(contexto)
        response.write(csv_content)
        return response
    except Exception as e:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="dashboard_direcao_erro.csv"'
        )
        response.write(f"Erro,{str(e)}")
        return response


def listar_metricas_professor(request):
    """MÃƒÂ©tricas por professor/disciplina."""
    try:
        admin = _get_administrative_service()
        contexto = admin.get_metricas_professor(
            professor_id=request.GET.get("professor_id"),
            disciplina=request.GET.get("disciplina"),
            periodo=request.GET.get("periodo"),
        )
        contexto["titulo"] = "MÃƒÂ©tricas por Professor"
        return render(request, "presencas/metricas_professor.html", contexto)
    except Exception as e:
        contexto = {
            "titulo": "MÃƒÂ©tricas por Professor",
            "erro": f"Erro ao carregar dados: {str(e)}",
            "estatisticas_professor": {},
            "dados_turmas": [],
        }
        return render(request, "presencas/metricas_professor.html", contexto)


def filtrar_metricas_professor(request):
    """Filtro AJAX para mÃƒÂ©tricas de professor."""
    try:
        admin = _get_administrative_service()
        dados = admin.get_metricas_professor(
            professor_id=request.GET.get("professor_id"),
            disciplina=request.GET.get("disciplina"),
            periodo=request.GET.get("periodo"),
        )
        return JsonResponse(dados)
    except Exception as e:
        return JsonResponse(
            {"erro": str(e), "estatisticas_professor": {}, "dados_turmas": []}
        )


def exportar_csv_metricas_professor(request):
    """Exporta mÃƒÂ©tricas de professor para CSV."""
    try:
        admin = _get_administrative_service()
        contexto = admin.get_metricas_professor(
            professor_id=request.GET.get("professor_id"),
            disciplina=request.GET.get("disciplina"),
            periodo=request.GET.get("periodo"),
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="metricas_professor.csv"'
        )

        csv_content = admin.csv_metricas_professor(contexto)
        response.write(csv_content)
        return response
    except Exception as e:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="metricas_professor_erro.csv"'
        )
        response.write(f"Erro,{str(e)}")
        return response


def listar_indicadores_qualidade(request):
    """Indicadores de qualidade institucional."""
    try:
        admin = _get_administrative_service()
        contexto = admin.get_indicadores_qualidade()
        contexto["titulo"] = "Indicadores de Qualidade"
        return render(request, "presencas/indicadores_qualidade.html", contexto)
    except Exception as e:
        contexto = {
            "titulo": "Indicadores de Qualidade",
            "erro": f"Erro ao carregar dados: {str(e)}",
            "indicadores_principais": {},
            "indices_qualidade": {},
        }
        return render(request, "presencas/indicadores_qualidade.html", contexto)


def exportar_csv_indicadores_qualidade(request):
    """Exporta indicadores de qualidade para CSV."""
    try:
        admin = _get_administrative_service()
        contexto = admin.get_indicadores_qualidade()

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="indicadores_qualidade.csv"'
        )

        csv_content = admin.csv_indicadores_qualidade(contexto)
        response.write(csv_content)
        return response
    except Exception as e:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="indicadores_qualidade_erro.csv"'
        )
        response.write(f"Erro,{str(e)}")
        return response


# ===== CATEGORIA 4: RELATÃƒâ€œRIOS PREDITIVOS (MACHINE LEARNING) =====


def listar_previsao_evasao(request):
    """Lista previsÃƒÂ£o de evasÃƒÂ£o baseada em ML."""
    try:
        analytics = _get_analytics_service()
        contexto = analytics.get_previsao_evasao(
            turma_id=request.GET.get("turma_id"),
            ano=request.GET.get("ano"),
            limite_risco=request.GET.get("limite_risco", 60),
        )
        contexto["titulo"] = "PrevisÃƒÂ£o de EvasÃƒÂ£o (Machine Learning)"
        return render(request, "presencas/previsao_evasao.html", contexto)
    except Exception as e:
        contexto = {
            "titulo": "PrevisÃƒÂ£o de EvasÃƒÂ£o (Machine Learning)",
            "erro": f"Erro ao carregar dados: {str(e)}",
            "alunos": [],
            "estatisticas": {},
        }
        return render(request, "presencas/previsao_evasao.html", contexto)


def filtrar_previsao_evasao(request):
    """Filtro AJAX para previsÃƒÂ£o de evasÃƒÂ£o."""
    try:
        analytics = _get_analytics_service()
        dados = analytics.get_previsao_evasao(
            turma_id=request.GET.get("turma_id"),
            ano=request.GET.get("ano"),
            limite_risco=request.GET.get("limite_risco", 60),
        )
        return JsonResponse(dados)
    except Exception as e:
        return JsonResponse({"erro": str(e), "alunos": [], "estatisticas": {}})


def exportar_csv_previsao_evasao(request):
    """Exporta previsÃƒÂ£o de evasÃƒÂ£o para CSV."""
    try:
        analytics = _get_analytics_service()
        contexto = analytics.get_previsao_evasao(
            turma_id=request.GET.get("turma_id"),
            ano=request.GET.get("ano"),
            limite_risco=request.GET.get("limite_risco", 60),
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="previsao_evasao.csv"'

        csv_content = analytics.csv_previsao_evasao(contexto)
        response.write(csv_content)
        return response
    except Exception as e:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="previsao_evasao_erro.csv"'
        )
        response.write(f"Erro,{str(e)}")
        return response


def listar_intervencoes_automaticas(request):
    """Lista intervenÃƒÂ§ÃƒÂµes automÃƒÂ¡ticas sugeridas por ML."""
    try:
        analytics = _get_analytics_service()
        contexto = analytics.get_intervencoes_automaticas(
            turma_id=request.GET.get("turma_id"),
            ano=request.GET.get("ano"),
            urgencia=request.GET.get("urgencia"),
        )
        contexto["titulo"] = "IntervenÃƒÂ§ÃƒÂµes AutomÃƒÂ¡ticas (IA)"
        return render(request, "presencas/intervencoes_automaticas.html", contexto)
    except Exception as e:
        contexto = {
            "titulo": "IntervenÃƒÂ§ÃƒÂµes AutomÃƒÂ¡ticas (IA)",
            "erro": f"Erro ao carregar dados: {str(e)}",
            "intervencoes": {},
            "estatisticas": {},
        }
        return render(request, "presencas/intervencoes_automaticas.html", contexto)


def filtrar_intervencoes_automaticas(request):
    """Filtro AJAX para intervenÃƒÂ§ÃƒÂµes automÃƒÂ¡ticas."""
    try:
        analytics = _get_analytics_service()
        dados = analytics.get_intervencoes_automaticas(
            turma_id=request.GET.get("turma_id"),
            ano=request.GET.get("ano"),
            urgencia=request.GET.get("urgencia"),
        )
        return JsonResponse(dados)
    except Exception as e:
        return JsonResponse({"erro": str(e), "intervencoes": {}, "estatisticas": {}})


def exportar_csv_intervencoes_automaticas(request):
    """Exporta intervenÃƒÂ§ÃƒÂµes automÃƒÂ¡ticas para CSV."""
    try:
        analytics = _get_analytics_service()
        contexto = analytics.get_intervencoes_automaticas(
            turma_id=request.GET.get("turma_id"),
            ano=request.GET.get("ano"),
            urgencia=request.GET.get("urgencia"),
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="intervencoes_automaticas.csv"'
        )

        csv_content = analytics.csv_intervencoes_automaticas(contexto)
        response.write(csv_content)
        return response
    except Exception as e:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="intervencoes_automaticas_erro.csv"'
        )
        response.write(f"Erro,{str(e)}")
        return response


def listar_correlacao_presenca_desempenho(request):
    """Lista correlaÃƒÂ§ÃƒÂ£o entre presenÃƒÂ§a e desempenho."""
    try:
        analytics = _get_analytics_service()
        contexto = analytics.get_correlacao_presenca_desempenho(
            turma_id=request.GET.get("turma_id"),
            ano=request.GET.get("ano"),
            disciplina=request.GET.get("disciplina"),
        )
        contexto["titulo"] = "CorrelaÃƒÂ§ÃƒÂ£o PresenÃƒÂ§a-Desempenho"
        return render(
            request, "presencas/correlacao_presenca_desempenho.html", contexto
        )
    except Exception as e:
        contexto = {
            "titulo": "CorrelaÃƒÂ§ÃƒÂ£o PresenÃƒÂ§a-Desempenho",
            "erro": f"Erro ao carregar dados: {str(e)}",
            "correlacoes": [],
            "estatisticas": {},
        }
        return render(
            request, "presencas/correlacao_presenca_desempenho.html", contexto
        )


def filtrar_correlacao_presenca_desempenho(request):
    """Filtro AJAX para correlaÃƒÂ§ÃƒÂ£o presenÃƒÂ§a-desempenho."""
    try:
        analytics = _get_analytics_service()
        dados = analytics.get_correlacao_presenca_desempenho(
            turma_id=request.GET.get("turma_id"),
            ano=request.GET.get("ano"),
            disciplina=request.GET.get("disciplina"),
        )
        return JsonResponse(dados)
    except Exception as e:
        return JsonResponse({"erro": str(e), "correlacoes": [], "estatisticas": {}})


def exportar_csv_correlacao_presenca_desempenho(request):
    """Exporta correlaÃƒÂ§ÃƒÂ£o presenÃƒÂ§a-desempenho para CSV."""
    try:
        analytics = _get_analytics_service()
        contexto = analytics.get_correlacao_presenca_desempenho(
            turma_id=request.GET.get("turma_id"),
            ano=request.GET.get("ano"),
            disciplina=request.GET.get("disciplina"),
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="correlacao_presenca_desempenho.csv"'
        )

        csv_content = analytics.csv_correlacao_presenca_desempenho(contexto)
        response.write(csv_content)
        return response
    except Exception as e:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="correlacao_presenca_desempenho_erro.csv"'
        )
        response.write(f"Erro,{str(e)}")
        return response


def _get_reporting_service():
    """ObtÃƒÂ©m o mÃƒÂ³dulo de serviÃƒÂ§os de relatÃƒÂ³rios."""
    try:
        return import_module("presencas.services.reporting")
    except ImportError:
        # Fallback para desenvolvimento/testes
        class MockReporting:
            def get_boletim_aluno(self, *args, **kwargs):
                return {"aluno_id": None, "linhas": []}

            def csv_boletim_aluno(self, *args, **kwargs):
                return ([], ["Sem dados"], "mock.csv")

            def get_consolidado_turma(self, *args, **kwargs):
                return {"turma_id": None, "linhas": []}

            def csv_consolidado_turma(self, *args, **kwargs):
                return ([], ["Sem dados"], "mock.csv")

            def get_alunos_em_risco(self, *args, **kwargs):
                return {"alunos_em_risco": [], "total_alunos_risco": 0}

            def csv_alunos_em_risco(self, *args, **kwargs):
                return ([], ["Sem dados"], "mock.csv")

            def get_ranking_engajamento(self, *args, **kwargs):
                return {"ranking": [], "total_participantes": 0}

            def csv_ranking_engajamento(self, *args, **kwargs):
                return ([], ["Sem dados"], "mock.csv")

            def get_comparativo_frequencias(self, *args, **kwargs):
                return {"comparativo": [], "total_alunos": 0}

            def csv_comparativo_frequencias(self, *args, **kwargs):
                return ([], ["Sem dados"], "mock.csv")

            def get_dashboard_presencas(self, *args, **kwargs):
                return {
                    "kpis": {},
                    "top_turmas": [],
                    "evolucao_mensal": [],
                    "dados_json": {},
                }

            def csv_dashboard_presencas(self, *args, **kwargs):
                return ([], ["Sem dados"], "mock.csv")

        return MockReporting()


# ===== CATEGORIA 2: RELATÃƒâ€œRIOS DE CONSOLIDAÃƒâ€¡ÃƒÆ’O =====


def listar_boletim_frequencia_aluno(request):
    """Lista boletim de frequÃƒÂªncia do aluno com filtros."""
    reporting = _get_reporting_service()

    # ParÃƒÂ¢metros de filtro
    aluno_id = request.GET.get("aluno_id")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")
    export_csv = request.GET.get("export") == "csv"

    # Obter dados
    contexto = reporting.get_boletim_aluno(aluno_id, mes, ano)

    if export_csv:
        # Retorna CSV
        rows, headers, filename = reporting.csv_boletim_aluno(contexto)

        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = f'attachment; filename="{smart_str(filename)}"'

        writer = csv.writer(resp)
        writer.writerow(headers)
        writer.writerows(rows)
        return resp

    # Retorna HTML
    return render(request, "presencas/boletim_frequencia_aluno.html", contexto)


def filtrar_boletim_frequencia_aluno(request):
    """AJAX: Filtra boletim de frequÃƒÂªncia do aluno."""
    reporting = _get_reporting_service()

    aluno_id = request.GET.get("aluno_id")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")

    contexto = reporting.get_boletim_aluno(aluno_id, mes, ano)

    return render(
        request, "presencas/partials/boletim_frequencia_aluno_partial.html", contexto
    )


def listar_consolidado_frequencia_turma(request):
    """Lista consolidado de frequÃƒÂªncia da turma com filtros."""
    reporting = _get_reporting_service()

    # ParÃƒÂ¢metros de filtro
    turma_id = request.GET.get("turma_id")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")
    export_csv = request.GET.get("export") == "csv"

    # Obter dados
    contexto = reporting.get_consolidado_turma(turma_id, mes, ano)

    if export_csv:
        # Retorna CSV
        rows, headers, filename = reporting.csv_consolidado_turma(contexto)

        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = f'attachment; filename="{smart_str(filename)}"'

        writer = csv.writer(resp)
        writer.writerow(headers)
        writer.writerows(rows)
        return resp

    # Retorna HTML
    return render(request, "presencas/consolidado_frequencia_turma.html", contexto)


def filtrar_consolidado_frequencia_turma(request):
    """AJAX: Filtra consolidado de frequÃƒÂªncia da turma."""
    reporting = _get_reporting_service()

    turma_id = request.GET.get("turma_id")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")

    contexto = reporting.get_consolidado_turma(turma_id, mes, ano)

    return render(
        request,
        "presencas/partials/consolidado_frequencia_turma_partial.html",
        contexto,
    )


# ===== CATEGORIA 3: RELATÃƒâ€œRIOS ANALÃƒÂTICOS =====


def listar_alunos_em_risco(request):
    """Lista alunos em risco com filtros."""
    reporting = _get_reporting_service()

    # ParÃƒÂ¢metros de filtro
    turma_id = request.GET.get("turma_id")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")
    nivel_carencia = request.GET.get("nivel_carencia", 1)
    export_csv = request.GET.get("export") == "csv"

    # Obter dados
    contexto = reporting.get_alunos_em_risco(turma_id, mes, ano, nivel_carencia)

    if export_csv:
        # Retorna CSV
        rows, headers, filename = reporting.csv_alunos_em_risco(contexto)

        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = f'attachment; filename="{smart_str(filename)}"'

        writer = csv.writer(resp)
        writer.writerow(headers)
        writer.writerows(rows)
        return resp

    # Retorna HTML
    return render(request, "presencas/alunos_em_risco.html", contexto)


def filtrar_alunos_em_risco(request):
    """AJAX: Filtra alunos em risco."""
    reporting = _get_reporting_service()

    turma_id = request.GET.get("turma_id")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")
    nivel_carencia = request.GET.get("nivel_carencia", 1)

    contexto = reporting.get_alunos_em_risco(turma_id, mes, ano, nivel_carencia)

    return render(request, "presencas/partials/alunos_em_risco_partial.html", contexto)


def listar_ranking_engajamento(request):
    """Lista ranking de engajamento com filtros."""
    reporting = _get_reporting_service()

    # ParÃƒÂ¢metros de filtro
    turma_id = request.GET.get("turma_id")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")
    export_csv = request.GET.get("export") == "csv"

    # Obter dados
    contexto = reporting.get_ranking_engajamento(turma_id, mes, ano)

    if export_csv:
        # Retorna CSV
        rows, headers, filename = reporting.csv_ranking_engajamento(contexto)

        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = f'attachment; filename="{smart_str(filename)}"'

        writer = csv.writer(resp)
        writer.writerow(headers)
        writer.writerows(rows)
        return resp

    # Retorna HTML
    return render(request, "presencas/ranking_engajamento.html", contexto)


def filtrar_ranking_engajamento(request):
    """AJAX: Filtra ranking de engajamento."""
    reporting = _get_reporting_service()

    turma_id = request.GET.get("turma_id")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")

    contexto = reporting.get_ranking_engajamento(turma_id, mes, ano)

    return render(
        request, "presencas/partials/ranking_engajamento_partial.html", contexto
    )


def listar_comparativo_frequencia(request):
    """Lista comparativo de frequÃƒÂªncia entre dois perÃƒÂ­odos."""
    reporting = _get_reporting_service()

    # ParÃƒÂ¢metros de filtro
    turma_id = request.GET.get("turma_id")
    mes1 = request.GET.get("mes1")
    ano1 = request.GET.get("ano1")
    mes2 = request.GET.get("mes2")
    ano2 = request.GET.get("ano2")
    export_csv = request.GET.get("export") == "csv"

    # Validar perÃƒÂ­odos
    contexto = {}
    if mes1 and ano1 and mes2 and ano2:
        try:
            periodo1 = (int(mes1), int(ano1))
            periodo2 = (int(mes2), int(ano2))
            contexto = reporting.get_comparativo_frequencias(
                turma_id, periodo1, periodo2
            )
        except (ValueError, TypeError):
            pass

    if export_csv and contexto.get("comparativo"):
        # Retorna CSV
        rows, headers, filename = reporting.csv_comparativo_frequencias(contexto)

        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = f'attachment; filename="{smart_str(filename)}"'

        writer = csv.writer(resp)
        writer.writerow(headers)
        writer.writerows(rows)
        return resp

    # Retorna HTML
    return render(request, "presencas/comparativo_frequencia.html", contexto)


def filtrar_comparativo_frequencia(request):
    """AJAX: Filtra comparativo de frequÃƒÂªncia."""
    reporting = _get_reporting_service()

    turma_id = request.GET.get("turma_id")
    mes1 = request.GET.get("mes1")
    ano1 = request.GET.get("ano1")
    mes2 = request.GET.get("mes2")
    ano2 = request.GET.get("ano2")

    # Validar perÃƒÂ­odos
    contexto = {}
    if mes1 and ano1 and mes2 and ano2:
        try:
            periodo1 = (int(mes1), int(ano1))
            periodo2 = (int(mes2), int(ano2))
            contexto = reporting.get_comparativo_frequencias(
                turma_id, periodo1, periodo2
            )
        except (ValueError, TypeError):
            pass

    return render(
        request, "presencas/partials/comparativo_frequencia_partial.html", contexto
    )


def listar_dashboard_presencas(request):
    """Lista dashboard executivo."""
    reporting = _get_reporting_service()

    export_csv = request.GET.get("export") == "csv"

    # Obter dados
    contexto = reporting.get_dashboard_presencas()

    if export_csv:
        # Retorna CSV
        rows, headers, filename = reporting.csv_dashboard_presencas(contexto)

        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = f'attachment; filename="{smart_str(filename)}"'

        writer = csv.writer(resp)
        writer.writerow(headers)
        writer.writerows(rows)
        return resp

    # Retorna HTML
    return render(request, "presencas/dashboard_presencas.html", contexto)


def filtrar_dashboard_presencas(request):
    """AJAX: Atualiza dashboard."""
    reporting = _get_reporting_service()

    contexto = reporting.get_dashboard_presencas()

    return render(
        request, "presencas/partials/dashboard_presencas_partial.html", contexto
    )


# ===== AJAX ENDPOINTS PARA FILTROS DINÃƒâ€šMICOS =====


def ajax_turmas(request):
    """Retorna lista de turmas para filtros dinÃƒÂ¢micos."""
    try:
        Turma = getattr(import_module("turmas.models"), "Turma", None)
        if Turma:
            turmas = list(Turma.objects.all().values("id", "nome").order_by("nome"))
        else:
            turmas = []
    except Exception:
        turmas = []

    return JsonResponse({"turmas": turmas})


def ajax_anos(request):
    """Retorna lista de anos disponÃƒÂ­veis para filtros dinÃƒÂ¢micos."""
    from datetime import date

    # Anos disponÃƒÂ­veis (ÃƒÂºltimos 5 anos + prÃƒÂ³ximo ano)
    ano_atual = date.today().year
    anos = []
    for ano in range(ano_atual - 4, ano_atual + 2):
        anos.append({"ano": ano, "label": str(ano)})

    return JsonResponse({"anos": anos})


def ajax_alunos(request):
    """Retorna lista de alunos por turma para filtros dinÃƒÂ¢micos."""
    turma_id = request.GET.get("turma_id")

    try:
        Aluno = getattr(import_module("alunos.models"), "Aluno", None)
        if Aluno and turma_id:
            alunos = list(
                Aluno.objects.filter(turma_id=turma_id)
                .values("id", "nome")
                .order_by("nome")
            )
        else:
            alunos = []
    except Exception:
        alunos = []

    return JsonResponse({"alunos": alunos})
