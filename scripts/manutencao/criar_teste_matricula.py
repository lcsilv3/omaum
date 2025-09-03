#!/usr/bin/env python
"""
Script para criar dados de teste para o sistema de Dados Iniciáticos
"""

import os
import django
from django.conf import settings

# Configurar Django
if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
    django.setup()

from alunos.models import Aluno
from cursos.models import Curso
from turmas.models import Turma
from matriculas.models import Matricula
from datetime import date


def criar_dados_teste():
    """Cria dados de teste para validar o sistema"""
    print("=== Criando dados de teste ===")

    # Criar curso se não existir
    curso, created = Curso.objects.get_or_create(
        nome="Aprendiz", defaults={"descricao": "Curso de Aprendiz"}
    )
    print(f"Curso: {curso.nome} (criado: {created})")

    # Criar turma se não existir
    turma, created = Turma.objects.get_or_create(
        nome="Turma Aprendiz 2025", curso=curso, defaults={"vagas": 20}
    )
    print(f"Turma: {turma.nome} (criada: {created})")

    # Obter primeiro aluno
    aluno = Aluno.objects.first()
    if not aluno:
        print("ERRO: Nenhum aluno encontrado!")
        return

    print(f"Aluno: {aluno.nome}")

    # Criar matrícula
    matricula, created = Matricula.objects.get_or_create(
        aluno=aluno, turma=turma, defaults={"data_matricula": date.today()}
    )
    print(f"Matrícula criada: {created}")

    # Testar grau automático
    grau_atual = aluno.grau_atual_automatico
    print(f"Grau atual automático: {grau_atual}")

    # Testar último curso
    ultimo_curso = aluno.ultimo_curso_matriculado
    print(f"Último curso matriculado: {ultimo_curso}")

    print("\n=== Teste concluído ===")


if __name__ == "__main__":
    criar_dados_teste()
