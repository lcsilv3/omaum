from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date
from .models import Matricula
from alunos.models import Aluno
from turmas.models import Turma
from cursos.models import Curso


class MatriculaTestCase(TestCase):
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

        # Criar uma matrícula de teste
        self.matricula = Matricula.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data_matricula=timezone.now().date(),
            status="A"  # Usar 'A' conforme o modelo
        )

    def test_listar_matriculas(self):
        """Testar a listagem de matrículas"""
        response = self.client.get(reverse("matriculas:listar_matriculas"))
        self.assertEqual(response.status_code, 200)

    def test_criar_matricula(self):
        """Testar a criação de uma nova matrícula"""
        # Criar um novo aluno para a matrícula
        novo_aluno = Aluno.objects.create(
            nome="Novo Aluno",
            cpf="98765432100",
            email="novo@aluno.com",
            data_nascimento=date(1990, 1, 1)
        )
        
        data = {
            "aluno": novo_aluno.cpf,
            "turma": self.turma.id,
            "data_matricula": timezone.now().date(),
            "status": "A"  # Usar 'A' conforme o modelo
        }
        response = self.client.post(reverse("matriculas:criar_matricula"), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

    def test_editar_matricula(self):
        """Testar a edição de uma matrícula existente"""
        url = reverse("matriculas:editar_matricula", args=[self.matricula.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_excluir_matricula(self):
        """Testar a exclusão de uma matrícula"""
        url = reverse("matriculas:excluir_matricula", args=[self.matricula.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

    def test_detalhar_matricula(self):
        """Testar a visualização de detalhes de uma matrícula"""
        url = reverse("matriculas:detalhar_matricula", args=[self.matricula.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_str_matricula(self):
        """Testar a representação string da matrícula"""
        expected_str = f"{self.aluno.nome} - {self.turma.nome}"
        self.assertEqual(str(self.matricula), expected_str)

    def test_matricula_status(self):
        """Testar o status da matrícula"""
        self.assertEqual(self.matricula.status, "A")
        
        # Alterar status
        self.matricula.status = "C"
        self.matricula.save()
        self.assertEqual(self.matricula.status, "C")

    def test_relacionamentos(self):
        """Testar os relacionamentos da matrícula"""
        self.assertEqual(self.matricula.aluno, self.aluno)
        self.assertEqual(self.matricula.turma, self.turma)
        self.assertEqual(self.matricula.turma.curso, self.curso)
