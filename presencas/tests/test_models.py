from django.test import TestCase
from presencas.models import PresencaAcademica
from turmas.models import Turma
from alunos.models import Aluno
from datetime import date, time

class PresencaAcademicaModelTest(TestCase):
    def setUp(self):
        self.turma = Turma.objects.create(codigo_turma='TURMA001')
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email='joao@example.com',
            sexo='M',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='Maria Silva',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Mãe',
            nome_segundo_contato='José Silva',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Pai',
            tipo_sanguineo='A',
            fator_rh='+'
        )

    def test_criar_presenca(self):
        presenca = PresencaAcademica.objects.create(
            turma=self.turma,
            aluno=self.aluno,
            data=date(2023, 10, 1),
            presente=True
        )
        self.assertEqual(presenca.presente, True)
        self.assertEqual(presenca.aluno, self.aluno)
