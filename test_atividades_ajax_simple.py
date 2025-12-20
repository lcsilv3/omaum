#!/usr/bin/env python
"""
Teste de requisição AJAX para atividades
"""
import requests
import json

# Fazer login primeiro para obter cookie de sessão
login_url = "http://localhost:8000/entrar/"
ajax_url = "http://localhost:8000/atividades/"

session = requests.Session()

# 1. Login
print("🔐 Fazendo login...")
# Obter CSRF token
response = session.get(login_url)
csrf_token = session.cookies.get('csrftoken')

# Fazer login
login_data = {
    'username': 'desenv',
    'password': 'desenv',
    'csrfmiddlewaretoken': csrf_token
}
response = session.post(login_url, data=login_data, headers={'Referer': login_url})

print(f"Status do login: {response.status_code}")
print(f"Cookies após login: {dict(session.cookies)}")
print(f"URL final: {response.url}")

if response.status_code == 200 and 'sessionid' in session.cookies:
    print("✅ Login bem-sucedido\n")
else:
    print(f"❌ Login falhou: {response.status_code}\n")
    exit(1)

# 2. Requisição AJAX
print("📡 Fazendo requisição AJAX para /atividades/?q=aula")
print("=" * 60)

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://localhost:8000/atividades/'
}

response = session.get(f"{ajax_url}?q=aula&curso=&turma=", headers=headers)

print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"Tamanho: {len(response.content)} bytes\n")

if 'application/json' in response.headers.get('content-type', ''):
    print("✅ Resposta é JSON:")
    data = response.json()
    print(f"   Chaves: {list(data.keys())}")
    if 'tabela_html' in data:
        print(f"   tabela_html: {len(data['tabela_html'])} chars")
    if 'cursos_html' in data:
        print(f"   cursos_html: {len(data['cursos_html'])} chars")
else:
    print("❌ Resposta é HTML:")
    content = response.text[:500]
    print(f"   Primeiros 500 chars:\n{content}\n")

print("=" * 60)
