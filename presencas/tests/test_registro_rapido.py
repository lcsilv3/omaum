"""
Testes para o sistema de registro rápido de presenças.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date
import json

from alunos.models import Aluno, Curso
from turmas.models import Turma
from atividades.models import Atividade
from presencas.models import PresencaAcademica, ObservacaoPresenca


class RegistroRapidoTestCase(TestCase):
    """Testes para o sistema de registro rápido."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        # Criar usuário de teste
        self.user = User.objects.create_user(
            username='test_user',
            password='test_password',
            email='test@example.com'
        )
        
        # Criar curso de teste
        self.curso = Curso.objects.create(
            nome='Curso Teste',
            codigo='CT001',
            descricao='Curso para testes'
        )
        
        # Criar turma de teste
        self.turma = Turma.objects.create(
            nome='Turma A',
            curso=self.curso,
            ano=2024,
            semestre=1
        )
        
        # Criar atividade de teste
        self.atividade = Atividade.objects.create(
            nome='Atividade Teste',
            descricao='Atividade para testes',
            tipo='academica'
        )
        
        # Criar alunos de teste
        self.aluno1 = Aluno.objects.create(
            nome='João da Silva',
            cpf='12345678901',
            email='joao@exemplo.com',
            telefone='11999999999',
            curso=self.curso
        )
        
        self.aluno2 = Aluno.objects.create(
            nome='Maria Santos',
            cpf='98765432109',
            email='maria@exemplo.com',
            telefone='11888888888',
            curso=self.curso
        )
        
        # Cliente para requisições
        self.client = Client()
        self.client.login(username='test_user', password='test_password')
    
    def test_view_registro_rapido_otimizado(self):
        """Testa se a view principal carrega corretamente."""
        url = reverse('presencas:registro_rapido_otimizado')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registro Rápido de Presenças')
        self.assertContains(response, 'Turma A')
        self.assertContains(response, 'Atividade Teste')
    
    def test_buscar_alunos_ajax(self):
        """Testa a busca AJAX de alunos."""
        url = reverse('presencas:buscar_alunos_ajax')
        response = self.client.get(url, {'q': 'João', 'limit': 10})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn('alunos', data)
        self.assertEqual(len(data['alunos']), 1)
        self.assertEqual(data['alunos'][0]['nome'], 'João da Silva')
        self.assertEqual(data['alunos'][0]['cpf'], '12345678901')
    
    def test_buscar_alunos_ajax_query_pequena(self):
        """Testa busca com query muito pequena."""
        url = reverse('presencas:buscar_alunos_ajax')
        response = self.client.get(url, {'q': 'J', 'limit': 10})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['alunos'], [])
    
    def test_obter_alunos_turma_ajax(self):
        """Testa obtenção de alunos por turma."""
        # Primeiro, associar alunos à turma através de matrículas
        from matriculas.models import Matricula
        
        Matricula.objects.create(
            aluno=self.aluno1,
            turma=self.turma,
            data_matricula=date.today(),
            status='ativa'
        )
        
        Matricula.objects.create(
            aluno=self.aluno2,
            turma=self.turma,
            data_matricula=date.today(),
            status='ativa'
        )
        
        url = reverse('presencas:obter_alunos_turma_ajax')
        response = self.client.get(url, {'turma_id': self.turma.id})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn('alunos', data)
        self.assertEqual(len(data['alunos']), 2)
    
    def test_salvar_presencas_lote_ajax(self):
        """Testa salvamento em lote de presenças."""
        url = reverse('presencas:salvar_presencas_lote_ajax')
        
        data_presenca = {
            'turma_id': self.turma.id,
            'atividade_id': self.atividade.id,
            'data': '2024-01-15',
            'presencas': [
                {
                    'aluno_id': self.aluno1.id,
                    'presente': True,
                    'observacao': 'Participou ativamente'
                },
                {
                    'aluno_id': self.aluno2.id,
                    'presente': False,
                    'observacao': 'Faltou por motivo médico'
                }
            ]
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data_presenca),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['registradas'], 2)
        self.assertEqual(response_data['total_processadas'], 2)
        
        # Verificar se as presenças foram criadas
        presencas = PresencaAcademica.objects.filter(
            turma=self.turma,
            atividade=self.atividade,
            data='2024-01-15'
        )
        self.assertEqual(presencas.count(), 2)
        
        # Verificar observações
        observacoes = ObservacaoPresenca.objects.filter(
            turma=self.turma,
            atividade=self.atividade,
            data='2024-01-15'
        )
        self.assertEqual(observacoes.count(), 2)
    
    def test_validar_presenca_ajax(self):
        """Testa validação de presença existente."""
        # Criar uma presença
        PresencaAcademica.objects.create(
            aluno=self.aluno1,
            turma=self.turma,
            atividade=self.atividade,
            data='2024-01-15',
            presente=True,
            registrado_por=self.user.username,
            data_registro=timezone.now()
        )
        
        url = reverse('presencas:validar_presenca_ajax')
        response = self.client.get(url, {
            'aluno_id': self.aluno1.id,
            'turma_id': self.turma.id,
            'atividade_id': self.atividade.id,
            'data': '2024-01-15'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertTrue(data['existe'])
        self.assertTrue(data['presente'])
        self.assertEqual(data['registrado_por'], self.user.username)
    
    def test_validar_presenca_ajax_nao_existe(self):
        """Testa validação quando presença não existe."""
        url = reverse('presencas:validar_presenca_ajax')
        response = self.client.get(url, {
            'aluno_id': self.aluno1.id,
            'turma_id': self.turma.id,
            'atividade_id': self.atividade.id,
            'data': '2024-01-15'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertFalse(data['existe'])
    
    def test_salvar_presencas_lote_dados_incompletos(self):
        """Testa salvamento com dados incompletos."""
        url = reverse('presencas:salvar_presencas_lote_ajax')
        
        data_presenca = {
            'turma_id': self.turma.id,
            # atividade_id ausente
            'data': '2024-01-15',
            'presencas': []
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data_presenca),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
    
    def test_view_sem_autenticacao(self):
        """Testa acesso sem autenticação."""
        self.client.logout()
        
        url = reverse('presencas:registro_rapido_otimizado')
        response = self.client.get(url)
        
        # Deve redirecionar para login
        self.assertEqual(response.status_code, 302)
    
    def test_buscar_alunos_por_cpf(self):
        """Testa busca de alunos por CPF."""
        url = reverse('presencas:buscar_alunos_ajax')
        response = self.client.get(url, {'q': '123456', 'limit': 10})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(len(data['alunos']), 1)
        self.assertEqual(data['alunos'][0]['cpf'], '12345678901')
    
    def test_salvar_presencas_atualizacao(self):
        """Testa atualização de presenças existentes."""
        # Criar presença existente
        PresencaAcademica.objects.create(
            aluno=self.aluno1,
            turma=self.turma,
            atividade=self.atividade,
            data='2024-01-15',
            presente=False,
            registrado_por='outro_usuario',
            data_registro=timezone.now()
        )
        
        url = reverse('presencas:salvar_presencas_lote_ajax')
        
        data_presenca = {
            'turma_id': self.turma.id,
            'atividade_id': self.atividade.id,
            'data': '2024-01-15',
            'presencas': [
                {
                    'aluno_id': self.aluno1.id,
                    'presente': True,
                    'observacao': 'Corrigindo presença'
                }
            ]
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data_presenca),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['atualizadas'], 1)
        self.assertEqual(response_data['registradas'], 0)
        
        # Verificar se foi atualizada
        presenca = PresencaAcademica.objects.get(
            aluno=self.aluno1,
            turma=self.turma,
            atividade=self.atividade,
            data='2024-01-15'
        )
        self.assertTrue(presenca.presente)
        self.assertEqual(presenca.registrado_por, self.user.username)
