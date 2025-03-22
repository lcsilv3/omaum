from django.test import TestCase
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from cursos.models import Curso
from datetime import date

class AtividadeAcademicaModelTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        
    def test_criar_atividade(self):
        atividade = AtividadeAcademica.objects.create(
            nome='Aula de Matemática',
            descricao='Aula introdutória sobre álgebra.',
            data_inicio=date(2023, 2, 1),
            data_fim=date(2023, 2, 28),
            turma=self.turma
        )
        
        self.assertEqual(atividade.nome, 'Aula de Matemática')
        self.assertEqual(atividade.descricao, 'Aula introdutória sobre álgebra.')
        self.assertEqual(str(atividade), 'Aula de Matemática')
