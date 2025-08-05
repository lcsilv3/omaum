#!/usr/bin/env python
"""
Script para testar o endpoint AJAX de presença diretamente.
"""

import os
import sys
import django
import json
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from presencas.views_ext.registro_presenca import registrar_presenca_dias_atividades_ajax

def testar_endpoint_ajax():
    """
    Testa o endpoint AJAX exatamente com os dados que o frontend está enviando.
    """
    print("🧪 TESTE DO ENDPOINT AJAX")
    print("=" * 50)
    
    # Dados exatos do frontend (do console do navegador)
    presencas_json = {
        "1": {"1": {"81991045700": {"presente": True, "justificativa": "", "convocado": True}}},
        "2": {"2": {"81991045700": {"presente": False, "justificativa": "", "convocado": True}}},
        "3": {
            "3": {"81991045700": {"presente": True, "justificativa": "", "convocado": False}},
            "4": {"81991045700": {"presente": False, "justificativa": "", "convocado": False}}
        }
    }
    
    print(f"📊 Dados de teste:")
    print(json.dumps(presencas_json, indent=2))
    
    # Criar cliente de teste
    client = Client()
    
    # Criar/obter usuário para teste
    user, created = User.objects.get_or_create(username='teste_ajax', defaults={'email': 'teste@teste.com'})
    if created:
        user.set_password('teste123')
        user.save()
        print(f"✅ Usuário de teste criado: {user.username}")
    
    # Login
    client.force_login(user)
    
    # Configurar sessão
    session = client.session
    session['presenca_turma_id'] = 1
    session['presenca_ano'] = 2025
    session['presenca_mes'] = 8
    session.save()
    
    # Dados do POST
    post_data = {
        'presencas_json': json.dumps(presencas_json),
        'convocados_json': '{"81991045700": false}',
        'dias_json': '{"1": [1], "2": [2], "3": [3, 4]}'
    }
    
    print(f"📤 Enviando POST para o endpoint...")
    
    # Fazer requisição
    response = client.post('/presencas/registrar-presenca/dias-atividades/ajax/', post_data)
    
    print(f"📊 Resposta HTTP: {response.status_code}")
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            print(f"📋 Resposta JSON:")
            print(json.dumps(response_data, indent=2))
            
            if response_data.get('success'):
                print("✅ SUCESSO! Presenças foram processadas.")
            else:
                print("❌ FALHA! Mensagem:", response_data.get('message'))
                
        except json.JSONDecodeError:
            print("❌ Resposta não é JSON válido")
            print(f"📄 Conteúdo da resposta: {response.content.decode()}")
    else:
        print(f"❌ Erro HTTP {response.status_code}")
        print(f"📄 Conteúdo: {response.content.decode()}")
    
    # Verificar se presenças foram criadas
    print(f"\n🔍 Verificando banco de dados...")
    from presencas.models import Presenca
    from django.utils import timezone
    from datetime import timedelta
    
    # Buscar presenças criadas nos últimos minutos
    agora = timezone.now()
    recentes = Presenca.objects.filter(
        data_registro__gte=agora - timedelta(minutes=5),
        registrado_por=user.username
    ).order_by('-data_registro')
    
    print(f"📊 Presenças criadas nos últimos 5 min: {recentes.count()}")
    
    if recentes.exists():
        for p in recentes:
            print(f"   ✅ {p.aluno.nome} - {p.atividade.nome if p.atividade else 'N/A'} - {p.data} - {'Presente' if p.presente else 'Ausente'}")
    else:
        print("❌ Nenhuma presença encontrada no banco")

if __name__ == '__main__':
    testar_endpoint_ajax()
