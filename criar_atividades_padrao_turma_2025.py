#!/usr/bin/env python
"""
Script para criar as atividades padrão na turma 2025:
- Aula (tipo AULA)
- Plenilúnio (tipo PLENILUNIO)
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from turmas.models import Turma
from atividades.models import Atividade

# Obter turma 2025
turma_2025 = Turma.objects.get(id=32)
curso = turma_2025.curso

print("=" * 70)
print(f"CRIANDO ATIVIDADES PADRÃO PARA TURMA 2025")
print("=" * 70)
print(f"\nTurma: {turma_2025.nome}")
print(f"Curso: {curso.nome}\n")

# Data padrão: hoje
data_padrao = datetime.now().date()

# Criar Atividade "Aula"
aula = Atividade.objects.create(
    nome="Aula",
    tipo_atividade="AULA",
    data_inicio=data_padrao,
    hora_inicio="09:00",
    status="PENDENTE",
    curso=curso,
)
aula.turmas.add(turma_2025)
print(f"✓ Criada: {aula.nome} (tipo: {aula.get_tipo_atividade_display()})")

# Criar Atividade "Plenilúnio"
plenilunio = Atividade.objects.create(
    nome="Plenilúnio",
    tipo_atividade="PLENILUNIO",
    data_inicio=data_padrao,
    hora_inicio="20:00",
    status="PENDENTE",
    curso=curso,
)
plenilunio.turmas.add(turma_2025)
print(f"✓ Criada: {plenilunio.nome} (tipo: {plenilunio.get_tipo_atividade_display()})")

# Verificar resultado final
print("\n" + "=" * 70)
print("RESULTADO FINAL")
print("=" * 70)

atividades_atuais = turma_2025.atividades.all()
print(f"\nTotal de atividades na turma 2025: {atividades_atuais.count()}")
print("\nAtividades vinculadas:")
for ativ in atividades_atuais.order_by('tipo_atividade', 'nome'):
    print(f"  ✓ {ativ.nome} ({ativ.get_tipo_atividade_display()})")

print("\n" + "=" * 70)
