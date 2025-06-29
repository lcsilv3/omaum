import os
import django
import random

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from faker import Faker
from cursos.models import Curso

# Inicializar o Faker com localização brasileira
fake = Faker("pt_BR")

# Criar alguns cursos básicos
cursos_basicos = [
    {
        "codigo_curso": 101,
        "nome": "Curso de Teste",
        "descricao": "Descrição do curso de teste",
        "duracao": 6,
    },
    {
        "codigo_curso": 102,
        "nome": "Curso de Python",
        "descricao": "Aprenda Python do zero",
        "duracao": 3,
    },
    {
        "codigo_curso": 103,
        "nome": "Meditação Avançada",
        "descricao": "Técnicas avançadas de meditação",
        "duracao": 12,
    },
]

print("Criando cursos básicos...")
for curso_data in cursos_basicos:
    try:
        curso, created = Curso.objects.update_or_create(
            codigo_curso=curso_data["codigo_curso"], defaults=curso_data
        )
        if created:
            print(f"Curso criado: {curso.id} - {curso.nome}")
        else:
            print(f"Curso atualizado: {curso.id} - {curso.nome}")
    except Exception as e:
        print(f"Erro ao criar curso {curso_data['codigo_curso']}: {e}")

print(f"\nTotal de cursos após criação: {Curso.objects.count()}")
