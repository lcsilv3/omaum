#!/usr/bin/env python
"""
Script para testar o fluxo completo da sessão
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
from presencas.models import TotalAtividadeMes


def get_model_class(model_name):
    if model_name == "Atividade":
        return Atividade
    return None


print("=== TESTE FLUXO SESSÃO COMPLETO ===")

# 1. Simular dados básicos (o que vem de dados-basicos)
turma_id = 1
ano = 2025
mes = 5

# 2. Simular primeira chamada GET para totais-atividades
print("\n=== PASSO 1: GET /totais-atividades/ ===")
turma = Turma.objects.get(id=turma_id)
curso = turma.curso

# Simular sessão vazia (primeira vez)
sessao = {"presenca_turma_id": turma_id, "presenca_ano": ano, "presenca_mes": mes}

print(f"Sessão inicial: {sessao}")

# Executar lógica da view GET
totais_atividades = sessao.get("presenca_totais_atividades", {})
print(f"totais_atividades da sessão: {totais_atividades}")

atividades = []
if turma and curso and ano and mes:
    if totais_atividades:
        print("Usando atividades da sessão anterior")
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
        print("Primeira vez - usando filtro por data E curso")
        primeiro_dia = date(int(ano), int(mes), 1)
        ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
        Atividade_Model = get_model_class("Atividade")
        atividades = (
            Atividade_Model.objects.filter(
                turmas__id=turma.id,
                curso=curso,  # IMPORTANTE: este filtro por curso!
            )
            .filter(
                Q(data_inicio__lte=ultimo_dia)
                & (Q(data_fim__isnull=True) | Q(data_fim__gte=primeiro_dia))
            )
            .distinct()
        )

print(f"Atividades encontradas no GET: {len(atividades)}")
for ativ in atividades:
    print(f"  - ID: {ativ.id}, Nome: {ativ.nome}, Curso: {ativ.curso}")

# Salvar na sessão (simular)
sessao["presenca_atividades_ids"] = [a.id for a in atividades]
print(f"IDs salvos na sessão: {sessao['presenca_atividades_ids']}")

# 3. Simular chamada AJAX POST (quando usuário submete)
print("\n=== PASSO 2: POST AJAX /totais-atividades/ajax/ ===")

# Recuperar da sessão (como faz a view AJAX)
atividades_ids_sessao = sessao.get("presenca_atividades_ids", [])
print(f"IDs recuperados da sessão: {atividades_ids_sessao}")

if atividades_ids_sessao:
    Atividade_Model = get_model_class("Atividade")
    atividades_ajax = Atividade_Model.objects.filter(
        id__in=atividades_ids_sessao,
        turmas__id=turma.id,  # Nota: sem filtro por curso aqui!
    )
    print(f"Atividades encontradas no AJAX: {len(atividades_ajax)}")
    for ativ in atividades_ajax:
        print(f"  - ID: {ativ.id}, Nome: {ativ.nome}")
else:
    print("Fallback: usando filtro por data (sem curso)")
    primeiro_dia = date(int(ano), int(mes), 1)
    ultimo_dia = date(int(ano), int(mes), monthrange(int(ano), int(mes))[1])
    Atividade_Model = get_model_class("Atividade")
    atividades_ajax = (
        Atividade_Model.objects.filter(
            turmas__id=turma.id  # SEM filtro por curso
        )
        .filter(
            Q(data_inicio__lte=ultimo_dia)
            & (Q(data_fim__isnull=True) | Q(data_fim__gte=primeiro_dia))
        )
        .distinct()
    )
    print(f"Atividades encontradas no AJAX (fallback): {len(atividades_ajax)}")

# 4. Verificar se há algum TotalAtividadeMes existente que pode interferir
print("\n=== VERIFICAÇÃO: TotalAtividadeMes existentes ===")
totais_existentes = TotalAtividadeMes.objects.filter(turma=turma, ano=ano, mes=mes)
print(f"Totais já registrados: {totais_existentes.count()}")
for total in totais_existentes:
    print(
        f"  - Atividade: {total.atividade.nome} (ID: {total.atividade.id}), Qtd: {total.qtd_ativ_mes}"
    )
