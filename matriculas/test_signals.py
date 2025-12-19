"""
Testes para os signals de matrícula.

Valida que o campo grau_atual do aluno é atualizado automaticamente
quando uma matrícula é criada, atualizada ou excluída.
"""

from django.test import TestCase
from django.utils import timezone
from alunos.models import Aluno, Pais
from turmas.models import Turma
from cursos.models import Curso
from matriculas.models import Matricula


class MatriculaSignalsTestCase(TestCase):
    """Testes para os signals de matrícula."""

    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar país
        self.pais = Pais.objects.create(
            codigo="BRA", nome="Brasil", nacionalidade="Brasileiro(a)", ativo=True
        )

        # Criar aluno de teste
        self.aluno = Aluno.objects.create(
            nome="João da Silva",
            cpf="12345678901",
            email="joao@example.com",
            data_nascimento="1990-01-01",
            sexo="M",
            situacao="a",
            pais_nacionalidade=self.pais,
            grau_atual="",  # Inicialmente vazio
        )

        # Criar cursos
        self.curso1 = Curso.objects.create(
            nome="Aprendiz",
            descricao="Curso de Aprendiz",
            carga_horaria=40,
            duracao_meses=6,
            ativo=True,
        )

        self.curso2 = Curso.objects.create(
            nome="Companheiro",
            descricao="Curso de Companheiro",
            carga_horaria=60,
            duracao_meses=12,
            ativo=True,
        )

        # Criar turmas
        self.turma1 = Turma.objects.create(
            nome="Turma Aprendiz 2025",
            curso=self.curso1,
            data_inicio=timezone.now().date(),
            data_fim=timezone.now().date(),
            vagas_totais=30,
            status="A",
        )

        self.turma2 = Turma.objects.create(
            nome="Turma Companheiro 2025",
            curso=self.curso2,
            data_inicio=timezone.now().date(),
            data_fim=timezone.now().date(),
            vagas_totais=20,
            status="A",
        )

    def test_grau_atual_atualizado_ao_criar_matricula(self):
        """Testa se grau_atual é atualizado quando uma matrícula é criada."""
        # Verificar que grau_atual está vazio
        self.assertEqual(self.aluno.grau_atual, "")

        # Criar matrícula
        matricula = Matricula.objects.create(
            aluno=self.aluno,
            turma=self.turma1,
            data_matricula=timezone.now().date(),
            status='A',
            status="A",
        )

        # Recarregar aluno do banco
        self.aluno.refresh_from_db()

        # Verificar que grau_atual foi atualizado
        self.assertEqual(self.aluno.grau_atual, "Aprendiz")

    def test_grau_atual_atualizado_com_matricula_mais_recente(self):
        """Testa se grau_atual reflete a matrícula mais recente."""
        # Criar primeira matrícula
        matricula1 = Matricula.objects.create(
            aluno=self.aluno,
            turma=self.turma1,
            data_matricula=timezone.now().date(),
            status='A',
            status="A",
        )

        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.grau_atual, "Aprendiz")

        # Criar segunda matrícula (mais recente)
        from datetime import timedelta

        matricula2 = Matricula.objects.create(
            aluno=self.aluno,
            turma=self.turma2,
            data_matricula=timezone.now().date() + timedelta(days=1),
            status='A',
            status="A",
        )

        self.aluno.refresh_from_db()

        # Verificar que grau_atual foi atualizado para o curso mais recente
        self.assertEqual(self.aluno.grau_atual, "Companheiro")

    def test_grau_atual_limpo_ao_excluir_ultima_matricula(self):
        """Testa se grau_atual é limpo quando todas as matrículas são excluídas."""
        # Criar matrícula
        matricula = Matricula.objects.create(
            aluno=self.aluno,
            turma=self.turma1,
            data_matricula=timezone.now().date(),
            status='A',
            status="A",
        )

        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.grau_atual, "Aprendiz")

        # Excluir matrícula
        matricula.delete()

        self.aluno.refresh_from_db()

        # Verificar que grau_atual foi limpo
        self.assertEqual(self.aluno.grau_atual, "")

    def test_grau_atual_nao_atualizado_se_matricula_inativa(self):
        """Testa que grau_atual não é atualizado se a matrícula não está ativa."""
        # Criar matrícula inativa
        matricula = Matricula.objects.create(
            aluno=self.aluno,
            turma=self.turma1,
            data_matricula=timezone.now().date(),
            status='C',  # Inativa
            status="C",  # Cancelada
        )

        self.aluno.refresh_from_db()

        # Verificar que grau_atual permanece vazio
        self.assertEqual(self.aluno.grau_atual, "")

    def test_grau_atual_volta_para_matricula_anterior_ao_excluir(self):
        """Testa se grau_atual volta para matrícula anterior após exclusão."""
        # Criar duas matrículas
        from datetime import timedelta

        matricula1 = Matricula.objects.create(
            aluno=self.aluno,
            turma=self.turma1,
            data_matricula=timezone.now().date(),
            status='A',
            status="A",
        )

        matricula2 = Matricula.objects.create(
            aluno=self.aluno,
            turma=self.turma2,
            data_matricula=timezone.now().date() + timedelta(days=1),
            status='A',
            status="A",
        )

        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.grau_atual, "Companheiro")

        # Excluir matrícula mais recente
        matricula2.delete()

        self.aluno.refresh_from_db()

        # Verificar que voltou para o curso da primeira matrícula
        self.assertEqual(self.aluno.grau_atual, "Aprendiz")
