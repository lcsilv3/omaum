#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from atividades.models import Atividade
from turmas.models import Turma
from cursos.models import Curso

# Pegar turma 2025 e seu curso
turma_2025 = Turma.objects.get(id=32)
curso = turma_2025.curso  # Colégio Sacerdotal

print(f'Turma: {turma_2025.nome}')
print(f'Curso: {curso.nome}\n')

# Verificar quantos plenilúnios já existem
existing_plenilunios = Atividade.objects.filter(tipo_atividade='PLENILUNIO', curso=curso)
print(f'Plenilunios existentes para este curso: {existing_plenilunios.count()}')

# Criar 2 plenilúnios se não existirem
if existing_plenilunios.count() < 2:
    today = datetime.now().date()
    plenilunios_criar = 2 - existing_plenilunios.count()
    
    for i in range(plenilunios_criar):
        data = today + timedelta(days=30 + i*15)
        p = Atividade.objects.create(
            nome=f'Plenilúnio {i+1}',
            tipo_atividade='PLENILUNIO',
            data_inicio=data,
            hora_inicio='20:00',
            hora_fim='22:00',
            local='Online',
            responsavel='Coordenação',
            status='CONFIRMADA',
            curso=curso,
        )
        p.turmas.add(turma_2025)
        print(f'✓ Criado: {p.nome} em {p.data_inicio}')

# Verificar contagem final
aulas = turma_2025.atividades.filter(tipo_atividade='AULA').count()
plenilunios = turma_2025.atividades.filter(tipo_atividade='PLENILUNIO').count()

print(f'\nResumo final para Turma 2025:')
print(f'✓ Aulas: {aulas}')
print(f'✓ Plenilúnios: {plenilunios}')
print(f'✓ Total de atividades: {turma_2025.atividades.count()}')
