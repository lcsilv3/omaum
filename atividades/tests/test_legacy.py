from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Atividade
from datetime import date, time


class AtividadeTestCase(TestCase):
    def setUp(self):
        """Configurar dados de teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        # Criar uma atividade de teste
        self.atividade = Atividade.objects.create(
            nome="Atividade Teste",
            descricao="Descrição da atividade teste",
            tipo_atividade="AULA",
            data_inicio=date.today(),
            hora_inicio=time(9, 0),
            local="Sala 1",
            responsavel="Professor Teste",
            status="CONFIRMADA",
        )

    def test_listar_atividades(self):
        """Testar a listagem de atividades"""
        response = self.client.get(reverse("atividades:listar_atividades"))
        self.assertEqual(response.status_code, 200)

    def test_criar_atividade(self):
        """Testar a criação de uma nova atividade"""
        data = {
            "nome": "Nova Atividade",
            "descricao": "Descrição da nova atividade",
            "tipo_atividade": "PALESTRA",
            "data_inicio": date.today(),
            "hora_inicio": time(14, 0),
            "local": "Auditório",
            "responsavel": "Palestrante",
            "status": "PENDENTE",
        }
        response = self.client.post(reverse("atividades:criar_atividade"), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

    def test_editar_atividade(self):
        """Testar a edição de uma atividade existente"""
        url = reverse("atividades:editar_atividade", args=[self.atividade.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_excluir_atividade(self):
        """Testar a exclusão de uma atividade"""
        url = reverse("atividades:excluir_atividade", args=[self.atividade.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

    def test_detalhar_atividade(self):
        """Testar a visualização de detalhes de uma atividade"""
        url = reverse("atividades:detalhar_atividade", args=[self.atividade.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_str_atividade(self):
        """Testar a representação string da atividade"""
        self.assertEqual(str(self.atividade), "Atividade Teste")

    def test_atividade_choices(self):
        """Testar os choices da atividade"""
        self.assertEqual(self.atividade.tipo_atividade, "AULA")
        self.assertEqual(self.atividade.status, "CONFIRMADA")


class PresencaAtividadeTestCase(TestCase):
    def setUp(self):
        """Configurar dados de teste para presença"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        # Criar uma atividade de teste
        self.atividade = Atividade.objects.create(
            nome="Atividade Teste",
            tipo_atividade="AULA",
            data_inicio=date.today(),
            hora_inicio=time(9, 0),
            status="CONFIRMADA",
        )

    def test_str_presenca(self):
        """Testar a representação string da presença"""
        # Nota: Este teste é limitado pois requer modelos de aluno e turma
        # que são importados dinamicamente
        pass
