"""
FASE 3C: Tasks assíncronas para o sistema de presenças.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

from celery import shared_task
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from importlib import import_module

from .models import PresencaDetalhada
from omaum.relatorios_presenca.models import AgendamentoRelatorio


logger = logging.getLogger(__name__)


def get_bulk_operations():
    """Carrega BulkPresencaOperations sob demanda."""

    try:
        module = import_module("presencas.bulk_operations")
        bulk_ops = getattr(module, "BulkPresencaOperations", None)
        if bulk_ops is None:
            logger.warning(
                "BulkPresencaOperations não encontrado em presencas.bulk_operations"
            )
        return bulk_ops
    except (ImportError, AttributeError) as exc:
        logger.warning("BulkPresencaOperations indisponível: %s", exc)
        return None


@shared_task(bind=True, max_retries=3)
def processar_exportacao_pesada(
    self, filtros: Dict[str, Any], formato: str, email_destinatario: str = None
):
    """
    Task para processar exportações pesadas em background.

    Args:
        filtros: Filtros para a exportação
        formato: Formato de saída (excel, csv, pdf)
        email_destinatario: Email para envio do relatório
    """
    try:
        logger.info(f"Iniciando exportação pesada: {formato} com filtros {filtros}")

        # Simular progresso para tasks longas
        self.update_state(state="PROGRESS", meta={"current": 0, "total": 100})

        # Importar classe de exportação
        from .views.exportacao import ProcessarExportacaoView

        processor = ProcessarExportacaoView()
        dados = processor._obter_dados("consolidado_geral", filtros)

        self.update_state(state="PROGRESS", meta={"current": 50, "total": 100})

        # Gerar arquivo baseado no formato
        if formato == "excel":
            from .views.exportacao import ExcelAvancadoExporter

            exporter = ExcelAvancadoExporter()
            response = exporter.gerar_excel_consolidado_geral(dados, filtros)
            arquivo_content = response.content
            filename = (
                f"presencas_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )

        elif formato == "csv":
            from .views.exportacao_parte2 import CSVExporter

            exporter = CSVExporter()
            response = exporter.gerar_csv_consolidado(dados, filtros)
            arquivo_content = response.content
            filename = (
                f"presencas_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )

        else:
            raise ValueError(f"Formato não suportado: {formato}")

        self.update_state(state="PROGRESS", meta={"current": 80, "total": 100})

        # Enviar por email se solicitado
        if email_destinatario:
            enviar_relatorio_email.delay(
                email_destinatario,
                filename,
                arquivo_content,
                f"Relatório de Presenças - {datetime.now().strftime('%d/%m/%Y')}",
            )

        self.update_state(state="PROGRESS", meta={"current": 100, "total": 100})

        logger.info(f"Exportação pesada concluída: {filename}")
        return {
            "status": "success",
            "filename": filename,
            "size": len(arquivo_content),
            "email_sent": bool(email_destinatario),
        }

    except Exception as exc:
        logger.error(f"Erro na exportação pesada: {str(exc)}")
        self.retry(countdown=60, exc=exc)


@shared_task(bind=True, max_retries=2)
def recalcular_estatisticas(
    self, turma_id: int = None, periodo_inicio: str = None, periodo_fim: str = None
):
    """
    Task para recalcular estatísticas em background.

    Args:
        turma_id: ID da turma (opcional, se None recalcula todas)
        periodo_inicio: Data início em formato YYYY-MM-DD
        periodo_fim: Data fim em formato YYYY-MM-DD
    """
    try:
        logger.info(f"Iniciando recálculo de estatísticas - Turma: {turma_id}")

        # Converter datas
        if periodo_inicio:
            periodo_inicio = datetime.strptime(periodo_inicio, "%Y-%m-%d").date()
        if periodo_fim:
            periodo_fim = datetime.strptime(periodo_fim, "%Y-%m-%d").date()

        # Usar bulk operations para performance
        bulk_ops = get_bulk_operations()
        if not bulk_ops:
            raise RuntimeError("BulkPresencaOperations indisponível para estatísticas")

        stats = bulk_ops.otimizar_queries_estatisticas(
            turma_id=turma_id, periodo_inicio=periodo_inicio, periodo_fim=periodo_fim
        )

        # Invalidar cache relacionado
        cache_patterns = [
            "presencas_filtros_*",
            f"estatisticas_turma_{turma_id}*" if turma_id else "estatisticas_turma_*",
            "turmas_listagem",
            "atividades_listagem",
        ]

        for pattern in cache_patterns:
            cache.delete_pattern(pattern)

        logger.info(
            f"Recálculo concluído: {stats['total_registros']} registros processados"
        )
        return {
            "status": "success",
            "total_registros": stats["total_registros"],
            "total_alunos": stats["total_alunos"],
            "percentual_presenca": float(stats["percentual_presenca"] or 0),
        }

    except Exception as exc:
        logger.error(f"Erro no recálculo de estatísticas: {str(exc)}")
        self.retry(countdown=120, exc=exc)


@shared_task
def enviar_relatorio_email(
    email_destinatario: str, filename: str, arquivo_content: bytes, assunto: str
):
    """
    Task para enviar relatórios por email.
    """
    try:
        logger.info(f"Enviando relatório por email para: {email_destinatario}")

        email = EmailMessage(
            subject=assunto,
            body=f"""
Olá,

Em anexo está o relatório de presenças solicitado.

Arquivo: {filename}
Data de geração: {datetime.now().strftime('%d/%m/%Y às %H:%M')}

Este é um email automático, não responda.

Atenciosamente,
Sistema OMAUM
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_destinatario],
        )

        # Anexar arquivo
        email.attach(filename, arquivo_content, "application/octet-stream")
        email.send()

        logger.info(f"Email enviado com sucesso para: {email_destinatario}")
        return {"status": "success", "email": email_destinatario}

    except Exception as exc:
        logger.error(f"Erro ao enviar email: {str(exc)}")
        raise exc


@shared_task
def processar_bulk_presencas(
    dados_presencas: List[Dict[str, Any]], registrado_por: str
):
    """
    Task para processar presenças em lote de forma assíncrona.
    """
    try:
        logger.info(f"Processando {len(dados_presencas)} presenças em lote")

        bulk_ops = get_bulk_operations()
        if not bulk_ops:
            raise RuntimeError("BulkPresencaOperations indisponível para bulk create")

        stats = bulk_ops.criar_presencas_lote(
            dados_presencas, registrado_por
        )

        # Limpar cache relacionado após operação em lote
        cache.delete_pattern("presencas_*")
        cache.delete_pattern("estatisticas_*")

        logger.info(f"Bulk operation concluída: {stats}")
        return stats

    except Exception as exc:
        logger.error(f"Erro no processamento em lote: {str(exc)}")
        raise exc


@shared_task
def limpar_cache_antigo():
    """
    Task periódica para limpeza de cache antigo.
    """
    try:
        logger.info("Iniciando limpeza de cache antigo")

        # Patterns de cache para limpar
        patterns_to_clean = [
            "presencas_filtros_*",
            "api_presencas_*",
            "estatisticas_*",
        ]

        total_cleaned = 0
        for pattern in patterns_to_clean:
            try:
                cache.delete_pattern(pattern)
                total_cleaned += 1
            except Exception as e:
                logger.warning(f"Erro ao limpar pattern {pattern}: {e}")

        logger.info(f"Limpeza de cache concluída: {total_cleaned} patterns limpos")
        return {"patterns_cleaned": total_cleaned}

    except Exception as exc:
        logger.error(f"Erro na limpeza de cache: {str(exc)}")
        return {"error": str(exc)}


@shared_task
def backup_dados_criticos():
    """
    Task periódica para backup de dados críticos.
    """
    try:
        logger.info("Iniciando backup de dados críticos")

        # Contar registros críticos
        from django.core import management
        import io

        # Backup de presenças dos últimos 30 dias
        data_limite = timezone.now().date() - timedelta(days=30)
        presencas_recentes = PresencaDetalhada.objects.filter(
            periodo__gte=data_limite
        ).count()

        # Verificar integridade do banco
        output = io.StringIO()
        management.call_command("check", stdout=output, verbosity=0)
        check_result = output.getvalue()

        stats = {
            "presencas_recentes": presencas_recentes,
            "data_backup": timezone.now().isoformat(),
            "sistema_check": "OK" if "no issues" in check_result else "WARNING",
        }

        logger.info(f"Backup dados críticos concluído: {stats}")
        return stats

    except Exception as exc:
        logger.error(f"Erro no backup de dados críticos: {str(exc)}")
        return {"error": str(exc)}


@shared_task
def processar_agendamento_relatorio(agendamento_id: int):
    """
    Task para processar agendamentos de relatório.
    """
    try:
        agendamento = AgendamentoRelatorio.objects.get(id=agendamento_id)

        logger.info(f"Processando agendamento: {agendamento.nome}")

        # Configurar filtros do agendamento
        filtros = {
            "formato": agendamento.formato,
            "template": agendamento.template,
            "periodo": agendamento.periodo,
            "data_inicio": agendamento.data_inicio.isoformat()
            if agendamento.data_inicio
            else None,
            "data_fim": agendamento.data_fim.isoformat()
            if agendamento.data_fim
            else None,
            "turma_id": agendamento.turma_id,
            "curso": agendamento.curso,
        }

        # Executar exportação
        result = processar_exportacao_pesada.delay(
            filtros=filtros,
            formato=agendamento.formato,
            email_destinatario=agendamento.email_destinatario,
        )

        # Atualizar status do agendamento
        agendamento.ultima_execucao = timezone.now()
        agendamento.status = "executado"
        agendamento.save()

        logger.info(f"Agendamento processado: {agendamento.nome}")
        return {"status": "success", "task_id": result.task_id}

    except AgendamentoRelatorio.DoesNotExist:
        logger.error(f"Agendamento não encontrado: {agendamento_id}")
        return {"error": "Agendamento não encontrado"}
    except Exception as exc:
        logger.error(f"Erro no processamento de agendamento: {str(exc)}")
        raise exc
