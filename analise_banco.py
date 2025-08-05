#!/usr/bin/env python
import os
import sys
import django

# Adicionar o diretório atual ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from presencas.models import Presenca
from turmas.models import Turma
from django.utils import timezone
from datetime import timedelta

print('🔍 ANÁLISE REVERSA - VERIFICAÇÃO DO BANCO')
print('=' * 50)

# Busca presenças recentes (últimas 24h)
ontem = timezone.now() - timedelta(days=1)
presencas_recentes = Presenca.objects.filter(data_registro__gte=ontem).order_by('-data_registro')

print(f'📊 Presenças registradas nas últimas 24h: {presencas_recentes.count()}')

if presencas_recentes.exists():
    print('📋 DADOS ENCONTRADOS:')
    for p in presencas_recentes[:10]:
        print(f'   ID: {p.id} | Aluno: {p.aluno.nome} | Atividade: {p.atividade.nome if p.atividade else "N/A"}')
        print(f'      Data: {p.data} | Presente: {p.presente} | Criado: {p.data_registro}')
        print(f'      Turma: {p.turma.nome if p.turma else "N/A"}')
        print('   ---')
else:
    print('❌ NENHUMA PRESENÇA ENCONTRADA nas últimas 24h')

print('\n🔍 Buscando especificamente para Turma ID=1...')
try:
    turma = Turma.objects.get(id=1)
    presencas_turma = Presenca.objects.filter(turma=turma).order_by('-data_registro')[:5]
    print(f'📊 Presenças da turma "{turma.nome}": {Presenca.objects.filter(turma=turma).count()} total')
    
    if presencas_turma.exists():
        print('📋 ÚLTIMAS PRESENÇAS DA TURMA:')
        for p in presencas_turma:
            atividade_nome = p.atividade.nome if p.atividade else "N/A"
            print(f'   {atividade_nome} - Data {p.data} - {p.aluno.nome} - {"Presente" if p.presente else "Ausente"} - {p.data_registro}')
    else:
        print('❌ Nenhuma presença encontrada para esta turma')
        
except Turma.DoesNotExist:
    print('❌ Turma ID=1 não encontrada')
