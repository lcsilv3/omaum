import os
import django
import random

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from faker import Faker
from cursos.models import Curso
from django.db import IntegrityError

# Inicializar o Faker com localização brasileira
fake = Faker("pt_BR")

# Lista de possíveis áreas de estudo para gerar nomes de cursos mais realistas
areas_estudo = [
    "Filosofia",
    "Psicologia",
    "Meditação",
    "Yoga",
    "Astrologia",
    "Numerologia",
    "Tarô",
    "Alquimia",
    "Metafísica",
    "Espiritualidade",
    "Terapia",
    "Cura",
    "Energias",
    "Xamanismo",
    "Rituais",
    "Mantras",
    "Chakras",
    "Cristais",
    "Reiki",
    "Ayurveda",
]

# Lista de prefixos para os cursos
prefixos = [
    "Introdução a",
    "Fundamentos de",
    "Avançado em",
    "Prática de",
    "Teoria e Prática de",
    "Estudos em",
    "Imersão em",
    "Workshop de",
    "Especialização em",
    "Técnicas de",
    "Princípios de",
    "Aplicação de",
    "Desenvolvimento de",
    "Aprofundamento em",
    "Iniciação em",
]


def limpar_cursos_existentes():
    """Remove todos os cursos existentes para evitar conflitos"""
    try:
        count = Curso.objects.all().delete()[0]
        print(f"Removidos {count} cursos existentes.")
    except Exception as e:
        print(f"Erro ao remover cursos existentes: {e}")


def criar_cursos_para_testes():
    """Cria cursos específicos para cobrir casos de teste"""

    # Lista de cursos específicos para testes
    cursos_teste = [
        # Curso com código 101 (usado em test_criar_curso_com_dados_validos)
        {
            "codigo_curso": 101,
            "nome": "Curso de Teste",
            "descricao": "Descrição do curso de teste",
            "duracao": 6,
        },
        # Curso com código 102 (usado em test_str_representation)
        {
            "codigo_curso": 102,
            "nome": "Curso de Python",
            "descricao": "Aprenda Python do zero",
            "duracao": 3,
        },
        # Cursos para test_ordering
        {
            "codigo_curso": 103,
            "nome": "Curso A",
            "descricao": "Primeiro curso na ordenação",
            "duracao": 6,
        },
        {
            "codigo_curso": 104,
            "nome": "Curso M",
            "descricao": "Segundo curso na ordenação",
            "duracao": 6,
        },
        {
            "codigo_curso": 105,
            "nome": "Curso Z",
            "descricao": "Terceiro curso na ordenação",
            "duracao": 6,
        },
        # Curso para test_form_valid
        {
            "codigo_curso": 201,
            "nome": "Curso de Teste para Formulário",
            "descricao": "Descrição do curso para teste de formulário",
            "duracao": 6,
        },
        # Curso para test_editar_curso_view_post_valido
        {
            "codigo_curso": 301,
            "nome": "Curso de Teste para Edição",
            "descricao": "Descrição do curso para teste de edição",
            "duracao": 6,
        },
        # Curso para test_fluxo_completo_curso
        {
            "codigo_curso": 401,
            "nome": "Curso de Integração",
            "descricao": "Descrição do curso de integração",
            "duracao": 8,
        },
        # Curso com duração mínima
        {
            "codigo_curso": 501,
            "nome": "Curso Rápido",
            "descricao": "Curso com duração mínima",
            "duracao": 1,
        },
        # Curso com duração máxima
        {
            "codigo_curso": 502,
            "nome": "Curso Extenso",
            "descricao": "Curso com duração máxima",
            "duracao": 24,
        },
        # Curso com nome longo
        {
            "codigo_curso": 503,
            "nome": "Curso com Nome Extremamente Longo para Testar o Limite de Caracteres do Campo Nome do Modelo Curso",
            "descricao": "Descrição de curso com nome longo",
            "duracao": 12,
        },
        # Curso com descrição longa
        {
            "codigo_curso": 504,
            "nome": "Curso com Descrição Longa",
            "descricao": fake.text(max_nb_chars=1000),  # Descrição longa
            "duracao": 12,
        },
    ]

    # Criar os cursos de teste
    for curso_data in cursos_teste:
        try:
            curso = Curso.objects.create(**curso_data)
            print(
                f"Curso de teste criado: {curso.codigo_curso} - {curso.nome} ({curso.duracao} meses)"
            )
        except IntegrityError:
            print(
                f"Curso com código {curso_data['codigo_curso']} já existe. Pulando."
            )
        except Exception as e:
            print(f"Erro ao criar curso de teste: {e}")


def criar_cursos_aleatorios(quantidade=8):
    """Cria cursos aleatórios adicionais"""

    # Lista para armazenar os códigos de curso já utilizados
    codigos_existentes = list(
        Curso.objects.values_list("codigo_curso", flat=True)
    )

    cursos_criados = 0
    tentativas = 0
    max_tentativas = 100  # Limite de tentativas para evitar loop infinito

    # Começar a partir do código 600 para não conflitar com os cursos de teste
    codigo_base = 600

    while cursos_criados < quantidade and tentativas < max_tentativas:
        tentativas += 1

        # Gerar código de curso único
        codigo_curso = codigo_base + cursos_criados
        if codigo_curso in codigos_existentes:
            continue

        # Gerar nome do curso
        prefixo = random.choice(prefixos)
        area = random.choice(areas_estudo)
        nome = f"{prefixo} {area}"

        # Gerar descrição
        descricao = fake.paragraph(nb_sentences=3)

        # Gerar duração (entre 1 e 24 meses)
        duracao = random.randint(1, 24)

        # Criar o curso
        try:
            curso = Curso.objects.create(
                codigo_curso=codigo_curso,
                nome=nome,
                descricao=descricao,
                duracao=duracao,
            )
            print(f"Curso aleatório criado: {curso.id} - {curso.nome} ({curso.duracao} meses)")
        except Exception as e:
            print(f"Erro ao criar curso aleatório: {e}")

    print(f"\nTotal de cursos aleatórios criados: {cursos_criados}")


def main():
    """Função principal para popular o banco de dados com cursos"""
    print("Iniciando criação de cursos para testes...")

    # Perguntar se deseja limpar os cursos existentes
    resposta = input(
        "Deseja remover todos os cursos existentes antes de criar novos? (s/n): "
    )
    if resposta.lower() == "s":
        limpar_cursos_existentes()

    # Criar cursos específicos para testes
    criar_cursos_para_testes()

    # Criar cursos aleatórios adicionais
    criar_cursos_aleatorios(8)

    # Contar total de cursos no banco de dados
    total_cursos = Curso.objects.count()
    print(f"\nTotal de cursos no banco de dados: {total_cursos}")
    print("Processo concluído!")


if __name__ == "__main__":
    main()
