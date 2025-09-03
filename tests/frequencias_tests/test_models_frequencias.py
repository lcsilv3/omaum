import pytest
from django.test import TestCase
from frequencias.models import FrequenciaMensal, Carencia
from alunos.services import criar_aluno
from turmas.models import Turma


@pytest.mark.django_db
class FrequenciaMensalModelTestCase(TestCase):
    """Testes unitários para o modelo FrequenciaMensal."""

    def setUp(self):
        from cursos.models import Curso

        self.curso = Curso.objects.create(nome="Curso Teste")
        self.turma = Turma.objects.create(
            nome="Turma Teste", curso=self.curso, status="A"
        )
        self.frequencia_mensal = FrequenciaMensal.objects.create(
            turma=self.turma, mes=1, ano=2024, percentual_minimo=75
        )

    def test_criacao_frequencia_mensal(self):
        self.assertEqual(self.frequencia_mensal.turma, self.turma)
        self.assertEqual(self.frequencia_mensal.mes, 1)
        self.assertEqual(self.frequencia_mensal.ano, 2024)
        self.assertEqual(self.frequencia_mensal.percentual_minimo, 75)

    def test_str(self):
        representacao = str(self.frequencia_mensal)
        self.assertIn("Turma Teste", representacao)
        self.assertIn("Janeiro", representacao)
        self.assertIn("2024", representacao)


@pytest.mark.django_db
class CarenciaModelTestCase(TestCase):
    """Testes unitários para o modelo Carencia."""

    def setUp(self):
        from cursos.models import Curso

        self.curso = Curso.objects.create(nome="Curso Teste")
        self.turma = Turma.objects.create(
            nome="Turma Teste", curso=self.curso, status="A"
        )
        self.frequencia_mensal = FrequenciaMensal.objects.create(
            turma=self.turma, mes=2, ano=2024, percentual_minimo=80
        )
        self.aluno = criar_aluno(
            {
                "cpf": "98765432100",
                "nome": "Aluno Carencia",
                "email": "carencia@teste.com",
                "data_nascimento": "1995-05-05",
            }
        )
        self.carencia = Carencia.objects.create(
            frequencia_mensal=self.frequencia_mensal,
            aluno=self.aluno,
            total_presencas=8,
            total_atividades=10,
            percentual_presenca=80.0,
            numero_carencias=2,
            liberado=True,
            status="RESOLVIDO",
            observacoes="Aluno liberado por bom desempenho.",
        )

    def test_criacao_carencia(self):
        self.assertEqual(self.carencia.frequencia_mensal, self.frequencia_mensal)
        self.assertEqual(self.carencia.aluno, self.aluno)
        self.assertEqual(self.carencia.total_presencas, 8)
        self.assertEqual(self.carencia.total_atividades, 10)
        self.assertEqual(float(self.carencia.percentual_presenca), 80.0)
        self.assertEqual(self.carencia.numero_carencias, 2)
        self.assertTrue(self.carencia.liberado)
        self.assertEqual(self.carencia.status, "RESOLVIDO")
        self.assertEqual(
            self.carencia.observacoes, "Aluno liberado por bom desempenho."
        )

    def test_str(self):
        representacao = str(self.carencia)
        self.assertIn("Aluno Carencia", representacao)
        self.assertIn("Turma Teste", representacao)
