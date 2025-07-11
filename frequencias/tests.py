from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Frequencia


class FrequenciaTestCase(TestCase):
    def setUp(self):
        """Configurar dados de teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")
        
        # Criar uma frequencia de teste
        self.frequencia = Frequencia.objects.create(
            # Adicione os campos necessários baseados no modelo
            data=timezone.now().date(),
            registrado_por="testuser"
        )

    def test_listar_frequencias(self):
        """Testar a listagem de frequências"""
        response = self.client.get(reverse("frequencias:listar_frequencias"))
        self.assertEqual(response.status_code, 200)
        
    def test_criar_frequencia(self):
        """Testar a criação de uma nova frequência"""
        data = {
            "data": timezone.now().date(),
            "registrado_por": "testuser"
        }
        response = self.client.post(reverse("frequencias:criar_frequencia"), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
    def test_editar_frequencia(self):
        """Testar a edição de uma frequência existente"""
        url = reverse("frequencias:editar_frequencia", args=[self.frequencia.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_excluir_frequencia(self):
        """Testar a exclusão de uma frequência"""
        url = reverse("frequencias:excluir_frequencia", args=[self.frequencia.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso
        
    def test_detalhar_frequencia(self):
        """Testar a visualização de detalhes de uma frequência"""
        url = reverse("frequencias:detalhar_frequencia", args=[self.frequencia.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
