from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Nota
from alunos.models import Aluno
from turmas.models import Turma
from cursos.models import Curso
from atividades.models import Atividade
from decimal import Decimal


class NotaTestCase(TestCase):
    def setUp(self):
        """Configurar dados de teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        # Criar objetos relacionados
        self.curso = Curso.objects.create(
            nome="Curso Teste",
            codigo_curso="CUR001",
            descricao="Curso de teste"
        )

        self.turma = Turma.objects.create(
            nome="Turma Teste",
            curso=self.curso,
            status="ATIVA"
        )

        self.aluno = Aluno.objects.create(
            nome="Aluno Teste",
            cpf="12345678901",
            email="aluno@teste.com"
        )

        self.atividade = Atividade.objects.create(
            nome="Atividade Teste",
            tipo_atividade="AULA",
            data_inicio=timezone.now().date(),
            hora_inicio="09:00",
            status="CONFIRMADA"
        )

        # Criar uma nota de teste
        self.nota = Nota.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            valor=Decimal('8.5'),
            data_avaliacao=timezone.now().date()
        )

    def test_listar_notas(self):
        """Testar a listagem de notas"""
        response = self.client.get(reverse("notas:listar_notas"))
        self.assertEqual(response.status_code, 200)

    def test_criar_nota(self):
        """Testar a criação de uma nova nota"""
        data = {
            "aluno": self.aluno.id,
            "turma": self.turma.id,
            "atividade": self.atividade.id,
            "valor": Decimal('9.0'),
            "data_avaliacao": timezone.now().date()
        }
        response = self.client.post(reverse("notas:criar_nota"), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

    def test_editar_nota(self):
        """Testar a edição de uma nota existente"""
        url = reverse("notas:editar_nota", args=[self.nota.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_excluir_nota(self):
        """Testar a exclusão de uma nota"""
        url = reverse("notas:excluir_nota", args=[self.nota.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

    def test_detalhar_nota(self):
        """Testar a visualização de detalhes de uma nota"""
        url = reverse("notas:detalhar_nota", args=[self.nota.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_str_nota(self):
        """Testar a representação string da nota"""
        expected_str = f"{self.aluno.nome} - {self.atividade.nome}: {self.nota.valor}"
        self.assertEqual(str(self.nota), expected_str)

    def test_nota_valor(self):
        """Testar o valor da nota"""
        self.assertEqual(self.nota.valor, Decimal('8.5'))
        
        # Alterar valor
        self.nota.valor = Decimal('9.5')
        self.nota.save()
        self.assertEqual(self.nota.valor, Decimal('9.5'))

    def test_relacionamentos(self):
        """Testar os relacionamentos da nota"""
        self.assertEqual(self.nota.aluno, self.aluno)
        self.assertEqual(self.nota.turma, self.turma)
        self.assertEqual(self.nota.atividade, self.atividade)

    def test_nota_validacao(self):
        """Testar validação da nota"""
        # Notas devem estar entre 0 e 10
        with self.assertRaises(Exception):
            Nota.objects.create(
                aluno=self.aluno,
                turma=self.turma,
                atividade=self.atividade,
                valor=Decimal('11.0'),  # Valor inválido
                data_avaliacao=timezone.now().date()
            )
