#!/usr/bin/env python
"""
Teste direto do formset
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from alunos.forms import RegistroHistoricoFormSet


def test_formset_direct():
    """Testa o formset diretamente"""
    # Criar formset vazio
    formset = RegistroHistoricoFormSet(prefix="historico")

    # Renderizar management form
    mgmt_form = str(formset.management_form)
    print("Management form renderizado:")
    print(mgmt_form)
    print()

    # Contar quantos campos TOTAL_FORMS existem
    total_forms_count = mgmt_form.count('name="historico-TOTAL_FORMS"')
    print(f"Campos TOTAL_FORMS no management form: {total_forms_count}")

    # Verificar se há duplicação interna
    if total_forms_count > 1:
        print("❌ ERRO: Duplicação encontrada no próprio formset!")
    else:
        print("✅ Management form parece OK")


if __name__ == "__main__":
    test_formset_direct()
