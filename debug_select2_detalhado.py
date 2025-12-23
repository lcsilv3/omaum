#!/usr/bin/env python
"""
Debug detalhado do formulário de matrícula e Select2.
"""
import re
from django.test import Client

print("=" * 80)
print("DEBUG: Formulário de Matrícula e Select2")
print("=" * 80)

# Verificar banco de dados
print("\n1️⃣ VERIFICAÇÃO DO BANCO DE DADOS:")
print("-" * 80)

# Alunos ativos
alunos_ativos = Aluno.objects.filter(situacao='a').count()
print(f"✓ Alunos com situacao='a': {alunos_ativos}")

# Turmas ativas
turmas_ativas = Turma.objects.filter(ativo=True).count()
print(f"✓ Turmas com ativo=True: {turmas_ativas}")

if alunos_ativos == 0:
    print("⚠️  ALERTA: Nenhum aluno ativo no banco!")
if turmas_ativas == 0:
    print("⚠️  ALERTA: Nenhuma turma ativa no banco!")

# Importar modelos
from alunos.models import Aluno
from turmas.models import Turma

# Criar cliente
print("\n2️⃣ ACESSO À PÁGINA:")
print("-" * 80)

client = Client()

# Tentar acessar a página de criação de matrícula
try:
    response = client.get('/matriculas/criar/')
    print(f"✓ Status HTTP: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Erro: Página retornou {response.status_code}")
        if response.status_code == 302:
            print(f"   Redirecionando para: {response.get('Location', 'não informado')}")
        print(f"   Possível razão: Página de login ou erro no servidor")
    else:
        print("✓ Página acessada com sucesso")
        
except Exception as e:
    print(f"❌ Erro ao acessar página: {e}")
    import traceback
    traceback.print_exc()

# Analisar HTML
print("\n3️⃣ ANÁLISE DO HTML:")
print("-" * 80)

html = response.content.decode('utf-8')

# Procurar pelo campo select
aluno_select_match = re.search(r'<select[^>]*id="id_aluno"[^>]*>.*?</select>', html, re.DOTALL)

if aluno_select_match:
    print("✓ Campo SELECT encontrado no HTML")
    select_html = aluno_select_match.group(0)
    
    # Contar opções
    options = re.findall(r'<option[^>]*>', select_html)
    print(f"✓ Total de <option> tags: {len(options)}")
    
    if len(options) > 0:
        print("\n📋 Primeiras 5 opções:")
        for i, opt in enumerate(options[:5]):
            print(f"   {i+1}. {opt}")
        
        if len(options) > 5:
            print(f"   ... e mais {len(options) - 5}")
    else:
        print("❌ PROBLEMA: Nenhuma opção encontrada no SELECT!")
    
    # Verificar atributos do select
    select_attrs = re.search(r'<select([^>]*)>', select_html)
    if select_attrs:
        print(f"\n🔍 Atributos do SELECT: {select_attrs.group(1)}")
        
        # Verificar classe select2-enable
        if 'select2-enable' in select_attrs.group(1):
            print("✓ Classe 'select2-enable' presente")
        else:
            print("❌ AVISO: Classe 'select2-enable' NÃO encontrada!")
            
else:
    print("❌ CRÍTICO: Campo SELECT com id='id_aluno' NÃO encontrado!")
    print("\n   Procurando por qualquer campo aluno...")
    
    # Procurar por qualquer select que possa ser aluno
    aluno_matches = re.findall(r'<[^>]*aluno[^>]*>', html)
    if aluno_matches:
        print(f"   Encontrados {len(aluno_matches)} elementos com 'aluno':")
        for i, match in enumerate(aluno_matches[:5]):
            print(f"   {i+1}. {match[:80]}...")
    else:
        print("   Nenhum elemento com 'aluno' encontrado no HTML!")
        
        # Procurar por QUALQUER select
        selects = re.findall(r'<select[^>]*id="([^"]*)"', html)
        if selects:
            print(f"\n   Selects encontrados no formulário: {selects}")
        else:
            print("\n   ❌ Nenhum SELECT encontrado no formulário!")

# Verificar script do Select2
print("\n4️⃣ VERIFICAÇÃO DO SELECT2:")
print("-" * 80)

if 'select2' in html.lower():
    print("✓ Select2 mencionado no HTML")
    
    # Procurar script que inicializa Select2
    select2_init = re.search(r'\.select2\s*\(\s*\{', html, re.IGNORECASE)
    if select2_init:
        print("✓ Código de inicialização do Select2 encontrado")
    else:
        print("⚠️  Inicialização do Select2 não encontrada")
else:
    print("❌ Select2 não encontrado no HTML")

# Verificar Bootstrap
print("\n5️⃣ VERIFICAÇÃO DO BOOTSTRAP E DEPENDÊNCIAS:")
print("-" * 80)

if 'bootstrap' in html.lower():
    print("✓ Bootstrap mencionado no HTML")
else:
    print("⚠️  Bootstrap não mencionado no HTML")

if 'jquery' in html.lower() or 'jquery' in response.content.decode('utf-8', errors='ignore').lower():
    print("✓ jQuery mencionado no HTML")
else:
    print("⚠️  jQuery não mencionado explicitamente")

# Resumo
print("\n" + "=" * 80)
print("RESUMO")
print("=" * 80)

if aluno_select_match and len(options) > 10:
    print("✅ SUCESSO: Formulário renderizando corretamente com todas as opções")
    print(f"   {alunos_ativos} alunos disponíveis, {len(options)} opções no SELECT")
elif aluno_select_match:
    print("⚠️  PARCIAL: SELECT encontrado mas com poucas opções")
    print(f"   Esperado: {alunos_ativos}, Encontrado: {len(options)}")
else:
    print("❌ CRÍTICO: SELECT não renderizado corretamente no HTML")
    print("   Verificar:")
    print("   • Se form.aluno está sendo passado ao template")
    print("   • Se {% render_field %} está funcionando")
    print("   • Possível erro na view ou formulário")

print("=" * 80)
