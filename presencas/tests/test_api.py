"""
Testes para API endpoints do sistema de presenças.
"""

import json
from datetime import date, datetime
from decimal import Decimal

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from ..models import PresencaDetalhada, ConfiguracaoPresenca
from atividades.models import Atividade
from turmas.models import Turma
from alunos.models import Aluno


class PresencasAPITestCase(TestCase):
    """Classe base para testes da API de presenças."""
    
    def setUp(self):
        """Configuração inicial para todos os testes."""
        self.client = Client()
        
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Criar dados de teste
        self.turma = Turma.objects.create(
            nome='Turma Teste',
            perc_carencia=75.0
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            tipo='Acadêmica'
        )
        
        self.aluno = Aluno.objects.create(
            nome='Aluno Teste',
            cpf='12345678901',
            email='aluno@test.com',
            turma=self.turma
        )
        
        # Login do usuário
        self.client.login(username='testuser', password='testpass123')
    
    def tearDown(self):
        """Limpeza após os testes."""
        self.client.logout()


class TestAtualizarPresencasAPI(PresencasAPITestCase):
    """Testes para endpoint de atualização de presenças."""
    
    def test_atualizar_presencas_sucesso(self):
        """Testa atualização bem-sucedida de presenças."""
        url = reverse('presencas:presencas_api:atualizar_presencas')
        
        data = {
            'presencas': [
                {
                    'aluno_id': self.aluno.id,
                    'turma_id': self.turma.id,
                    'atividade_id': self.atividade.id,
                    'periodo': '2024-01-01',
                    'convocacoes': 10,
                    'presencas': 8,
                    'faltas': 2,
                    'voluntario_extra': 1,
                    'voluntario_simples': 2
                }
            ]
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['data']['presencas_criadas'], 1)
        
        # Verificar se foi criada no banco
        presenca = PresencaDetalhada.objects.get(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade
        )
        self.assertEqual(presenca.convocacoes, 10)
        self.assertEqual(presenca.presencas, 8)
        self.assertEqual(presenca.faltas, 2)
    
    def test_atualizar_presencas_dados_invalidos(self):
        """Testa atualização com dados inválidos."""
        url = reverse('presencas:presencas_api:atualizar_presencas')
        
        data = {
            'presencas': [
                {
                    'aluno_id': self.aluno.id,
                    'turma_id': self.turma.id,
                    'atividade_id': self.atividade.id,
                    'periodo': '2024-01-01',
                    'convocacoes': 5,
                    'presencas': 8,  # Maior que convocações
                    'faltas': 2
                }
            ]
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
    
    def test_atualizar_presencas_sem_login(self):
        """Testa acesso sem login."""
        self.client.logout()
        
        url = reverse('presencas:presencas_api:atualizar_presencas')
        data = {'presencas': []}
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect para login


class TestCalcularEstatisticasAPI(PresencasAPITestCase):
    """Testes para endpoint de cálculo de estatísticas."""
    
    def setUp(self):
        """Configuração específica para testes de estatísticas."""
        super().setUp()
        
        # Criar presença detalhada de teste
        self.presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=8,
            faltas=2,
            voluntario_extra=1,
            voluntario_simples=2,
            registrado_por=self.user.username
        )
    
    def test_calcular_estatisticas_gerais(self):
        """Testa cálculo de estatísticas gerais."""
        url = reverse('presencas:presencas_api:calcular_estatisticas')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        stats = response_data['data']['estatisticas_gerais']
        self.assertEqual(stats['total_registros'], 1)
        self.assertEqual(stats['total_convocacoes'], 10)
        self.assertEqual(stats['total_presencas_efetivas'], 8)
        self.assertEqual(stats['total_faltas'], 2)
    
    def test_calcular_estatisticas_por_turma(self):
        """Testa cálculo de estatísticas filtradas por turma."""
        url = reverse('presencas:presencas_api:calcular_estatisticas')
        
        response = self.client.get(url, {'turma_id': self.turma.id})
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        # Deve retornar dados da turma específica
        stats = response_data['data']['estatisticas_gerais']
        self.assertEqual(stats['total_registros'], 1)


class TestBuscarAlunosAPI(PresencasAPITestCase):
    """Testes para endpoint de busca de alunos."""
    
    def test_buscar_alunos_por_nome(self):
        """Testa busca de alunos por nome."""
        url = reverse('presencas:presencas_api:buscar_alunos')
        
        response = self.client.get(url, {'q': 'Aluno'})
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        alunos = response_data['data']['alunos']
        self.assertEqual(len(alunos), 1)
        self.assertEqual(alunos[0]['nome'], 'Aluno Teste')
    
    def test_buscar_alunos_por_cpf(self):
        """Testa busca de alunos por CPF."""
        url = reverse('presencas:presencas_api:buscar_alunos')
        
        response = self.client.get(url, {'q': '12345'})
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        alunos = response_data['data']['alunos']
        self.assertEqual(len(alunos), 1)
        self.assertEqual(alunos[0]['cpf'], '12345678901')
    
    def test_buscar_alunos_sem_termo(self):
        """Testa busca sem termo."""
        url = reverse('presencas:presencas_api:buscar_alunos')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 400)
        
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])


class TestValidarDadosAPI(PresencasAPITestCase):
    """Testes para endpoint de validação de dados."""
    
    def test_validar_dados_validos(self):
        """Testa validação de dados válidos."""
        url = reverse('presencas:presencas_api:validar_dados')
        
        data = {
            'aluno_id': self.aluno.id,
            'turma_id': self.turma.id,
            'atividade_id': self.atividade.id,
            'periodo': '2024-01-01',
            'convocacoes': 10,
            'presencas': 8,
            'faltas': 2
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertTrue(response_data['data']['valido'])
    
    def test_validar_dados_invalidos(self):
        """Testa validação de dados inválidos."""
        url = reverse('presencas:presencas_api:validar_dados')
        
        data = {
            'aluno_id': self.aluno.id,
            'turma_id': self.turma.id,
            'atividade_id': self.atividade.id,
            'periodo': '2024-01-15',  # Não é primeiro dia do mês
            'convocacoes': 5,
            'presencas': 8,  # Maior que convocações
            'faltas': 2
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('errors', response_data)


class TestAtividadesTurmaAPI(PresencasAPITestCase):
    """Testes para endpoint de atividades por turma."""
    
    def test_listar_atividades_turma(self):
        """Testa listagem de atividades por turma."""
        url = reverse('presencas:presencas_api:atividades_turma')
        
        response = self.client.get(url, {'turma_id': self.turma.id})
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        turma_data = response_data['data']['turma']
        self.assertEqual(turma_data['nome'], 'Turma Teste')
        
        atividades = response_data['data']['atividades']
        self.assertGreaterEqual(len(atividades), 1)
    
    def test_listar_atividades_turma_inexistente(self):
        """Testa listagem de atividades para turma inexistente."""
        url = reverse('presencas:presencas_api:atividades_turma')
        
        response = self.client.get(url, {'turma_id': 99999})
        
        self.assertEqual(response.status_code, 400)
        
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
    
    def test_listar_atividades_sem_turma(self):
        """Testa listagem sem especificar turma."""
        url = reverse('presencas:presencas_api:atividades_turma')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 400)
        
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])


class TestConfiguracaoPresencaAPI(PresencasAPITestCase):
    """Testes para endpoint de configuração de presença."""
    
    def setUp(self):
        """Configuração específica para testes de configuração."""
        super().setUp()
        
        # Criar configuração de teste
        self.configuracao = ConfiguracaoPresenca.objects.create(
            turma=self.turma,
            atividade=self.atividade,
            limite_carencia_0_25=0,
            limite_carencia_26_50=1,
            limite_carencia_51_75=2,
            limite_carencia_76_100=3,
            obrigatoria=True,
            peso_calculo=Decimal('1.00'),
            registrado_por=self.user.username
        )
    
    def test_listar_configuracoes(self):
        """Testa listagem de configurações."""
        url = reverse('presencas:presencas_api:configuracao_presenca')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        configuracoes = response_data['data']['configuracoes']
        self.assertEqual(len(configuracoes), 1)
        self.assertEqual(configuracoes[0]['turma']['nome'], 'Turma Teste')
    
    def test_listar_configuracoes_por_turma(self):
        """Testa listagem de configurações filtradas por turma."""
        url = reverse('presencas:presencas_api:configuracao_presenca')
        
        response = self.client.get(url, {'turma_id': self.turma.id})
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        configuracoes = response_data['data']['configuracoes']
        self.assertEqual(len(configuracoes), 1)
        self.assertEqual(configuracoes[0]['turma']['id'], self.turma.id)
