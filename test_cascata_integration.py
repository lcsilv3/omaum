#!/usr/bin/env python
"""
Teste de integração para validar cascateamento Estado → Cidade → Bairro
usando requests (sem Selenium).
"""
import os
import sys
import django
import json

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.development")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from alunos.models import Estado, Cidade

User = get_user_model()

def test_autocomplete_workflow():
    """Testa o workflow completo de autocomplete."""
    
    print("\n" + "="*60)
    print("🧪 TESTE DE INTEGRAÇÃO: CASCATEAMENTO ESTADO → CIDADE")
    print("="*60)
    
    # 1. Setup
    print("\n📋 Configuração inicial...")
    user = User.objects.first()
    if not user:
        print("❌ Nenhum usuário encontrado no banco!")
        return False
    
    client = Client()
    client.force_login(user)
    print(f"✅ Autenticado como: {user.username}")
    
    # 2. Verifica dados de teste
    print("\n📊 Verificando dados de teste...")
    estado_al = Estado.objects.filter(codigo="AL").first()
    if not estado_al:
        print("❌ Estado AL não encontrado!")
        return False
    
    print(f"✅ Estado encontrado: {estado_al.nome} (ID: {estado_al.id})")
    
    cidades_al = Cidade.objects.filter(estado=estado_al)
    print(f"✅ Cidades em AL: {cidades_al.count()}")
    
    if cidades_al.count() == 0:
        print("❌ Nenhuma cidade encontrada para AL!")
        return False
    
    # 3. Pula teste da página (problema com testserver no ALLOWED_HOSTS)
    print("\n⏩ Pulando teste da página /alunos/criar/ (testando apenas autocompletes)")
    
    # 4. Testa autocomplete de Estados (sem filtro)
    print("\n🔍 Testando autocomplete de Estados...")
    print("   GET /alunos/autocomplete/estado-autocomplete/?q=AL")
    
    response = client.get(
        "/alunos/autocomplete/estado-autocomplete/",
        {"q": "AL"}
    )
    
    if response.status_code != 200:
        print(f"❌ Erro no autocomplete de estados: {response.status_code}")
        print(f"   Response: {response.content.decode()[:500]}")
        return False
    
    try:
        data = response.json()
        print(f"✅ Autocomplete retornou: {len(data.get('results', []))} resultados")
        
        if len(data.get('results', [])) == 0:
            print("❌ Nenhum estado encontrado com 'AL'!")
            return False
        
        # Pega o ID do estado AL
        estado_id = None
        for result in data['results']:
            if 'AL' in result['text'].upper():
                estado_id = result['id']
                print(f"✅ Estado AL encontrado: ID={estado_id}, Texto='{result['text']}'")
                break
        
        if not estado_id:
            print("❌ Estado AL não encontrado nos resultados!")
            return False
            
    except json.JSONDecodeError:
        print("❌ Resposta não é JSON válido!")
        print(f"   Response: {response.content.decode()[:500]}")
        return False
    
    # 5. Testa autocomplete de Cidades SEM filtro de estado
    print("\n🔍 Testando autocomplete de Cidades SEM filtro...")
    print("   GET /alunos/autocomplete/cidade-autocomplete/?q=mac")
    
    response = client.get(
        "/alunos/autocomplete/cidade-autocomplete/",
        {"q": "mac"}
    )
    
    if response.status_code != 200:
        print(f"❌ Erro: {response.status_code}")
        return False
    
    data = response.json()
    total_sem_filtro = len(data.get('results', []))
    print(f"✅ Sem filtro: {total_sem_filtro} cidades com 'mac'")
    
    # 6. Testa autocomplete de Cidades COM filtro de estado (CRÍTICO!)
    print("\n🔍 TESTE CRÍTICO: Autocomplete de Cidades COM filtro de estado")
    print(f"   GET /alunos/autocomplete/cidade-autocomplete/?q=mac&forward={{\"estado_ref\":\"{estado_id}\"}}")
    
    response = client.get(
        "/alunos/autocomplete/cidade-autocomplete/",
        {
            "q": "mac",
            "forward": json.dumps({"estado_ref": str(estado_id)})
        }
    )
    
    if response.status_code != 200:
        print(f"❌ Erro: {response.status_code}")
        print(f"   Response: {response.content.decode()[:500]}")
        return False
    
    try:
        data = response.json()
        total_com_filtro = len(data.get('results', []))
        print(f"✅ Com filtro estado_ref={estado_id}: {total_com_filtro} cidades")
        
        if total_com_filtro == 0:
            print("❌ FALHA: Nenhuma cidade retornada ao filtrar por estado!")
            print(f"   Esperado: Cidades de AL com 'mac' no nome")
            print(f"   Obtido: {data}")
            
            # Debug: Verifica o que há no banco
            cidades_banco = Cidade.objects.filter(
                estado_id=estado_id,
                nome__icontains="mac"
            )
            print(f"\n🔍 Debug: No banco há {cidades_banco.count()} cidades AL com 'mac':")
            for cidade in cidades_banco[:5]:
                print(f"   - {cidade.nome} (ID: {cidade.id})")
            
            return False
        
        # Mostra as cidades retornadas
        print(f"\n📋 Cidades retornadas:")
        for result in data['results'][:5]:
            print(f"   - ID={result['id']}, Texto='{result['text']}'")
        
        # Verifica se as cidades são realmente de AL
        cidade_ids = [r['id'] for r in data['results']]
        cidades_verificacao = Cidade.objects.filter(id__in=cidade_ids)
        
        erradas = []
        for cidade in cidades_verificacao:
            if cidade.estado_id != int(estado_id):
                erradas.append(f"{cidade.nome} (estado={cidade.estado.codigo})")
        
        if erradas:
            print(f"\n❌ FALHA: Algumas cidades não são de AL:")
            for erro in erradas:
                print(f"   - {erro}")
            return False
        
        print(f"✅ Todas as {total_com_filtro} cidades são de AL!")
        
    except json.JSONDecodeError:
        print("❌ Resposta não é JSON válido!")
        print(f"   Response: {response.content.decode()[:500]}")
        return False
    
    # 7. Resultado final
    print("\n" + "="*60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("="*60)
    print(f"\n📊 Resumo:")
    print(f"   - Estado AL encontrado: ID={estado_id}")
    print(f"   - Cidades sem filtro: {total_sem_filtro}")
    print(f"   - Cidades com filtro AL: {total_com_filtro}")
    print(f"   - Filtro funcionando: {'✅ SIM' if total_com_filtro > 0 else '❌ NÃO'}")
    
    return True

def main():
    """Função principal."""
    try:
        sucesso = test_autocomplete_workflow()
        return 0 if sucesso else 1
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
