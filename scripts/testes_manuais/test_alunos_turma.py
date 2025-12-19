#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from alunos.models import Aluno
from matriculas.models import Matricula
from turmas.models import Turma

print("=== TURMAS EXISTENTES ===")
turmas = list(Turma.objects.all()[:5])
for t in turmas:
    print(f"ID: {t.id}, Nome: {t.nome}")

print("\n=== MATRÍCULAS POR TURMA ===")
for t in turmas[:3]:
    count = Matricula.objects.filter(turma=t, ativa=True).count()
    alunos = Aluno.objects.filter(matricula__turma_id=t.id, situacao="a").count()
    print(f"Turma {t.id} ({t.nome}): {count} matrículas ativas, {alunos} alunos ativos")

print("\n=== ALUNOS ATIVOS TOTAL ===")
alunos_ativos = Aluno.objects.filter(situacao="a").count()
print(f"Total de alunos ativos: {alunos_ativos}")

print("\n=== TESTE ENDPOINT ESPECÍFICO ===")
# Simula a query do endpoint
turma_id = 1  # Testando com turma ID 1
alunos_turma1 = (
    Aluno.objects.filter(matricula__turma_id=turma_id, situacao="a")
    .distinct()
    .order_by("nome")
)

print(f"Alunos na turma ID {turma_id}:")
for aluno in alunos_turma1:
    print(f"- {aluno.nome} (CPF: {aluno.cpf})")

print(f"\nTotal: {alunos_turma1.count()} alunos")
