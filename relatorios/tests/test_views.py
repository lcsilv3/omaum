from django.test import TestCase, Client
from django.urls import reverse
from alunos.models import Aluno
from datetime import date, time

class RelatorioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='Maria Oliveira',
            data_nascimento=date(1985, 5, 15),
            hora_nascimento=time(14, 30),
            email='maria@example.com',
            sexo='F',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='João Oliveira',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Pai',
            nome_segundo_contato='Ana Oliveira',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Mãe',
            tipo_sanguineo='A',
            fator_rh='+'
        )

    def test_relatorio_alunos(self):
        response = self.client.get(reverse('relatorio_alunos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Oliveira')

    def test_relatorio_alunos_pdf(self):
        response = self.client.get(reverse('relatorio_alunos_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')