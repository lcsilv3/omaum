#!/usr/bin/env python
"""
Script para criar um aluno de teste para validar a otimização da seção Dados Iniciáticos.
"""

import os
import django
from datetime import date

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from alunos.models import Aluno


def criar_aluno_teste():
    """Cria um aluno de teste para validação."""
    try:
        # Verificar se já existe
        if Aluno.objects.filter(cpf="12345678900").exists():
            print("Aluno já existe!")
            return

        # Criar aluno
        aluno = Aluno.objects.create(
            nome="João da Silva",
            cpf="12345678900",
            email="joao@example.com",
            data_nascimento=date(1990, 1, 1),
            sexo="M",
            situacao="a",
            ativo=True,
            numero_iniciatico="123456",
            nome_iniciatico="João dos Santos",
            grau_atual="Aprendiz",
            situacao_iniciatica="INICIADO",
            historico_iniciatico=[],
        )

        print(f"Aluno criado com sucesso: {aluno.nome} - CPF: {aluno.cpf}")

    except Exception as e:
        print(f"Erro ao criar aluno: {e}")


if __name__ == "__main__":
    criar_aluno_teste()
