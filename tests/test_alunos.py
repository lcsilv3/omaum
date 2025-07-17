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

from alunos.models import Aluno, TipoAluno
from alunos.forms import AlunoForm
from alunos.services import AlunoService
from tests.factories import AlunoFactory, TipoAlunoFactory, UserFactory


class TipoAlunoModelTest(TestCase):
    """Testes para o modelo TipoAluno."""
    
    def setUp(self):
        self.tipo_aluno = TipoAlunoFactory()
    
    def test_str_representation(self):
        """Teste da representação string do TipoAluno."""
        assert str(self.tipo_aluno) == self.tipo_aluno.nome
    
    def test_tipo_aluno_creation(self):
        """Teste da criação de TipoAluno."""
        assert self.tipo_aluno.nome
        assert self.tipo_aluno.ativo is True
        assert self.tipo_aluno.descricao
    
    def test_tipo_aluno_unique_name(self):
        """Teste da unicidade do nome do TipoAluno."""
        with pytest.raises(Exception):
            TipoAlunoFactory(nome=self.tipo_aluno.nome)
    
    def test_tipo_aluno_deactivation(self):
        """Teste da desativação do TipoAluno."""
        self.tipo_aluno.ativo = False
        self.tipo_aluno.save()
        assert self.tipo_aluno.ativo is False


class AlunoModelTest(TestCase):
    """Testes para o modelo Aluno."""
    
    def setUp(self):
        self.tipo_aluno = TipoAlunoFactory()
        self.aluno = AlunoFactory(tipo_aluno=self.tipo_aluno)
    
    def test_str_representation(self):
        """Teste da representação string do Aluno."""
        assert str(self.aluno) == self.aluno.nome
    
    def test_aluno_creation(self):
        """Teste da criação de Aluno."""
        assert self.aluno.nome
        assert self.aluno.cpf
        assert self.aluno.email
        assert self.aluno.tipo_aluno == self.tipo_aluno
        assert self.aluno.ativo is True
        assert self.aluno.data_cadastro
        assert self.aluno.data_nascimento
    
    def test_aluno_cpf_unique(self):
        """Teste da unicidade do CPF."""
        with pytest.raises(Exception):
            AlunoFactory(cpf=self.aluno.cpf)
    
    def test_aluno_email_validation(self):
        """Teste da validação de email."""
        aluno = AlunoFactory.build(email='email_invalido')
        with pytest.raises(ValidationError):
            aluno.full_clean()
    
    def test_aluno_idade_calculation(self):
        """Teste do cálculo da idade."""
        data_nascimento = date(1990, 1, 1)
        aluno = AlunoFactory(data_nascimento=data_nascimento)
        
        idade_esperada = (date.today() - data_nascimento).days // 365
        assert aluno.idade == idade_esperada
    
    def test_aluno_deactivation(self):
        """Teste da desativação do aluno."""
        self.aluno.ativo = False
        self.aluno.save()
        assert self.aluno.ativo is False
    
    def test_aluno_with_tipo_aluno_relation(self):
        """Teste da relação com TipoAluno."""
        assert self.aluno.tipo_aluno.nome
        assert self.aluno.tipo_aluno.ativo is True
    
    def test_aluno_codigo_iniciatico(self):
        """Teste do código iniciático."""
        codigo = 'ABC123'
        aluno = AlunoFactory(codigo_iniciatico=codigo)
        assert aluno.codigo_iniciatico == codigo


class AlunoFormTest(TestCase):
    """Testes para o formulário de Aluno."""
    
    def setUp(self):
        self.tipo_aluno = TipoAlunoFactory()
        self.valid_data = {
            'nome': 'João Silva',
            'cpf': '123.456.789-00',
            'email': 'joao@example.com',
            'telefone': '(11) 99999-9999',
            'endereco': 'Rua das Flores, 123',
            'data_nascimento': '1990-01-01',
            'tipo_aluno': self.tipo_aluno.id,
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


class AlunoServiceTest(TestCase):
    """Testes para o serviço de Aluno."""
    
    def setUp(self):
        self.tipo_aluno = TipoAlunoFactory()
        self.aluno = AlunoFactory(tipo_aluno=self.tipo_aluno)
        self.service = AlunoService()
    
    def test_listar_alunos_ativos(self):
        """Teste da listagem de alunos ativos."""
        AlunoFactory(ativo=False)  # Aluno inativo
        alunos_ativos = self.service.listar_alunos_ativos()
        assert len(alunos_ativos) == 1
        assert self.aluno in alunos_ativos
    
    def test_obter_aluno_por_id(self):
        """Teste da obtenção de aluno por ID."""
        aluno = self.service.obter_aluno_por_id(self.aluno.id)
        assert aluno == self.aluno
    
    def test_obter_aluno_inexistente(self):
        """Teste da obtenção de aluno inexistente."""
        aluno = self.service.obter_aluno_por_id(99999)
        assert aluno is None
    
    def test_obter_aluno_por_cpf(self):
        """Teste da obtenção de aluno por CPF."""
        aluno = self.service.obter_aluno_por_cpf(self.aluno.cpf)
        assert aluno == self.aluno
    
    def test_obter_aluno_por_cpf_inexistente(self):
        """Teste da obtenção de aluno por CPF inexistente."""
        aluno = self.service.obter_aluno_por_cpf('999.999.999-99')
        assert aluno is None
    
    def test_criar_aluno(self):
        """Teste da criação de aluno."""
        dados = {
            'nome': 'Maria Santos',
            'cpf': '987.654.321-00',
            'email': 'maria@example.com',
            'telefone': '(11) 88888-8888',
            'endereco': 'Rua das Palmeiras, 456',
            'data_nascimento': date(1985, 5, 15),
            'tipo_aluno': self.tipo_aluno
        }
        
        novo_aluno = self.service.criar_aluno(dados)
        assert novo_aluno.nome == dados['nome']
        assert novo_aluno.cpf == dados['cpf']
        assert novo_aluno.tipo_aluno == self.tipo_aluno
    
    def test_atualizar_aluno(self):
        """Teste da atualização de aluno."""
        novos_dados = {
            'nome': 'João Santos Silva',
            'email': 'joao.santos@example.com'
        }
        
        aluno_atualizado = self.service.atualizar_aluno(self.aluno.id, novos_dados)
        assert aluno_atualizado.nome == novos_dados['nome']
        assert aluno_atualizado.email == novos_dados['email']
    
    def test_desativar_aluno(self):
        """Teste da desativação de aluno."""
        self.service.desativar_aluno(self.aluno.id)
        self.aluno.refresh_from_db()
        assert self.aluno.ativo is False
    
    def test_filtrar_alunos_por_tipo(self):
        """Teste da filtragem de alunos por tipo."""
        outro_tipo = TipoAlunoFactory()
        AlunoFactory(tipo_aluno=outro_tipo)
        
        alunos_filtrados = self.service.filtrar_alunos_por_tipo(self.tipo_aluno.id)
        assert len(alunos_filtrados) == 1
        assert self.aluno in alunos_filtrados
    
    def test_buscar_alunos_por_nome(self):
        """Teste da busca de alunos por nome."""
        alunos_encontrados = self.service.buscar_alunos_por_nome(self.aluno.nome[:3])
        assert len(alunos_encontrados) >= 1
        assert self.aluno in alunos_encontrados
    
    def test_validar_cpf_existente(self):
        """Teste da validação de CPF existente."""
        cpf_existe = self.service.validar_cpf_existente(self.aluno.cpf)
        assert cpf_existe is True
        
        cpf_nao_existe = self.service.validar_cpf_existente('999.999.999-99')
        assert cpf_nao_existe is False
    
    def test_obter_alunos_por_faixa_etaria(self):
        """Teste da obtenção de alunos por faixa etária."""
        # Criar alunos com idades diferentes
        aluno_jovem = AlunoFactory(data_nascimento=date(2000, 1, 1))
        aluno_adulto = AlunoFactory(data_nascimento=date(1980, 1, 1))
        
        alunos_jovens = self.service.obter_alunos_por_faixa_etaria(18, 25)
        alunos_adultos = self.service.obter_alunos_por_faixa_etaria(40, 45)
        
        assert aluno_jovem in alunos_jovens
        assert aluno_adulto in alunos_adultos


class AlunoViewTest(TestCase):
    """Testes para as views de Aluno."""
    
    def setUp(self):
        self.user = UserFactory()
        self.tipo_aluno = TipoAlunoFactory()
        self.aluno = AlunoFactory(tipo_aluno=self.tipo_aluno)
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
            'cpf': '111.222.333-44',
            'email': 'novo@example.com',
            'telefone': '(11) 77777-7777',
            'endereco': 'Rua Nova, 789',
            'data_nascimento': '1995-01-01',
            'tipo_aluno': self.tipo_aluno.id,
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
            'tipo_aluno': self.tipo_aluno.id,
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
        assert data['nome'] == self.aluno.nome


@pytest.mark.django_db
class AlunoIntegrationTest:
    """Testes de integração para Aluno."""
    
    def test_fluxo_completo_aluno(self):
        """Teste do fluxo completo de aluno."""
        # Criar tipo de aluno
        tipo_aluno = TipoAlunoFactory()
        
        # Criar aluno
        aluno = AlunoFactory(tipo_aluno=tipo_aluno)
        
        # Verificar criação
        assert Aluno.objects.filter(id=aluno.id).exists()
        
        # Atualizar aluno
        aluno.nome = 'Aluno Atualizado'
        aluno.save()
        
        # Verificar atualização
        aluno.refresh_from_db()
        assert aluno.nome == 'Aluno Atualizado'
        
        # Desativar aluno
        aluno.ativo = False
        aluno.save()
        
        # Verificar desativação
        aluno.refresh_from_db()
        assert aluno.ativo is False
    
    def test_relacionamento_tipo_aluno(self):
        """Teste do relacionamento com TipoAluno."""
        tipo_aluno = TipoAlunoFactory()
        alunos = AlunoFactory.create_batch(3, tipo_aluno=tipo_aluno)
        
        # Verificar relacionamento
        assert tipo_aluno.aluno_set.count() == 3
        for aluno in alunos:
            assert aluno.tipo_aluno == tipo_aluno
    
    def test_performance_listagem_alunos(self):
        """Teste de performance na listagem de alunos."""
        import time
        
        # Criar muitos alunos
        AlunoFactory.create_batch(100)
        
        # Medir tempo de listagem
        start_time = time.time()
        alunos = list(Aluno.objects.select_related('tipo_aluno').all())
        end_time = time.time()
        
        # Verificar que a consulta é rápida (< 1 segundo)
        assert end_time - start_time < 1.0
        assert len(alunos) == 100
    
    def test_validacao_cpf_unico(self):
        """Teste da validação de CPF único."""
        aluno1 = AlunoFactory()
        
        # Tentar criar aluno com mesmo CPF deve falhar
        with pytest.raises(Exception):
            AlunoFactory(cpf=aluno1.cpf)
    
    def test_codigo_iniciatico_funcionalidade(self):
        """Teste da funcionalidade de código iniciático."""
        codigo = 'INIT123'
        aluno = AlunoFactory(codigo_iniciatico=codigo)
        
        # Verificar que o código foi salvo
        assert aluno.codigo_iniciatico == codigo
        
        # Buscar aluno pelo código
        aluno_encontrado = Aluno.objects.filter(codigo_iniciatico=codigo).first()
        assert aluno_encontrado == aluno
