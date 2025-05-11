from django.test import TestCase
from django.utils import timezone
from pagamentos.forms import PagamentoForm, RegistrarPagamentoForm
from alunos.models import Aluno
from turmas.models import Turma
from pagamentos.models import TipoPagamento
import datetime

class PagamentoFormTestCase(TestCase):
    """Testes unitários para o formulário de pagamento."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar um aluno para os testes
        self.aluno = Aluno.objects.create(
            cpf="12345678900",
            nome="Aluno Teste",
            email="aluno@teste.com",
            data_nascimento="1990-01-01"
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
    
    def test_pagamento_form_valido(self):
        """Testa se o formulário é válido com dados corretos."""
        form_data = {
            'aluno': self.aluno.cpf,
            'turma': self.turma.id,
            'tipo_pagamento': self.tipo_pagamento.id,
            'valor': 500.00,
            'data_vencimento': (timezone.now().date() + datetime.timedelta(days=30)).strftime('%Y-%m-%d'),
            'status': 'pendente',
            'observacao': 'Mensalidade de junho'
        }
        form = PagamentoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_pagamento_form_invalido(self):
        """Testa se o formulário é inválido com dados incorretos."""
        # Formulário sem aluno
        form_data = {
            'turma': self.turma.id,
            'tipo_pagamento': self.tipo_pagamento.id,
            'valor': 500.00,
            'data_vencimento': (timezone.now().date() + datetime.timedelta(days=30)).strftime('%Y-%m-%d'),
            'status': 'pendente',
            'observacao': 'Mensalidade de junho'
        }
        form = PagamentoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('aluno', form.errors)
        
        # Formulário com valor negativo
        form_data = {
            'aluno': self.aluno.cpf,
            'turma': self.turma.id,
            'tipo_pagamento': self.tipo_pagamento.id,
            'valor': -100.00,
            'data_vencimento': (timezone.now().date() + datetime.timedelta(days=30)).strftime('%Y-%m-%d'),
            'status': 'pendente',
            'observacao': 'Mensalidade de junho'
        }
        form = PagamentoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('valor', form.errors)

class RegistrarPagamentoFormTestCase(TestCase):
    """Testes unitários para o formulário de registro de pagamento."""
    
    def test_registrar_pagamento_form_valido(self):
        """Testa se o formulário é válido com dados corretos."""
        form_data = {
            'data_pagamento': timezone.now().date().strftime('%Y-%m-%d'),
            'forma_pagamento': 'pix',
            'observacao': 'Pagamento via PIX'
        }
        form = RegistrarPagamentoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_registrar_pagamento_form_invalido(self):
        """Testa se o formulário é inválido com dados incorretos."""
        # Formulário sem data de pagamento
        form_data = {
            'forma_pagamento': 'pix',
            'observacao': 'Pagamento via PIX'
        }
        form = RegistrarPagamentoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('data_pagamento', form.errors)
        
        # Formulário sem forma de pagamento
        form_data = {
            'data_pagamento': timezone.now().date().strftime('%Y-%m-%d'),
            'observacao': 'Pagamento via PIX'
        }
        form = RegistrarPagamentoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('forma_pagamento', form.errors)