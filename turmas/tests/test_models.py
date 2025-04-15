from django.test import TestCase
from turmas.models import Turma
from cursos.models import Curso
from datetime import date


class TurmaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome="Curso de Teste", descricao="Descrição do curso de teste"
        )

    def test_criar_turma(self):
        turma = Turma.objects.create(
            nome="Turma de Teste",
            curso=self.curso,
            data_inicio=date(2023, 10, 1),
            data_fim=date(2023, 12, 31),
        )

        self.assertEqual(turma.nome, "Turma de Teste")
        self.assertEqual(turma.curso, self.curso)
        self.assertEqual(str(turma), "Turma de Teste - Curso de Teste")


class CargoAdministrativoTest(TestCase):
    def test_criar_cargo(self):
        cargo = CargoAdministrativo.objects.create(
            codigo_cargo="CARGO001",
            nome="Coordenador",
            descricao="Responsável pela coordenação do curso.",
        )
        self.assertEqual(cargo.nome, "Coordenador")
        self.assertEqual(cargo.codigo_cargo, "CARGO001")
