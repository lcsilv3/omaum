#!/usr/bin/env python
"""Script para corrigir atividades que têm turmas mas não têm curso definido."""

import os
import sys
import django

# Configurar Django
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
    django.setup()

    from atividades.models import Atividade
    
    print("Verificando atividades que precisam de correção...")
    
    # Buscar atividades sem curso mas com turmas
    atividades_sem_curso = Atividade.objects.filter(curso__isnull=True).prefetch_related('turmas__curso')
    
    corrigidas = 0
    for atividade in atividades_sem_curso:
        if atividade.turmas.exists():
            # Pegar o curso da primeira turma
            primeira_turma = atividade.turmas.first()
            if primeira_turma and primeira_turma.curso:
                atividade.curso = primeira_turma.curso
                atividade.save()
                corrigidas += 1
                print(f"✓ Atividade '{atividade.nome}' corrigida - curso: {primeira_turma.curso.nome}")
    
    print(f"\n{corrigidas} atividades foram corrigidas.")
    
    # Verificar se ainda há inconsistências
    inconsistencias = 0
    for atividade in Atividade.objects.all().prefetch_related('turmas__curso'):
        if atividade.turmas.exists():
            cursos_das_turmas = set(turma.curso_id for turma in atividade.turmas.all() if turma.curso)
            if atividade.curso and len(cursos_das_turmas) > 0:
                if atividade.curso.id not in cursos_das_turmas:
                    print(f"⚠️  Inconsistência: Atividade '{atividade.nome}' - curso: {atividade.curso.nome}, turmas de cursos diferentes")
                    inconsistencias += 1
    
    if inconsistencias == 0:
        print("✓ Nenhuma inconsistência encontrada!")
    else:
        print(f"⚠️  {inconsistencias} inconsistências encontradas.")
