#!/usr/bin/env python
"""
Script para debugar o Select2 na matrícula
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings.development')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

client = Client()
User = get_user_model()
user = User.objects.filter(is_superuser=True).first()

if user:
    client.force_login(user)
    response = client.get('/matriculas/criar/')
    html = response.content.decode('utf-8')
    
    # Procurar por "id_aluno"
    if 'id_aluno' in html:
        print('✓ Campo id_aluno encontrado no HTML')
        
        # Procurar por <select
        if '<select' in html:
            # Extrair seção que contém id_aluno
            idx = html.find('id="id_aluno"')
            # Voltar para encontrar o <select mais próximo
            select_idx = html.rfind('<select', 0, idx)
            if select_idx > 0:
                # Procurar o </select> após id_aluno
                end_select = html.find('</select>', idx)
                select_html = html[select_idx:end_select+9]
                
                option_count = select_html.count('<option')
                print(f'✓ Total de <option> tags: {option_count}')
                
                if option_count > 0:
                    print(f'\nPrimeiros 2000 chars do select:')
                    print(select_html[:2000])
                else:
                    print('✗ Nenhuma <option> encontrada!')
                    # Mostrar o HTML do select
                    print(f'\nHTML do select:')
                    print(select_html[:1000])
            else:
                print('✗ <select> não encontrado')
        else:
            print('✗ Nenhum <select> no HTML')
    else:
        print('✗ Campo id_aluno não encontrado no HTML')
else:
    print('✗ Superuser não encontrado')
