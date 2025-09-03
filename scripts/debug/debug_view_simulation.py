#!/usr/bin/env python
"""
Script para simular o problema da view de totais de atividades
"""

import os
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from datetime import date
from calendar import monthrange
from django.db.models import Q
from atividades.models import Atividade
from turmas.models import Turma


def get_model_class(model_name):
    """Obtém classe de modelo dinamicamente para evitar imports circulares."""
    if model_name == "Atividade":
        return Atividade
    return None


print("=== SIMULAÇÃO COMPLETA DA VIEW ===")

# Simular dados da sessão (primeira chamada, sem totais_atividades ainda)
turma_id = 1
ano = 2025
mes = 5

turma = Turma.objects.get(id=turma_id)
curso = turma.curso

print(f"Turma: {turma}")
print(f"Curso: {curso}")
print(f"Ano: {ano}, Mês: {mes}")

# Simular primeira parte da lógica da view
totais_atividades = {}  # Primeira vez, sessão vazia

if turma and curso and ano and mes:
    if totais_atividades:
        print("Caminho 1: Usando atividades da sessão")
        atividades_ids = [
            int(key.replace("qtd_ativ_", ""))
            for key in totais_atividades.keys()
            if int(totais_atividades[key]) > 0
        ]
        Atividade_Model = get_model_class("Atividade")
        atividades = Atividade_Model.objects.filter(
            id__in=atividades_ids,
            turmas__id=turma.id,
        )
    else:
        print("Caminho 2: Primeira vez - filtro por data")
        primeiro_dia = date(int(ano), int(mes), 1)
        ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
        print(f"Período de filtro: {primeiro_dia} a {ultimo_dia}")

        Atividade_Model = get_model_class("Atividade")
        atividades = (
            Atividade_Model.objects.filter(turmas__id=turma.id, curso=curso)
            .filter(
                Q(data_inicio__lte=ultimo_dia)
                & (Q(data_fim__isnull=True) | Q(data_fim__gte=primeiro_dia))
            )
            .distinct()
        )

print(f"\nQuantidade de atividades encontradas: {len(atividades)}")
print("IDs das atividades:")
for ativ in atividades:
    print(f"  - ID: {ativ.id}, Nome: {ativ.nome}")

# Simular o que iria para a sessão
atividades_ids = [a.id for a in atividades]
print(f"\nIDs que iriam para a sessão: {atividades_ids}")

# Testar se houve algum problema no QuerySet
print(f"\nTipo do objeto atividades: {type(atividades)}")
print(f"Query SQL: {atividades.query}")

# Verificar se há algum problema com avaliação lazy
list_atividades = list(atividades)
print(f"Após conversão para lista: {len(list_atividades)} atividades")
