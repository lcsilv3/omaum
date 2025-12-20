#!/usr/bin/env python
"""
Script de teste para validação de duplicatas de atividades.
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

# Configuração de teste
print("=" * 70)
print("TESTE DE VALIDAÇÃO DE DUPLICATAS DE ATIVIDADES")
print("=" * 70)

# Obter turma 2025 (Colégio Sacerdotal)
turma_2025 = Turma.objects.get(id=32)
curso = turma_2025.curso

print(f"\nTurma: {turma_2025.nome}")
print(f"Curso: {curso.nome}\n")

# Teste 1: Criar duas aulas com mesmo nome na mesma turma
print("TESTE 1: Duas AULAS com MESMO NOME e MESMO PERÍODO")
print("-" * 70)

aula1 = Atividade(
    nome="Aula de Matemática",
    tipo_atividade="AULA",
    data_inicio=datetime.now().date(),
    hora_inicio="10:00",
    curso=curso,
)

resultado = ValidacaoDuplicatasAtividades.verificar_duplicatas_na_turma(aula1, turma_2025.id)

print(f"Tem duplicatas: {resultado['tem_duplicatas']}")
print(f"Tem warning: {resultado['tem_warning']}")
print(f"Tem bloqueio: {resultado['tem_bloqueio']}")
print(f"Mensagem: {resultado['mensagem']}")
print(f"Quantidade de duplicatas encontradas: {len(resultado['duplicatas'])}")
for dup in resultado['duplicatas']:
    print(f"  - {dup.nome} ({dup.get_tipo_atividade_display()}) em {dup.data_inicio}")

# Teste 2: Mesma atividade em período diferente
print("\n\nTESTE 2: Mesma AULA mas em PERÍODO DIFERENTE")
print("-" * 70)

aula2 = Atividade(
    nome="Aula de Matemática",
    tipo_atividade="AULA",
    data_inicio=(datetime.now() + timedelta(days=7)).date(),  # 7 dias depois
    hora_inicio="10:00",
    curso=curso,
)

resultado2 = ValidacaoDuplicatasAtividades.verificar_duplicatas_na_turma(aula2, turma_2025.id)

print(f"Tem duplicatas: {resultado2['tem_duplicatas']}")
print(f"Tem warning: {resultado2['tem_warning']}")
print(f"Tem bloqueio: {resultado2['tem_bloqueio']}")
print(f"Mensagem: {resultado2['mensagem']}")

# Teste 3: Nenhuma duplicata (nome diferente)
print("\n\nTESTE 3: AULA com NOME DIFERENTE (sem duplicata)")
print("-" * 70)

aula3 = Atividade(
    nome="Aula de Português",
    tipo_atividade="AULA",
    data_inicio=datetime.now().date(),
    hora_inicio="10:00",
    curso=curso,
)

resultado3 = ValidacaoDuplicatasAtividades.verificar_duplicatas_na_turma(aula3, turma_2025.id)

print(f"Tem duplicatas: {resultado3['tem_duplicatas']}")
print(f"Tem warning: {resultado3['tem_warning']}")
print(f"Tem bloqueio: {resultado3['tem_bloqueio']}")
print(f"Mensagem: {resultado3['mensagem']}")
print(f"Quantidade de duplicatas encontradas: {len(resultado3['duplicatas'])}")

# Teste 4: Diferentes tipos com mesmo nome
print("\n\nTESTE 4: Mesmo NOME mas TIPOS DIFERENTES")
print("-" * 70)

atividade_palestra = Atividade(
    nome="Aula de Matemática",  # Mesmo nome
    tipo_atividade="PALESTRA",   # Tipo diferente
    data_inicio=datetime.now().date(),
    hora_inicio="10:00",
    curso=curso,
)

resultado4 = ValidacaoDuplicatasAtividades.verificar_duplicatas_na_turma(
    atividade_palestra, turma_2025.id
)

print(f"Tem duplicatas: {resultado4['tem_duplicatas']}")
print(f"Tem warning: {resultado4['tem_warning']}")
print(f"Tem bloqueio: {resultado4['tem_bloqueio']}")
print(f"Mensagem: {resultado4['mensagem']}")
print(f"Quantidade de duplicatas encontradas: {len(resultado4['duplicatas'])}")

print("\n" + "=" * 70)
print("FIM DOS TESTES")
print("=" * 70)
