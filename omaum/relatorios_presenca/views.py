"""
Views para o app relatorios_presenca.

Implementa views function-based conforme premissas estabelecidas,
com nomenclatura padronizada e filtros dinâmicos AJAX.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime
import logging

# Importações dinâmicas conforme premissas
from importlib import import_module

from .services.relatorio_service import RelatorioPresencaService
from .generators.excel_generator import ExcelRelatorioGenerator
from .models import ConfiguracaoRelatorio, HistoricoRelatorio

logger = logging.getLogger(__name__)


@login_required
def listar_relatorios(request):
    """
    Lista relatórios disponíveis e histórico.
    URL: listar_relatorios
    """
    try:
        # Obter configurações ativas
        configuracoes = ConfiguracaoRelatorio.objects.filter(ativo=True).order_by(
            "tipo_relatorio", "nome"
        )

        # Obter histórico recente do usuário
        historico = HistoricoRelatorio.objects.filter(usuario=request.user).order_by(
            "-data_geracao"
        )[:10]

        # Obter turmas para filtros
        turmas_module = import_module("turmas.models")
        turmas = turmas_module.Turma.objects.filter(ativo=True).order_by("nome")

        context = {
            "configuracoes": configuracoes,
            "historico": historico,
            "turmas": turmas,
            "tipos_relatorio": ConfiguracaoRelatorio.TIPO_RELATORIO_CHOICES,
        }

        return render(request, "relatorios_presenca/listar_relatorios.html", context)

    except Exception as e:
        logger.error(f"Erro ao listar relatórios: {e}")
        messages.error(request, f"Erro ao carregar página: {e}")
        return redirect("home")


@login_required
@require_http_methods(["GET", "POST"])
def gerar_relatorio(request):
    """
    Gera relatório conforme parâmetros.
    URL: gerar_relatorio
    """
    if request.method == "GET":
        return _exibir_formulario_relatorio(request)

    try:
        # Obter parâmetros do POST
        tipo_relatorio = request.POST.get("tipo_relatorio")
        turma_id = request.POST.get("turma_id")
        formato = request.POST.get("formato", "excel")

        # Validar parâmetros obrigatórios
        if not tipo_relatorio or not turma_id:
            messages.error(request, "Tipo de relatório e turma são obrigatórios.")
            return redirect("relatorios_presenca:listar_relatorios")

        # Criar registro no histórico
        historico = HistoricoRelatorio.objects.create(
            usuario=request.user,
            tipo_relatorio=tipo_relatorio,
            parametros=request.POST.dict(),
            status="processando",
        )

        # Gerar relatório conforme tipo
        if tipo_relatorio == "consolidado":
            return _gerar_consolidado(request, historico)
        elif tipo_relatorio == "mensal":
            return _gerar_mensal(request, historico)
        elif tipo_relatorio == "coleta":
            return _gerar_coleta(request, historico)
        elif tipo_relatorio == "controle_geral":
            return _gerar_controle_geral(request, historico)
        else:
            messages.error(request, "Tipo de relatório inválido.")
            return redirect("relatorios_presenca:listar_relatorios")

    except Exception as e:
        logger.error(f"Erro ao gerar relatório: {e}")
        messages.error(request, f"Erro ao gerar relatório: {e}")
        return redirect("relatorios_presenca:listar_relatorios")


def _exibir_formulario_relatorio(request):
    """Exibe formulário para geração de relatório."""
    try:
        # Obter dados para formulário
        turmas_module = import_module("turmas.models")
        atividades_module = import_module("atividades.models")

        turmas = turmas_module.Turma.objects.filter(ativo=True).order_by("nome")
        atividades = atividades_module.Atividade.objects.filter(ativo=True).order_by(
            "nome"
        )

        context = {
            "turmas": turmas,
            "atividades": atividades,
            "tipos_relatorio": ConfiguracaoRelatorio.TIPO_RELATORIO_CHOICES,
            "formatos": ConfiguracaoRelatorio.FORMATO_CHOICES,
        }

        return render(request, "relatorios_presenca/gerar_relatorio.html", context)

    except Exception as e:
        logger.error(f"Erro ao exibir formulário: {e}")
        messages.error(request, f"Erro ao carregar formulário: {e}")
        return redirect("relatorios_presenca:listar_relatorios")


def _gerar_consolidado(request, historico):
    """Gera relatório consolidado por período."""
    try:
        # Obter parâmetros específicos
        turma_id = request.POST.get("turma_id")
        data_inicio = datetime.strptime(
            request.POST.get("data_inicio"), "%Y-%m-%d"
        ).date()
        data_fim = datetime.strptime(request.POST.get("data_fim"), "%Y-%m-%d").date()
        atividade_id = request.POST.get("atividade_id") or None

        # Gerar dados usando service
        service = RelatorioPresencaService()
        dados = service.obter_dados_consolidado_periodo(
            turma_id, data_inicio, data_fim, atividade_id
        )

        # Gerar arquivo Excel
        generator = ExcelRelatorioGenerator()
        arquivo_excel = generator.gerar_consolidado_periodo(dados)

        # Preparar resposta
        nome_arquivo = f"consolidado_{dados['turma']['nome']}_{data_inicio.strftime('%Y%m%d')}_{data_fim.strftime('%Y%m%d')}.xlsx"

        response = HttpResponse(
            arquivo_excel.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{nome_arquivo}"'

        # Atualizar histórico
        historico.marcar_como_concluido(nome_arquivo, len(arquivo_excel.getvalue()))

        return response

    except Exception as e:
        logger.error(f"Erro ao gerar consolidado: {e}")
        historico.marcar_como_erro(str(e))
        messages.error(request, f"Erro ao gerar relatório consolidado: {e}")
        return redirect("relatorios_presenca:listar_relatorios")


def _gerar_mensal(request, historico):
    """Gera relatório de apuração mensal."""
    try:
        # Obter parâmetros específicos
        turma_id = request.POST.get("turma_id")
        ano = int(request.POST.get("ano"))
        mes = int(request.POST.get("mes"))
        atividade_id = request.POST.get("atividade_id") or None

        # Gerar dados usando service
        service = RelatorioPresencaService()
        dados = service.obter_dados_apuracao_mensal(turma_id, ano, mes, atividade_id)

        # Gerar arquivo Excel
        generator = ExcelRelatorioGenerator()
        arquivo_excel = generator.gerar_apuracao_mensal(dados)

        # Preparar resposta
        nome_arquivo = f"mes{mes:02d}_{dados['turma']['nome']}_{ano}.xlsx"

        response = HttpResponse(
            arquivo_excel.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{nome_arquivo}"'

        # Atualizar histórico
        historico.marcar_como_concluido(nome_arquivo, len(arquivo_excel.getvalue()))

        return response

    except Exception as e:
        logger.error(f"Erro ao gerar mensal: {e}")
        historico.marcar_como_erro(str(e))
        messages.error(request, f"Erro ao gerar relatório mensal: {e}")
        return redirect("relatorios_presenca:listar_relatorios")


def _gerar_coleta(request, historico):
    """Gera formulário de coleta mensal."""
    try:
        # Obter parâmetros específicos
        turma_id = request.POST.get("turma_id")
        ano = int(request.POST.get("ano"))
        mes = int(request.POST.get("mes"))

        # Gerar dados usando service
        service = RelatorioPresencaService()
        dados = service.obter_dados_formulario_coleta(turma_id, ano, mes)

        # Gerar arquivo Excel
        generator = ExcelRelatorioGenerator()
        arquivo_excel = generator.gerar_formulario_coleta(dados)

        # Preparar resposta
        nome_arquivo = f"coleta_{dados['turma']['nome']}_{mes:02d}_{ano}.xlsx"

        response = HttpResponse(
            arquivo_excel.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{nome_arquivo}"'

        # Atualizar histórico
        historico.marcar_como_concluido(nome_arquivo, len(arquivo_excel.getvalue()))

        return response

    except Exception as e:
        logger.error(f"Erro ao gerar coleta: {e}")
        historico.marcar_como_erro(str(e))
        messages.error(request, f"Erro ao gerar formulário de coleta: {e}")
        return redirect("relatorios_presenca:listar_relatorios")


def _gerar_controle_geral(request, historico):
    """Gera relatório de controle geral da turma."""
    try:
        # Obter parâmetros específicos
        turma_id = request.POST.get("turma_id")

        # Gerar dados usando service
        service = RelatorioPresencaService()
        dados = service.obter_dados_controle_geral(turma_id)

        # Gerar arquivo Excel
        generator = ExcelRelatorioGenerator()
        arquivo_excel = generator.gerar_controle_geral(dados)

        # Preparar resposta
        nome_arquivo = f"controle_geral_{dados['turma']['nome']}.xlsx"

        response = HttpResponse(
            arquivo_excel.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{nome_arquivo}"'

        # Atualizar histórico
        historico.marcar_como_concluido(nome_arquivo, len(arquivo_excel.getvalue()))

        return response

    except Exception as e:
        logger.error(f"Erro ao gerar controle geral: {e}")
        historico.marcar_como_erro(str(e))
        messages.error(request, f"Erro ao gerar controle geral: {e}")
        return redirect("relatorios_presenca:listar_relatorios")


@login_required
def detalhar_relatorio(request, relatorio_id):
    """
    Exibe detalhes de um relatório específico.
    URL: detalhar_relatorio
    """
    try:
        relatorio = get_object_or_404(
            HistoricoRelatorio, id=relatorio_id, usuario=request.user
        )

        context = {
            "relatorio": relatorio,
        }

        return render(request, "relatorios_presenca/detalhar_relatorio.html", context)

    except Exception as e:
        logger.error(f"Erro ao detalhar relatório: {e}")
        messages.error(request, f"Erro ao carregar detalhes: {e}")
        return redirect("relatorios_presenca:listar_relatorios")


@login_required
def excluir_relatorio(request, relatorio_id):
    """
    Exclui um relatório do histórico.
    URL: excluir_relatorio
    """
    try:
        relatorio = get_object_or_404(
            HistoricoRelatorio, id=relatorio_id, usuario=request.user
        )

        if request.method == "POST":
            # Excluir arquivo se existir
            if relatorio.arquivo_gerado:
                try:
                    relatorio.arquivo_gerado.delete()
                except:
                    pass

            relatorio.delete()
            messages.success(request, "Relatório excluído com sucesso.")
            return redirect("relatorios_presenca:listar_relatorios")

        context = {
            "relatorio": relatorio,
        }

        return render(
            request, "relatorios_presenca/confirmar_exclusao_relatorio.html", context
        )

    except Exception as e:
        logger.error(f"Erro ao excluir relatório: {e}")
        messages.error(request, f"Erro ao excluir relatório: {e}")
        return redirect("relatorios_presenca:listar_relatorios")


# Views AJAX para filtros dinâmicos


@csrf_exempt
def ajax_obter_atividades_turma(request):
    """
    Obtém atividades de uma turma via AJAX.
    Implementa filtros dinâmicos conforme premissas.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        turma_id = request.POST.get("turma_id")

        if not turma_id:
            return JsonResponse({"atividades": []})

        # Obter atividades da turma
        atividades_module = import_module("atividades.models")
        atividades = (
            atividades_module.Atividade.objects.filter(turmas__id=turma_id, ativo=True)
            .distinct()
            .order_by("nome")
        )

        atividades_data = [
            {
                "id": atividade.id,
                "nome": atividade.nome,
                "tipo": getattr(atividade, "tipo", "N/A"),
            }
            for atividade in atividades
        ]

        return JsonResponse({"atividades": atividades_data})

    except Exception as e:
        logger.error(f"Erro ao obter atividades: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def ajax_obter_periodos_turma(request):
    """
    Obtém períodos disponíveis de uma turma via AJAX.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        turma_id = request.POST.get("turma_id")

        if not turma_id:
            return JsonResponse({"periodos": []})

        # Obter turma
        turmas_module = import_module("turmas.models")
        turma = turmas_module.Turma.objects.get(id=turma_id)

        # Calcular períodos baseado nas datas da turma
        periodos = []

        if hasattr(turma, "data_inicio_ativ") and turma.data_inicio_ativ:
            data_inicio = turma.data_inicio_ativ
            data_fim = (
                getattr(turma, "data_termino_atividades", None) or timezone.now().date()
            )

            # Gerar meses no período
            data_atual = data_inicio.replace(day=1)
            while data_atual <= data_fim:
                periodos.append(
                    {
                        "ano": data_atual.year,
                        "mes": data_atual.month,
                        "nome": f"{data_atual.strftime('%B')} {data_atual.year}",
                        "valor": f"{data_atual.year}-{data_atual.month:02d}",
                    }
                )

                if data_atual.month == 12:
                    data_atual = data_atual.replace(year=data_atual.year + 1, month=1)
                else:
                    data_atual = data_atual.replace(month=data_atual.month + 1)

        return JsonResponse({"periodos": periodos})

    except Exception as e:
        logger.error(f"Erro ao obter períodos: {e}")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def ajax_validar_parametros(request):
    """
    Valida parâmetros do relatório via AJAX.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        tipo_relatorio = request.POST.get("tipo_relatorio")
        turma_id = request.POST.get("turma_id")

        erros = []

        # Validações básicas
        if not tipo_relatorio:
            erros.append("Tipo de relatório é obrigatório")

        if not turma_id:
            erros.append("Turma é obrigatória")

        # Validações específicas por tipo
        if tipo_relatorio in ["consolidado"]:
            data_inicio = request.POST.get("data_inicio")
            data_fim = request.POST.get("data_fim")

            if not data_inicio:
                erros.append("Data de início é obrigatória")
            if not data_fim:
                erros.append("Data de fim é obrigatória")

            if data_inicio and data_fim:
                try:
                    dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
                    dt_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()

                    if dt_inicio > dt_fim:
                        erros.append("Data de início deve ser anterior à data de fim")

                except ValueError:
                    erros.append("Formato de data inválido")

        elif tipo_relatorio in ["mensal", "coleta"]:
            ano = request.POST.get("ano")
            mes = request.POST.get("mes")

            if not ano:
                erros.append("Ano é obrigatório")
            if not mes:
                erros.append("Mês é obrigatório")

            if ano and mes:
                try:
                    ano_int = int(ano)
                    mes_int = int(mes)

                    if ano_int < 2000 or ano_int > 2100:
                        erros.append("Ano deve estar entre 2000 e 2100")

                    if mes_int < 1 or mes_int > 12:
                        erros.append("Mês deve estar entre 1 e 12")

                except ValueError:
                    erros.append("Ano e mês devem ser números")

        return JsonResponse({"valido": len(erros) == 0, "erros": erros})

    except Exception as e:
        logger.error(f"Erro ao validar parâmetros: {e}")
        return JsonResponse({"error": str(e)}, status=500)
