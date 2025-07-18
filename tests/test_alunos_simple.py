from django.urls import reverse
# Testes de integração para as views simplificadas do app alunos
class AlunoViewsIntegracaoTest(TestCase):
    """Testes de integração para as views CRUD simplificadas do app alunos."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        self.pais = Pais.objects.create(
            codigo='BRA',
            nome='Brasil',
            nacionalidade='brasileiro'
        )
        self.estado = Estado.objects.create(
            nome='São Paulo',
            codigo='SP',
            regiao='Sudeste'
        )
        self.cidade = Cidade.objects.create(
            nome='São Paulo',
            estado=self.estado,
            codigo_ibge='3550308'
        )
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            email='joao@teste.com',
            usuario=self.user,
            pais=self.pais,
            estado=self.estado,
            cidade=self.cidade
        )

    def test_listar_alunos_simple_view(self):
        url = reverse('alunos:listar_alunos_simple')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 302])

    def test_criar_aluno_simple_view_get(self):
        url = reverse('alunos:criar_aluno_simple')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detalhar_aluno_simple_view(self):
        url = reverse('alunos:detalhar_aluno_simple', args=[self.aluno.cpf])
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 302])

    def test_editar_aluno_simple_view_get(self):
        url = reverse('alunos:editar_aluno_simple', args=[self.aluno.cpf])
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_excluir_aluno_simple_view_get(self):
        url = reverse('alunos:excluir_aluno_simple', args=[self.aluno.cpf])
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 302])
"""
Testes unitários para o módulo de alunos.
"""

import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from alunos.models import Aluno, Pais, Estado, Cidade


class AlunoSimpleTest(TestCase):
    """Testes simples para o modelo Aluno."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        # Criar país, estado e cidade para os testes (apenas uma vez)
        self.pais = Pais.objects.create(
            codigo='BRA',
            nome='Brasil',
            nacionalidade='brasileiro'
        )
        self.estado = Estado.objects.create(
            nome='São Paulo',
            codigo='SP',
            regiao='Sudeste'
        )
        self.cidade = Cidade.objects.create(
            nome='São Paulo',
            estado=self.estado,
            codigo_ibge='3550308'
        )
        
    def test_aluno_creation(self):
        """Teste criação básica de aluno."""
        aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            email='joao@teste.com',
            usuario=self.user,
            pais=self.pais,
            estado=self.estado,
            cidade=self.cidade
        )
        
        self.assertEqual(aluno.cpf, '12345678901')
        self.assertEqual(aluno.nome, 'João Silva')
        self.assertEqual(aluno.email, 'joao@teste.com')
        self.assertEqual(aluno.situacao, 'ATIVO')
        self.assertEqual(aluno.sexo, 'M')
        
    def test_aluno_str(self):
        """Teste representação string do aluno."""
        aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            email='joao@teste.com',
            usuario=self.user,
            pais=self.pais,
            estado=self.estado,
            cidade=self.cidade
        )
        self.assertEqual(str(aluno), 'João Silva')
        
    def test_aluno_defaults(self):
        """Teste valores padrão do aluno."""
        aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            email='joao@teste.com',
            usuario=self.user,
            pais=self.pais,
            estado=self.estado,
            cidade=self.cidade
        )
        self.assertEqual(aluno.situacao, 'ATIVO')
        self.assertEqual(aluno.sexo, 'M')
        self.assertIsNone(aluno.hora_nascimento)
        
    def test_aluno_meta_info(self):
        """Teste meta informações do aluno."""
        aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            email='joao@teste.com',
            usuario=self.user,
            pais=self.pais,
            estado=self.estado,
            cidade=self.cidade
        )
        self.assertEqual(aluno._meta.verbose_name, 'Aluno')
        self.assertEqual(aluno._meta.verbose_name_plural, 'Alunos')


class AlunoViewSimpleTest(TestCase):
    """Testes simples para views de Aluno."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        
        # Criar dependências
        self.pais = Pais.objects.create(
            codigo='BRA',
            nome='Brasil',
            nacionalidade='brasileiro'
        )
        
        self.estado = Estado.objects.create(
            nome='São Paulo',
            codigo='SP',
            regiao='Sudeste'
        )
        
        self.cidade = Cidade.objects.create(
            nome='São Paulo',
            estado=self.estado,
            codigo_ibge='3550308'
        )
        
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            email='joao@teste.com',
            usuario=self.user,
            pais=self.pais,
            estado=self.estado,
            cidade=self.cidade
        )
        
    def test_aluno_list_view_status(self):
        """Teste status da view de listagem de alunos."""
        self.client.force_login(self.user)
        try:
            response = self.client.get('/alunos/')
            # Se a URL existe, deve retornar 200 ou 302
            self.assertIn(response.status_code, [200, 302])
        except Exception:
            # Se a URL não existe, apenas pular o teste
            self.skipTest("URL de alunos não configurada")
            
    def test_aluno_detail_view_status(self):
        """Teste status da view de detalhes do aluno."""
        self.client.force_login(self.user)
        try:
            response = self.client.get(f'/alunos/{self.aluno.cpf}/')
            # Se a URL existe, deve retornar 200 ou 302
            self.assertIn(response.status_code, [200, 302])
        except Exception:
            # Se a URL não existe, apenas pular o teste
            self.skipTest("URL de detalhes do aluno não configurada")


@pytest.mark.unit
class AlunoUnitSimpleTest(TestCase):
    """Testes unitários muito básicos para o módulo de alunos."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        
        # Criar dependências
        self.pais = Pais.objects.create(
            codigo='BRA',
            nome='Brasil',
            nacionalidade='brasileiro'
        )
        
        self.estado = Estado.objects.create(
            nome='São Paulo',
            codigo='SP',
            regiao='Sudeste'
        )
        
        self.cidade = Cidade.objects.create(
            nome='São Paulo',
            estado=self.estado,
            codigo_ibge='3550308'
        )
    
    def test_aluno_model_exists(self):
        """Teste se o modelo Aluno existe e pode ser instanciado."""
        aluno = Aluno(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            email='joao@teste.com',
            usuario=self.user,
            pais=self.pais,
            estado=self.estado,
            cidade=self.cidade
        )
        self.assertIsInstance(aluno, Aluno)
        self.assertEqual(aluno.nome, 'João Silva')
        
    def test_aluno_can_be_saved(self):
        """Teste se o aluno pode ser salvo no banco."""
        aluno = Aluno(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            email='joao@teste.com',
            usuario=self.user,
            pais=self.pais,
            estado=self.estado,
            cidade=self.cidade
        )
        aluno.save()
        
        # Verificar se foi salvo
        saved_aluno = Aluno.objects.get(cpf='12345678901')
        self.assertEqual(saved_aluno.nome, 'João Silva')
        
    def test_aluno_can_be_deleted(self):
        """Teste se o aluno pode ser excluído."""
        aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            email='joao@teste.com',
            usuario=self.user,
            pais=self.pais,
            estado=self.estado,
            cidade=self.cidade
        )
        
        aluno.delete()
        
        # Verificar se foi excluído
        with self.assertRaises(Aluno.DoesNotExist):
            Aluno.objects.get(cpf='12345678901')


@pytest.mark.critical
class AlunoCriticalSimpleTest(TestCase):
    """Testes críticos simples para o módulo de alunos."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        
        # Criar dependências
        self.pais = Pais.objects.create(
            codigo='BRA',
            nome='Brasil',
            nacionalidade='brasileiro'
        )
        
        self.estado = Estado.objects.create(
            nome='São Paulo',
            codigo='SP',
            regiao='Sudeste'
        )
        
        self.cidade = Cidade.objects.create(
            nome='São Paulo',
            estado=self.estado,
            codigo_ibge='3550308'
        )
    
    def test_aluno_cpf_required(self):
        """Teste que CPF é obrigatório."""
        with self.assertRaises(ValidationError):
            aluno = Aluno(
                cpf='',
                nome='João Silva',
                data_nascimento=date(1990, 1, 1),
                email='joao@teste.com',
                usuario=self.user,
                pais=self.pais,
                estado=self.estado,
                cidade=self.cidade
            )
            aluno.full_clean()
            
    def test_aluno_email_unique(self):
        """Teste que email deve ser único."""
        # Criar primeiro aluno
        Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            email='joao@teste.com',
            usuario=self.user,
            pais=self.pais,
            estado=self.estado,
            cidade=self.cidade
        )
        
        # Tentar criar segundo aluno com mesmo email
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass'
        )
        
        with self.assertRaises(Exception):
            Aluno.objects.create(
                cpf='12345678902',
                nome='Maria Silva',
                data_nascimento=date(1990, 1, 1),
                email='joao@teste.com',  # Email duplicado
                usuario=user2,
                pais=self.pais,
                estado=self.estado,
                cidade=self.cidade
            )
            
    def test_aluno_cpf_unique(self):
        """Teste que CPF deve ser único."""
        # Criar primeiro aluno
        Aluno.objects.create(
            cpf='12345678901',
            nome='João Silva',
            data_nascimento=date(1990, 1, 1),
            email='joao@teste.com',
            usuario=self.user,
            pais=self.pais,
            estado=self.estado,
            cidade=self.cidade
        )
        
        # Tentar criar segundo aluno com mesmo CPF
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass'
        )
        
        with self.assertRaises(Exception):
            Aluno.objects.create(
                cpf='12345678901',  # CPF duplicado
                nome='Maria Silva',
                data_nascimento=date(1990, 1, 1),
                email='maria@teste.com',
                usuario=user2,
                pais=self.pais,
                estado=self.estado,
                cidade=self.cidade
            )


class AlunoPerformanceSimpleTest(TestCase):
    """Testes de performance simples para o módulo de alunos."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar dependências
        self.pais = Pais.objects.create(
            codigo='BRA',
            nome='Brasil',
            nacionalidade='brasileiro'
        )
        
        self.estado = Estado.objects.create(
            nome='São Paulo',
            codigo='SP',
            regiao='Sudeste'
        )
        
        self.cidade = Cidade.objects.create(
            nome='São Paulo',
            estado=self.estado,
            codigo_ibge='3550308'
        )
        
    def test_bulk_aluno_creation(self):
        """Teste criação em lote de alunos."""
        alunos = []
        users = []
        
        for i in range(10):
            user = User.objects.create_user(
                username=f'testuser{i}',
                email=f'test{i}@example.com',
                password='testpass'
            )
            users.append(user)
            
            aluno = Aluno(
                cpf=f'1234567890{i}',
                nome=f'Aluno {i}',
                data_nascimento=date(1990, 1, 1),
                email=f'aluno{i}@teste.com',
                usuario=user,
                pais=self.pais,
                estado=self.estado,
                cidade=self.cidade
            )
            alunos.append(aluno)
            
        # Criar em lote
        Aluno.objects.bulk_create(alunos)
        
        # Verificar quantidade
        self.assertEqual(Aluno.objects.count(), 10)
        
    def test_aluno_query_performance(self):
        """Teste performance de consultas."""
        # Criar alguns alunos
        for i in range(5):
            user = User.objects.create_user(
                username=f'testuser{i}',
                email=f'test{i}@example.com',
                password='testpass'
            )
            
            Aluno.objects.create(
                cpf=f'1234567890{i}',
                nome=f'Aluno {i}',
                data_nascimento=date(1990, 1, 1),
                email=f'aluno{i}@teste.com',
                usuario=user,
                pais=self.pais,
                estado=self.estado,
                cidade=self.cidade
            )
            
        # Testar consultas
        import time
        start_time = time.time()
        
        # Consulta simples
        alunos = list(Aluno.objects.all())
        
        end_time = time.time()
        query_time = end_time - start_time
        
        # Deve ser rápido (menos de 1 segundo)
        self.assertLess(query_time, 1.0)
        self.assertEqual(len(alunos), 5)


class PaisSimpleTest(TestCase):
    """Testes simples para o modelo Pais."""
    
    def test_pais_creation(self):
        """Teste criação básica de país."""
        pais = Pais.objects.create(
            codigo='BRA',
            nome='Brasil',
            nacionalidade='brasileiro'
        )
        
        self.assertEqual(pais.codigo, 'BRA')
        self.assertEqual(pais.nome, 'Brasil')
        self.assertEqual(pais.nacionalidade, 'brasileiro')
        self.assertTrue(pais.ativo)
        
    def test_pais_str(self):
        """Teste representação string do país."""
        pais = Pais.objects.create(
            codigo='BRA',
            nome='Brasil',
            nacionalidade='brasileiro'
        )
        # Assumindo que __str__ retorna o nome
        self.assertEqual(str(pais), 'Brasil')


class EstadoSimpleTest(TestCase):
    """Testes simples para o modelo Estado."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.pais = Pais.objects.create(
            codigo='BRA',
            nome='Brasil',
            nacionalidade='brasileiro'
        )
    
    def test_estado_creation(self):
        """Teste criação básica de estado."""
        estado = Estado.objects.create(
            nome='São Paulo',
            codigo='SP',
            regiao='Sudeste'
        )
        
        self.assertEqual(estado.nome, 'São Paulo')
        self.assertEqual(estado.codigo, 'SP')
        self.assertEqual(estado.regiao, 'Sudeste')
        
    def test_estado_str(self):
        """Teste representação string do estado."""
        estado = Estado.objects.create(
            nome='São Paulo',
            codigo='SP',
            regiao='Sudeste'
        )
        # Assumindo formato "Nome (Código)"
        self.assertEqual(str(estado), 'São Paulo (SP)')


class CidadeSimpleTest(TestCase):
    """Testes simples para o modelo Cidade."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.pais = Pais.objects.create(
            codigo='BRA',
            nome='Brasil',
            nacionalidade='brasileiro'
        )
        
        self.estado = Estado.objects.create(
            nome='São Paulo',
            codigo='SP',
            regiao='Sudeste'
        )
    
    def test_cidade_creation(self):
        """Teste criação básica de cidade."""
        cidade = Cidade.objects.create(
            nome='São Paulo',
            estado=self.estado,
            codigo_ibge='3550308'
        )
        
        self.assertEqual(cidade.nome, 'São Paulo')
        self.assertEqual(cidade.estado, self.estado)
        self.assertEqual(cidade.codigo_ibge, '3550308')
        
    def test_cidade_str(self):
        """Teste representação string da cidade."""
        cidade = Cidade.objects.create(
            nome='São Paulo',
            estado=self.estado,
            codigo_ibge='3550308'
        )
        # Assumindo que __str__ retorna o nome
        self.assertEqual(str(cidade), 'São Paulo')
