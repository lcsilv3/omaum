#!/usr/bin/env python
"""
Script para debug das atividades
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from datetime import date
from calendar import monthrange
from django.db.models import Q
from atividades.models import Atividade
from turmas.models import Turma
from cursos.models import Curso

print("=== DEBUG ATIVIDADES ===")

# Parâmetros do teste (maio de 2025, turma ID 1)
turma_id = 1
ano = 2025
mes = 5

primeiro_dia = date(int(ano), int(mes), 1)
ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])

print(f"Período: {primeiro_dia} a {ultimo_dia}")

# Buscar turma e curso
turma = Turma.objects.get(id=turma_id)
curso = turma.curso
print(f"Turma: {turma}")
print(f"Curso: {curso}")

# Buscar todas as atividades relacionadas à turma
print("\n=== TODAS AS ATIVIDADES DA TURMA ===")
todas_atividades = Atividade.objects.filter(turmas__id=turma.id)
for ativ in todas_atividades:
    print(f"ID: {ativ.id}, Nome: {ativ.nome}, Data início: {ativ.data_inicio}, Data fim: {ativ.data_fim}, Curso: {ativ.curso}")

# Aplicar o filtro atual (problemático)
print("\n=== FILTRO ATUAL ===")
atividades_filtro_atual = Atividade.objects.filter(
    turmas__id=turma.id,
    curso=curso
).filter(
    Q(data_inicio__lte=ultimo_dia) &
    (Q(data_fim__isnull=True) | Q(data_fim__gte=primeiro_dia))
).distinct()

print(f"Query: {atividades_filtro_atual.query}")
for ativ in atividades_filtro_atual:
    print(f"ID: {ativ.id}, Nome: {ativ.nome}, Data início: {ativ.data_inicio}, Data fim: {ativ.data_fim}")

# Testar filtro sem curso
print("\n=== FILTRO SEM CURSO ===")
atividades_sem_curso = Atividade.objects.filter(
    turmas__id=turma.id
).filter(
    Q(data_inicio__lte=ultimo_dia) &
    (Q(data_fim__isnull=True) | Q(data_fim__gte=primeiro_dia))
).distinct()

for ativ in atividades_sem_curso:
    print(f"ID: {ativ.id}, Nome: {ativ.nome}, Data início: {ativ.data_inicio}, Data fim: {ativ.data_fim}")

# Verificar se curso está correto
print(f"\n=== VERIFICAÇÃO CURSO ===")
print(f"Curso da turma: {turma.curso} (ID: {turma.curso.id})")
for ativ in todas_atividades:
    print(f"Atividade {ativ.nome} - Curso: {ativ.curso} (ID: {ativ.curso.id if ativ.curso else 'None'})")
