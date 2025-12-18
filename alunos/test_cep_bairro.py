"""
Testes para busca de CEP e criação de bairro.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from alunos.models import Estado, Cidade, Bairro
import json


class CepBairroTestCase(TestCase):
    """Testes para funcionalidade de CEP e criação de bairro."""

    def setUp(self):
        """Configura dados de teste."""
        self.client = Client()
        
        # Cria usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Cria estado e cidade de teste
        self.estado_ma = Estado.objects.create(
            codigo='MA',
            nome='Maranhão',
            regiao='Nordeste'
        )
        
        self.cidade_slz = Cidade.objects.create(
            nome='São Luís',
            estado=self.estado_ma,
            codigo_ibge='2111300'
        )
        
        # Cria um bairro de teste
        self.bairro_centro = Bairro.objects.create(
            nome='Centro',
            cidade=self.cidade_slz
        )

    def test_01_buscar_cep_autenticado(self):
        """Testa busca de CEP com usuário autenticado."""
        # Teste com CEP de São Luís - MA (65000-000)
        response = self.client.get('/alunos/api/localidade/cep/65000-000/')
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Pode não ter sucesso se a API externa falhar, mas deve retornar JSON válido
        self.assertIn('success', data)

    def test_02_buscar_cep_nao_autenticado(self):
        """Testa que busca de CEP requer autenticação."""
        self.client.logout()
        response = self.client.get('/alunos/api/localidade/cep/65000-000/')
        
        # Deve redirecionar para login ou retornar 403
        self.assertIn(response.status_code, [302, 403])

    def test_03_buscar_cep_invalido(self):
        """Testa busca com CEP inválido."""
        response = self.client.get('/alunos/api/localidade/cep/123/')
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('inválido', data['error'].lower())

    def test_04_criar_bairro_novo(self):
        """Testa criação de novo bairro."""
        response = self.client.post(
            '/alunos/api/localidade/bairros/criar/',
            data=json.dumps({
                'nome': 'Bairro Novo',
                'cidade_id': self.cidade_slz.id
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertTrue(data['success'])
        self.assertEqual(data['nome'], 'Bairro Novo')
        self.assertFalse(data['ja_existia'])
        
        # Verifica que foi criado no banco
        bairro = Bairro.objects.get(id=data['bairro_id'])
        self.assertEqual(bairro.nome, 'Bairro Novo')
        self.assertEqual(bairro.cidade, self.cidade_slz)

    def test_05_criar_bairro_existente(self):
        """Testa criação de bairro que já existe."""
        response = self.client.post(
            '/alunos/api/localidade/bairros/criar/',
            data=json.dumps({
                'nome': 'Centro',  # Já existe
                'cidade_id': self.cidade_slz.id
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertTrue(data['success'])
        self.assertEqual(data['bairro_id'], self.bairro_centro.id)
        self.assertTrue(data['ja_existia'])

    def test_06_criar_bairro_sem_nome(self):
        """Testa criação de bairro sem nome."""
        response = self.client.post(
            '/alunos/api/localidade/bairros/criar/',
            data=json.dumps({
                'nome': '',
                'cidade_id': self.cidade_slz.id
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('obrigatório', data['error'].lower())

    def test_07_criar_bairro_sem_cidade(self):
        """Testa criação de bairro sem cidade."""
        response = self.client.post(
            '/alunos/api/localidade/bairros/criar/',
            data=json.dumps({
                'nome': 'Bairro Teste',
                'cidade_id': None
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])

    def test_08_criar_bairro_cidade_inexistente(self):
        """Testa criação de bairro com cidade inexistente."""
        response = self.client.post(
            '/alunos/api/localidade/bairros/criar/',
            data=json.dumps({
                'nome': 'Bairro Teste',
                'cidade_id': 99999
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('não encontrada', data['error'].lower())
