from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date
from .models import Pagamento
from alunos.models import Aluno
from turmas.models import Turma
from cursos.models import Curso
from decimal import Decimal


class PagamentoTestCase(TestCase):
    def setUp(self):
        """Configurar dados de teste"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        # Criar objetos relacionados
        self.curso = Curso.objects.create(
            nome="Curso Teste",
            descricao="Curso de teste"
        )

        self.turma = Turma.objects.create(
            nome="Turma Teste",
            curso=self.curso,
            status="ATIVA"
        )

        self.aluno = Aluno.objects.create(
            nome="Aluno Teste",
            cpf="12345678901",
            email="aluno@teste.com",
            data_nascimento=date(1990, 1, 1)
        )

        # Criar um pagamento de teste
        self.pagamento = Pagamento.objects.create(
            aluno=self.aluno,
            valor=Decimal('100.00'),
            data_vencimento=timezone.now().date(),
            status="PENDENTE"
        )

    def test_listar_pagamentos(self):
        """Testar a listagem de pagamentos"""
        response = self.client.get(reverse("pagamentos:listar_pagamentos"))
        self.assertEqual(response.status_code, 200)

    def test_criar_pagamento(self):
        """Testar a criação de um novo pagamento"""
        data = {
            "aluno": self.aluno.id,
            "valor": Decimal('150.00'),
            "data_vencimento": timezone.now().date(),
            "status": "PENDENTE"
        }
        response = self.client.post(reverse("pagamentos:criar_pagamento"), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

    def test_editar_pagamento(self):
        """Testar a edição de um pagamento existente"""
        url = reverse("pagamentos:editar_pagamento", args=[self.pagamento.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_excluir_pagamento(self):
        """Testar a exclusão de um pagamento"""
        url = reverse("pagamentos:excluir_pagamento", args=[self.pagamento.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

    def test_detalhar_pagamento(self):
        """Testar a visualização de detalhes de um pagamento"""
        url = reverse("pagamentos:detalhar_pagamento", args=[self.pagamento.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_str_pagamento(self):
        """Testar a representação string do pagamento"""
        expected_str = f"Pagamento de {self.aluno.nome} - R$ {self.pagamento.valor} ({self.pagamento.get_status_display()})"
        self.assertEqual(str(self.pagamento), expected_str)

    def test_pagamento_status(self):
        """Testar o status do pagamento"""
        self.assertEqual(self.pagamento.status, "PENDENTE")
        
        # Alterar status
        self.pagamento.status = "PAGO"
        self.pagamento.save()
        self.assertEqual(self.pagamento.status, "PAGO")

    def test_pagamento_valor(self):
        """Testar o valor do pagamento"""
        self.assertEqual(self.pagamento.valor, Decimal('100.00'))
        
        # Alterar valor
        self.pagamento.valor = Decimal('200.00')
        self.pagamento.save()
        self.assertEqual(self.pagamento.valor, Decimal('200.00'))

    def test_relacionamentos(self):
        """Testar os relacionamentos do pagamento"""
        self.assertEqual(self.pagamento.aluno, self.aluno)

    def test_pagamento_validacao(self):
        """Testar validação do pagamento"""
        # Valor deve ser positivo
        with self.assertRaises(Exception):
            Pagamento.objects.create(
                aluno=self.aluno,
                valor=Decimal('-50.00'),  # Valor negativo
                data_vencimento=timezone.now().date(),
                status="PENDENTE"
            )
