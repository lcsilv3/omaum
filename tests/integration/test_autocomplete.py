#!/usr/bin/env python
"""Script para testar o autocomplete de cidades."""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
import json

User = get_user_model()
user = User.objects.first()

client = Client()
client.force_login(user)

# Testar cidade autocomplete com forward de estado
print("=" * 60)
print("Testando CidadeAutocomplete com estado_ref=14 (AL)")
print("=" * 60)

# Simular a requisição com forward
response = client.get(
    '/alunos/autocomplete/cidade-autocomplete/',
    {
        'q': 'mac',
        'forward': json.dumps({"estado_ref": "14"})
    }
)

print(f"Status: {response.status_code}")
print(f"Content: {response.content.decode()}")

# Teste sem estado
print("\n" + "=" * 60)
print("Testando CidadeAutocomplete SEM filtro de estado")
print("=" * 60)

response2 = client.get(
    '/alunos/autocomplete/cidade-autocomplete/',
    {'q': 'mac'}
)

print(f"Status: {response2.status_code}")
print(f"Content (primeiros 500 chars): {response2.content.decode()[:500]}")
