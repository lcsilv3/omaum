from django.core.management.base import BaseCommand
from alunos.models import Aluno
from matriculas.models import Matricula


class Command(BaseCommand):
    help = "Verifica o status dos alunos e suas matrículas"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Verificando status dos alunos..."))

        # Verificar todos os alunos
        alunos = Aluno.objects.all()
        self.stdout.write(f"Total de alunos: {alunos.count()}")

        # Contar alunos por situação
        situacoes = {}
        for aluno in alunos:
            situacao = aluno.situacao
            if situacao not in situacoes:
                situacoes[situacao] = 0
            situacoes[situacao] += 1

        self.stdout.write("Contagem de alunos por situação:")
        for situacao, count in situacoes.items():
            self.stdout.write(f"  - {situacao}: {count}")

        # Verificar alunos ativos
        alunos_ativos = Aluno.objects.filter(situacao="ATIVO")
        self.stdout.write(f"Total de alunos ativos: {alunos_ativos.count()}")

        # Verificar matrículas em cursos pré-iniciáticos
        matriculas_pre_iniciatico = Matricula.objects.filter(
            turma__curso__nome__icontains="Pré-iniciático"
        )
        self.stdout.write(
            f"Total de matrículas em cursos pré-iniciáticos: {matriculas_pre_iniciatico.count()}"
        )

        # Listar alunos ativos com matrículas em cursos pré-iniciáticos
        alunos_pre_iniciatico = set()
        for matricula in matriculas_pre_iniciatico:
            if matricula.aluno.situacao == "ATIVO":
                alunos_pre_iniciatico.add(matricula.aluno.cpf)

        self.stdout.write(
            f"Total de alunos ativos em cursos pré-iniciáticos: {len(alunos_pre_iniciatico)}"
        )

        # Listar alunos ativos que podem ser instrutores
        alunos_instrutores = []
        for aluno in alunos_ativos:
            if aluno.pode_ser_instrutor:
                alunos_instrutores.append(aluno)

        self.stdout.write(
            f"Total de alunos ativos que podem ser instrutores: {len(alunos_instrutores)}"
        )

        if alunos_instrutores:
            self.stdout.write("Alunos que podem ser instrutores:")
            for aluno in alunos_instrutores[:10]:  # Mostrar apenas os 10 primeiros
                self.stdout.write(f"  - {aluno.nome} (CPF: {aluno.cpf})")

            if len(alunos_instrutores) > 10:
                self.stdout.write(f"  ... e mais {len(alunos_instrutores) - 10} alunos")
        else:
            self.stdout.write(self.style.WARNING("Nenhum aluno pode ser instrutor!"))
