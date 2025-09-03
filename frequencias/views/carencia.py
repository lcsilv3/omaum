"""
Views para gerenciamento de carências.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import logging

# Importar funções utilitárias do módulo utils
from ..utils import get_models, get_model_dynamically

logger = logging.getLogger(__name__)


@login_required
def editar_carencia(request, carencia_id):
    """Edita uma carência específica."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)

        if request.method == "POST":
            # Atualizar campos da carência
            liberado = request.POST.get("liberado") == "on"
            observacoes = request.POST.get("observacoes", "")

            carencia.liberado = liberado
            carencia.observacoes = observacoes
            carencia.save()

            messages.success(request, "Carência atualizada com sucesso!")
            return redirect(
                "frequencias:detalhar_frequencia_mensal",
                frequencia_id=carencia.frequencia_mensal.id,
            )

        context = {"carencia": carencia}

        return render(request, "frequencias/editar_carencia.html", context)

    except Exception as e:
        logger.error(f"Erro ao editar carência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao editar carência: {str(e)}")
        return redirect("frequencias:listar_frequencias")


@login_required
def resolver_carencia(request, carencia_id):
    """Resolve uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)

        if request.method == "POST":
            # Atualizar status da carência
            carencia.status = "RESOLVIDO"
            carencia.data_resolucao = timezone.now()
            carencia.resolvido_por = request.user
            carencia.motivo_resolucao = request.POST.get("motivo_resolucao")
            carencia.observacoes_resolucao = request.POST.get(
                "observacoes_resolucao", ""
            )
            carencia.liberado = True
            carencia.save()

            # Processar documentos anexados
            for arquivo in request.FILES.getlist("documentos"):
                Documento = get_model_dynamically("documentos", "Documento")

                documento = Documento.objects.create(
                    nome=arquivo.name,
                    arquivo=arquivo,
                    tipo="CARENCIA",
                    aluno=carencia.aluno,
                    uploaded_by=request.user,
                )

                # Associar documento à carência
                carencia.documentos_resolucao.add(documento)

            messages.success(request, "Carência resolvida com sucesso!")
            return redirect("frequencias:detalhar_carencia", carencia_id=carencia.id)

        context = {"carencia": carencia}

        return render(request, "frequencias/resolver_carencia.html", context)

    except Exception as e:
        logger.error(f"Erro ao resolver carência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao resolver carência: {str(e)}")
        return redirect("frequencias:detalhar_carencia", carencia_id=carencia_id)


@login_required
def detalhar_carencia(request, carencia_id):
    """Exibe os detalhes de uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)

        context = {"carencia": carencia}

        return render(request, "frequencias/detalhar_carencia.html", context)

    except Exception as e:
        logger.error(f"Erro ao detalhar carência: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao detalhar carência: {str(e)}")
        return redirect("frequencias:listar_frequencias")


@login_required
def iniciar_acompanhamento(request, carencia_id):
    """Inicia o acompanhamento de uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)

        if request.method == "POST":
            # Atualizar status da carência
            carencia.status = "EM_ACOMPANHAMENTO"
            carencia.data_acompanhamento = timezone.now()
            carencia.acompanhado_por = request.user
            carencia.observacoes = request.POST.get("observacoes", "")
            carencia.prazo_resolucao = request.POST.get("prazo_resolucao")
            carencia.save()

            # Criar notificação se solicitado
            if request.POST.get("criar_notificacao"):
                Notificacao = get_model_dynamically("notificacoes", "Notificacao")

                notificacao = Notificacao.objects.create(
                    aluno=carencia.aluno,
                    carencia=carencia,
                    assunto=request.POST.get("assunto"),
                    mensagem=request.POST.get("mensagem"),
                    criado_por=request.user,
                    data_criacao=timezone.now(),
                )

                # Enviar notificação imediatamente se solicitado
                if request.POST.get("enviar_agora"):
                    notificacao.status = "ENVIADA"
                    notificacao.data_envio = timezone.now()
                    notificacao.enviado_por = request.user
                    notificacao.save()

                    # Lógica para enviar a notificação (e-mail, SMS, etc.)
                    try:
                        # Implementar envio de notificação
                        pass
                    except Exception as e:
                        logger.error(
                            f"Erro ao enviar notificação: {str(e)}", exc_info=True
                        )
                        messages.warning(
                            request,
                            f"Acompanhamento iniciado, mas houve um erro ao enviar a notificação: {str(e)}",
                        )
                        return redirect(
                            "frequencias:detalhar_carencia", carencia_id=carencia.id
                        )

            messages.success(request, "Acompanhamento iniciado com sucesso!")
            return redirect("frequencias:detalhar_carencia", carencia_id=carencia.id)

        context = {"carencia": carencia, "data_atual": timezone.now().date()}

        return render(request, "frequencias/iniciar_acompanhamento.html", context)

    except Exception as e:
        logger.error(f"Erro ao iniciar acompanhamento: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao iniciar acompanhamento: {str(e)}")
        return redirect("frequencias:detalhar_carencia", carencia_id=carencia_id)
