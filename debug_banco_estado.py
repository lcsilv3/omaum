#!/usr/bin/env python
"""
Script para verificar estado atual do banco e possíveis interferências
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from presencas.models import TotalAtividadeMes
from atividades.models import Atividade
from turmas.models import Turma

print("=== VERIFICAÇÃO ESTADO BANCO DE DADOS ===")

# Parâmetros do problema
turma_id = 1
ano = 2025
mes = 5

turma = Turma.objects.get(id=turma_id)

# 1. Verificar se existem TotalAtividadeMes para este período
print(f"\n1. TotalAtividadeMes para Turma {turma_id}, {ano}-{mes:02d}:")
totais = TotalAtividadeMes.objects.filter(turma=turma, ano=ano, mes=mes)
if totais.exists():
    for total in totais:
        print(f"   - Atividade: {total.atividade.nome} (ID: {total.atividade.id})")
        print(f"     Quantidade: {total.qtd_ativ_mes}")
        print(f"     Registrado por: {total.registrado_por}")
        print(f"     Data registro: {total.data_registro}")
else:
    print("   - Nenhum registro encontrado")

# 2. Verificar todas as atividades da turma
print(f"\n2. Todas as atividades da turma {turma.nome}:")
atividades_turma = Atividade.objects.filter(turmas__id=turma_id)
for ativ in atividades_turma:
    print(f"   - ID: {ativ.id}, Nome: {ativ.nome}")
    print(f"     Data início: {ativ.data_inicio}")
    print(f"     Data fim: {ativ.data_fim}")
    print(f"     Curso: {ativ.curso}")
    print(f"     Status: {ativ.status}")
    print(f"     Ativo: {ativ.ativo}")

# 3. Verificar atividades ativas da turma
print(f"\n3. Atividades ATIVAS da turma:")
atividades_ativas = Atividade.objects.filter(turmas__id=turma_id, ativo=True)
print(f"   Total ativas: {atividades_ativas.count()}")

# 4. Verificar atividades com status específico
print(f"\n4. Status das atividades:")
for status_choice in Atividade.STATUS_CHOICES:
    count = Atividade.objects.filter(turmas__id=turma_id, status=status_choice[0]).count()
    if count > 0:
        print(f"   - {status_choice[1]}: {count}")

# 5. Verificar logs recentes de TotalAtividadeMes
print(f"\n5. Logs recentes de TotalAtividadeMes (últimos 10):")
recentes = TotalAtividadeMes.objects.order_by('-data_registro')[:10]
for total in recentes:
    print(f"   - {total.data_registro.strftime('%Y-%m-%d %H:%M:%S')}: Turma {total.turma.nome}, Atividade {total.atividade.nome}, Ano {total.ano}, Mês {total.mes}")

# 6. Buscar possível inconsistência na relação many-to-many
print(f"\n6. Verificação relação Atividade-Turma:")
for ativ in atividades_turma:
    turmas_relacionadas = ativ.turmas.all()
    print(f"   - Atividade {ativ.nome} está relacionada a {turmas_relacionadas.count()} turma(s):")
    for t in turmas_relacionadas:
        print(f"     > {t.nome} (ID: {t.id})")
