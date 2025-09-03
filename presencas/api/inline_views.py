"""Views API simples para edição inline de presenças.
Fase 1: PATCH e DELETE.
"""

import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from presencas.models import Presenca
from presencas.services.inline_edit import InlinePresencaService
from presencas.domain.rules import PresencaChange


@login_required
@csrf_exempt
@require_http_methods(["PATCH"])
def presenca_patch(request, pk: int):
    presenca = get_object_or_404(Presenca, pk=pk)
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON_INVALIDO"}, status=400)

    change = PresencaChange(
        presente=payload.get("presente"),
        justificativa=payload.get("justificativa"),
        convocado=payload.get("convocado"),
    )
    try:
        presenca, diff = InlinePresencaService.atualizar(presenca, change, request.user)
        return JsonResponse({"success": True, "id": presenca.id, "diff": diff})
    except PermissionDenied as e:
        return JsonResponse(
            {"success": False, "error": "PERMISSAO_NEGADA", "motivo": str(e)},
            status=403,
        )
    except Exception:
        return JsonResponse({"success": False, "error": "ERRO_INTERNO"}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def presenca_delete(request, pk: int):
    presenca = get_object_or_404(Presenca, pk=pk)
    try:
        dia, vazio = InlinePresencaService.excluir(presenca, request.user)
        return JsonResponse(
            {
                "success": True,
                "dia": dia,
                "dia_vazio": vazio,
                "atividade_id": presenca.atividade_id,
            }
        )
    except PermissionDenied as e:
        return JsonResponse(
            {"success": False, "error": "PERMISSAO_NEGADA", "motivo": str(e)},
            status=403,
        )
    except Exception:
        return JsonResponse({"success": False, "error": "ERRO_INTERNO"}, status=500)
