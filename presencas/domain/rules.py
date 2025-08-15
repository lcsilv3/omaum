"""Regras de domínio e validações puras para Presenças.
Mantém lógica isolada de frameworks para facilitar testes unitários.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional, Tuple


@dataclass(frozen=True)
class PresencaChange:
    presente: Optional[bool] = None
    justificativa: Optional[str] = None
    convocado: Optional[bool] = None


def validar_data_nao_futura(data_ref: date, hoje: Optional[date] = None) -> None:
    from datetime import date as _d

    h = hoje or _d.today()
    if data_ref > h:
        raise ValueError("Data da presença não pode ser futura.")


def validar_justificativa(presente: bool, justificativa: str) -> None:
    if presente and justificativa and justificativa.strip():
        # Política: justificativa apenas para ausências; ajustar se regra mudar.
        pass
    if not presente:
        # Aceita justificativa vazia; nenhuma regra adicional agora.
        return


def aplicar_change(orig: dict, change: PresencaChange) -> Tuple[dict, dict]:
    """Aplica alterações em um snapshot (dict) retornando (novo, diff).
    - Somente campos não None no change são considerados.
    - diff retorna apenas campos modificados e seus novos valores.
    """
    novo = orig.copy()
    diff = {}
    for campo in ("presente", "justificativa", "convocado"):
        valor = getattr(change, campo)
        if valor is not None and novo.get(campo) != valor:
            novo[campo] = valor
            diff[campo] = valor
    return novo, diff
