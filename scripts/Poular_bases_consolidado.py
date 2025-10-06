import os
import sys
import django
import random
from datetime import date, time, timedelta
from decimal import Decimal

# Configuração do ambiente Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from django.contrib.auth.models import User

# --- Model Imports ---
from alunos.models import Aluno
from cursos.models import Curso
from turmas.models import Turma
from atividades.models import Atividade

# --- Script Imports ---
from scripts.popular_cursos import popular_cursos

# --- DADOS DE AMOSTRA ---
nomes = [
    "Miguel",
    "Arthur",
    "Gael",
    "Heitor",
    "Theo",
    "Davi",
    "Gabriel",
    "Bernardo",
    "Samuel",
    "Helena",
    "Alice",
    "Laura",
    "Maria Alice",
    "Sophia",
    "Manuela",
    "Maitê",
    "Liz",
    "Cecília",
    "Isabella",
]
sobrenomes = [
    "Silva",
    "Santos",
    "Oliveira",
    "Souza",
    "Rodrigues",
    "Ferreira",
    "Alves",
    "Pereira",
    "Lima",
    "Gomes",
    "Costa",
    "Ribeiro",
    "Martins",
    "Carvalho",
    "Almeida",
    "Lopes",
    "Soares",
    "Fernandes",
    "Vieira",
]
sexos = ["Masculino", "Feminino"]


def gerar_cpf_unico():
    """Gera um CPF com 11 dígitos numéricos, sem formatação."""
    # Gera um número de 11 dígitos e garante que tenha 11 caracteres com zeros à esquerda se necessário
    return str(random.randint(0, 99999999999)).zfill(11)


def gerar_email_unico(nome, sobrenome):
    return f"{nome.lower()}.{sobrenome.lower()}{random.randint(1, 9999)}@exemplo.com"


def popular_alunos():
    QUANTIDADE_ALUNOS = 50
    if Aluno.objects.count() >= QUANTIDADE_ALUNOS:
        print("Alunos já existem em quantidade suficiente.")
        return

    print(f"Criando {QUANTIDADE_ALUNOS} alunos...")
    for i in range(QUANTIDADE_ALUNOS):
        nome_aluno = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
        try:
            Aluno.objects.create(
                cpf=gerar_cpf_unico(),
                nome=nome_aluno,
                data_nascimento=date(
                    random.randint(1970, 2000),
                    random.randint(1, 12),
                    random.randint(1, 28),
                ),
                email=gerar_email_unico(nome_aluno.split()[0], nome_aluno.split()[-1]),
                sexo=random.choice(sexos)[0],
                numero_iniciatico=str(1000 + i),
            )
        except Exception as e:
            # Em caso de colisão de CPF ou e-mail, apenas ignore e continue
            print(f"Aviso ao criar aluno {i+1}: {e}")
            continue
    print(f"Total de {Aluno.objects.count()} alunos no banco.")


if __name__ == "__main__":
    print("Iniciando população da base de dados...")

    # 1. Popula os cursos
    print("--- Populando Cursos ---")
    popular_cursos()

    # 2. Popula os alunos
    print("\n--- Populando Alunos ---")
    popular_alunos()

    print("\nPopulação concluída.")
