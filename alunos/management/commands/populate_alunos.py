import os
import requests
from django.core.management.base import BaseCommand
from faker import Faker
from turmas.models import Turma
from matriculas.models import Matricula
from alunos.services import criar_aluno
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Popula o banco de dados com alunos de teste, incluindo fotos e matrículas.'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indica o número de alunos a serem criados.', default=50)

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        faker = Faker('pt_BR')
        # Buscamos apenas turmas que estão ativas para realizar a matrícula
        turmas = list(Turma.objects.filter(status='A'))

        if not turmas:
            self.stdout.write(self.style.ERROR('Nenhuma turma ativa encontrada. Por favor, crie e ative algumas turmas primeiro.'))
            return

        alunos_criados = 0
        for i in range(total):
            nome = faker.name()
            email = f'{nome.split(" ")[0].lower()}.{faker.last_name().lower()}@{faker.free_email_domain()}'
            data_nascimento = faker.date_of_birth(minimum_age=18, maximum_age=30)
            cpf = faker.unique.cpf().replace('.', '').replace('-', '')

            aluno_data = {
                'nome': nome,
                'email': email,
                'data_nascimento': data_nascimento,
                'cpf': cpf,
            }

            foto_url = 'https://thispersondoesnotexist.com/'

            try:
                aluno = criar_aluno(aluno_data, foto_url=foto_url)

                if aluno:
                    # Cria a matrícula para o aluno em uma turma aleatória
                    turma_aleatoria = random.choice(turmas)
                    Matricula.objects.create(
                        aluno=aluno,
                        turma=turma_aleatoria,
                        data_matricula=timezone.now().date(),
                        status='A'  # Matrícula ativa
                    )
                    self.stdout.write(self.style.SUCCESS(f'Aluno "{nome}" criado e matriculado na turma "{turma_aleatoria.nome}" com sucesso.'))
                    alunos_criados += 1
                else:
                    self.stdout.write(self.style.ERROR(f'Falha ao criar o aluno {nome}.'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ocorreu um erro inesperado ao processar o aluno {nome}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Processo concluído. {alunos_criados} de {total} alunos criados e matriculados.'))
