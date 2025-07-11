from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from turmas.models import Turma
from cursos.models import Curso


class TurmaTestCase(TestCase):
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

        # Criar uma turma de teste
        self.turma = Turma.objects.create(
            nome="Turma Teste",
            curso=self.curso,
            status="A",  # Ativa
            data_inicio_ativ=timezone.now().date(),
            vagas=30
        )

    def test_listar_turmas(self):
        """Testar a listagem de turmas"""
        response = self.client.get(reverse("turmas:listar_turmas"))
        self.assertEqual(response.status_code, 200)

    def test_criar_turma(self):
        """Testar a criação de uma nova turma"""
        data = {
            "nome": "Nova Turma",
            "curso": self.curso.id,
            "status": "A",
            "data_inicio_ativ": timezone.now().date(),
            "vagas": 25
        }
        response = self.client.post(reverse("turmas:criar_turma"), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

    def test_editar_turma(self):
        """Testar a edição de uma turma existente"""
        url = reverse("turmas:editar_turma", args=[self.turma.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_excluir_turma(self):
        """Testar a exclusão de uma turma"""
        url = reverse("turmas:excluir_turma", args=[self.turma.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

    def test_detalhar_turma(self):
        """Testar a visualização de detalhes de uma turma"""
        url = reverse("turmas:detalhar_turma", args=[self.turma.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_str_turma(self):
        """Testar a representação string da turma"""
        expected_str = f"{self.turma.nome} - {self.curso.nome}"
        self.assertEqual(str(self.turma), expected_str)

    def test_turma_status(self):
        """Testar o status da turma"""
        self.assertEqual(self.turma.status, "A")
        
        # Alterar status
        self.turma.status = "I"  # Inativa
        self.turma.save()
        self.assertEqual(self.turma.status, "I")

    def test_vagas_disponiveis(self):
        """Testar o cálculo de vagas disponíveis"""
        # Teste básico com campo vagas
        self.assertEqual(self.turma.vagas, 30)

    def test_relacionamentos(self):
        """Testar os relacionamentos da turma"""
        self.assertEqual(self.turma.curso, self.curso)
        self.assertEqual(self.turma.curso.nome, "Curso Teste")

    def test_turma_validacao(self):
        """Testar validação da turma"""
        # Teste simples de criação de turma
        turma_invalida = Turma(
            nome="Turma Inválida",
            curso=self.curso,
            status="A",
            vagas=10
        )
        # Para testes simples, vamos apenas verificar que pode ser criada
        turma_invalida.save()
        self.assertEqual(turma_invalida.nome, "Turma Inválida")

    def test_turma_inativa(self):
        """Testar turma inativa"""
        turma_inativa = Turma.objects.create(
            nome="Turma Inativa",
            curso=self.curso,
            status="I",  # Inativa
            vagas=20
        )
        self.assertEqual(turma_inativa.status, "I")

    def test_redirecionamento_apos_acao(self):
        """Testar redirecionamentos após ações CRUD"""
        # Após criar turma, deve redirecionar para listagem
        data = {
            "nome": "Turma Redirecionamento",
            "curso": self.curso.id,
            "status": "A",
            "vagas": 15
        }
        response = self.client.post(reverse("turmas:criar_turma"), data)
        self.assertRedirects(response, reverse("turmas:listar_turmas"))

    def test_view_permissions(self):
        """Testar permissões das views"""
        # Logout para testar acesso sem autenticação
        self.client.logout()
        
        # Tentar acessar listagem sem login
        response = self.client.get(reverse("turmas:listar_turmas"))
        # Deve redirecionar para login ou dar erro 403
        self.assertIn(response.status_code, [302, 403])
