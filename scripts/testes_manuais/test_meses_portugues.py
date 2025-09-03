#!/usr/bin/env python
"""
Teste rápido para verificar se os nomes dos meses estão em português.
"""

import os
import sys
import django

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()

from presencas.forms import RegistrarPresencaForm


def test_mes_em_portugues():
    """Testa se os nomes dos meses estão em português."""
    form = RegistrarPresencaForm()
    choices = form.fields["mes"].choices

    meses_esperados = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    print("Verificando nomes dos meses no formulário:")
    for i, (valor, nome) in enumerate(choices, 1):
        esperado = meses_esperados[i - 1]
        if nome == esperado:
            print(f"✓ {i}: {nome}")
        else:
            print(f"✗ {i}: {nome} (esperado: {esperado})")
            return False

    print("\n✓ Todos os meses estão em português!")
    return True


if __name__ == "__main__":
    test_mes_em_portugues()
