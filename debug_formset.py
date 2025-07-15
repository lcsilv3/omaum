#!/usr/bin/env python
"""
Salva o HTML da página para análise
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

def save_html_for_analysis():
    """Salva o HTML para análise"""
    client = Client()
    
    # Login
    username = "lcsilv3"
    password = "iG356900"
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
    
    client.login(username=username, password=password)
    
    # Requisição
    url = reverse("alunos:criar_aluno")
    response = client.get(url)
    
    if response.status_code == 200:
        html = response.content.decode()
        
        # Salvar HTML
        with open("html_dump_formset_get.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        print("✅ HTML salvo em 'html_dump_formset_get.html'")
        
        # Contar management forms
        count = html.count('name="historico-TOTAL_FORMS"')
        print(f"📊 Total de TOTAL_FORMS encontrados: {count}")
        
        # Encontrar posições
        pos = 0
        positions = []
        while True:
            pos = html.find('name="historico-TOTAL_FORMS"', pos)
            if pos == -1:
                break
            positions.append(pos)
            pos += 1
        
        print(f"📍 Posições encontradas: {positions}")
        
        for i, pos in enumerate(positions):
            start = max(0, pos - 100)
            end = min(len(html), pos + 100)
            context = html[start:end]
            print(f"\n--- CONTEXTO {i+1} ---")
            print(context)
    else:
        print(f"❌ Erro: {response.status_code}")

if __name__ == "__main__":
    save_html_for_analysis()
