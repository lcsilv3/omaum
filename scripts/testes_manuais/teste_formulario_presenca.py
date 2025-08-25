#!/usr/bin/env python3
"""
🧪 TESTE RÁPIDO DO FORMULÁRIO DE PRESENÇA
===========================================

Este script ajuda a testar se o formulário está funcionando corretamente
e se os dados estão sendo enviados para o Django.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from presencas.models import *

def testar_endpoint_presenca():
    """Testa se o endpoint de presença está funcionando"""
    print("🧪 [TESTE] Testando endpoint de presença...")
    
    client = Client()
    
    # Tentar fazer uma requisição GET para a página
    try:
        response = client.get('/presencas/registrar-dias-atividades/')
        print(f"✅ [TESTE] GET Status: {response.status_code}")
        
        if response.status_code == 302:
            print("🔄 [TESTE] Redirecionamento (provavelmente para login)")
        elif response.status_code == 200:
            print("✅ [TESTE] Página carregou com sucesso")
            
    except Exception as e:
        print(f"❌ [TESTE] Erro no GET: {e}")
    
    # Simular envio de dados POST
    dados_teste = {
        'presencas_json': '{"1": {"15": {"123": "presente"}}}',
        'convocados_json': '{"123": {"1": {"15": "convocado"}}}',
        'dias_json': '{"1": [15]}'
    }
    
    try:
        response = client.post('/presencas/registrar-dias-atividades/', dados_teste)
        print(f"📤 [TESTE] POST Status: {response.status_code}")
        
        if response.status_code == 302:
            print("🔄 [TESTE] POST aceito (redirecionamento)")
        elif response.status_code == 200:
            print("✅ [TESTE] POST processado")
        else:
            print(f"⚠️ [TESTE] POST retornou: {response.status_code}")
            
    except Exception as e:
        print(f"❌ [TESTE] Erro no POST: {e}")

def verificar_estrutura_dados():
    """Verifica se as estruturas de dados necessárias existem"""
    print("\n🔍 [VERIFICAÇÃO] Verificando estrutura de dados...")
    
    # Verificar modelos
    try:
        from presencas.models import Presenca, TipoPresenca
        print("✅ [VERIFICAÇÃO] Modelo Presenca encontrado")
        print("✅ [VERIFICAÇÃO] Modelo TipoPresenca encontrado")
        
        # Contar registros
        total_presencas = Presenca.objects.count()
        total_tipos = TipoPresenca.objects.count()
        
        print(f"📊 [VERIFICAÇÃO] Total de presenças: {total_presencas}")
        print(f"📊 [VERIFICAÇÃO] Total de tipos: {total_tipos}")
        
    except Exception as e:
        print(f"❌ [VERIFICAÇÃO] Erro ao verificar modelos: {e}")

if __name__ == "__main__":
    print("🧪 INICIANDO TESTES DO FORMULÁRIO DE PRESENÇA")
    print("=" * 50)
    
    verificar_estrutura_dados()
    testar_endpoint_presenca()
    
    print("\n" + "=" * 50)
    print("🏁 TESTES CONCLUÍDOS")
    print("\n💡 PRÓXIMOS PASSOS:")
    print("1. Abra o navegador e vá para a página de presença")
    print("2. Abra o console do navegador (F12)")
    print("3. Selecione alguns dias nos calendários")
    print("4. Clique nos dias azuis para marcar presenças")
    print("5. Execute no console: debugarFormulario()")
    print("6. Execute no console: verificarDadosFormulario()")
    print("7. Clique em 'Finalizar Registro' e observe os logs")
