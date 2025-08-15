"""Repositório para consultas agregadas de Presença.
Centraliza padrões de queries para reduzir N+1 e duplicações.
Inclui um cache simples por período (turma/ano/mês) com TTL curto.
"""

from typing import Dict
from django.core.cache import cache
from presencas.models import Presenca, ConvocacaoPresenca


CACHE_TTL_SECONDS = 60  # cache curto para evitar dados obsoletos após alterações


def _key_presencas(turma_id: int, ano: int, mes: int) -> str:
    return f"presencas:mapa:{turma_id}:{ano}:{mes}"


def _key_convocacoes(turma_id: int, ano: int, mes: int) -> str:
    return f"presencas:convocacoes:{turma_id}:{ano}:{mes}"


def mapa_presencas_periodo(
    turma_id: int, ano: int, mes: int
) -> Dict[str, Dict[int, Dict[str, dict]]]:
    """Retorna mapa: atividade_id -> dia -> cpf -> dados de presença.
    Usa cache curto por período para reduzir consultas repetidas.
    """
    cache_key = _key_presencas(turma_id, ano, mes)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    qs = Presenca.objects.filter(
        turma_id=turma_id, data__year=ano, data__month=mes
    ).select_related("aluno", "atividade")
    estrutura: Dict[str, Dict[int, Dict[str, dict]]] = {}
    for p in qs:
        atividade_id = str(p.atividade_id)
        dia = p.data.day
        by_dia = estrutura.setdefault(atividade_id, {})
        by_cpf = by_dia.setdefault(dia, {})
        by_cpf[p.aluno.cpf] = {
            "id": p.id,
            "presente": p.presente,
            "justificativa": p.justificativa or "",
        }

    cache.set(cache_key, estrutura, CACHE_TTL_SECONDS)
    return estrutura


def mapa_convocacoes_periodo(turma_id: int, ano: int, mes: int) -> Dict[tuple, bool]:
    """Retorna mapa: (atividade_id, dia, cpf) -> convocado.
    Usa cache curto por período para reduzir consultas repetidas.
    """
    cache_key = _key_convocacoes(turma_id, ano, mes)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    qs = ConvocacaoPresenca.objects.filter(
        turma_id=turma_id, data__year=ano, data__month=mes
    )
    mapa = {(str(c.atividade_id), c.data.day, c.aluno.cpf): c.convocado for c in qs}
    cache.set(cache_key, mapa, CACHE_TTL_SECONDS)
    return mapa


def invalidate_period_cache(turma_id: int, ano: int, mes: int) -> None:
    """Invalida caches do período para refletir alterações imediatas."""
    cache.delete_many(
        [
            _key_presencas(turma_id, ano, mes),
            _key_convocacoes(turma_id, ano, mes),
        ]
    )
