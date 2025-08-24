"""
Testes unitários para o módulo de alunos.
"""

import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils import timezone

from alunos.models import Aluno
from alunos.forms import AlunoForm
from tests.factories import AlunoFactory, UserFactory




@pytest.mark.django_db
class AlunoModelTest(TestCase):
    """Testes para o modelo Aluno."""
    def setUp(self):
        self.aluno = AlunoFactory()

    def test_str_representation(self):
        assert str(self.aluno) == self.aluno.nome

    def test_aluno_creation(self):
        assert self.aluno.nome
        assert self.aluno.cpf
        assert self.aluno.email
        assert self.aluno.ativo is True
        assert self.aluno.data_cadastro
        assert self.aluno.data_nascimento

    def test_aluno_cpf_unique(self):
        with pytest.raises(Exception):
            AlunoFactory(cpf=self.aluno.cpf)

    def test_aluno_email_validation(self):
        aluno = AlunoFactory.build(email='email_invalido')
        with pytest.raises(ValidationError):
            aluno.full_clean()

    def test_aluno_idade_calculation(self):
        data_nascimento = date(1990, 1, 1)
        aluno = AlunoFactory(data_nascimento=data_nascimento)
        idade_esperada = (date.today() - data_nascimento).days // 365
        assert aluno.idade == idade_esperada

    def test_aluno_deactivation(self):
        self.aluno.ativo = False
        self.aluno.save()
        assert self.aluno.ativo is False

    def test_aluno_codigo_iniciatico(self):
        codigo = 'ABC123'
        aluno = AlunoFactory(codigo_iniciatico=codigo)
        assert aluno.codigo_iniciatico == codigo


@pytest.mark.django_db
class AlunoFormTest(TestCase):
    """Testes para o formulário de Aluno."""
    def setUp(self):
        self.valid_data = {
            'nome': 'João Silva',
            'cpf': '123.456.789-00',
            'email': 'joao@example.com',
            'telefone': '(11) 99999-9999',
            'endereco': 'Rua das Flores, 123',
            'data_nascimento': '1990-01-01',
            'ativo': True
        }
    
    def test_valid_form(self):
        """Teste de formulário válido."""
        form = AlunoForm(data=self.valid_data)
        assert form.is_valid()
    
    def test_form_missing_required_fields(self):
        """Teste de formulário com campos obrigatórios ausentes."""
        data = self.valid_data.copy()
        del data['nome']
        form = AlunoForm(data=data)
        assert not form.is_valid()
        assert 'nome' in form.errors
    
    def test_form_invalid_cpf(self):
        """Teste de formulário com CPF inválido."""
        data = self.valid_data.copy()
        data['cpf'] = '123.456.789-99'  # CPF inválido
        form = AlunoForm(data=data)
        assert not form.is_valid()
    
    def test_form_invalid_email(self):
        """Teste de formulário com email inválido."""
        data = self.valid_data.copy()
        data['email'] = 'email_invalido'
        form = AlunoForm(data=data)
        assert not form.is_valid()
    
    def test_form_save(self):
        """Teste de salvamento do formulário."""
        form = AlunoForm(data=self.valid_data)
        assert form.is_valid()
        aluno = form.save()
        assert aluno.nome == self.valid_data['nome']
        assert aluno.tipo_aluno == self.tipo_aluno


@pytest.mark.django_db


@pytest.mark.django_db
class AlunoViewTest(TestCase):
    """Testes para as views de Aluno."""
    
    def setUp(self):
        self.user = UserFactory()
        self.aluno = AlunoFactory()
        self.client.force_login(self.user)
    
    def test_lista_alunos_view(self):
        """Teste da view de listagem de alunos."""
        url = reverse('alunos:lista')
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert self.aluno in response.context['alunos']
    
    def test_detalhe_aluno_view(self):
        """Teste da view de detalhes do aluno."""
        url = reverse('alunos:detalhe', kwargs={'pk': self.aluno.id})
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert response.context['aluno'] == self.aluno
    
    def test_criar_aluno_view_get(self):
        """Teste da view de criação de aluno (GET)."""
        url = reverse('alunos:criar')
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_criar_aluno_view_post(self):
        """Teste da view de criação de aluno (POST)."""
        url = reverse('alunos:criar')
        data = {
            'nome': 'Novo Aluno',
            'cpf': '11122233344',
            'email': 'novo@example.com',
            'telefone': '(11) 77777-7777',
            'endereco': 'Rua Nova, 789',
            'data_nascimento': '1995-01-01',
            'ativo': True
        }
        response = self.client.post(url, data)
        assert response.status_code == 302  # Redirect após sucesso
        assert Aluno.objects.filter(nome='Novo Aluno').exists()
    
    def test_editar_aluno_view(self):
        """Teste da view de edição de aluno."""
        url = reverse('alunos:editar', kwargs={'pk': self.aluno.id})
        data = {
            'nome': 'Aluno Editado',
            'cpf': self.aluno.cpf,
            'email': self.aluno.email,
            'telefone': self.aluno.telefone,
            'endereco': self.aluno.endereco,
            'data_nascimento': self.aluno.data_nascimento.strftime('%Y-%m-%d'),
            'ativo': True
        }
        response = self.client.post(url, data)
        assert response.status_code == 302
        self.aluno.refresh_from_db()
        assert self.aluno.nome == 'Aluno Editado'
    
    def test_deletar_aluno_view(self):
        """Teste da view de exclusão de aluno."""
        url = reverse('alunos:deletar', kwargs={'pk': self.aluno.id})
        response = self.client.post(url)
        
        assert response.status_code == 302
        self.aluno.refresh_from_db()
        assert self.aluno.ativo is False
    
    def test_buscar_alunos_view(self):
        """Teste da view de busca de alunos."""
        url = reverse('alunos:buscar')
        response = self.client.get(url, {'q': self.aluno.nome[:5]})
        
        assert response.status_code == 200
        assert self.aluno in response.context['alunos']
    
    def test_filtrar_alunos_por_tipo_view(self):
        """Teste da view de filtro por tipo."""
        url = reverse('alunos:filtrar_por_tipo')
        response = self.client.get(url, {'tipo': self.tipo_aluno.id})
        
        assert response.status_code == 200
        assert self.aluno in response.context['alunos']
    
    def test_verificar_cpf_view(self):
        """Teste da view de verificação de CPF."""
        url = reverse('alunos:verificar_cpf')
        response = self.client.get(url, {'cpf': self.aluno.cpf})
        
        assert response.status_code == 200
        data = response.json()
        assert data['exists'] is True


@pytest.mark.django_db
class AlunoAPITest(TestCase):
    """Testes para a API de Aluno."""
    
    def setUp(self):
        self.user = UserFactory()
        self.tipo_aluno = TipoAlunoFactory()
        self.aluno = AlunoFactory(tipo_aluno=self.tipo_aluno)
        self.client.force_login(self.user)
    
    def test_api_lista_alunos(self):
        """Teste da API de listagem de alunos."""
        url = reverse('alunos:api_lista')
        response = self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['nome'] == self.aluno.nome
    
    def test_api_detalhe_aluno(self):
        """Teste da API de detalhes do aluno."""
        url = reverse('alunos:api_detalhe', kwargs={'pk': self.aluno.id})
        response = self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data['nome'] == self.aluno.nome
        assert data['cpf'] == self.aluno.cpf
    
    def test_api_criar_aluno(self):
        """Teste da API de criação de aluno."""
        url = reverse('alunos:api_criar')
        data = {
            'nome': 'Aluno API',
            'cpf': '555.666.777-88',
            'email': 'api@example.com',
            'telefone': '(11) 55555-5555',
            'endereco': 'Rua API, 123',
            'data_nascimento': '1990-01-01',
            'tipo_aluno': self.tipo_aluno.id
        }
        
        response = self.client.post(url, data, content_type='application/json')
        
        assert response.status_code == 201
        assert Aluno.objects.filter(nome='Aluno API').exists()
    
    def test_api_buscar_por_cpf(self):
        """Teste da API de busca por CPF."""
        url = reverse('alunos:api_buscar_cpf', kwargs={'cpf': self.aluno.cpf})
        response = self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()

