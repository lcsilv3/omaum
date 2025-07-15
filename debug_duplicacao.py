#!/usr/bin/env python
"""
Script para debuggar a duplicação de management forms
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse


def debug_formset_duplication():
    """Debug específico para encontrar duplicação"""
    client = Client()

    # Criar/logar usuário
    username = "lcsilv3"
    password = "iG356900"
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

    client.login(username=username, password=password)

    # Testar URL de criação
    print("🔍 TESTANDO URL: alunos:criar_aluno")
    url = reverse("alunos:criar_aluno")
    response = client.get(url)
    
    if response.status_code != 200:
        print(f"❌ ERRO: Status {response.status_code}")
        return

    html = response.content.decode()
    
    # Procurar todas as ocorrências do management form
    total_forms_positions = []
    search_start = 0
    while True:
        pos = html.find('name="historico-TOTAL_FORMS"', search_start)
        if pos == -1:
            break
        total_forms_positions.append(pos)
        search_start = pos + 1
    
    print(f"📊 TOTAL_FORMS encontrados: {len(total_forms_positions)}")
    
    for i, pos in enumerate(total_forms_positions):
        # Mostrar contexto ao redor de cada ocorrência
        start = max(0, pos - 200)
        end = min(len(html), pos + 200)
        context = html[start:end]
        print(f"\n--- OCORRÊNCIA {i+1} (posição {pos}) ---")
        print(context)
        print("--- FIM OCORRÊNCIA ---")
    
    # Verificar se há MANAGEMENT_FORM_START/END duplicados
    mgmt_starts = html.count("MANAGEMENT_FORM_START")
    mgmt_ends = html.count("MANAGEMENT_FORM_END")
    
    print("\n🔍 MARCADORES DEBUG:")
    print(f"  - MANAGEMENT_FORM_START: {mgmt_starts}")
    print(f"  - MANAGEMENT_FORM_END: {mgmt_ends}")
    
    # Verificar se há includes duplicados
    includes_count = html.count("{% include")
    print(f"  - Includes encontrados: {includes_count}")


if __name__ == "__main__":
    debug_formset_duplication()
