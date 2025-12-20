#!/usr/bin/env python
"""
Script para remover atividades da turma 2025, mantendo apenas
as atividades padrão: "Aula" (tipo AULA) e "Plenilúnio" (tipo PLENILUNIO).
"""
import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from turmas.models import Turma
from atividades.models import Atividade

# Obter turma 2025
turma_2025 = Turma.objects.get(id=32)

print("=" * 70)
print(f"REMOVENDO ATIVIDADES DA TURMA 2025")
print("=" * 70)
print(f"\nTurma: {turma_2025.nome}")
print(f"Curso: {turma_2025.curso.nome}\n")

# Atividades vinculadas à turma 2025
atividades_turma = turma_2025.atividades.all()
print(f"Total de atividades vinculadas: {atividades_turma.count()}")

# Identificar atividades a manter
atividades_manter = atividades_turma.filter(
    Q(nome='Aula', tipo_atividade='AULA') |
    Q(nome='Plenilúnio', tipo_atividade='PLENILUNIO')
)

print(f"Atividades a manter: {atividades_manter.count()}")
for ativ in atividades_manter:
    print(f"  ✓ {ativ.nome} ({ativ.get_tipo_atividade_display()})")

# Identificar atividades a remover
atividades_remover = atividades_turma.exclude(
    id__in=atividades_manter.values_list('id', flat=True)
)

print(f"\nAtividades a remover: {atividades_remover.count()}")
for ativ in atividades_remover:
    print(f"  ✗ {ativ.nome} ({ativ.get_tipo_atividade_display()})")

# Remover atividades
if atividades_remover.count() > 0:
    print("\n" + "-" * 70)
    print("REMOVENDO ATIVIDADES DA TURMA...")
    print("-" * 70)
    
    for ativ in atividades_remover:
        # Remover vínculo entre atividade e turma
        ativ.turmas.remove(turma_2025)
        print(f"✓ Removido vínculo: {ativ.nome}")
    
    print(f"\n✓ {atividades_remover.count()} atividades desvinculadas com sucesso!")
else:
    print("\n✓ Não há atividades para remover.")

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
