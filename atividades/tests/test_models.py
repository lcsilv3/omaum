from django.test import TestCase
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from cursos.models import Curso
from alunos.services import criar_aluno
from datetime import date, timedelta
from django.utils import timezone


class AtividadeAcademicaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome="Curso de Teste", descricao="Descrição do curso de teste"
        )
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31),
        )

    def test_criar_atividade(self):
        data_inicio = timezone.now()
        data_fim = data_inicio + timedelta(days=7)

        atividade = AtividadeAcademica.objects.create(
            nome="Aula de Matemática",
            descricao="Aula introdutória sobre álgebra.",
            data_inicio=data_inicio,
            data_fim=data_fim,
            turma=self.turma,
        )

        self.assertEqual(atividade.nome, "Aula de Matemática")
        self.assertEqual(atividade.descricao, "Aula introdutória sobre álgebra.")
        self.assertEqual(atividade.data_inicio, data_inicio)
        self.assertEqual(atividade.data_fim, data_fim)
        self.assertEqual(atividade.turma, self.turma)
        self.assertEqual(str(atividade), "Aula de Matemática")


class AtividadeRitualisticaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome="Curso de Teste", descricao="Descrição do curso de teste"
        )
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31),
        )
        self.aluno1 = criar_aluno(
            {
                "nome": "Aluno 1",
                "email": "aluno1@teste.com",
                "cpf": "11111111111",
                "data_nascimento": "2000-01-01",
            }
        )
        self.aluno2 = criar_aluno(
            {
                "nome": "Aluno 2",
                "email": "aluno2@teste.com",
                "cpf": "22222222222",
                "data_nascimento": "2000-01-02",
            }
        )

    def test_criar_atividade_ritualistica(self):
        data_inicio = timezone.now()
        data_fim = data_inicio + timedelta(days=7)

        atividade = AtividadeRitualistica.objects.create(
            nome="Ritual de Iniciação",
            descricao="Ritual para novos membros",
            data_inicio=data_inicio,
            data_fim=data_fim,
            turma=self.turma,
        )
        atividade.alunos.add(self.aluno1, self.aluno2)

        self.assertEqual(atividade.nome, "Ritual de Iniciação")
        self.assertEqual(atividade.descricao, "Ritual para novos membros")
        self.assertEqual(atividade.data_inicio, data_inicio)
        self.assertEqual(atividade.data_fim, data_fim)
        self.assertEqual(atividade.turma, self.turma)
        self.assertEqual(atividade.alunos.count(), 2)
        self.assertTrue(self.aluno1 in atividade.alunos.all())
        self.assertTrue(self.aluno2 in atividade.alunos.all())
        self.assertEqual(str(atividade), "Ritual de Iniciação")
