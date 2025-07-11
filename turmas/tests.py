from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Turma
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
            codigo_curso="CUR001",
            descricao="Curso de teste"
        )

        # Criar uma turma de teste
        self.turma = Turma.objects.create(
            nome="Turma Teste",
            curso=self.curso,
            status="A",  # Ativa
            data_inicio=timezone.now().date(),
            vagas_totais=30,
            vagas_ocupadas=0
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
            "data_inicio": timezone.now().date(),
            "vagas_totais": 25,
            "vagas_ocupadas": 0
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
        vagas_disponiveis = self.turma.vagas_totais - self.turma.vagas_ocupadas
        self.assertEqual(vagas_disponiveis, 30)
        
        # Ocupar algumas vagas
        self.turma.vagas_ocupadas = 10
        self.turma.save()
        vagas_disponiveis = self.turma.vagas_totais - self.turma.vagas_ocupadas
        self.assertEqual(vagas_disponiveis, 20)

    def test_relacionamentos(self):
        """Testar os relacionamentos da turma"""
        self.assertEqual(self.turma.curso, self.curso)
        self.assertEqual(self.turma.curso.nome, "Curso Teste")

    def test_turma_validacao(self):
        """Testar validação da turma"""
        # Vagas ocupadas não podem ser maiores que vagas totais
        with self.assertRaises(Exception):
            Turma.objects.create(
                nome="Turma Inválida",
                curso=self.curso,
                status="A",
                data_inicio=timezone.now().date(),
                vagas_totais=10,
                vagas_ocupadas=15  # Mais que o total
            )

    def test_turma_inativa(self):
        """Testar turma inativa"""
        turma_inativa = Turma.objects.create(
            nome="Turma Inativa",
            curso=self.curso,
            status="I",  # Inativa
            data_inicio=timezone.now().date(),
            vagas_totais=20,
            vagas_ocupadas=0
        )
        self.assertEqual(turma_inativa.status, "I")

    def test_redirecionamento_apos_acao(self):
        """Testar redirecionamentos após ações CRUD"""
        # Após criar turma, deve redirecionar para listagem
        data = {
            "nome": "Turma Redirecionamento",
            "curso": self.curso.id,
            "status": "A",
            "data_inicio": timezone.now().date(),
            "vagas_totais": 15,
            "vagas_ocupadas": 0
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
