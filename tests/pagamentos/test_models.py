from django.test import TestCase
from django.utils import timezone
from pagamentos.models import Pagamento, TipoPagamento
from alunos.services import criar_aluno
from turmas.models import Turma
import datetime


class TipoPagamentoModelTestCase(TestCase):
    """Testes unitários para o modelo TipoPagamento."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar tipo de pagamento para os testes
        self.tipo_pagamento = TipoPagamento.objects.create(
            nome="Mensalidade",
            descricao="Pagamento mensal do curso",
            valor_padrao=500.00
        )
    
    def test_criacao_tipo_pagamento(self):
        """Testa a criação de um tipo de pagamento."""
        self.assertEqual(self.tipo_pagamento.nome, "Mensalidade")
        self.assertEqual(self.tipo_pagamento.descricao, "Pagamento mensal do curso")
        self.assertEqual(self.tipo_pagamento.valor_padrao, 500.00)
    
    def test_representacao_string(self):
        """Testa a representação em string do modelo."""
        self.assertEqual(str(self.tipo_pagamento), "Mensalidade")


class PagamentoModelTestCase(TestCase):
    """Testes unitários para o modelo Pagamento."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
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
    
    def test_criacao_pagamento(self):
        """Testa a criação de um pagamento."""
        self.assertEqual(self.pagamento.aluno, self.aluno)
        self.assertEqual(self.pagamento.turma, self.turma)
        self.assertEqual(self.pagamento.tipo_pagamento, self.tipo_pagamento)
        self.assertEqual(self.pagamento.valor, 500.00)
        self.assertEqual(self.pagamento.status, "pendente")
        self.assertEqual(self.pagamento.observacao, "Mensalidade de junho")
        self.assertIsNone(self.pagamento.data_pagamento)
    
    def test_representacao_string(self):
        """Testa a representação em string do modelo."""
        representacao_esperada = f"{self.aluno.nome} - {self.tipo_pagamento.nome} - R$ 500.00"
        self.assertEqual(str(self.pagamento), representacao_esperada)
    
    def test_registrar_pagamento(self):
        """Testa o método de registrar pagamento."""
        data_pagamento = timezone.now().date()
        self.pagamento.registrar_pagamento(data_pagamento, "pix", "Pagamento via PIX")
        
        self.assertEqual(self.pagamento.data_pagamento, data_pagamento)
        self.assertEqual(self.pagamento.status, "pago")
        self.assertEqual(self.pagamento.forma_pagamento, "pix")
        self.assertEqual(self.pagamento.observacao, "Pagamento via PIX")
    
    def test_cancelar_pagamento(self):
        """Testa o método de cancelar pagamento."""
        self.pagamento.cancelar_pagamento("Cancelado a pedido do aluno")
        
        self.assertEqual(self.pagamento.status, "cancelado")
        self.assertEqual(self.pagamento.observacao, "Cancelado a pedido do aluno")