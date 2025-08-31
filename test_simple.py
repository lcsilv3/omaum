#!/usr/bin/env python
"""
Script simples para testar paginação
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')

try:
    django.setup()
    print("Django configurado com sucesso")
except Exception as e:
    print(f"Erro ao configurar Django: {e}")
    sys.exit(1)

from django.test import Client
from django.contrib.auth.models import User

def test_simple():
    print("=== TESTE SIMPLES DE PAGINAÇÃO ===")

    try:
        # Verificar se há alunos no banco
        from alunos.models import Aluno
        total_alunos = Aluno.objects.count()
        print(f"Total de alunos no banco: {total_alunos}")

        # Criar cliente
        client = Client()

        # Criar usuário se necessário
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
            print("Superusuário criado")

        # Login
        login_result = client.login(username='admin', password='admin123')
        print(f"Login realizado: {login_result}")

        # Teste página 1
        print("\n--- Teste /alunos/?page=1 ---")
        response = client.get('/alunos/?page=1')
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.get('Content-Type', 'N/A')}")

        # Teste página 2
        print("\n--- Teste /alunos/?page=2 ---")
        response2 = client.get('/alunos/?page=2')
        print(f"Status: {response2.status_code}")
        print(f"Content-Type: {response2.get('Content-Type', 'N/A')}")

        # Teste AJAX página 2
        print("\n--- Teste AJAX /alunos/?page=2 ---")
        response3 = client.get('/alunos/?page=2', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        print(f"Status: {response3.status_code}")
        print(f"Content-Type: {response3.get('Content-Type', 'N/A')}")

        if response3.status_code == 200:
            try:
                import json
                data = response3.json()
                print(f"Resposta JSON: {data.keys() if isinstance(data, dict) else 'Não é dict'}")
            except:
                print("Resposta não é JSON válido")
                print(f"Conteúdo: {response3.content.decode('utf-8', errors='ignore')[:200]}")

    except Exception as e:
        print(f"Erro durante teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_simple()
