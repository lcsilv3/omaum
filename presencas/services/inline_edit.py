"""Serviço para edição inline de Presenças (create/update/delete).
Mantém transações curtas e validações centralizadas.
"""

from typing import Tuple
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from presencas.models import Presenca, ConvocacaoPresenca
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
        presenca: Presenca, change: PresencaChange, user: User
    ) -> Tuple[Presenca, dict]:
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
        presenca.save(update_fields=["presente", "justificativa", "registrado_por"])

        # Convocação opcional
        if change.convocado is not None:
            ConvocacaoPresenca.objects.update_or_create(
                aluno=presenca.aluno,
                turma=presenca.turma,
                atividade=presenca.atividade,
                data=presenca.data,
                defaults={
                    "convocado": change.convocado,
                    "registrado_por": user.username,
                },
            )
        # Invalidar cache do período
        invalidate_period_cache(
            presenca.turma_id, presenca.data.year, presenca.data.month
        )
        return presenca, diff

    @staticmethod
    def excluir(presenca: Presenca, user: User) -> Tuple[int, bool]:
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
            ConvocacaoPresenca.objects.filter(
                aluno=presenca.aluno,
                turma_id=turma_id,
                atividade_id=atividade_id,
                data=presenca.data,
            ).delete()
            # Verificar se restam presenças no mesmo dia/atividade
            vazio = not Presenca.objects.filter(
                turma_id=turma_id,
                atividade_id=atividade_id,
                data=presenca.data,
            ).exists()
        # Invalidar cache do período
        invalidate_period_cache(turma_id, presenca.data.year, presenca.data.month)
        return dia, vazio
