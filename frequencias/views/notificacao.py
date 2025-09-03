from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from importlib import import_module
import logging

logger = logging.getLogger(__name__)


def get_models():
    """Obtém os modelos FrequenciaMensal e Carencia."""
    frequencias_module = import_module("frequencias.models")
    FrequenciaMensal = getattr(frequencias_module, "FrequenciaMensal")
    Carencia = getattr(frequencias_module, "Carencia")
    return FrequenciaMensal, Carencia


def get_model_dynamically(app_name, model_name):
    """Obtém um modelo dinamicamente para evitar importações circulares."""
    module = import_module(f"{app_name}.models")
    return getattr(module, model_name)


@login_required
def criar_notificacao(request, carencia_id):
    """Cria uma notificação para uma carência."""
    try:
        _, Carencia = get_models()
        carencia = get_object_or_404(Carencia, id=carencia_id)

        if request.method == "POST":
            Notificacao = get_model_dynamically("notificacoes", "Notificacao")

            notificacao = Notificacao.objects.create(
                aluno=carencia.aluno,
                carencia=carencia,
                assunto=request.POST.get("assunto"),
                mensagem=request.POST.get("mensagem"),
                tipo_notificacao=request.POST.get("tipo_notificacao"),
                prioridade=request.POST.get("prioridade"),
                criado_por=request.user,
                data_criacao=timezone.now(),
            )

            # Processar anexos
            for arquivo in request.FILES.getlist("anexos"):
                Anexo = get_model_dynamically("notificacoes", "Anexo")

                Anexo.objects.create(
                    notificacao=notificacao,
                    nome=arquivo.name,
                    arquivo=arquivo,
                    uploaded_by=request.user,
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
                    logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
                    messages.warning(
                        request,
                        f"Notificação criada, mas houve um erro ao enviá-la: {str(e)}",
                    )
                    return redirect(
                        "frequencias:detalhar_notificacao",
                        notificacao_id=notificacao.id,
                    )

            messages.success(request, "Notificação criada com sucesso!")
            return redirect(
                "frequencias:detalhar_notificacao", notificacao_id=notificacao.id
            )

        context = {"carencia": carencia}

        return render(request, "frequencias/criar_notificacao.html", context)

    except Exception as e:
        logger.error(f"Erro ao criar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao criar notificação: {str(e)}")
        return redirect("frequencias:detalhar_carencia", carencia_id=carencia_id)


@login_required
def detalhar_notificacao(request, notificacao_id):
    """Exibe os detalhes de uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)

        context = {"notificacao": notificacao}

        return render(request, "frequencias/detalhar_notificacao.html", context)

    except Exception as e:
        logger.error(f"Erro ao detalhar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao detalhar notificação: {str(e)}")
        return redirect("frequencias:listar_frequencias")


@login_required
def editar_notificacao(request, notificacao_id):
    """Edita uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)

        # Verificar se a notificação já foi enviada
        if notificacao.status != "PENDENTE":
            messages.warning(
                request, "Esta notificação já foi enviada e não pode ser editada."
            )
            return redirect(
                "frequencias:detalhar_notificacao", notificacao_id=notificacao.id
            )

        if request.method == "POST":
            action = request.POST.get("action", "salvar")

            # Atualizar dados da notificação
            notificacao.assunto = request.POST.get("assunto")
            notificacao.mensagem = request.POST.get("mensagem")

            # Processar anexos
            for arquivo in request.FILES.getlist("anexos"):
                Anexo = get_model_dynamically("notificacoes", "Anexo")

                anexo = Anexo.objects.create(
                    notificacao=notificacao,
                    nome=arquivo.name,
                    arquivo=arquivo,
                    uploaded_by=request.user,
                )

            # Remover anexos selecionados
            for anexo_id in request.POST.getlist("remover_anexos"):
                Anexo = get_model_dynamically("notificacoes", "Anexo")
                anexo = get_object_or_404(Anexo, id=anexo_id)
                anexo.delete()

            notificacao.save()

            # Enviar notificação se solicitado
            if action == "salvar_enviar":
                notificacao.status = "ENVIADA"
                notificacao.data_envio = timezone.now()
                notificacao.enviado_por = request.user
                notificacao.save()

                # Lógica para enviar a notificação (e-mail, SMS, etc.)
                try:
                    # Implementar envio de notificação
                    pass
                except Exception as e:
                    logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
                    messages.warning(
                        request,
                        f"Notificação atualizada, mas houve um erro ao enviá-la: {str(e)}",
                    )
                    return redirect(
                        "frequencias:detalhar_notificacao",
                        notificacao_id=notificacao.id,
                    )

                messages.success(
                    request, "Notificação atualizada e enviada com sucesso!"
                )
            else:
                messages.success(request, "Notificação atualizada com sucesso!")

            return redirect(
                "frequencias:detalhar_notificacao", notificacao_id=notificacao.id
            )

        context = {"notificacao": notificacao}

        return render(request, "frequencias/editar_notificacao.html", context)

    except Exception as e:
        logger.error(f"Erro ao editar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao editar notificação: {str(e)}")
        return redirect(
            "frequencias:detalhar_notificacao", notificacao_id=notificacao_id
        )


@login_required
def enviar_notificacao(request, notificacao_id):
    """Envia uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)

        # Verificar se a notificação já foi enviada
        if notificacao.status != "PENDENTE":
            messages.warning(request, "Esta notificação já foi enviada.")
            return redirect(
                "frequencias:detalhar_notificacao", notificacao_id=notificacao.id
            )

        if request.method == "POST":
            # Atualizar status da notificação
            notificacao.status = "ENVIADA"
            notificacao.data_envio = timezone.now()
            notificacao.enviado_por = request.user

            # Atualizar status da carência se solicitado
            if (
                request.POST.get("marcar_acompanhamento")
                and notificacao.carencia
                and notificacao.carencia.status == "PENDENTE"
            ):
                notificacao.carencia.status = "EM_ACOMPANHAMENTO"
                notificacao.carencia.data_acompanhamento = timezone.now()
                notificacao.carencia.acompanhado_por = request.user
                notificacao.carencia.save()

            notificacao.save()

            # Enviar cópia para o usuário se solicitado
            request.POST.get("enviar_copia")

            # Lógica para enviar a notificação (e-mail, SMS, etc.)
            try:
                # Implementar envio de notificação
                pass
            except Exception as e:
                logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
                messages.warning(
                    request, f"Houve um erro ao enviar a notificação: {str(e)}"
                )
                return redirect(
                    "frequencias:detalhar_notificacao", notificacao_id=notificacao.id
                )

            messages.success(request, "Notificação enviada com sucesso!")
            return redirect(
                "frequencias:detalhar_notificacao", notificacao_id=notificacao.id
            )

        context = {"notificacao": notificacao}

        return render(request, "frequencias/enviar_notificacao.html", context)

    except Exception as e:
        logger.error(f"Erro ao enviar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao enviar notificação: {str(e)}")
        return redirect(
            "frequencias:detalhar_notificacao", notificacao_id=notificacao_id
        )


@login_required
def reenviar_notificacao(request, notificacao_id):
    """Reenvia uma notificação."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)

        # Verificar se a notificação pode ser reenviada
        if notificacao.status not in ["ENVIADA", "LIDA"]:
            messages.warning(request, "Esta notificação não pode ser reenviada.")
            return redirect(
                "frequencias:detalhar_notificacao", notificacao_id=notificacao.id
            )

        # Atualizar data de envio
        notificacao.data_envio = timezone.now()
        notificacao.enviado_por = request.user
        notificacao.save()

        # Lógica para reenviar a notificação (e-mail, SMS, etc.)
        try:
            # Implementar reenvio de notificação
            pass
        except Exception as e:
            logger.error(f"Erro ao reenviar notificação: {str(e)}", exc_info=True)
            messages.warning(
                request, f"Houve um erro ao reenviar a notificação: {str(e)}"
            )
            return redirect(
                "frequencias:detalhar_notificacao", notificacao_id=notificacao.id
            )

        messages.success(request, "Notificação reenviada com sucesso!")
        return redirect(
            "frequencias:detalhar_notificacao", notificacao_id=notificacao.id
        )

    except Exception as e:
        logger.error(f"Erro ao reenviar notificação: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao reenviar notificação: {str(e)}")
        return redirect(
            "frequencias:detalhar_notificacao", notificacao_id=notificacao_id
        )


@login_required
def responder_aluno(request, notificacao_id):
    """Responde a uma notificação do aluno."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")
        notificacao = get_object_or_404(Notificacao, id=notificacao_id)

        # Verificar se a notificação pode ser respondida
        if notificacao.status != "RESPONDIDA":
            messages.warning(request, "Esta notificação não possui resposta do aluno.")
            return redirect(
                "frequencias:detalhar_notificacao", notificacao_id=notificacao.id
            )

        if request.method == "POST":
            # Criar nova notificação como resposta
            nova_notificacao = Notificacao.objects.create(
                aluno=notificacao.aluno,
                carencia=notificacao.carencia,
                assunto=f"RE: {notificacao.assunto}",
                mensagem=request.POST.get("mensagem"),
                tipo_notificacao=notificacao.tipo_notificacao,
                prioridade=notificacao.prioridade,
                criado_por=request.user,
                data_criacao=timezone.now(),
                notificacao_pai=notificacao,
            )

            # Processar anexos
            for arquivo in request.FILES.getlist("anexos"):
                Anexo = get_model_dynamically("notificacoes", "Anexo")

                Anexo.objects.create(
                    notificacao=nova_notificacao,
                    nome=arquivo.name,
                    arquivo=arquivo,
                    uploaded_by=request.user,
                )

            # Enviar notificação imediatamente
            nova_notificacao.status = "ENVIADA"
            nova_notificacao.data_envio = timezone.now()
            nova_notificacao.enviado_por = request.user
            nova_notificacao.save()

            # Lógica para enviar a notificação (e-mail, SMS, etc.)
            try:
                # Implementar envio de notificação
                pass
            except Exception as e:
                logger.error(f"Erro ao enviar resposta: {str(e)}", exc_info=True)
                messages.warning(
                    request, f"Resposta criada, mas houve um erro ao enviá-la: {str(e)}"
                )
                return redirect(
                    "frequencias:detalhar_notificacao",
                    notificacao_id=nova_notificacao.id,
                )

            messages.success(request, "Resposta enviada com sucesso!")
            return redirect(
                "frequencias:detalhar_notificacao", notificacao_id=nova_notificacao.id
            )

        context = {"notificacao": notificacao}

        return render(request, "frequencias/responder_aluno.html", context)

    except Exception as e:
        logger.error(f"Erro ao responder aluno: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao responder aluno: {str(e)}")
        return redirect(
            "frequencias:detalhar_notificacao", notificacao_id=notificacao_id
        )


@login_required
def listar_notificacoes_carencia(request):
    """Lista todas as notificações de carência."""
    try:
        Notificacao = get_model_dynamically("notificacoes", "Notificacao")

        # Obter parâmetros de filtro
        status = request.GET.get("status")
        aluno_id = request.GET.get("aluno")
        tipo = request.GET.get("tipo")

        # Construir query base
        notificacoes = Notificacao.objects.filter(
            carencia__isnull=False
        ).select_related("aluno", "carencia")

        # Aplicar filtros
        if status:
            notificacoes = notificacoes.filter(status=status)

        if aluno_id:
            notificacoes = notificacoes.filter(aluno__cpf=aluno_id)

        if tipo:
            notificacoes = notificacoes.filter(tipo_notificacao=tipo)

        # Ordenar por data de criação (mais recente primeiro)
        notificacoes = notificacoes.order_by("-data_criacao")

        # Paginação
        paginator = Paginator(notificacoes, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "notificacoes": page_obj,
            "page_obj": page_obj,
            "filtros": {"status": status, "aluno": aluno_id, "tipo": tipo},
        }

        return render(request, "frequencias/listar_notificacoes.html", context)

    except Exception as e:
        logger.error(f"Erro ao listar notificações: {str(e)}", exc_info=True)
        messages.error(request, f"Erro ao listar notificações: {str(e)}")
        return redirect("frequencias:listar_frequencias")
