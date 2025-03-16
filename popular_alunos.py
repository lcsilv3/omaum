import os
import django
from datetime import time
import random

# Django configuration
os.environ['DJANGO_SETTINGS_MODULE'] = 'omaum.settings'
django.setup()

from faker import Faker
from alunos.models import Aluno

# Initialize Faker with Brazilian locale
fake = Faker('pt_BR')

def criar_alunos_ficticios(quantidade=50):
    for _ in range(quantidade):
        # Generate random time for hora_nascimento
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        hora_nascimento = time(hour=random_hour, minute=random_minute)

        Aluno.objects.create(
            cpf=fake.unique.numerify('###########'),
            nome=fake.name(),
            data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=65),
            hora_nascimento=hora_nascimento,  # Add this field
            email=fake.unique.email(),
            foto=None,
            numero_iniciatico=fake.unique.numerify('######'),
            nome_iniciatico=fake.name(),
            sexo=fake.random_element(elements=('M', 'F', 'O')),
            nacionalidade='Brasileira',
            naturalidade=fake.city(),
            rua=fake.street_name(),
            numero_imovel=fake.building_number(),
            complemento=fake.random_element(elements=['Apto 101', 'Casa 1', 'Bloco A', 'Fundos']),  # Brazilian-style complements
            cidade=fake.city(),
            estado=fake.estado_sigla(),
            bairro=fake.bairro(),
            cep=fake.postcode(),
            nome_primeiro_contato=fake.name(),
            celular_primeiro_contato=fake.cellphone_number(),
            tipo_relacionamento_primeiro_contato=fake.random_element(elements=('Pai', 'Mãe', 'Irmão', 'Amigo')),
            nome_segundo_contato=fake.name(),
            celular_segundo_contato=fake.cellphone_number(),
            tipo_relacionamento_segundo_contato=fake.random_element(elements=('Pai', 'Mãe', 'Irmão', 'Amigo')),
            tipo_sanguineo=fake.random_element(elements=('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
            fator_rh=fake.random_element(elements=('+', '-')),
            alergias=fake.text(max_nb_chars=200),
            condicoes_medicas_gerais=fake.text(max_nb_chars=200),
            convenio_medico=fake.company(),
            hospital=fake.company()
        )
    print(f"{quantidade} alunos fictícios criados com sucesso!")

if __name__ == '__main__':
    criar_alunos_ficticios()