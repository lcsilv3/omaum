from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date
from .models import Nota
from alunos.models import Aluno
from turmas.models import Turma
from cursos.models import Curso
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
            email="aluno@teste.com",
            data_nascimento=date(1990, 1, 1)
        )

        # Criar uma nota de teste
        self.nota = Nota.objects.create(
            aluno=self.aluno,
            curso=self.curso,
            turma=self.turma,
            tipo_avaliacao="prova",
            valor=Decimal('8.5'),
            data=timezone.now().date()
        )

    def test_listar_notas(self):
        """Testar a listagem de notas"""
        response = self.client.get(reverse("notas:listar_notas"))
        self.assertEqual(response.status_code, 200)

    def test_criar_nota(self):
        """Testar a criação de uma nova nota"""
        data = {
            "aluno": self.aluno.id,
            "curso": self.curso.id,
            "turma": self.turma.id,
            "tipo_avaliacao": "trabalho",
            "valor": Decimal('9.0'),
            "data": timezone.now().date()
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
        expected_str = f"Nota de {self.aluno.nome} em {self.curso.nome} (Prova): {self.nota.valor}"
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
        self.assertEqual(self.nota.curso, self.curso)

    def test_nota_validacao(self):
        """Testar validação da nota"""
        # Notas devem estar entre 0 e 10
        with self.assertRaises(Exception):
            Nota.objects.create(
                aluno=self.aluno,
                curso=self.curso,
                turma=self.turma,
                tipo_avaliacao="exame",
                valor=Decimal('11.0'),  # Valor inválido
                data=timezone.now().date()
            )
