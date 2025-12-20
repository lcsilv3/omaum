#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from atividades.models import AtividadeAcademica
from turmas.models import Turma

# Buscar plenilúnios
plenilunios = AtividadeAcademica.objects.filter(tipo_atividade='PLENILUNIO')
print(f'Total de Plenilunios no sistema: {plenilunios.count()}')

# Vincular à turma 2025
turma_2025 = Turma.objects.get(id=32)
for p in plenilunios:
    turma_2025.atividades.add(p)

# Verificar resultado
count = turma_2025.atividades.filter(tipo_atividade='PLENILUNIO').count()
print(f'Plenilunios na turma 2025 agora: {count}')

# Resumo final
aulas = turma_2025.atividades.filter(tipo_atividade='AULA').count()
print(f'\nResumo da Turma 2025 (Colégio Sacerdotal):')
print(f'- Aulas: {aulas}')
print(f'- Plenilunios: {count}')
