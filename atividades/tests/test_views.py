from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import AtividadeAcademica, AtividadeRitualistica
from turmas.models import Turma
from cursos.models import Curso
from datetime import date

class AtividadeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            codigo_curso='CUR01',
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31)
        )
        self.atividade = AtividadeAcademica.objects.create(
            nome='Aula de Matemática',
            descricao='Aula introdutória sobre álgebra.',
            data_inicio=date(2023, 2, 1),
            data_fim=date(2023, 2, 28),
            turma=self.turma
        )

    def test_listar_atividades(self):
        response = self.client.get(reverse('atividades:academica_lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aula de Matemática')

    def test_criar_atividade(self):
        response = self.client.get(reverse('atividades:academica_criar'))
        self.assertEqual(response.status_code, 200)
