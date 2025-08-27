"""
View para o painel de estatísticas do sistema de presenças.
Integra com CalculadoraEstatisticas para exibir gráficos e métricas visuais.
"""

import logging
from datetime import datetime, date, timedelta
from typing import Dict, List, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum
from django.utils import timezone
from django.contrib import messages

from ..services.calculadora_estatisticas import CalculadoraEstatisticas
from ..models import PresencaDetalhada

# Importação dinâmica de modelos
from importlib import import_module

logger = logging.getLogger(__name__)


def get_turma_model():
    """Obtém o modelo Turma dinamicamente."""
    turmas_module = import_module("turmas.models")
    return getattr(turmas_module, "Turma")


def get_atividade_model():
    """Obtém o modelo AtividadeAcademica dinamicamente."""
    atividades_module = import_module("atividades.models")
    return getattr(atividades_module, "AtividadeAcademica")


class PainelEstatisticasView(LoginRequiredMixin, TemplateView):
    """
    View principal do painel de estatísticas.
    Exibe gráficos, métricas e visualizações consolidadas.
    """

    template_name = "presencas/painel_estatisticas.html"

    def get_context_data(self, **kwargs):
        """Prepara dados para o painel de estatísticas."""
        context = super().get_context_data(**kwargs)

        try:
            # Filtros da requisição
            filtros = self._extrair_filtros()

            # Estatísticas principais
            context["metricas_principais"] = self._calcular_metricas_principais(filtros)

            # Dados para gráficos
            context["dados_graficos"] = {
                "distribuicao_presencas": self._dados_grafico_distribuicao_presencas(
                    filtros
                ),
                "evolucao_temporal": self._dados_grafico_evolucao_temporal(filtros),
                "ranking_alunos": self._dados_grafico_ranking_alunos(filtros),
                "carencias_por_turma": self._dados_grafico_carencias_turma(filtros),
                "performance_atividades": self._dados_grafico_performance_atividades(
                    filtros
                ),
            }

            # Filtros disponíveis
            context["filtros_disponiveis"] = self._obter_filtros_disponiveis()
            context["filtros_ativos"] = filtros

            # Configurações do painel
            context["configuracoes_painel"] = self._obter_configuracoes_painel()

            logger.info(f"Painel de estatísticas carregado com filtros: {filtros}")

        except Exception as e:
            logger.error(f"Erro ao carregar painel de estatísticas: {str(e)}")
            messages.error(self.request, f"Erro ao carregar painel: {str(e)}")
            context["erro"] = True

        return context

    def _extrair_filtros(self) -> Dict[str, Any]:
        """Extrai filtros da requisição."""
        filtros = {}

        # Período
        if self.request.GET.get("periodo_inicio"):
            try:
                filtros["periodo_inicio"] = datetime.strptime(
                    self.request.GET["periodo_inicio"], "%Y-%m-%d"
                ).date()
            except ValueError:
                pass

        if self.request.GET.get("periodo_fim"):
            try:
                filtros["periodo_fim"] = datetime.strptime(
                    self.request.GET["periodo_fim"], "%Y-%m-%d"
                ).date()
            except ValueError:
                pass

        # Turma
        if self.request.GET.get("turma_id"):
            try:
                filtros["turma_id"] = int(self.request.GET["turma_id"])
            except ValueError:
                pass

        # Atividade
        if self.request.GET.get("atividade_id"):
            try:
                filtros["atividade_id"] = int(self.request.GET["atividade_id"])
            except ValueError:
                pass

        # Período padrão se não especificado (últimos 6 meses)
        if not filtros.get("periodo_inicio"):
            filtros["periodo_inicio"] = date.today() - timedelta(days=180)

        if not filtros.get("periodo_fim"):
            filtros["periodo_fim"] = date.today()

        return filtros

    def _calcular_metricas_principais(self, filtros: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula métricas principais do painel."""
        try:
            # Filtrar presenças
            presencas_qs = PresencaDetalhada.objects.all()

            if filtros.get("turma_id"):
                presencas_qs = presencas_qs.filter(turma_id=filtros["turma_id"])

            if filtros.get("atividade_id"):
                presencas_qs = presencas_qs.filter(atividade_id=filtros["atividade_id"])

            if filtros.get("periodo_inicio"):
                presencas_qs = presencas_qs.filter(
                    periodo__gte=filtros["periodo_inicio"]
                )

            if filtros.get("periodo_fim"):
                presencas_qs = presencas_qs.filter(periodo__lte=filtros["periodo_fim"])

            # Agregações
            agregacoes = presencas_qs.aggregate(
                total_convocacoes=Sum("convocacoes"),
                total_presencas=Sum("presencas"),
                total_faltas=Sum("faltas"),
                total_carencias=Sum("carencias"),
                total_alunos=Count("aluno", distinct=True),
                total_turmas=Count("turma", distinct=True),
                total_atividades=Count("atividade", distinct=True),
            )

            # Calcular percentuais
            total_convocacoes = agregacoes["total_convocacoes"] or 0
            total_presencas = agregacoes["total_presencas"] or 0
            total_faltas = agregacoes["total_faltas"] or 0
            total_carencias = agregacoes["total_carencias"] or 0

            percentual_presenca = 0.0
            if total_convocacoes > 0:
                percentual_presenca = round(
                    (total_presencas / total_convocacoes) * 100, 2
                )

            percentual_faltas = 0.0
            if total_convocacoes > 0:
                percentual_faltas = round((total_faltas / total_convocacoes) * 100, 2)

            # Média de carências por aluno
            media_carencias = 0.0
            if agregacoes["total_alunos"] and agregacoes["total_alunos"] > 0:
                media_carencias = round(total_carencias / agregacoes["total_alunos"], 2)

            return {
                "total_alunos": agregacoes["total_alunos"] or 0,
                "total_turmas": agregacoes["total_turmas"] or 0,
                "total_atividades": agregacoes["total_atividades"] or 0,
                "total_convocacoes": total_convocacoes,
                "total_presencas": total_presencas,
                "total_faltas": total_faltas,
                "total_carencias": total_carencias,
                "percentual_presenca": percentual_presenca,
                "percentual_faltas": percentual_faltas,
                "media_carencias": media_carencias,
            }

        except Exception as e:
            logger.error(f"Erro ao calcular métricas principais: {str(e)}")
            return {
                "total_alunos": 0,
                "total_turmas": 0,
                "total_atividades": 0,
                "total_convocacoes": 0,
                "total_presencas": 0,
                "total_faltas": 0,
                "total_carencias": 0,
                "percentual_presenca": 0.0,
                "percentual_faltas": 0.0,
                "media_carencias": 0.0,
            }

    def _dados_grafico_distribuicao_presencas(
        self, filtros: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepara dados para gráfico de distribuição de presenças (pizza/donut)."""
        try:
            # Usar calculadora para obter estatísticas consolidadas
            tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
                turma_id=filtros.get("turma_id"),
                atividade_id=filtros.get("atividade_id"),
                periodo_inicio=filtros.get("periodo_inicio"),
                periodo_fim=filtros.get("periodo_fim"),
            )

            # Contar alunos por faixas de percentual
            distribuicao = {
                "Excelente (90-100%)": 0,
                "Bom (80-89%)": 0,
                "Regular (70-79%)": 0,
                "Atenção (60-69%)": 0,
                "Crítico (<60%)": 0,
            }

            for linha in tabela["linhas"]:
                percentual = linha["percentual_geral"]
                if percentual >= 90:
                    distribuicao["Excelente (90-100%)"] += 1
                elif percentual >= 80:
                    distribuicao["Bom (80-89%)"] += 1
                elif percentual >= 70:
                    distribuicao["Regular (70-79%)"] += 1
                elif percentual >= 60:
                    distribuicao["Atenção (60-69%)"] += 1
                else:
                    distribuicao["Crítico (<60%)"] += 1

            return {
                "tipo": "doughnut",
                "labels": list(distribuicao.keys()),
                "dados": list(distribuicao.values()),
                "cores": ["#28a745", "#17a2b8", "#ffc107", "#fd7e14", "#dc3545"],
            }

        except Exception as e:
            logger.error(f"Erro ao gerar dados do gráfico de distribuição: {str(e)}")
            return {"tipo": "doughnut", "labels": [], "dados": [], "cores": []}

    def _dados_grafico_evolucao_temporal(
        self, filtros: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepara dados para gráfico de evolução temporal (linha)."""
        try:
            # Filtrar presenças
            presencas_qs = PresencaDetalhada.objects.all()

            if filtros.get("turma_id"):
                presencas_qs = presencas_qs.filter(turma_id=filtros["turma_id"])

            if filtros.get("atividade_id"):
                presencas_qs = presencas_qs.filter(atividade_id=filtros["atividade_id"])

            if filtros.get("periodo_inicio"):
                presencas_qs = presencas_qs.filter(
                    periodo__gte=filtros["periodo_inicio"]
                )

            if filtros.get("periodo_fim"):
                presencas_qs = presencas_qs.filter(periodo__lte=filtros["periodo_fim"])

            # Agrupar por mês
            dados_mensais = {}
            for presenca in presencas_qs.order_by("periodo"):
                mes_ano = presenca.periodo.strftime("%Y-%m")

                if mes_ano not in dados_mensais:
                    dados_mensais[mes_ano] = {
                        "convocacoes": 0,
                        "presencas": 0,
                        "faltas": 0,
                    }

                dados_mensais[mes_ano]["convocacoes"] += presenca.convocacoes
                dados_mensais[mes_ano]["presencas"] += presenca.presencas
                dados_mensais[mes_ano]["faltas"] += presenca.faltas

            # Calcular percentuais
            labels = []
            percentuais_presenca = []
            percentuais_faltas = []

            for mes_ano in sorted(dados_mensais.keys()):
                dados = dados_mensais[mes_ano]

                # Formatar label
                ano, mes = mes_ano.split("-")
                mes_nome = [
                    "Jan",
                    "Fev",
                    "Mar",
                    "Abr",
                    "Mai",
                    "Jun",
                    "Jul",
                    "Ago",
                    "Set",
                    "Out",
                    "Nov",
                    "Dez",
                ][int(mes) - 1]
                labels.append(f"{mes_nome}/{ano}")

                # Calcular percentuais
                if dados["convocacoes"] > 0:
                    perc_presenca = round(
                        (dados["presencas"] / dados["convocacoes"]) * 100, 2
                    )
                    perc_faltas = round(
                        (dados["faltas"] / dados["convocacoes"]) * 100, 2
                    )
                else:
                    perc_presenca = 0.0
                    perc_faltas = 0.0

                percentuais_presenca.append(perc_presenca)
                percentuais_faltas.append(perc_faltas)

            return {
                "tipo": "line",
                "labels": labels,
                "datasets": [
                    {
                        "label": "Percentual de Presenças",
                        "data": percentuais_presenca,
                        "borderColor": "#28a745",
                        "backgroundColor": "rgba(40, 167, 69, 0.1)",
                        "tension": 0.4,
                    },
                    {
                        "label": "Percentual de Faltas",
                        "data": percentuais_faltas,
                        "borderColor": "#dc3545",
                        "backgroundColor": "rgba(220, 53, 69, 0.1)",
                        "tension": 0.4,
                    },
                ],
            }

        except Exception as e:
            logger.error(
                f"Erro ao gerar dados do gráfico de evolução temporal: {str(e)}"
            )
            return {"tipo": "line", "labels": [], "datasets": []}

    def _dados_grafico_ranking_alunos(self, filtros: Dict[str, Any]) -> Dict[str, Any]:
        """Prepara dados para gráfico de ranking de alunos (barras)."""
        try:
            # Usar calculadora para obter estatísticas consolidadas
            tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
                turma_id=filtros.get("turma_id"),
                atividade_id=filtros.get("atividade_id"),
                periodo_inicio=filtros.get("periodo_inicio"),
                periodo_fim=filtros.get("periodo_fim"),
                ordenar_por="percentual",
            )

            # Top 10 alunos
            top_alunos = tabela["linhas"][:10]

            labels = []
            percentuais = []
            cores = []

            for linha in top_alunos:
                # Nome do aluno (limitado para visualização)
                nome = linha["aluno"]["nome"]
                if len(nome) > 20:
                    nome = nome[:17] + "..."
                labels.append(nome)

                percentuais.append(linha["percentual_geral"])

                # Cor baseada no percentual
                percentual = linha["percentual_geral"]
                if percentual >= 90:
                    cores.append("#28a745")  # Verde
                elif percentual >= 80:
                    cores.append("#17a2b8")  # Azul
                elif percentual >= 70:
                    cores.append("#ffc107")  # Amarelo
                elif percentual >= 60:
                    cores.append("#fd7e14")  # Laranja
                else:
                    cores.append("#dc3545")  # Vermelho

            return {
                "tipo": "bar",
                "labels": labels,
                "dados": percentuais,
                "cores": cores,
            }

        except Exception as e:
            logger.error(f"Erro ao gerar dados do gráfico de ranking: {str(e)}")
            return {"tipo": "bar", "labels": [], "dados": [], "cores": []}

    def _dados_grafico_carencias_turma(self, filtros: Dict[str, Any]) -> Dict[str, Any]:
        """Prepara dados para gráfico de carências por turma (barras)."""
        try:
            get_turma_model()

            # Filtrar presenças
            presencas_qs = PresencaDetalhada.objects.all()

            if filtros.get("atividade_id"):
                presencas_qs = presencas_qs.filter(atividade_id=filtros["atividade_id"])

            if filtros.get("periodo_inicio"):
                presencas_qs = presencas_qs.filter(
                    periodo__gte=filtros["periodo_inicio"]
                )

            if filtros.get("periodo_fim"):
                presencas_qs = presencas_qs.filter(periodo__lte=filtros["periodo_fim"])

            # Se filtro de turma específica, mostrar carências por aluno dessa turma
            if filtros.get("turma_id"):
                presencas_qs = presencas_qs.filter(turma_id=filtros["turma_id"])

                # Agrupar por aluno
                carencias_por_aluno = {}
                for presenca in presencas_qs:
                    aluno_nome = presenca.aluno.nome
                    if aluno_nome not in carencias_por_aluno:
                        carencias_por_aluno[aluno_nome] = 0
                    carencias_por_aluno[aluno_nome] += presenca.carencias

                # Ordenar por carências (decrescente) e pegar top 10
                top_carencias = sorted(
                    carencias_por_aluno.items(), key=lambda x: x[1], reverse=True
                )[:10]

                labels = [
                    item[0][:20] + "..." if len(item[0]) > 20 else item[0]
                    for item in top_carencias
                ]
                dados = [item[1] for item in top_carencias]

            else:
                # Agrupar por turma
                carencias_por_turma = {}
                for presenca in presencas_qs:
                    turma_nome = presenca.turma.nome if presenca.turma else "Sem turma"
                    if turma_nome not in carencias_por_turma:
                        carencias_por_turma[turma_nome] = 0
                    carencias_por_turma[turma_nome] += presenca.carencias

                # Ordenar por carências (decrescente)
                top_carencias = sorted(
                    carencias_por_turma.items(), key=lambda x: x[1], reverse=True
                )

                labels = [item[0] for item in top_carencias]
                dados = [item[1] for item in top_carencias]

            return {
                "tipo": "bar",
                "labels": labels,
                "dados": dados,
                "cor": "#dc3545",  # Vermelho para carências
            }

        except Exception as e:
            logger.error(f"Erro ao gerar dados do gráfico de carências: {str(e)}")
            return {"tipo": "bar", "labels": [], "dados": [], "cor": "#dc3545"}

    def _dados_grafico_performance_atividades(
        self, filtros: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepara dados para gráfico de performance por atividades (radar)."""
        try:
            get_atividade_model()

            # Filtrar presenças
            presencas_qs = PresencaDetalhada.objects.all()

            if filtros.get("turma_id"):
                presencas_qs = presencas_qs.filter(turma_id=filtros["turma_id"])

            if filtros.get("periodo_inicio"):
                presencas_qs = presencas_qs.filter(
                    periodo__gte=filtros["periodo_inicio"]
                )

            if filtros.get("periodo_fim"):
                presencas_qs = presencas_qs.filter(periodo__lte=filtros["periodo_fim"])

            # Agrupar por atividade
            performance_atividades = {}
            for presenca in presencas_qs:
                atividade_nome = presenca.atividade.nome

                if atividade_nome not in performance_atividades:
                    performance_atividades[atividade_nome] = {
                        "convocacoes": 0,
                        "presencas": 0,
                    }

                performance_atividades[atividade_nome]["convocacoes"] += (
                    presenca.convocacoes
                )
                performance_atividades[atividade_nome]["presencas"] += (
                    presenca.presencas
                )

            # Calcular percentuais
            labels = []
            percentuais = []

            for atividade, dados in performance_atividades.items():
                if dados["convocacoes"] > 0:
                    percentual = round(
                        (dados["presencas"] / dados["convocacoes"]) * 100, 2
                    )
                    labels.append(atividade)
                    percentuais.append(percentual)

            return {"tipo": "radar", "labels": labels, "dados": percentuais}

        except Exception as e:
            logger.error(f"Erro ao gerar dados do gráfico de performance: {str(e)}")
            return {"tipo": "radar", "labels": [], "dados": []}

    def _obter_filtros_disponiveis(self) -> Dict[str, List]:
        """Obtém listas de filtros disponíveis."""
        try:
            Turma = get_turma_model()
            Atividade = get_atividade_model()

            turmas = list(Turma.objects.all().values("id", "nome").order_by("nome"))
            atividades = list(
                Atividade.objects.all().values("id", "nome").order_by("nome")
            )

            return {"turmas": turmas, "atividades": atividades}

        except Exception as e:
            logger.error(f"Erro ao obter filtros disponíveis: {str(e)}")
            return {"turmas": [], "atividades": []}

    def _obter_configuracoes_painel(self) -> Dict[str, Any]:
        """Obtém configurações do painel."""
        return {
            "atualizar_automaticamente": True,
            "intervalo_atualizacao": 300000,  # 5 minutos em ms
            "mostrar_animacoes": True,
            "tema_cores": {
                "primaria": "#007bff",
                "sucesso": "#28a745",
                "aviso": "#ffc107",
                "perigo": "#dc3545",
                "info": "#17a2b8",
            },
        }


class PainelDadosAjaxView(LoginRequiredMixin, TemplateView):
    """View para fornecer dados via AJAX para atualização dinâmica do painel."""

    def get(self, request, *args, **kwargs):
        """Retorna dados específicos via AJAX."""
        try:
            tipo_dado = request.GET.get("tipo")

            if not tipo_dado:
                return JsonResponse(
                    {"erro": "Tipo de dado não especificado"}, status=400
                )

            # Extrair filtros
            filtros = self._extrair_filtros(request)

            # Dados específicos
            if tipo_dado == "metricas":
                dados = self._calcular_metricas_principais(filtros)
            elif tipo_dado == "distribuicao":
                dados = self._dados_grafico_distribuicao_presencas(filtros)
            elif tipo_dado == "evolucao":
                dados = self._dados_grafico_evolucao_temporal(filtros)
            elif tipo_dado == "ranking":
                dados = self._dados_grafico_ranking_alunos(filtros)
            elif tipo_dado == "carencias":
                dados = self._dados_grafico_carencias_turma(filtros)
            elif tipo_dado == "performance":
                dados = self._dados_grafico_performance_atividades(filtros)
            else:
                return JsonResponse({"erro": "Tipo de dado inválido"}, status=400)

            return JsonResponse(
                {
                    "sucesso": True,
                    "dados": dados,
                    "filtros": filtros,
                    "timestamp": timezone.now().isoformat(),
                }
            )

        except Exception as e:
            logger.error(f"Erro ao obter dados via AJAX: {str(e)}")
            return JsonResponse({"erro": f"Erro interno: {str(e)}"}, status=500)

    def _extrair_filtros(self, request) -> Dict[str, Any]:
        """Extrai filtros da requisição AJAX."""
        filtros = {}

        if request.GET.get("periodo_inicio"):
            try:
                filtros["periodo_inicio"] = datetime.strptime(
                    request.GET["periodo_inicio"], "%Y-%m-%d"
                ).date()
            except ValueError:
                pass

        if request.GET.get("periodo_fim"):
            try:
                filtros["periodo_fim"] = datetime.strptime(
                    request.GET["periodo_fim"], "%Y-%m-%d"
                ).date()
            except ValueError:
                pass

        if request.GET.get("turma_id"):
            try:
                filtros["turma_id"] = int(request.GET["turma_id"])
            except ValueError:
                pass

        if request.GET.get("atividade_id"):
            try:
                filtros["atividade_id"] = int(request.GET["atividade_id"])
            except ValueError:
                pass

        return filtros

    def _calcular_metricas_principais(self, filtros: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula métricas principais (reutiliza método da view principal)."""
        view_principal = PainelEstatisticasView()
        return view_principal._calcular_metricas_principais(filtros)

    def _dados_grafico_distribuicao_presencas(
        self, filtros: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Dados para gráfico de distribuição (reutiliza método da view principal)."""
        view_principal = PainelEstatisticasView()
        return view_principal._dados_grafico_distribuicao_presencas(filtros)

    def _dados_grafico_evolucao_temporal(
        self, filtros: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Dados para gráfico de evolução temporal (reutiliza método da view principal)."""
        view_principal = PainelEstatisticasView()
        return view_principal._dados_grafico_evolucao_temporal(filtros)

    def _dados_grafico_ranking_alunos(self, filtros: Dict[str, Any]) -> Dict[str, Any]:
        """Dados para gráfico de ranking (reutiliza método da view principal)."""
        view_principal = PainelEstatisticasView()
        return view_principal._dados_grafico_ranking_alunos(filtros)

    def _dados_grafico_carencias_turma(self, filtros: Dict[str, Any]) -> Dict[str, Any]:
        """Dados para gráfico de carências (reutiliza método da view principal)."""
        view_principal = PainelEstatisticasView()
        return view_principal._dados_grafico_carencias_turma(filtros)

    def _dados_grafico_performance_atividades(
        self, filtros: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Dados para gráfico de performance (reutiliza método da view principal)."""
        view_principal = PainelEstatisticasView()
        return view_principal._dados_grafico_performance_atividades(filtros)


class ExportarRelatorioView(LoginRequiredMixin, TemplateView):
    """View para exportar relatórios do painel em diferentes formatos."""

    def get(self, request, *args, **kwargs):
        """Exporta relatório baseado no formato solicitado."""
        try:
            formato = request.GET.get("formato", "pdf")

            # Extrair filtros
            filtros = self._extrair_filtros(request)

            # Gerar dados do relatório
            dados_relatorio = self._gerar_dados_relatorio(filtros)

            if formato == "json":
                response = JsonResponse(dados_relatorio)
                response["Content-Disposition"] = (
                    'attachment; filename="relatorio_painel.json"'
                )
                return response

            elif formato == "csv":
                return self._exportar_csv(dados_relatorio)

            elif formato == "pdf":
                return self._exportar_pdf(dados_relatorio)

            else:
                return JsonResponse({"erro": "Formato não suportado"}, status=400)

        except Exception as e:
            logger.error(f"Erro ao exportar relatório: {str(e)}")
            return JsonResponse({"erro": f"Erro na exportação: {str(e)}"}, status=500)

    def _extrair_filtros(self, request) -> Dict[str, Any]:
        """Extrai filtros da requisição."""
        # Reutiliza método da view principal
        view_principal = PainelEstatisticasView()
        view_principal.request = request
        return view_principal._extrair_filtros()

    def _gerar_dados_relatorio(self, filtros: Dict[str, Any]) -> Dict[str, Any]:
        """Gera dados consolidados para o relatório."""
        try:
            # Usar calculadora para obter dados completos
            tabela = CalculadoraEstatisticas.gerar_tabela_consolidada(
                turma_id=filtros.get("turma_id"),
                atividade_id=filtros.get("atividade_id"),
                periodo_inicio=filtros.get("periodo_inicio"),
                periodo_fim=filtros.get("periodo_fim"),
            )

            # Métricas principais
            view_principal = PainelEstatisticasView()
            metricas = view_principal._calcular_metricas_principais(filtros)

            return {
                "relatorio": {
                    "titulo": "Relatório do Painel de Estatísticas",
                    "data_geracao": timezone.now().isoformat(),
                    "filtros_aplicados": filtros,
                    "metricas_principais": metricas,
                    "tabela_consolidada": tabela,
                },
                "metadados": {
                    "versao": "1.0",
                    "sistema": "OMAUM - Sistema de Presenças",
                    "modulo": "Painel de Estatísticas",
                },
            }

        except Exception as e:
            logger.error(f"Erro ao gerar dados do relatório: {str(e)}")
            raise

    def _exportar_csv(self, dados_relatorio: Dict[str, Any]) -> HttpResponse:
        """Exporta relatório em formato CSV."""
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)

        # Cabeçalho
        writer.writerow(
            [
                "Nome",
                "CPF",
                "Turma",
                "Convocações",
                "Presenças",
                "Faltas",
                "Percentual",
                "Carências",
                "Status",
            ]
        )

        # Dados
        for linha in dados_relatorio["relatorio"]["tabela_consolidada"]["linhas"]:
            writer.writerow(
                [
                    linha["aluno"]["nome"],
                    linha["aluno"]["cpf"],
                    linha["turma"]["nome"] if linha["turma"] else "",
                    linha["totais"]["convocacoes"],
                    linha["totais"]["presencas"],
                    linha["totais"]["faltas"],
                    f"{linha['percentual_geral']:.2f}%",
                    linha["totais"]["carencias"],
                    linha["status"],
                ]
            )

        response = HttpResponse(output.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="relatorio_painel.csv"'

        return response

    def _exportar_pdf(self, dados_relatorio: Dict[str, Any]) -> HttpResponse:
        """Exporta relatório em formato PDF."""
        # Implementação básica - pode ser expandida com bibliotecas como ReportLab
        from django.template.loader import render_to_string
        from django.http import HttpResponse

        html_content = render_to_string(
            "presencas/relatorio_painel_pdf.html", {"dados": dados_relatorio}
        )

        response = HttpResponse(html_content, content_type="text/html")
        response["Content-Disposition"] = 'attachment; filename="relatorio_painel.html"'

        return response
