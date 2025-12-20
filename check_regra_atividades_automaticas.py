#!/usr/bin/env python
"""
Verifica a regra de criação automática de atividades ao criar turma.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omaum.settings')
django.setup()

from turmas.models import Turma
from atividades.models import Atividade

# Verificar uma turma existente (a 2025)
turma = Turma.objects.get(id=32)
atividades = turma.atividades.all()

print("=" * 70)
print(f"TURMA: {turma.nome} (ID: {turma.id})")
print(f"CURSO: {turma.curso.nome}")
print("=" * 70)

print(f"\nTotal de atividades vinculadas: {atividades.count()}")
print("\nAtividades vinculadas:")
for ativ in atividades.order_by('tipo_atividade', 'nome'):
    print(f"  - {ativ.nome} ({ativ.get_tipo_atividade_display()})")
    print(f"    Período: {ativ.data_inicio} a {ativ.data_fim or 'N/A'}")
    print(f"    Status: {ativ.status}")

# Verificar se há aula e plenilúnio
aulas = atividades.filter(tipo_atividade='AULA')
plenilunios = atividades.filter(tipo_atividade='PLENILUNIO')

print(f"\n" + "=" * 70)
print(f"VERIFICAÇÃO DE ATIVIDADES AUTOMÁTICAS:")
print("=" * 70)
print(f"✓ Aulas: {aulas.count()}")
print(f"✓ Plenilúnios: {plenilunios.count()}")

# Verificar se há atividades "Aula" e "Plenilúnio" padrão criadas
aula_padrao = atividades.filter(nome='Aula', tipo_atividade='AULA').first()
plenilunio_padrao = atividades.filter(nome='Plenilúnio', tipo_atividade='PLENILUNIO').first()

print(f"\nAtividades Padrão (criadas automaticamente ao criar turma):")
if aula_padrao:
    print(f"✓ Aula padrão: SIM (ID: {aula_padrao.id})")
else:
    print(f"✗ Aula padrão: NÃO encontrada")
    
if plenilunio_padrao:
    print(f"✓ Plenilúnio padrão: SIM (ID: {plenilunio_padrao.id})")
else:
    print(f"✗ Plenilúnio padrão: NÃO encontrado")

# Informações sobre o signal
print(f"\n" + "=" * 70)
print("INFORMAÇÃO SOBRE A REGRA:")
print("=" * 70)
print("""
A regra está implementada via Django Signal em turmas/signals.py:

@receiver(post_save, sender='turmas.Turma')
def criar_atividades_padrao(sender, instance, created, **kwargs):
    '''Cria automaticamente as atividades padrão 'Aula' e 'Plenilúnio' 
       quando uma nova turma é criada.'''
    
COMPORTAMENTO:
✓ Ao criar uma nova turma: Cria automaticamente 2 atividades
  1. Uma atividade de tipo "AULA" (nome: "Aula")
  2. Uma atividade de tipo "PLENILUNIO" (nome: "Plenilúnio")
  
✓ As atividades são criadas com:
  - data_inicio: data_inicio_ativ da turma (ou hoje se não definida)
  - status: PENDENTE
  - turmas: vinculada à turma que foi criada
  - curso: mesmo curso da turma

✓ Estas atividades podem ser editadas ou removidas posteriormente
  
NOTA: O signal dispara APENAS ao criar nova turma (created=True)
      Não executa em atualizações de turma existente.
""")
