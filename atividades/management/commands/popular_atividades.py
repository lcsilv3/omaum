from django.core.management.base import BaseCommand
from atividades.models import Atividade
from cursos.models import Curso
from turmas.models import Turma
from alunos.models import Aluno
from django.utils import timezone
import random
from datetime import timedelta, time


class Command(BaseCommand):
    help = "Popula o banco de dados com atividades para todos os casos possíveis."

    def handle(self, *args, **options):
        tipos = [c[0] for c in Atividade.TIPO_CHOICES]
        status_list = [c[0] for c in Atividade.STATUS_CHOICES]

        cursos = list(Curso.objects.all())
        turmas = list(Turma.objects.all())
        alunos = list(Aluno.objects.all())

        # Limpa atividades antigas para evitar duplicidade
        Atividade.objects.all().delete()

        # Atividades
        for tipo in tipos:
            for status in status_list:
                for i in range(2):  # Cria 2 para cada combinação
                    data_inicio = timezone.now().date() + timedelta(
                        days=random.randint(-10, 10)
                    )
                    data_fim = None
                    if i % 2 == 0:
                        data_fim = data_inicio + timedelta(days=random.randint(1, 10))

                    atividade = Atividade(
                        nome=f"{tipo.title()} {status.title()} {i+1}",
                        descricao=f"Descrição para {tipo} - {status} - {i+1}",
                        tipo_atividade=tipo,
                        data_inicio=data_inicio,
                        data_fim=data_fim,
                        hora_inicio=time(hour=random.randint(8, 18), minute=0),
                        hora_fim=time(hour=random.randint(19, 22), minute=0)
                        if i % 2 == 0
                        else None,
                        local=f"Sala {random.randint(1, 10)}" if i % 2 == 0 else "",
                        responsavel=random.choice(alunos).nome
                        if alunos and i % 2 == 0
                        else "",
                        status=status,
                        curso=random.choice(cursos) if cursos and i % 2 == 0 else None,
                    )
                    atividade.save()
                    # Turmas
                    if turmas and i % 2 == 0:
                        turmas_selecionadas = random.sample(
                            turmas, min(len(turmas), random.randint(1, 3))
                        )
                        atividade.turmas.set(turmas_selecionadas)
                    atividade.save()

        # Atividade sem curso e sem turma
        Atividade.objects.create(
            nome="Atividade Sem Curso e Turma",
            descricao="Sem curso e sem turma",
            tipo_atividade="OUTRO",
            data_inicio=timezone.now().date(),
            hora_inicio=time(hour=10, minute=0),
            status="PENDENTE",
        )

        self.stdout.write(self.style.SUCCESS("Atividades populadas com sucesso!"))
