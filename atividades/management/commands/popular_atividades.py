from django.core.management.base import BaseCommand
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from cursos.models import Curso
from turmas.models import Turma
from alunos.models import Aluno
from django.utils import timezone
import random
from datetime import timedelta, time

class Command(BaseCommand):
    help = 'Popula o banco de dados com atividades acadêmicas e ritualísticas para todos os casos possíveis.'

    def handle(self, *args, **options):
        tipos = [c[0] for c in AtividadeAcademica.TIPO_CHOICES]
        status_acad = [c[0] for c in AtividadeAcademica.STATUS_CHOICES]
        status_rit = [c[0] for c in AtividadeRitualistica.STATUS_CHOICES]

        cursos = list(Curso.objects.all())
        turmas = list(Turma.objects.all())
        alunos = list(Aluno.objects.all())

        # Limpa atividades antigas para evitar duplicidade
        AtividadeAcademica.objects.all().delete()
        AtividadeRitualistica.objects.all().delete()

        # Atividades Acadêmicas
        for tipo in tipos:
            for status in status_acad:
                for i in range(2):  # Cria 2 para cada combinação
                    atividade = AtividadeAcademica(
                        nome=f"{tipo.title()} {status.title()} {i+1}",
                        descricao=f"Descrição para {tipo} - {status} - {i+1}",
                        tipo_atividade=tipo,
                        data_inicio=timezone.now().date() + timedelta(days=random.randint(-10, 10)),
                        data_fim=timezone.now().date() + timedelta(days=random.randint(11, 20)) if i % 2 == 0 else None,
                        hora_inicio=time(hour=random.randint(8, 18), minute=0),
                        hora_fim=time(hour=random.randint(19, 22), minute=0) if i % 2 == 0 else None,
                        local=f"Sala {random.randint(1, 10)}" if i % 2 == 0 else "",
                        responsavel=random.choice(alunos).nome if alunos and i % 2 == 0 else "",
                        status=status,
                        curso=random.choice(cursos) if cursos and i % 2 == 0 else None,
                    )
                    atividade.save()
                    # Turmas
                    if turmas and i % 2 == 0:
                        atividade.turmas.set(random.sample(turmas, min(len(turmas), random.randint(1, 3))))
                    atividade.save()

        # Atividades Acadêmicas sem curso e sem turma
        AtividadeAcademica.objects.create(
            nome="Atividade Sem Curso e Turma",
            descricao="Sem curso e sem turma",
            tipo_atividade="OUTRO",
            data_inicio=timezone.now().date(),
            hora_inicio=time(hour=10, minute=0),
            status="PENDENTE"
        )

        # Atividades Ritualísticas
        for status in status_rit:
            for i in range(2):
                atividade = AtividadeRitualistica(
                    nome=f"Ritual {status.title()} {i+1}",
                    descricao=f"Descrição para Ritual - {status} - {i+1}",
                    data=timezone.now().date() + timedelta(days=random.randint(-10, 10)),
                    hora_inicio=time(hour=random.randint(8, 18), minute=0),
                    hora_fim=time(hour=random.randint(19, 22), minute=0) if i % 2 == 0 else None,
                    local=f"Templo {random.randint(1, 5)}" if i % 2 == 0 else "",
                    responsavel=random.choice(alunos).nome if alunos and i % 2 == 0 else "",
                    status=status,
                )
                atividade.save()
                # Participantes
                if alunos and i % 2 == 0:
                    atividade.participantes.set(random.sample(alunos, min(len(alunos), random.randint(1, 5))))
                atividade.save()

        # Atividade Ritualística sem participantes
        AtividadeRitualistica.objects.create(
            nome="Ritual Sem Participantes",
            descricao="Sem participantes",
            data=timezone.now().date(),
            hora_inicio=time(hour=15, minute=0),
            status="PENDENTE"
        )

        self.stdout.write(self.style.SUCCESS('Atividades acadêmicas e ritualísticas populadas com sucesso!'))