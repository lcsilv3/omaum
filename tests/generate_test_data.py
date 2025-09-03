import os
import django
import random
from datetime import timedelta

# Configurar o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings")
django.setup()

from tests.factories import UserFactory, AlunoFactory, TurmaFactory, AtividadeFactory
from matriculas.models import Matricula


def generate_test_data():
    """Gera dados de teste para o sistema."""
    print("Gerando dados de teste...")

    # Criar usuários
    print("Criando usuários...")
    UserFactory(username="admin", is_staff=True, is_superuser=True)
    users = UserFactory.create_batch(5)

    # Criar alunos
    print("Criando alunos...")
    alunos = AlunoFactory.create_batch(50)

    # Criar turmas
    print("Criando turmas...")
    turmas = TurmaFactory.create_batch(10)

    # Criar matrículas
    print("Criando matrículas...")
    for turma in turmas:
        # Selecionar alunos aleatórios para esta turma
        alunos_selecionados = random.sample(alunos, random.randint(5, 20))

        for aluno in alunos_selecionados:
            # Criar matrícula
            data_matricula = turma.data_inicio - timedelta(days=random.randint(1, 30))

            Matricula.objects.create(
                aluno=aluno, turma=turma, data_matricula=data_matricula, status="A"
            )

    # Criar atividades acadêmicas
    print("Criando atividades acadêmicas...")
    for _ in range(30):
        # Selecionar turmas aleatórias
        random.sample(turmas, random.randint(1, 3))

        AtividadeFactory()

    # Criar atividades ritualísticas
    print("Criando atividades ritualísticas...")
    for turma in turmas:
        # Selecionar alunos matriculados nesta turma
        alunos_matriculados = [m.aluno for m in Matricula.objects.filter(turma=turma)]

        if alunos_matriculados:
            # Criar entre 1 e 3 atividades ritualísticas para esta turma
            for _ in range(random.randint(1, 3)):
                # Selecionar participantes aleatórios entre os alunos matriculados
                random.sample(
                    alunos_matriculados,
                    min(
                        len(alunos_matriculados),
                        random.randint(3, len(alunos_matriculados)),
                    ),
                )

                AtividadeFactory(turma=turma)

    print("Dados de teste gerados com sucesso!")
    print(f"- {len(users) + 1} usuários (incluindo admin)")
    print(f"- {len(alunos)} alunos")
    print(f"- {len(turmas)} turmas")
    print(f"- {Matricula.objects.count()} matrículas")
    print(f"- {AtividadeFactory._meta.model.objects.count()} atividades")


if __name__ == "__main__":
    generate_test_data()
