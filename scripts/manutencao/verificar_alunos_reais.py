#!/usr/bin/env python
import os
import sys
import django

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from alunos.models import Aluno
from turmas.models import Turma

print("🔍 Verificando alunos reais na turma...")

# Buscar turma ID 1
try:
    turma = Turma.objects.get(id=1)
    print(f"✅ Turma encontrada: {turma.nome}")

    # Buscar alunos ativos da turma
    alunos = Aluno.objects.filter(matricula__turma=turma, situacao="ATIVO").distinct()

    print(f"📊 Total de alunos ativos: {alunos.count()}")

    if alunos.exists():
        print("\n👥 Alunos disponíveis:")
        for i, aluno in enumerate(alunos[:5], 1):  # Mostrar apenas os primeiros 5
            print(f"   {i}. CPF: {aluno.cpf} - Nome: {aluno.nome}")

        # Pegar o primeiro aluno para usar no teste
        primeiro_aluno = alunos.first()
        print(f"\n🎯 Para usar no teste, use o CPF: {primeiro_aluno.cpf}")

    else:
        print("❌ Nenhum aluno ativo encontrado na turma")

except Turma.DoesNotExist:
    print("❌ Turma com ID 1 não encontrada")
except Exception as e:
    print(f"❌ Erro: {e}")
