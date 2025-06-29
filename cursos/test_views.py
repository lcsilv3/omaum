from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from cursos.models import Curso


class CursoViewTest(TestCase):
    """Testes para as views do aplicativo cursos"""

    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        # Criar um usuário para testes
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        # Fazer login com o usuário de teste
        self.client.login(username="testuser", password="testpassword")
        # Criar um curso para testes
        self.curso = Curso.objects.create(
            nome="Curso de Teste",
            descricao="Descrição do curso de teste",
            duracao=6,
        )

    def test_listar_cursos_view(self):
        """Teste da view de listagem de cursos"""
        response = self.client.get(reverse("cursos:listar_cursos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cursos/listar_cursos.html")
        self.assertContains(response, "Curso de Teste")

    def test_criar_curso_view_get(self):
        """Teste da view de criação de curso (GET)"""
        response = self.client.get(reverse("cursos:criar_curso"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cursos/criar_curso.html")

    def test_detalhar_curso_view(self):
        """Teste da view de detalhes de curso"""
        response = self.client.get(
            reverse("cursos:detalhar_curso", args=[self.curso.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cursos/detalhar_curso.html")
        self.assertContains(response, "Curso de Teste")
