#!/usr/bin/env python
"""
Script para executar linters e formatadores no código do projeto OMAUM.
"""
import os
import sys
import subprocess
from pathlib import Path

# Diretório raiz do projeto
ROOT_DIR = Path(__file__).parent.parent

# Diretórios a serem verificados
DIRS_TO_CHECK = [
    "alunos",
    "atividades",
    "core",
    "cursos",
    "matriculas",
    "notas",
    "pagamentos",
    "turmas",
    "omaum",
    "scripts",
]


def run_black():
    """Executa o Black para formatar o código."""
    print("Executando Black...")

    result = subprocess.run(
        ["black", "."], cwd=ROOT_DIR, capture_output=True, text=True
    )

    if result.returncode != 0:
        print("Black encontrou problemas:")
        print(result.stderr)
    else:
        print("Black formatou o código com sucesso")


def run_pylint():
    """Executa o Pylint nos diretórios especificados."""
    print("\nExecutando Pylint...")

    for directory in DIRS_TO_CHECK:
        dir_path = ROOT_DIR / directory
        if not dir_path.exists():
            continue

        print(f"Verificando {directory}...")
        result = subprocess.run(
            ["pylint", directory], cwd=ROOT_DIR, capture_output=True, text=True
        )

        if result.returncode != 0:
            print(f"Pylint encontrou problemas em {directory}:")
            print(result.stdout)
        else:
            print(f"Pylint não encontrou problemas em {directory}")


def run_flake8():
    """Executa o Flake8 nos diretórios especificados."""
    print("\nExecutando Flake8...")

    for directory in DIRS_TO_CHECK:
        dir_path = ROOT_DIR / directory
        if not dir_path.exists():
            continue

        print(f"Verificando {directory}...")
        result = subprocess.run(
            ["flake8", directory], cwd=ROOT_DIR, capture_output=True, text=True
        )

        if result.stdout:
            print(f"Flake8 encontrou problemas em {directory}:")
            print(result.stdout)
        else:
            print(f"Flake8 não encontrou problemas em {directory}")


if __name__ == "__main__":
    run_black()  # Primeiro formata o código
    run_pylint()
    run_flake8()

    print("\nVerificação de código concluída!")
