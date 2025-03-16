from django.test import TestCase, Client
from django.urls import reverse
from turmas.models import Turma
from ..usuarios.models import Usuario  # Ensure this path is correct
from datetime import date

class TurmaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.instrutor = Usuario.objects.create(
            cpf='12345678901',
            nome='Professor João',
            email='joao@escola.com',
            senha='senha123',
            cargo='Professor'
        )
        self.turma = Turma.objects.create(
            codigo_turma='TURMA001',
            codigo_ordem_servico='OS001',
            nome_curso='Curso de Iniciação',
            cpf_instrutor=self.instrutor,
            data_aula_inaugural=date(2023, 10, 1)
        )

    def test_listar_turmas(self):
        response = self.client.get(reverse('listar_turmas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TURMA001')
        self.assertContains(response, 'Curso de Iniciação')

    def test_detalhe_turma(self):
        response = self.client.get(reverse('detalhe_turma', args=[self.turma.codigo_turma]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.turma.nome_curso)
