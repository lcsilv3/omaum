"""Serviço para edição inline de Presenças (create/update/delete).
Mantém transações curtas e validações centralizadas.
"""

from typing import Tuple
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from presencas.models import RegistroPresenca
from presencas.permissions import PresencaPermissionEngine
from presencas.domain.rules import (
    PresencaChange,
    aplicar_change,
    validar_data_nao_futura,
)
from presencas.repositories.presenca_repo import invalidate_period_cache


class InlinePresencaService:
    @staticmethod
    def atualizar(
        presenca: RegistroPresenca, change: PresencaChange, user: User
    ) -> Tuple[RegistroPresenca, dict]:
        pode_alterar, motivo = PresencaPermissionEngine.pode_alterar_presenca(
            presenca, user
        )
        if not pode_alterar:
            raise PermissionDenied(motivo)

        # Valida data não futura
        validar_data_nao_futura(presenca.data)

        snapshot = {
            "presente": presenca.presente,
            "justificativa": presenca.justificativa or "",
        }
        novo, diff = aplicar_change(snapshot, change)
        if not diff:
            return presenca, {}

        presenca.presente = novo["presente"]
        presenca.justificativa = novo["justificativa"]
        presenca.registrado_por = (
            f"{presenca.registrado_por} (edit inline {user.username})"
        )
        presenca.save(update_fields=["status", "justificativa", "registrado_por"])

        # Atualizar flag de convocação se fornecida
        if change.convocado is not None:
            presenca.convocado = change.convocado
            presenca.save(update_fields=["convocado"])
        
        # Invalidar cache do período
        invalidate_period_cache(
            presenca.turma_id, presenca.data.year, presenca.data.month
        )
        return presenca, diff

    @staticmethod
    def excluir(presenca: RegistroPresenca, user: User) -> Tuple[int, bool]:
        pode_alterar, motivo = PresencaPermissionEngine.pode_alterar_presenca(
            presenca, user
        )
        if not pode_alterar:
            raise PermissionDenied(motivo)
        validar_data_nao_futura(presenca.data)
        dia = presenca.data.day
        atividade_id = presenca.atividade_id
        turma_id = presenca.turma_id
        with transaction.atomic():
            presenca.delete()
            # Verificar se restam presenças no mesmo dia/atividade
            vazio = not RegistroPresenca.objects.filter(
                turma_id=turma_id,
                atividade_id=atividade_id,
                data=presenca.data,
            ).exists()
        # Invalidar cache do período
        invalidate_period_cache(turma_id, presenca.data.year, presenca.data.month)
        return dia, vazio
