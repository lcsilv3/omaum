from django.test import TestCase
from alunos.models import Aluno
from datetime import date, time

class AlunoModelTest(TestCase):
    def test_criar_aluno(self):
        aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Test',
            data_nascimento=date(1995, 5, 15),
            hora_nascimento=time(14, 30),
            email='joao@test.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Test',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Test',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )
        self.assertEqual(aluno.nome, 'João Test')
