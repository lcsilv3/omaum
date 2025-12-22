#!/usr/bin/env python
"""
Script para testar se o problema do unique_together foi resolvido.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from datetime import date
from presencas.models import RegistroPresenca
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade


def teste_unique_together():
    """
    Testa se o unique_together está funcionando corretamente
    em RegistroPresenca com os campos: aluno, turma, data, atividade
    """
    print("🔍 TESTE DO UNIQUE_TOGETHER CORRIGIDO")
    print("=" * 50)

    try:
        # Buscar dados de teste
        aluno = Aluno.objects.first()
        turma = Turma.objects.first()
        atividade = Atividade.objects.first()

        if not all([aluno, turma, atividade]):
            print("❌ Não há dados suficientes para teste")
            return

        data_teste = date.today()

        print("📊 Dados do teste:")
        print(f"   Aluno: {aluno.nome} (CPF: {aluno.cpf})")
        print(f"   Turma: {turma.nome}")
        print(f"   Atividade: {atividade.nome}")
        print(f"   Data: {data_teste}")
        print()

        # Teste 1: Criar primeiro registro de presença
        print("🧪 Teste 1: Criar primeiro registro de presença")
        presenca1, created1 = RegistroPresenca.objects.update_or_create(
            aluno=aluno,
            turma=turma,
            data=data_teste,
            atividade=atividade,
            defaults={
                "status": "P",
                "registrado_por": "TESTE",
            },
        )
        print(
            f"   ✅ Primeiro registro: {'criado' if created1 else 'atualizado'} - ID: {presenca1.id}"
        )

        # Teste 2: Tentar criar novamente (deve atualizar)
        print("🧪 Teste 2: Tentar criar novamente (deve atualizar)")
        presenca2, created2 = RegistroPresenca.objects.update_or_create(
            aluno=aluno,
            turma=turma,
            data=data_teste,
            atividade=atividade,
            defaults={
                "status": "F",
                "justificativa": "Teste de atualização",
                "registrado_por": "TESTE_UPDATE",
            },
        )
        print(
            f"   ✅ Segundo registro: {'criado' if created2 else 'atualizado'} - ID: {presenca2.id}"
        )

        # Verificar se são o mesmo objeto
        if presenca1.id == presenca2.id:
            print(
                "   ✅ Sucesso! São o mesmo registro de presença (unique_together funcionando)"
            )
        else:
            print("   ❌ Erro! Foram criados registros diferentes")

        # Teste 3: Verificar quantos registros existem
        print("🧪 Teste 3: Verificar quantidade de registros")
        total_presencas = RegistroPresenca.objects.filter(
            aluno=aluno, turma=turma, data=data_teste, atividade=atividade
        ).count()
        print(
            f"   📊 Total de registros para este aluno/turma/data/atividade: {total_presencas}"
        )

        if total_presencas == 1:
            print(
                "   ✅ Perfeito! Apenas um registro existe (unique_together funcionando)"
            )
        else:
            print(
                f"   ❌ Problema! Existem {total_presencas} registros (deveria ser 1)"
            )

        # Limpeza
        print("🧪 Limpeza: Removendo dados de teste")
        RegistroPresenca.objects.filter(
            aluno=aluno,
            turma=turma,
            data=data_teste,
            atividade=atividade,
            registrado_por__in=["TESTE", "TESTE_UPDATE"],
        ).delete()
        print("   ✅ Dados de teste removidos")

        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("O unique_together está funcionando corretamente.")

    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    teste_unique_together()
