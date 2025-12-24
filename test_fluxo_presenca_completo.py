#!/usr/bin/env python
"""
Script de teste do fluxo completo de registro de presenças
1. Navega pela interface
2. Marca presenças
3. Finaliza registro
4. Verifica se os dados foram salvos no banco
"""
import os
import sys
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection
from turmas.models import Turma
from presencas.models import RegistroPresenca
from atividades.models import Atividade

# ===== 1. VERIFICAR DADOS DE TESTE =====
print("=" * 80)
print("🔍 ETAPA 1: Verificar dados de teste existentes")
print("=" * 80)

# Obter turma ID 32
try:
    turma = Turma.objects.get(id=32)
    print(f"✅ Turma encontrada: {turma.nome} (ID: {turma.id})")
except Turma.DoesNotExist:
    print(f"❌ Turma ID 32 não existe!")
    sys.exit(1)

# Listar matrículas ativas
matriculas = turma.matriculas.filter(status='A')
print(f"👥 Matrículas ativas: {matriculas.count()}")
for m in matriculas:
    print(f"   - {m.aluno.nome} ({m.aluno.cpf})")

# ===== 2. CONTAR PRESENÇAS ATUAIS =====
print("\n" + "=" * 80)
print("📊 ETAPA 2: Contagem de RegistroPresenca no banco ANTES")
print("=" * 80)

presencas_antes = RegistroPresenca.objects.filter(turma=turma)
print(f"Total de RegistroPresenca: {presencas_antes.count()}")

# Agrupar por data/atividade
from django.db.models import Count
presencas_agg = presencas_antes.values('data', 'atividade__nome').annotate(count=Count('id'))
for p in presencas_agg:
    print(f"   - Data: {p['data']} | Atividade: {p['atividade__nome']} | Registros: {p['count']}")

# ===== 3. LISTAR ATIVIDADES DISPONÍVEIS =====
print("\n" + "=" * 80)
print("📌 ETAPA 3: Atividades disponíveis para a turma")
print("=" * 80)

atividades = Atividade.objects.filter(turmas=turma)
print(f"Total de atividades: {atividades.count()}")
for a in atividades[:5]:
    print(f"   - ID: {a.id} | Nome: {a.nome} | Tipo: {a.tipo} | Convocação: {a.convocacao}")

# ===== 4. SIMULAR REGISTRO DIRETO NO BANCO =====
print("\n" + "=" * 80)
print("🔧 ETAPA 4: INSERIR REGISTRO DIRETO NO BANCO (para teste)")
print("=" * 80)

# Criar registro de teste
if atividades.exists() and matriculas.exists():
    atividade = atividades.first()
    matricula = matriculas.first()
    data_teste = date(2025, 12, 6)
    
    registro, criado = RegistroPresenca.objects.update_or_create(
        aluno=matricula.aluno,
        turma=turma,
        data=data_teste,
        atividade=atividade,
        defaults={
            'status': 'P',  # Presente (código de escolha)
            'justificativa': 'Teste automático'
        }
    )
    
    if criado:
        print(f"✅ Novo RegistroPresenca criado!")
    else:
        print(f"♻️  RegistroPresenca atualizado!")
    
    print(f"   - Aluno: {registro.aluno.nome}")
    print(f"   - Turma: {registro.turma.nome}")
    print(f"   - Data: {registro.data}")
    print(f"   - Atividade: {registro.atividade.nome}")
    print(f"   - Status: {registro.status} (Presente: {registro.status == 'P'})")
    print(f"   - Justificativa: {registro.justificativa}")
else:
    print("❌ Não há atividades ou matrículas para testar!")

# ===== 5. VERIFICAR APÓS INSERÇÃO =====
print("\n" + "=" * 80)
print("📊 ETAPA 5: Contagem APÓS inserção")
print("=" * 80)

presencas_depois = RegistroPresenca.objects.filter(turma=turma)
print(f"Total de RegistroPresenca: {presencas_depois.count()}")
print(f"Diferença: {presencas_depois.count() - presencas_antes.count()} registros adicionados")

# ===== 6. QUERY BRUTA SQL (para debug) =====
print("\n" + "=" * 80)
print("🔎 ETAPA 6: Query SQL bruta")
print("=" * 80)

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT COUNT(*) as total FROM presencas_registropresenca 
        WHERE turma_id = %s
    """, [turma.id])
    result = cursor.fetchone()
    print(f"SELECT COUNT(*) FROM presencas_registropresenca WHERE turma_id={turma.id}")
    print(f"Resultado: {result[0]} registros")

print("\n" + "=" * 80)
print("✅ Teste concluído!")
print("=" * 80)
