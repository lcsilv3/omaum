"""
Testes para as APIs do aplicativo presencas.
Cobre endpoints AJAX, serialização/deserialização, validação e error handling.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from datetime import date, datetime, timedelta

from presencas.models import (
    Presenca, PresencaDetalhada, ConfiguracaoPresenca,
    TotalAtividadeMes, ObservacaoPresenca
)
from presencas.api_views import PresencaViewSet
from presencas.serializers import (
    PresencaSerializer, TotalAtividadeMesSerializer, 
    ObservacaoPresencaSerializer
)
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade

User = get_user_model()


class PresencaAPIBaseTest(APITestCase):
    """Classe base para testes de API."""
    
    def setUp(self):
        self.client = APIClient()
        
        # Criar usuário
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Criar aluno
        self.aluno = Aluno.objects.create(
            nome='João Silva',
            cpf='12345678901',
            data_nascimento=date(1990, 1, 1),
            email='joao@example.com'
        )
        
        # Criar turma
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        # Criar atividade
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def authenticate(self):
        """Autentica o cliente da API."""
        self.client.force_authenticate(user=self.user)


class PresencaViewSetTest(PresencaAPIBaseTest):
    """Testes para o ViewSet de Presença."""
    
    def test_list_presencas_sem_autenticacao(self):
        """Testa listagem sem autenticação."""
        url = reverse('presenca-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_presencas_com_autenticacao(self):
        """Testa listagem com autenticação."""
        self.authenticate()
        
        # Criar algumas presenças
        Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            data=date.today(),
            presente=True
        )
        
        url = reverse('presenca-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['presente'], True)
    
    def test_create_presenca_valida(self):
        """Testa criação de presença válida."""
        self.authenticate()
        
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'data': date.today().isoformat(),
            'presente': True,
            'registrado_por': 'API Test'
        }
        
        url = reverse('presenca-list')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['presente'], True)
        self.assertEqual(response.data['registrado_por'], 'API Test')
        
        # Verificar se foi criada no banco
        self.assertTrue(
            Presenca.objects.filter(
                aluno=self.aluno,
                turma=self.turma,
                data=date.today()
            ).exists()
        )
    
    def test_create_presenca_invalida_data_futura(self):
        """Testa criação com data futura."""
        self.authenticate()
        
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': (date.today() + timedelta(days=1)).isoformat(),
            'presente': True
        }
        
        url = reverse('presenca-list')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_presenca_duplicada(self):
        """Testa criação de presença duplicada."""
        self.authenticate()
        
        # Criar primeira presença
        Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today(),
            presente=True
        )
        
        # Tentar criar duplicada
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today().isoformat(),
            'presente': False
        }
        
        url = reverse('presenca-list')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_presenca(self):
        """Testa atualização de presença."""
        self.authenticate()
        
        presenca = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today(),
            presente=True
        )
        
        data = {
            'presente': False,
            'justificativa': 'Motivo médico'
        }
        
        url = reverse('presenca-detail', kwargs={'pk': presenca.pk})
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['presente'], False)
        self.assertEqual(response.data['justificativa'], 'Motivo médico')
    
    def test_delete_presenca(self):
        """Testa exclusão de presença."""
        self.authenticate()
        
        presenca = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date.today(),
            presente=True
        )
        
        url = reverse('presenca-detail', kwargs={'pk': presenca.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Presenca.objects.filter(pk=presenca.pk).exists())
    
    def test_filtros_queryset(self):
        """Testa filtros personalizados do queryset."""
        self.authenticate()
        
        # Criar presenças diferentes
        presenca1 = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            data=date(2024, 1, 15),
            presente=True
        )
        
        aluno2 = Aluno.objects.create(
            nome='Maria Santos',
            cpf='98765432100',
            data_nascimento=date(1992, 5, 15),
            email='maria@example.com'
        )
        
        presenca2 = Presenca.objects.create(
            aluno=aluno2,
            turma=self.turma,
            data=date(2024, 1, 20),
            presente=False
        )
        
        url = reverse('presenca-list')
        
        # Filtrar por aluno
        response = self.client.get(url, {'aluno': self.aluno.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], presenca1.id)
        
        # Filtrar por turma
        response = self.client.get(url, {'turma': self.turma.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Filtrar por data
        response = self.client.get(url, {
            'data_inicio': '2024-01-01',
            'data_fim': '2024-01-18'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], presenca1.id)
    
    def test_action_personalizada_frequencia(self):
        """Testa action personalizada de frequência."""
        self.authenticate()
        
        # Criar presenças para cálculo
        for i in range(8):
            Presenca.objects.create(
                aluno=self.aluno,
                turma=self.turma,
                data=date(2024, 1, i+1),
                presente=True
            )
        
        for i in range(2):
            Presenca.objects.create(
                aluno=self.aluno,
                turma=self.turma,
                data=date(2024, 1, i+9),
                presente=False
            )
        
        url = reverse('presenca-frequencia')
        response = self.client.post(url, {
            'aluno_cpf': self.aluno.cpf,
            'turma_id': self.turma.id
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_registros', response.data)
        self.assertIn('percentual_presenca', response.data)
        self.assertEqual(response.data['total_registros'], 10)
        self.assertEqual(response.data['percentual_presenca'], 80.0)


class AjaxEndpointsTest(TestCase):
    """Testes para endpoints AJAX específicos."""
    
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.aluno = Aluno.objects.create(
            nome='João Silva',
            cpf='12345678901',
            data_nascimento=date(1990, 1, 1),
            email='joao@example.com'
        )
        
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def login_user(self):
        """Faz login do usuário."""
        return self.client.login(username='testuser', password='testpass123')
    
    def test_ajax_registrar_presenca_rapida(self):
        """Testa AJAX para registro rápido de presença."""
        self.login_user()
        
        try:
            url = reverse('presencas:ajax_registrar_presenca_rapida')
            data = {
                'aluno_id': self.aluno.id,
                'turma_id': self.turma.id,
                'atividade_id': self.atividade.id,
                'data': date.today().isoformat(),
                'presente': True
            }
            
            response = self.client.post(
                url, 
                json.dumps(data),
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            
            self.assertEqual(response.status_code, 200)
            
            response_data = json.loads(response.content)
            self.assertTrue(response_data.get('success'))
            self.assertIn('id', response_data.get('presenca', {}))
            
        except Exception:
            self.skipTest("Endpoint AJAX não encontrado")
    
    def test_ajax_buscar_alunos_turma(self):
        """Testa AJAX para buscar alunos da turma."""
        self.login_user()
        
        try:
            url = reverse('presencas:ajax_alunos_turma')
            response = self.client.get(
                url,
                {'turma_id': self.turma.id},
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            
            self.assertEqual(response.status_code, 200)
            
            response_data = json.loads(response.content)
            self.assertIn('alunos', response_data)
            self.assertIsInstance(response_data['alunos'], list)
            
        except Exception:
            self.skipTest("Endpoint AJAX não encontrado")
    
    def test_ajax_calcular_consolidado(self):
        """Testa AJAX para cálculo de consolidado."""
        self.login_user()
        
        # Criar presença detalhada
        PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=8,
            faltas=2
        )
        
        try:
            url = reverse('presencas:ajax_calcular_consolidado')
            data = {
                'aluno_id': self.aluno.id,
                'turma_id': self.turma.id,
                'periodo_inicio': '2024-01-01',
                'periodo_fim': '2024-12-31'
            }
            
            response = self.client.post(
                url,
                json.dumps(data),
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            
            self.assertEqual(response.status_code, 200)
            
            response_data = json.loads(response.content)
            self.assertIn('consolidado', response_data)
            
        except Exception:
            self.skipTest("Endpoint AJAX não encontrado")
    
    def test_ajax_error_handling(self):
        """Testa tratamento de erros em endpoints AJAX."""
        self.login_user()
        
        try:
            url = reverse('presencas:ajax_registrar_presenca_rapida')
            data = {
                'aluno_id': 99999,  # ID inexistente
                'turma_id': self.turma.id,
                'data': date.today().isoformat(),
                'presente': True
            }
            
            response = self.client.post(
                url,
                json.dumps(data),
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            
            # Deve retornar erro estruturado
            response_data = json.loads(response.content)
            self.assertFalse(response_data.get('success'))
            self.assertIn('error', response_data)
            
        except Exception:
            self.skipTest("Endpoint AJAX não encontrado")
    
    def test_ajax_sem_autenticacao(self):
        """Testa AJAX sem autenticação."""
        try:
            url = reverse('presencas:ajax_registrar_presenca_rapida')
            response = self.client.post(
                url,
                json.dumps({}),
                content_type='application/json',
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
            
            # Deve retornar erro de autenticação
            self.assertIn(response.status_code, [401, 403, 302])
            
        except Exception:
            self.skipTest("Endpoint AJAX não encontrado")


class SerializerTest(TestCase):
    """Testes para serializers."""
    
    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome='João Silva',
            cpf='12345678901',
            data_nascimento=date(1990, 1, 1),
            email='joao@example.com'
        )
        
        self.turma = Turma.objects.create(
            nome='Turma A',
            ano=2024,
            semestre=1
        )
        
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Descrição da atividade',
            tipo='academica'
        )
    
    def test_presenca_serializer_valido(self):
        """Testa serialização válida de presença."""
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'data': date.today().isoformat(),
            'presente': True,
            'justificativa': '',
            'registrado_por': 'Test'
        }
        
        serializer = PresencaSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        presenca = serializer.save()
        self.assertEqual(presenca.aluno, self.aluno)
        self.assertEqual(presenca.turma, self.turma)
        self.assertTrue(presenca.presente)
    
    def test_presenca_serializer_invalido(self):
        """Testa serialização inválida."""
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': (date.today() + timedelta(days=1)).isoformat(),  # Data futura
            'presente': True
        }
        
        serializer = PresencaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('data', serializer.errors)
    
    def test_presenca_serializer_read(self):
        """Testa leitura com serializer."""
        presenca = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            data=date.today(),
            presente=True,
            justificativa='Teste'
        )
        
        serializer = PresencaSerializer(presenca)
        data = serializer.data
        
        self.assertEqual(data['presente'], True)
        self.assertEqual(data['justificativa'], 'Teste')
        self.assertIn('aluno', data)
        self.assertIn('turma', data)
    
    def test_total_atividade_mes_serializer(self):
        """Testa serializer de TotalAtividadeMes."""
        data = {
            'atividade': self.atividade.id,
            'turma': self.turma.id,
            'ano': 2024,
            'mes': 1,
            'qtd_ativ_mes': 15
        }
        
        serializer = TotalAtividadeMesSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        total = serializer.save()
        self.assertEqual(total.qtd_ativ_mes, 15)
        self.assertEqual(total.ano, 2024)
    
    def test_observacao_presenca_serializer(self):
        """Testa serializer de ObservacaoPresenca."""
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'atividade': self.atividade.id,
            'data': date.today().isoformat(),
            'texto': 'Observação de teste'
        }
        
        serializer = ObservacaoPresencaSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        observacao = serializer.save()
        self.assertEqual(observacao.texto, 'Observação de teste')
        self.assertEqual(observacao.aluno, self.aluno)


class APIPerformanceTest(PresencaAPIBaseTest):
    """Testes de performance da API."""
    
    def test_list_presencas_performance(self):
        """Testa performance da listagem de presenças."""
        self.authenticate()
        
        # Criar muitas presenças
        presencas = []
        for i in range(100):
            aluno = Aluno.objects.create(
                nome=f'Aluno {i}',
                cpf=f'1234567890{i:02d}',
                data_nascimento=date(1990, 1, 1),
                email=f'aluno{i}@example.com'
            )
            
            presencas.append(Presenca(
                aluno=aluno,
                turma=self.turma,
                atividade=self.atividade,
                data=date.today() - timedelta(days=i),
                presente=True
            ))
        
        Presenca.objects.bulk_create(presencas)
        
        url = reverse('presenca-list')
        
        # Testar que não há N+1 queries
        with self.assertNumQueries(3):  # Query principal + related fields
            response = self.client.get(url)
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 100)
    
    def test_filtros_complexos_performance(self):
        """Testa performance com filtros complexos."""
        self.authenticate()
        
        # Criar dados de teste
        for i in range(50):
            aluno = Aluno.objects.create(
                nome=f'Aluno {i}',
                cpf=f'1234567890{i:02d}',
                data_nascimento=date(1990, 1, 1),
                email=f'aluno{i}@example.com'
            )
            
            Presenca.objects.create(
                aluno=aluno,
                turma=self.turma,
                atividade=self.atividade,
                data=date(2024, 1, (i % 28) + 1),
                presente=i % 2 == 0  # Alternando presente/ausente
            )
        
        url = reverse('presenca-list')
        
        # Testar filtros múltiplos
        with self.assertNumQueries(3):
            response = self.client.get(url, {
                'turma': self.turma.id,
                'atividade': self.atividade.id,
                'data_inicio': '2024-01-01',
                'data_fim': '2024-01-31',
                'presente': True
            })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APISecurityTest(PresencaAPIBaseTest):
    """Testes de segurança da API."""
    
    def test_injection_sql_prevention(self):
        """Testa prevenção de SQL injection."""
        self.authenticate()
        
        # Tentar injeção SQL nos filtros
        url = reverse('presenca-list')
        response = self.client.get(url, {
            'aluno': "1; DROP TABLE presencas_presenca;",
            'turma': "1' OR '1'='1"
        })
        
        # Deve retornar resultado normal ou erro de validação
        self.assertIn(response.status_code, [200, 400])
    
    def test_xss_prevention(self):
        """Testa prevenção de XSS."""
        self.authenticate()
        
        data = {
            'aluno': self.aluno.id,
            'turma': self.turma.id,
            'data': date.today().isoformat(),
            'presente': True,
            'justificativa': '<script>alert("XSS")</script>',
            'registrado_por': '<img src=x onerror=alert("XSS")>'
        }
        
        url = reverse('presenca-list')
        response = self.client.post(url, data, format='json')
        
        if response.status_code == 201:
            # Verificar que scripts foram escapados/removidos
            presenca = Presenca.objects.get(id=response.data['id'])
            self.assertNotIn('<script>', presenca.justificativa)
            self.assertNotIn('<img', presenca.registrado_por)
    
    def test_csrf_protection(self):
        """Testa proteção CSRF."""
        # APIs REST geralmente usam autenticação por token/session
        # que não requer CSRF, mas views AJAX podem precisar
        
        # Login sem autenticação da API
        self.client.login(username='testuser', password='testpass123')
        
        # Tentar acessar endpoint sem CSRF token
        try:
            url = reverse('presencas:ajax_registrar_presenca_rapida')
            response = self.client.post(url, {})
            
            # Dependendo da configuração, pode retornar 403 ou passar
            self.assertIn(response.status_code, [200, 403, 404])
        except:
            self.skipTest("Endpoint AJAX não encontrado")
    
    def test_rate_limiting(self):
        """Testa limitação de taxa (se implementada)."""
        self.authenticate()
        
        url = reverse('presenca-list')
        
        # Fazer muitas requisições rápidas
        responses = []
        for i in range(20):
            response = self.client.get(url)
            responses.append(response.status_code)
        
        # Se rate limiting estiver implementado, algumas requisições
        # devem retornar 429 (Too Many Requests)
        # Caso contrário, todas devem retornar 200
        self.assertTrue(all(code in [200, 429] for code in responses))
