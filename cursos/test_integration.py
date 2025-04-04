from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from cursos.models import Curso

class CursoIntegrationTest(TestCase):
    """Testes de integração para o aplicativo cursos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        # Criar um usuário para testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        # Fazer login com o usuário de teste
        self.client.login(username='testuser', password='testpassword')
    
    def test_fluxo_completo_curso(self):
        """Teste do fluxo completo: criar, visualizar, editar e excluir um curso"""
        
        # 1. Criar um novo curso
        response_criar = self.client.post(
            reverse('cursos:criar_curso'),
            {
                'codigo_curso': 401,
                'nome': 'Curso de Integração',
                'descricao': 'Descrição do curso de integração',
                'duracao': 8
            }
        )
        self.assertEqual(response_criar.status_code, 302)  # Redirecionamento após sucesso
        self.assertTrue(Curso.objects.filter(codigo_curso=401).exists())
