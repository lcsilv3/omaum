from django.test import TestCase
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time


class IniciacaoModelTest(TestCase):
    def setUp(self):
        self.aluno = Aluno.objects.create(
            cpf="12345678901",
            nome="João Silva",
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email="joao@example.com",
            sexo="M",
            nacionalidade="Brasileira",
            naturalidade="São Paulo",
            rua="Rua Test",
            numero_imovel="123",
            cidade="São Paulo",
            estado="SP",
            bairro="Centro",
            cep="01234567",
            nome_primeiro_contato="Maria Silva",
            celular_primeiro_contato="11999999999",
            tipo_relacionamento_primeiro_contato="Mãe",
            nome_segundo_contato="José Silva",
            celular_segundo_contato="11988888888",
            tipo_relacionamento_segundo_contato="Pai",
            tipo_sanguineo="A",
            fator_rh="+",
        )

    def test_criar_iniciacao(self):
        iniciacao = Iniciacao.objects.create(
            aluno=self.aluno,
            nome_curso="Curso de Iniciação",
            data_iniciacao=date(2023, 10, 1),
        )
        self.assertEqual(iniciacao.nome_curso, "Curso de Iniciação")
        self.assertEqual(iniciacao.aluno, self.aluno)
