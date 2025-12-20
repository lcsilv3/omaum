"""
Script para verificar alunos e turmas disponíveis para matrícula.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from alunos.models import Aluno
from turmas.models import Turma

print("=" * 80)
print("VERIFICAÇÃO DE DADOS PARA MATRÍCULA")
print("=" * 80)

# Verificar alunos ativos
alunos_ativos = Aluno.objects.filter(situacao='a')
print(f"\n✓ Total de alunos ativos (situacao='a'): {alunos_ativos.count()}")

if alunos_ativos.exists():
    print("\nPrimeiros 5 alunos ativos:")
    for aluno in alunos_ativos[:5]:
        print(f"  - ID {aluno.id}: {aluno.nome} (situação={aluno.situacao})")
else:
    print("\n⚠ ATENÇÃO: Nenhum aluno ativo encontrado!")

# Verificar turmas ativas
turmas_ativas = Turma.objects.filter(ativo=True)
print(f"\n✓ Total de turmas ativas: {turmas_ativas.count()}")

if turmas_ativas.exists():
    print("\nPrimeiras 5 turmas ativas:")
    for turma in turmas_ativas[:5]:
        print(f"  - ID {turma.id}: {turma.nome} (ativo={turma.ativo})")
else:
    print("\n⚠ ATENÇÃO: Nenhuma turma ativa encontrada!")

# Verificar se há alunos com outros valores de situação
print("\n" + "=" * 80)
print("DISTRIBUIÇÃO DE ALUNOS POR SITUAÇÃO:")
print("=" * 80)
from django.db.models import Count
situacoes = Aluno.objects.values('situacao').annotate(total=Count('id')).order_by('-total')
for s in situacoes:
    situacao_label = dict(Aluno.SITUACAO_CHOICES).get(s['situacao'], 'Desconhecida')
    print(f"  Situação '{s['situacao']}' ({situacao_label}): {s['total']} alunos")

print("\n" + "=" * 80)
