#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste para verificar se os logs da presença estão funcionando.
"""

import os
import django
import logging

# Configurar Django
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
    django.setup()
    
    # Configurar logging básico para teste
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Importar após configurar Django
    from django.test import Client
    from django.contrib.auth.models import User
    
    print("🔍 Testando logs da função registrar_presenca_dias_atividades_ajax...")
    
    # Criar cliente de teste
    client = Client()
    
    # Criar/obter usuário para teste
    user, created = User.objects.get_or_create(username='teste_logs', defaults={'email': 'teste@teste.com'})
    if created:
        user.set_password('123456')
        user.save()
        print(f"✅ Usuário de teste criado: {user.username}")
    
    # Login
    client.force_login(user)
    
    # Configurar sessão mínima
    session = client.session
    session['presenca_turma_id'] = 1
    session['presenca_ano'] = 2025
    session['presenca_mes'] = 8
    session.save()
    
    # Dados de teste simples
    post_data = {
        'presencas_json': '{"1": {"1": {"12345678901": {"presente": true}}}}',
    }
    
    print(f"📤 Enviando POST para o endpoint...")
    print(f"📊 Dados: {post_data}")
    
    # Fazer requisição
    response = client.post('/presencas/registrar-presenca/dias-atividades/ajax/', post_data)
    
    print(f"📊 Resposta HTTP: {response.status_code}")
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            print(f"📋 Resposta JSON:")
            import json
            print(json.dumps(response_data, indent=2))
            
        except:
            print("❌ Resposta não é JSON válido")
            print(f"📄 Conteúdo: {response.content.decode()}")
    else:
        print(f"❌ Erro HTTP {response.status_code}")
        print(f"📄 Conteúdo: {response.content.decode()}")
    
    print("\n✅ Teste concluído!")
    print("🔍 Se você não viu logs com '🔍 ANÁLISE REVERSA', então há um problema na configuração de logging.")
