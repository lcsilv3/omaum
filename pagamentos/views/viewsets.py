import datetime
import json
import logging
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from importlib import import_module


logger = logging.getLogger(__name__)


def get_pagamento_model():
    pagamentos_module = import_module("pagamentos.models")
    return getattr(pagamentos_module, "Pagamento")


def get_aluno_model():
    alunos_module = import_module("alunos.models")
    return getattr(alunos_module, "Aluno")


def get_pagamento_or_404(pagamento_id):
    Pagamento = get_pagamento_model()
    from django.shortcuts import get_object_or_404

    return get_object_or_404(Pagamento, id=pagamento_id)


@login_required
def buscar_alunos_com_pagamentos_pendentes(request):
    """
    API para buscar alunos com pagamentos pendentes ou atrasados.
    """
    try:
        query = request.GET.get("q", "")
        if len(query) < 2:
            return JsonResponse([], safe=False)
        Pagamento = get_pagamento_model()
        Aluno = get_aluno_model()
        alunos_com_pagamentos = Aluno.objects.filter(
            Q(nome__icontains=query)
            | Q(cpf__icontains=query)
            | Q(numero_iniciatico__icontains=query),
            pagamento__status__in=["PENDENTE", "ATRASADO"],
        ).distinct()[:10]
        resultados = []
        for aluno in alunos_com_pagamentos:
            pagamentos_pendentes = Pagamento.objects.filter(
                aluno=aluno, status="PENDENTE"
            ).count()
            pagamentos_atrasados = Pagamento.objects.filter(
                aluno=aluno, status="ATRASADO"
            ).count()
            resultados.append(
                {
                    "cpf": aluno.cpf,
                    "nome": aluno.nome,
                    "numero_iniciatico": aluno.numero_iniciatico or "N/A",
                    "foto": aluno.foto.url
                    if hasattr(aluno, "foto") and aluno.foto
                    else None,
                    "pagamentos_pendentes": pagamentos_pendentes,
                    "pagamentos_atrasados": pagamentos_atrasados,
                    "total_pendente": pagamentos_pendentes + pagamentos_atrasados,
                }
            )
        return JsonResponse(resultados, safe=False)
    except Exception as e:
        logger.error(
            f"Erro em buscar_alunos_com_pagamentos_pendentes: {str(e)}", exc_info=True
        )
        return JsonResponse(
            {"status": "error", "message": f"Erro ao buscar alunos: {str(e)}"},
            status=500,
        )


@login_required
def api_buscar_pagamentos_aluno(request, aluno_id):
    """
    API para buscar pagamentos de um aluno específico.
    """
    try:
        Pagamento = get_pagamento_model()
        Aluno = get_aluno_model()
        try:
            aluno = Aluno.objects.get(cpf=aluno_id)
        except Aluno.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Aluno não encontrado."}, status=404
            )
        pagamentos = Pagamento.objects.filter(aluno=aluno).order_by("-data_vencimento")
        resultados = []
        for pagamento in pagamentos:
            resultados.append(
                {
                    "id": pagamento.id,
                    "valor": float(pagamento.valor),
                    "data_vencimento": pagamento.data_vencimento.strftime("%d/%m/%Y"),
                    "status": pagamento.status,
                    "status_display": pagamento.get_status_display(),
                    "observacoes": pagamento.observacoes,
                    "data_pagamento": pagamento.data_pagamento.strftime("%d/%m/%Y")
                    if pagamento.data_pagamento
                    else None,
                    "valor_pago": float(pagamento.valor_pago)
                    if pagamento.valor_pago is not None
                    else None,
                    "metodo_pagamento": pagamento.metodo_pagamento,
                    "metodo_pagamento_display": pagamento.get_metodo_pagamento_display()
                    if pagamento.metodo_pagamento
                    else None,
                }
            )
        return JsonResponse(resultados, safe=False)
    except Exception as e:
        logger.error(f"Erro em api_buscar_pagamentos_aluno: {str(e)}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": f"Erro ao buscar pagamentos: {str(e)}"},
            status=500,
        )


@login_required
@require_http_methods(["POST"])
def api_registrar_pagamento(request):
    """
    API para registrar um pagamento via AJAX.
    """
    try:
        data = json.loads(request.body)
        aluno_id = data.get("aluno_id")
        valor = data.get("valor")
        data_vencimento = data.get("data_vencimento")
        observacoes = data.get("observacoes", "")
        status = data.get("status", "PENDENTE")
        if not aluno_id or not valor or not data_vencimento:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Aluno, valor e data de vencimento são obrigatórios.",
                },
                status=400,
            )
        Pagamento = get_pagamento_model()
        Aluno = get_aluno_model()
        try:
            aluno = Aluno.objects.get(cpf=aluno_id)
        except Aluno.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Aluno não encontrado."}, status=404
            )
        try:
            valor = float(valor)
        except ValueError:
            return JsonResponse(
                {"status": "error", "message": "Valor inválido."}, status=400
            )
        try:
            data_vencimento = datetime.datetime.strptime(
                data_vencimento, "%Y-%m-%d"
            ).date()
        except ValueError:
            return JsonResponse(
                {"status": "error", "message": "Data de vencimento inválida."},
                status=400,
            )
        data_pagamento = None
        valor_pago = None
        metodo_pagamento = None
        if status == "PAGO":
            data_pagamento_str = data.get("data_pagamento")
            valor_pago_str = data.get("valor_pago")
            metodo_pagamento = data.get("metodo_pagamento")
            if not data_pagamento_str:
                data_pagamento = timezone.now().date()
            else:
                try:
                    data_pagamento = datetime.datetime.strptime(
                        data_pagamento_str, "%Y-%m-%d"
                    ).date()
                except ValueError:
                    return JsonResponse(
                        {"status": "error", "message": "Data de pagamento inválida."},
                        status=400,
                    )
            if not valor_pago_str:
                valor_pago = valor
            else:
                try:
                    valor_pago = float(valor_pago_str)
                except ValueError:
                    return JsonResponse(
                        {"status": "error", "message": "Valor pago inválido."},
                        status=400,
                    )
        pagamento = Pagamento(
            aluno=aluno,
            valor=valor,
            data_vencimento=data_vencimento,
            observacoes=observacoes,
            status=status,
            data_pagamento=data_pagamento,
            valor_pago=valor_pago,
            metodo_pagamento=metodo_pagamento,
        )
        pagamento.save()
        return JsonResponse(
            {
                "status": "success",
                "message": "Pagamento registrado com sucesso.",
                "pagamento_id": pagamento.id,
            }
        )
    except Exception as e:
        logger.error(f"Erro em api_registrar_pagamento: {str(e)}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": f"Erro ao registrar pagamento: {str(e)}"},
            status=500,
        )


@login_required
@require_http_methods(["POST"])
def api_atualizar_pagamento(request, pagamento_id):
    """
    API para atualizar um pagamento via AJAX.
    """
    try:
        data = json.loads(request.body)
        pagamento = get_pagamento_or_404(pagamento_id)
        if "valor" in data:
            try:
                pagamento.valor = float(data["valor"])
            except ValueError:
                return JsonResponse(
                    {"status": "error", "message": "Valor inválido."}, status=400
                )
        if "data_vencimento" in data:
            try:
                pagamento.data_vencimento = datetime.datetime.strptime(
                    data["data_vencimento"], "%Y-%m-%d"
                ).date()
            except ValueError:
                return JsonResponse(
                    {"status": "error", "message": "Data de vencimento inválida."},
                    status=400,
                )
        if "observacoes" in data:
            pagamento.observacoes = data["observacoes"]
        if "status" in data:
            Pagamento = get_pagamento_model()
            status = data["status"]
            if status not in [choice[0] for choice in Pagamento.STATUS_CHOICES]:
                return JsonResponse(
                    {"status": "error", "message": "Status inválido."}, status=400
                )
            pagamento.status = status
            if status == "PAGO":
                if "data_pagamento" in data:
                    try:
                        pagamento.data_pagamento = datetime.datetime.strptime(
                            data["data_pagamento"], "%Y-%m-%d"
                        ).date()
                    except ValueError:
                        return JsonResponse(
                            {
                                "status": "error",
                                "message": "Data de pagamento inválida.",
                            },
                            status=400,
                        )
                else:
                    pagamento.data_pagamento = timezone.now().date()
                if "valor_pago" in data:
                    try:
                        pagamento.valor_pago = float(data["valor_pago"])
                    except ValueError:
                        return JsonResponse(
                            {"status": "error", "message": "Valor pago inválido."},
                            status=400,
                        )
                else:
                    pagamento.valor_pago = pagamento.valor
                if "metodo_pagamento" in data:
                    pagamento.metodo_pagamento = data["metodo_pagamento"]
            elif status != "PAGO":
                pagamento.data_pagamento = None
                pagamento.valor_pago = None
                pagamento.metodo_pagamento = None
        pagamento.save()
        return JsonResponse(
            {"status": "success", "message": "Pagamento atualizado com sucesso."}
        )
    except Exception as e:
        logger.error(f"Erro em api_atualizar_pagamento: {str(e)}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": f"Erro ao atualizar pagamento: {str(e)}"},
            status=500,
        )


@login_required
@require_http_methods(["POST"])
def api_excluir_pagamento(request, pagamento_id):
    """
    API para excluir um pagamento via AJAX.
    """
    try:
        pagamento = get_pagamento_or_404(pagamento_id)
        pagamento.delete()
        return JsonResponse(
            {"status": "success", "message": "Pagamento excluído com sucesso."}
        )
    except Exception as e:
        logger.error(f"Erro em api_excluir_pagamento: {str(e)}", exc_info=True)
        return JsonResponse(
            {"status": "error", "message": f"Erro ao excluir pagamento: {str(e)}"},
            status=500,
        )


@login_required
@require_http_methods(["POST"])
def atualizar_status_pagamento(request, pagamento_id):
    """
    API para atualizar o status de um pagamento.
    """
    try:
        Pagamento = get_pagamento_model()
        pagamento = get_pagamento_or_404(pagamento_id)
        status = request.POST.get("status")
        if status not in [choice[0] for choice in Pagamento.STATUS_CHOICES]:
            return JsonResponse(
                {"status": "error", "message": "Status inválido."}, status=400
            )
        if status == "PAGO":
            data_pagamento = request.POST.get("data_pagamento")
            valor_pago = request.POST.get("valor_pago")
            metodo_pagamento = request.POST.get("metodo_pagamento")
            if not data_pagamento:
                data_pagamento = timezone.now().date()
            else:
                try:
                    data_pagamento = datetime.datetime.strptime(
                        data_pagamento, "%Y-%m-%d"
                    ).date()
                except ValueError:
                    return JsonResponse(
                        {"status": "error", "message": "Data de pagamento inválida."},
                        status=400,
                    )
            if not valor_pago:
                valor_pago = pagamento.valor
            else:
                try:
                    valor_pago = float(valor_pago)
                except ValueError:
                    return JsonResponse(
                        {"status": "error", "message": "Valor pago inválido."},
                        status=400,
                    )
            pagamento.status = status
            pagamento.data_pagamento = data_pagamento
            pagamento.valor_pago = valor_pago
            pagamento.metodo_pagamento = metodo_pagamento
        else:
            pagamento.status = status
            if status != "PAGO":
                pagamento.data_pagamento = None
                pagamento.valor_pago = None
                pagamento.metodo_pagamento = None
        pagamento.save()
        return JsonResponse(
            {"status": "success", "message": "Status atualizado com sucesso."}
        )
    except Exception as e:
        logger.error(f"Erro em atualizar_status_pagamento: {str(e)}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def api_listar_pagamentos(request):
    Pagamento = get_pagamento_model()
    pagamentos = Pagamento.objects.select_related("aluno").all()
    data = [
        {
            "id": p.id,
            "aluno": p.aluno.nome,
            "valor": float(p.valor),
            "status": p.status,
            "data_vencimento": p.data_vencimento,
        }
        for p in pagamentos
    ]
    return JsonResponse(data, safe=False)
