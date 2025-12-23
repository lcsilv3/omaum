import re
from django.test import Client

print("=" * 80)
print("DEBUG: Formulário de Matrícula e Select2")
print("=" * 80)

# Importar modelos
from alunos.models import Aluno
from turmas.models import Turma

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
    else:
        print("✓ Página acessada com sucesso")
        
except Exception as e:
    print(f"❌ Erro ao acessar página: {e}")

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
    print("❌ CRÍTICO: Campo SELECT com id='id_aluno' NÃO encontrado!")
    
    # Procurar por QUALQUER select
    selects = re.findall(r'<select[^>]*id="([^"]*)"', html)
    if selects:
        print(f"   Selects encontrados: {selects}")

# Verificar script do Select2
print("\n4️⃣ VERIFICAÇÃO DO SELECT2:")
print("-" * 80)

if 'select2' in html.lower():
    print("✓ Select2 mencionado no HTML")
else:
    print("❌ Select2 não encontrado")

# Resumo
print("\n" + "=" * 80)
print("RESUMO")
print("=" * 80)

if aluno_select_match:
    options_count = len(re.findall(r'<option[^>]*>', aluno_select_match.group(0)))
    if options_count > 10:
        print(f"✅ Formulário OK: {options_count} opções encontradas")
    else:
        print(f"⚠️  Formulário renderizado mas com poucas opções: {options_count}")
else:
    print("❌ CRÍTICO: SELECT não renderizado")

print("=" * 80)
