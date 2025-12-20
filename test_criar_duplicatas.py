#!/usr/bin/env python
"""
Script para criar atividades de teste com duplicatas.
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from atividades.models import Atividade
from atividades.services.validacao_duplicatas import ValidacaoDuplicatasAtividades
from turmas.models import Turma
from cursos.models import Curso

# Obter turma 2025
turma_2025 = Turma.objects.get(id=32)
curso = turma_2025.curso

print("=" * 70)
print("CRIANDO ATIVIDADES DE TESTE")
print("=" * 70)

# Criar primeira aula de Matemática
aula1 = Atividade.objects.create(
    nome="Aula de Matemática - Básico",
    tipo_atividade="AULA",
    data_inicio=datetime(2026, 1, 15).date(),
    data_fim=datetime(2026, 1, 15).date(),
    hora_inicio="09:00",
    hora_fim="11:00",
    local="Sala 101",
    responsavel="Prof. Silva",
    status="CONFIRMADA",
    curso=curso,
)
aula1.turmas.add(turma_2025)
print(f"✓ Criada: {aula1.nome}")

# Criar segunda aula de Matemática (duplicada - MESMO PERÍODO)
aula2 = Atividade.objects.create(
    nome="Aula de Matemática - Básico",  # MESMO NOME
    tipo_atividade="AULA",  # MESMO TIPO
    data_inicio=datetime(2026, 1, 15).date(),  # MESMO DIA
    data_fim=datetime(2026, 1, 15).date(),
    hora_inicio="14:00",
    hora_fim="16:00",
    local="Sala 102",
    responsavel="Prof. Santos",
    status="CONFIRMADA",
    curso=curso,
)
aula2.turmas.add(turma_2025)
print(f"✓ Criada: {aula2.nome} (duplicada no mesmo período)")

# Criar terceira aula de Matemática (duplicada - PERÍODO DIFERENTE)
aula3 = Atividade.objects.create(
    nome="Aula de Matemática - Básico",  # MESMO NOME
    tipo_atividade="AULA",  # MESMO TIPO
    data_inicio=datetime(2026, 2, 15).date(),  # PERÍODO DIFERENTE
    data_fim=datetime(2026, 2, 15).date(),
    hora_inicio="09:00",
    hora_fim="11:00",
    local="Sala 103",
    responsavel="Prof. Costa",
    status="CONFIRMADA",
    curso=curso,
)
aula3.turmas.add(turma_2025)
print(f"✓ Criada: {aula3.nome} (duplicada em período diferente)")

# Agora testar a validação
print("\n" + "=" * 70)
print("TESTANDO VALIDAÇÃO DE DUPLICATAS")
print("=" * 70)

# Teste: Tentar criar outra aula com mesmo nome no mesmo período
print("\nTeste: Validação ao tentar criar nova aula (mesmo nome, mesmo período que aula1)")
print("-" * 70)

aula_teste = Atividade(
    nome="Aula de Matemática - Básico",
    tipo_atividade="AULA",
    data_inicio=datetime(2026, 1, 15).date(),  # MESMO dia que aula1
    hora_inicio="10:00",
    curso=curso,
)

resultado = ValidacaoDuplicatasAtividades.verificar_duplicatas_na_turma(aula_teste, turma_2025.id)

print(f"✓ Tem duplicatas: {resultado['tem_duplicatas']}")
print(f"✓ Tem warning: {resultado['tem_warning']}")
print(f"✓ Tem bloqueio: {resultado['tem_bloqueio']}")
if resultado['mensagem']:
    print(f"✓ Mensagem: {resultado['mensagem']}")
print(f"✓ Duplicatas encontradas: {len(resultado['duplicatas'])}")
for dup in resultado['duplicatas']:
    print(f"  - {dup.nome} ({dup.get_tipo_atividade_display()})")
    print(f"    Período: {dup.data_inicio} a {dup.data_fim}")

# Teste 2: Validação com período diferente
print("\nTeste: Validação ao tentar criar nova aula (mesmo nome, período diferente de aula1)")
print("-" * 70)

aula_teste2 = Atividade(
    nome="Aula de Matemática - Básico",
    tipo_atividade="AULA",
    data_inicio=datetime(2026, 3, 15).date(),  # PERÍODO DIFERENTE
    hora_inicio="10:00",
    curso=curso,
)

resultado2 = ValidacaoDuplicatasAtividades.verificar_duplicatas_na_turma(aula_teste2, turma_2025.id)

print(f"✓ Tem duplicatas: {resultado2['tem_duplicatas']}")
print(f"✓ Tem warning: {resultado2['tem_warning']}")
print(f"✓ Tem bloqueio: {resultado2['tem_bloqueio']}")
if resultado2['mensagem']:
    print(f"✓ Mensagem: {resultado2['mensagem']}")
print(f"✓ Duplicatas encontradas: {len(resultado2['duplicatas'])}")
for dup in resultado2['duplicatas']:
    print(f"  - {dup.nome} ({dup.get_tipo_atividade_display()})")
    print(f"    Período: {dup.data_inicio} a {dup.data_fim}")

print("\n" + "=" * 70)
print("FIM DOS TESTES")
print("=" * 70)
