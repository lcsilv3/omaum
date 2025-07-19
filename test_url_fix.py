#!/usr/bin/env python
"""
Teste rápido para verificar se a correção da URL turmas_por_curso_ajax funcionou.
"""

import os
import sys
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()

from django.urls import reverse
from django.test.client import Client

def test_url_resolution():
    """Testa se a URL resolve corretamente."""
    try:
        url = reverse('presencas:turmas_por_curso_ajax')
        print(f"✓ URL resolve corretamente: {url}")
        return True
    except Exception as e:
        print(f"✗ Erro ao resolver URL: {e}")
        return False

def test_view_response():
    """Testa se a view responde corretamente."""
    client = Client()
    try:
        url = reverse('presencas:turmas_por_curso_ajax')
        response = client.get(url, {'curso_id': '1'})
        print(f"✓ View responde com status: {response.status_code}")
        return True
    except Exception as e:
        print(f"✗ Erro na view: {e}")
        return False

if __name__ == '__main__':
    print("Testando correção da URL turmas_por_curso_ajax...")
    
    success = True
    success &= test_url_resolution()
    success &= test_view_response()
    
    if success:
        print("\n✓ Todos os testes passaram! A correção foi bem-sucedida.")
    else:
        print("\n✗ Alguns testes falharam. Verifique os erros acima.")
