#!/usr/bin/env python
"""
Script para testar paginação de alunos
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_pagination():
    print("=== TESTE DE PAGINAÇÃO DE ALUNOS ===")

    # Criar cliente de teste
    client = Client()

    # Criar usuário de teste se não existir
    if not User.objects.filter(username='testuser').exists():
        User.objects.create_user('testuser', 'test@example.com', 'password123')
        print("✅ Usuário de teste criado")

    # Fazer login
    login_success = client.login(username='testuser', password='password123')
    print(f"Login realizado: {login_success}")

    # Testar requisição para página 1
    print("\n--- Teste Página 1 ---")
    response1 = client.get('/alunos/?page=1', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    print(f"Status Code: {response1.status_code}")
    print(f"Content Type: {response1.get('Content-Type', 'N/A')}")

    if response1.status_code == 200:
        try:
            import json
            data1 = response1.json()
            print(f"Página atual: {data1.get('page', 'N/A')}")
            print(f"Total de páginas: {data1.get('num_pages', 'N/A')}")
            print(f"Total de alunos: {data1.get('total_alunos', 'N/A')}")
        except Exception as e:
            print(f"Erro ao parsear JSON: {e}")
            print(f"Conteúdo (primeiros 200 chars): {response1.content.decode('utf-8', errors='ignore')[:200]}")
    else:
        print(f"❌ Erro na requisição página 1: {response1.status_code}")
        print(f"Conteúdo do erro: {response1.content.decode('utf-8', errors='ignore')}")

    # Testar requisição para página 2
    print("\n--- Teste Página 2 ---")
    response2 = client.get('/alunos/?page=2', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    print(f"Status Code: {response2.status_code}")
    print(f"Content Type: {response2.get('Content-Type', 'N/A')}")

    if response2.status_code == 200:
        try:
            import json
            data2 = response2.json()
            print(f"Página atual: {data2.get('page', 'N/A')}")
            print(f"Total de páginas: {data2.get('num_pages', 'N/A')}")
            print(f"Total de alunos: {data2.get('total_alunos', 'N/A')}")
        except Exception as e:
            print(f"Erro ao parsear JSON: {e}")
            print(f"Conteúdo (primeiros 200 chars): {response2.content.decode('utf-8', errors='ignore')[:200]}")
    else:
        print(f"❌ Erro na requisição página 2: {response2.status_code}")
        print(f"Conteúdo do erro: {response2.content.decode('utf-8', errors='ignore')}")

    # Testar requisição sem AJAX
    print("\n--- Teste Página 2 (sem AJAX) ---")
    response3 = client.get('/alunos/?page=2')
    print(f"Status Code: {response3.status_code}")
    print(f"Content Type: {response3.get('Content-Type', 'N/A')}")

    if response3.status_code == 200:
        print("✅ Página 2 (HTML) carregada com sucesso")
    else:
        print(f"❌ Erro na requisição página 2 (HTML): {response3.status_code}")

if __name__ == '__main__':
    test_pagination()
