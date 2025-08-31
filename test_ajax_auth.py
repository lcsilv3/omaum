#!/usr/bin/env python3
"""
Script para testar o endpoint AJAX de busca de alunos.
"""

import requests
import json

# URL do endpoint
url = "http://localhost:8000/alunos/search/"

# Headers para simular requisição AJAX
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json",
}

# Faz a requisição sem autenticação
try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Text: {response.text[:500]}...")

    if response.status_code == 401:
        print("✅ Middleware funcionando! Retornou 401 para AJAX não autenticado.")
        try:
            data = response.json()
            print(f"JSON Response: {data}")
        except json.JSONDecodeError:
            print("❌ Resposta não é JSON válido")
    else:
        print("❌ Middleware não funcionou como esperado")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
