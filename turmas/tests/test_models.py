from django.test import TestCase
from turmas.models import Turma
from usuarios.models import Usuario
from cargos.models import CargoAdministrativo
from datetime import date

class TurmaModelTest(TestCase):
    def setUp(self):
        self.instrutor = Usuario.objects.create(
            cpf='12345678901',
            nome='Professor João',
            email='joao@escola.com',
            senha='senha123',
            cargo='Professor'
        )

    def test_criar_turma(self):
        turma = Turma.objects.create(
            codigo_turma='TURMA001',
            codigo_ordem_servico='OS001',
            nome_curso='Curso de Iniciação',
            cpf_instrutor=self.instrutor,
            data_aula_inaugural=date(2023, 10, 1)
        )

        self.assertEqual(turma.codigo_turma, 'TURMA001')
        self.assertEqual(turma.nome_curso, 'Curso de Iniciação')

class CargoAdministrativoTest(TestCase):
    def test_criar_cargo(self):
        cargo = CargoAdministrativo.objects.create(
            codigo_cargo='CARGO001',
            nome='Coordenador',
            descricao='Responsável pela coordenação do curso.'
        )
        self.assertEqual(cargo.nome, 'Coordenador')
        self.assertEqual(cargo.codigo_cargo, 'CARGO001')