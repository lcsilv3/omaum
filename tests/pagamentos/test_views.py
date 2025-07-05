from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from pagamentos.models import Pagamento, TipoPagamento
from alunos.services import criar_aluno
from turmas.models import Turma
import datetime

class PagamentosViewsTestCase(TestCase):
    """Testes de integração para as views do módulo de pagamentos."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Criar um aluno para os testes
        self.aluno = criar_aluno(
            cpf="12345678900",
            nome="Aluno Teste",
            email="aluno@teste.com",
            data_nascimento=datetime.date(1990, 1, 1)
        )
        
        # Criar uma turma para os testes
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A"
        )
        
        # Criar tipo de pagamento para os testes
        self.tipo_pagamento = TipoPagamento.objects.create(
            nome="Mensalidade",
            descricao="Pagamento mensal do curso",
            valor_padrao=500.00
        )
        
        # Criar pagamento para os testes
        self.pagamento = Pagamento.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            tipo_pagamento=self.tipo_pagamento,
            valor=500.00,
            data_vencimento=timezone.now().date() + datetime.timedelta(days=30),
            data_pagamento=None,
            status="pendente",
            forma_pagamento="",
            observacao="Mensalidade de junho"
        )
        
        # Cliente para fazer requisições
        self.client = Client()
    
    def test_listar_pagamentos_view(self):
        """Testa se a view de listagem de pagamentos funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de listagem de pagamentos
        response = self.client.get(reverse('pagamentos:listar_pagamentos'))
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se os pagamentos estão no contexto
        self.assertIn('pagamentos', response.context)
        self.assertEqual(len(response.context['pagamentos']), 1)
        
        # Verificar se o pagamento está na página
        self.assertContains(response, self.aluno.nome)
        self.assertContains(response, "Mensalidade")
        self.assertContains(response, "R$ 500.00")
    
    def test_criar_pagamento_view(self):
        """Testa se a view de criação de pagamento funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de criação de pagamento
        response = self.client.get(reverse('pagamentos:criar_pagamento'))
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o formulário está no contexto
        self.assertIn('form', response.context)
        
        # Dados para o novo pagamento
        novo_pagamento_data = {
            'aluno': self.aluno.cpf,
            'turma': self.turma.id,
            'tipo_pagamento': self.tipo_pagamento.id,
            'valor': 300.00,
            'data_vencimento': (timezone.now().date() + datetime.timedelta(days=15)).strftime('%Y-%m-%d'),
            'status': 'pendente',
            'observacao': 'Taxa de matrícula'
        }
        
        # Enviar o formulário para criar um novo pagamento
        response = self.client.post(
            reverse('pagamentos:criar_pagamento'),
            data=novo_pagamento_data,
            follow=True
        )
        
        # Verificar se o redirecionamento foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o pagamento foi criado no banco de dados
        self.assertTrue(Pagamento.objects.filter(observacao='Taxa de matrícula').exists())
        
        # Verificar se a mensagem de sucesso está na página
        self.assertContains(response, "Pagamento criado com sucesso")
    
    def test_registrar_pagamento_view(self):
        """Testa se a view de registro de pagamento funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de registro de pagamento
        response = self.client.get(
            reverse('pagamentos:registrar_pagamento', args=[self.pagamento.id])
        )
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o formulário está no contexto
        self.assertIn('form', response.context)
        
        # Dados para o registro de pagamento
        registro_data = {
            'data_pagamento': timezone.now().date().strftime('%Y-%m-%d'),
            'forma_pagamento': 'pix',
            'observacao': 'Pagamento via PIX'
        }
        
        # Enviar o formulário para registrar o pagamento
        response = self.client.post(
            reverse('pagamentos:registrar_pagamento', args=[self.pagamento.id]),
            data=registro_data,
            follow=True
        )
        
        # Verificar se o redirecionamento foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o pagamento foi atualizado no banco de dados
        pagamento_atualizado = Pagamento.objects.get(id=self.pagamento.id)
        self.assertEqual(pagamento_atualizado.status, 'pago')
        self.assertEqual(pagamento_atualizado.forma_pagamento, 'pix')
        self.assertEqual(pagamento_atualizado.observacao, 'Pagamento via PIX')
        
        # Verificar se a mensagem de sucesso está na página
        self.assertContains(response, "Pagamento registrado com sucesso")
    
    def test_cancelar_pagamento_view(self):
        """Testa se a view de cancelamento de pagamento funciona corretamente."""
        # Fazer login
        self.client.login(username='testuser', password='testpassword')
        
        # Acessar a página de cancelamento de pagamento
        response = self.client.get(
            reverse('pagamentos:cancelar_pagamento', args=[self.pagamento.id])
        )
        
        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o formulário está no contexto
        self.assertIn('form', response.context)
        
        # Dados para o cancelamento de pagamento
        cancelamento_data = {
            'observacao': 'Cancelado a pedido do aluno'
        }
        
        # Enviar o formulário para cancelar o pagamento
        response = self.client.post(
            reverse('pagamentos:cancelar_pagamento', args=[self.pagamento.id]),
            data=cancelamento_data,
            follow=True
        )
        
        # Verificar se o redirecionamento foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o pagamento foi atualizado no banco de dados
        pagamento_atualizado = Pagamento.objects.get(id=self.pagamento.id)
        self.assertEqual(pagamento_atualizado.status, 'cancelado')
        self.assertEqual(pagamento_atualizado.observacao, 'Cancelado a pedido do aluno')
        
        # Verificar se a mensagem de sucesso está na página
        self.assertContains(response, "Pagamento cancelado com sucesso")        # Acessar