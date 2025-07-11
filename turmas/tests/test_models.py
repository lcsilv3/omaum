from django.test import TestCase
from turmas.models import Turma
from cursos.models import Curso


class TurmaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome="Curso de Teste", descricao="Descrição do curso de teste"
        )

    def test_criar_turma(self):
        turma = Turma.objects.create(
            nome="Turma de Teste",
            curso=self.curso,
        )

        self.assertEqual(turma.nome, "Turma de Teste")
        self.assertEqual(turma.curso, self.curso)
        self.assertEqual(str(turma), "Turma de Teste - Curso de Teste")
