"""
Testes unitários para o módulo de matrículas.
"""

import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date, timedelta
from django.utils import timezone

from matriculas.models import Matricula, StatusMatricula
from matriculas.forms import MatriculaForm
from matriculas.services import MatriculaService
from tests.factories import (
    MatriculaFactory, StatusMatriculaFactory, AlunoFactory, 
    CursoFactory, UserFactory
)


class StatusMatriculaModelTest(TestCase):
    """Testes para o modelo StatusMatricula."""
    
    def setUp(self):
        self.status_matricula = StatusMatriculaFactory()
    
    def test_str_representation(self):
        """Teste da representação string do StatusMatricula."""
        assert str(self.status_matricula) == self.status_matricula.nome
    
    def test_status_matricula_creation(self):
        """Teste da criação de StatusMatricula."""
        assert self.status_matricula.nome
        assert self.status_matricula.ativo is True
        assert self.status_matricula.descricao
    
    def test_status_matricula_unique_name(self):
        """Teste da unicidade do nome do StatusMatricula."""
        with pytest.raises(Exception):
            StatusMatriculaFactory(nome=self.status_matricula.nome)
    
    def test_status_matricula_deactivation(self):
        """Teste da desativação do StatusMatricula."""
        self.status_matricula.ativo = False
        self.status_matricula.save()
        assert self.status_matricula.ativo is False


class MatriculaModelTest(TestCase):
    """Testes para o modelo Matricula."""
    
    def setUp(self):
        self.aluno = AlunoFactory()
        self.curso = CursoFactory()
        self.status = StatusMatriculaFactory()
        self.matricula = MatriculaFactory(
            aluno=self.aluno,
            curso=self.curso,
            status=self.status
        )
    
    def test_str_representation(self):
        """Teste da representação string da Matricula."""
        expected = f"{self.aluno.nome} - {self.curso.nome}"
        assert str(self.matricula) == expected
    
    def test_matricula_creation(self):
        """Teste da criação de Matricula."""
        assert self.matricula.aluno == self.aluno
        assert self.matricula.curso == self.curso
        assert self.matricula.status == self.status
        assert self.matricula.data_matricula
        assert self.matricula.ativo is True
        assert self.matricula.valor_pago >= 0
    
    def test_matricula_unique_aluno_curso(self):
        """Teste da unicidade aluno-curso."""
        with pytest.raises(Exception):
            MatriculaFactory(aluno=self.aluno, curso=self.curso)
    
    def test_matricula_valor_pago_validation(self):
        """Teste da validação do valor pago."""
        matricula = MatriculaFactory.build(valor_pago=Decimal('-10.00'))
        with pytest.raises(ValidationError):
            matricula.full_clean()
    
    def test_matricula_deactivation(self):
        """Teste da desativação da matrícula."""
        self.matricula.ativo = False
        self.matricula.save()
        assert self.matricula.ativo is False
    
    def test_matricula_com_observacoes(self):
        """Teste da matrícula com observações."""
        observacoes = "Aluno com desconto especial"
        matricula = MatriculaFactory(observacoes=observacoes)
        assert matricula.observacoes == observacoes
    
    def test_matricula_valor_pendente(self):
        """Teste do cálculo do valor pendente."""
        valor_curso = self.curso.preco
        valor_pago = Decimal('100.00')
        
        matricula = MatriculaFactory(
            curso=self.curso,
            valor_pago=valor_pago
        )
        
        valor_pendente = valor_curso - valor_pago
        assert matricula.valor_pendente == valor_pendente


class MatriculaFormTest(TestCase):
    """Testes para o formulário de Matricula."""
    
    def setUp(self):
        self.aluno = AlunoFactory()
        self.curso = CursoFactory()
        self.status = StatusMatriculaFactory()
        self.valid_data = {
            'aluno': self.aluno.id,
            'curso': self.curso.id,
            'status': self.status.id,
            'data_matricula': timezone.now().date(),
            'valor_pago': '299.99',
            'observacoes': 'Matrícula de teste',
            'ativo': True
        }
    
    def test_valid_form(self):
        """Teste de formulário válido."""
        form = MatriculaForm(data=self.valid_data)
        assert form.is_valid()
    
    def test_form_missing_required_fields(self):
        """Teste de formulário com campos obrigatórios ausentes."""
        data = self.valid_data.copy()
        del data['aluno']
        form = MatriculaForm(data=data)
        assert not form.is_valid()
        assert 'aluno' in form.errors
    
    def test_form_invalid_valor_pago(self):
        """Teste de formulário com valor pago inválido."""
        data = self.valid_data.copy()
        data['valor_pago'] = '-10.00'
        form = MatriculaForm(data=data)
        assert not form.is_valid()
    
    def test_form_save(self):
        """Teste de salvamento do formulário."""
        form = MatriculaForm(data=self.valid_data)
        assert form.is_valid()
        matricula = form.save()
        assert matricula.aluno == self.aluno
        assert matricula.curso == self.curso
        assert matricula.status == self.status
    
    def test_form_duplicate_matricula(self):
        """Teste de formulário com matrícula duplicada."""
        # Criar primeira matrícula
        MatriculaFactory(aluno=self.aluno, curso=self.curso)
        
        # Tentar criar segunda matrícula com mesmo aluno e curso
        form = MatriculaForm(data=self.valid_data)
        assert not form.is_valid()


class MatriculaServiceTest(TestCase):
    """Testes para o serviço de Matricula."""
    
    def setUp(self):
        self.aluno = AlunoFactory()
        self.curso = CursoFactory()
        self.status = StatusMatriculaFactory()
        self.matricula = MatriculaFactory(
            aluno=self.aluno,
            curso=self.curso,
            status=self.status
        )
        self.service = MatriculaService()
    
    def test_listar_matriculas_ativas(self):
        """Teste da listagem de matrículas ativas."""
        MatriculaFactory(ativo=False)  # Matrícula inativa
        matriculas_ativas = self.service.listar_matriculas_ativas()
        assert len(matriculas_ativas) == 1
        assert self.matricula in matriculas_ativas
    
    def test_obter_matricula_por_id(self):
        """Teste da obtenção de matrícula por ID."""
        matricula = self.service.obter_matricula_por_id(self.matricula.id)
        assert matricula == self.matricula
    
    def test_obter_matricula_inexistente(self):
        """Teste da obtenção de matrícula inexistente."""
        matricula = self.service.obter_matricula_por_id(99999)
        assert matricula is None
    
    def test_criar_matricula(self):
        """Teste da criação de matrícula."""
        novo_aluno = AlunoFactory()
        novo_curso = CursoFactory()
        
        dados = {
            'aluno': novo_aluno,
            'curso': novo_curso,
            'status': self.status,
            'valor_pago': Decimal('199.99'),
            'observacoes': 'Nova matrícula'
        }
        
        nova_matricula = self.service.criar_matricula(dados)
        assert nova_matricula.aluno == novo_aluno
        assert nova_matricula.curso == novo_curso
        assert nova_matricula.status == self.status
    
    def test_atualizar_matricula(self):
        """Teste da atualização de matrícula."""
        novo_status = StatusMatriculaFactory(nome='Concluída')
        novos_dados = {
            'status': novo_status,
            'valor_pago': Decimal('399.99'),
            'observacoes': 'Matrícula atualizada'
        }
        
        matricula_atualizada = self.service.atualizar_matricula(
            self.matricula.id, novos_dados
        )
        assert matricula_atualizada.status == novo_status
        assert matricula_atualizada.valor_pago == novos_dados['valor_pago']
    
    def test_desativar_matricula(self):
        """Teste da desativação de matrícula."""
        self.service.desativar_matricula(self.matricula.id)
        self.matricula.refresh_from_db()
        assert self.matricula.ativo is False
    
    def test_obter_matriculas_por_aluno(self):
        """Teste da obtenção de matrículas por aluno."""
        # Criar mais uma matrícula para o mesmo aluno
        outro_curso = CursoFactory()
        MatriculaFactory(aluno=self.aluno, curso=outro_curso)
        
        matriculas = self.service.obter_matriculas_por_aluno(self.aluno.id)
        assert len(matriculas) == 2
        assert self.matricula in matriculas
    
    def test_obter_matriculas_por_curso(self):
        """Teste da obtenção de matrículas por curso."""
        # Criar mais uma matrícula para o mesmo curso
        outro_aluno = AlunoFactory()
        MatriculaFactory(aluno=outro_aluno, curso=self.curso)
        
        matriculas = self.service.obter_matriculas_por_curso(self.curso.id)
        assert len(matriculas) == 2
        assert self.matricula in matriculas
    
    def test_obter_matriculas_por_status(self):
        """Teste da obtenção de matrículas por status."""
        # Criar matrícula com status diferente
        outro_status = StatusMatriculaFactory()
        MatriculaFactory(status=outro_status)
        
        matriculas = self.service.obter_matriculas_por_status(self.status.id)
        assert len(matriculas) == 1
        assert self.matricula in matriculas
    
    def test_calcular_valor_pendente(self):
        """Teste do cálculo do valor pendente."""
        valor_pendente = self.service.calcular_valor_pendente(self.matricula.id)
        expected = self.curso.preco - self.matricula.valor_pago
        assert valor_pendente == expected
    
    def test_obter_estatisticas_matriculas(self):
        """Teste da obtenção de estatísticas de matrículas."""
        # Criar mais algumas matrículas
        MatriculaFactory.create_batch(3, ativo=True)
        MatriculaFactory.create_batch(2, ativo=False)
        
        stats = self.service.obter_estatisticas_matriculas()
        assert stats['total'] == 6  # 1 inicial + 3 + 2
        assert stats['ativas'] == 4  # 1 inicial + 3
        assert stats['inativas'] == 2
    
    def test_verificar_matricula_existe(self):
        """Teste da verificação se matrícula existe."""
        existe = self.service.verificar_matricula_existe(
            self.aluno.id, self.curso.id
        )
        assert existe is True
        
        outro_aluno = AlunoFactory()
        nao_existe = self.service.verificar_matricula_existe(
            outro_aluno.id, self.curso.id
        )
        assert nao_existe is False


class MatriculaViewTest(TestCase):
    """Testes para as views de Matricula."""
    
    def setUp(self):
        self.user = UserFactory()
        self.aluno = AlunoFactory()
        self.curso = CursoFactory()
        self.status = StatusMatriculaFactory()
        self.matricula = MatriculaFactory(
            aluno=self.aluno,
            curso=self.curso,
            status=self.status
        )
        self.client.force_login(self.user)
    
    def test_lista_matriculas_view(self):
        """Teste da view de listagem de matrículas."""
        url = reverse('matriculas:lista')
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert self.matricula in response.context['matriculas']
    
    def test_detalhe_matricula_view(self):
        """Teste da view de detalhes da matrícula."""
        url = reverse('matriculas:detalhe', kwargs={'pk': self.matricula.id})
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert response.context['matricula'] == self.matricula
    
    def test_criar_matricula_view_get(self):
        """Teste da view de criação de matrícula (GET)."""
        url = reverse('matriculas:criar')
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_criar_matricula_view_post(self):
        """Teste da view de criação de matrícula (POST)."""
        novo_aluno = AlunoFactory()
        novo_curso = CursoFactory()
        
        url = reverse('matriculas:criar')
        data = {
            'aluno': novo_aluno.id,
            'curso': novo_curso.id,
            'status': self.status.id,
            'data_matricula': timezone.now().date(),
            'valor_pago': '199.99',
            'observacoes': 'Nova matrícula',
            'ativo': True
        }
        
        response = self.client.post(url, data)
        
        assert response.status_code == 302  # Redirect após sucesso
        assert Matricula.objects.filter(
            aluno=novo_aluno, curso=novo_curso
        ).exists()
    
    def test_editar_matricula_view(self):
        """Teste da view de edição de matrícula."""
        url = reverse('matriculas:editar', kwargs={'pk': self.matricula.id})
        data = {
            'aluno': self.aluno.id,
            'curso': self.curso.id,
            'status': self.status.id,
            'data_matricula': self.matricula.data_matricula.strftime('%Y-%m-%d'),
            'valor_pago': '399.99',
            'observacoes': 'Matrícula editada',
            'ativo': True
        }
        
        response = self.client.post(url, data)
        
        assert response.status_code == 302
        self.matricula.refresh_from_db()
        assert self.matricula.valor_pago == Decimal('399.99')
    
    def test_deletar_matricula_view(self):
        """Teste da view de exclusão de matrícula."""
        url = reverse('matriculas:deletar', kwargs={'pk': self.matricula.id})
        response = self.client.post(url)
        
        assert response.status_code == 302
        self.matricula.refresh_from_db()
        assert self.matricula.ativo is False
    
    def test_filtrar_matriculas_por_aluno_view(self):
        """Teste da view de filtro por aluno."""
        url = reverse('matriculas:filtrar_por_aluno')
        response = self.client.get(url, {'aluno': self.aluno.id})
        
        assert response.status_code == 200
        assert self.matricula in response.context['matriculas']
    
    def test_filtrar_matriculas_por_curso_view(self):
        """Teste da view de filtro por curso."""
        url = reverse('matriculas:filtrar_por_curso')
        response = self.client.get(url, {'curso': self.curso.id})
        
        assert response.status_code == 200
        assert self.matricula in response.context['matriculas']
    
    def test_verificar_matricula_existe_view(self):
        """Teste da view de verificação de matrícula existente."""
        url = reverse('matriculas:verificar_existe')
        response = self.client.get(url, {
            'aluno': self.aluno.id,
            'curso': self.curso.id
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data['exists'] is True


class MatriculaAPITest(TestCase):
    """Testes para a API de Matricula."""
    
    def setUp(self):
        self.user = UserFactory()
        self.aluno = AlunoFactory()
        self.curso = CursoFactory()
        self.status = StatusMatriculaFactory()
        self.matricula = MatriculaFactory(
            aluno=self.aluno,
            curso=self.curso,
            status=self.status
        )
        self.client.force_login(self.user)
    
    def test_api_lista_matriculas(self):
        """Teste da API de listagem de matrículas."""
        url = reverse('matriculas:api_lista')
        response = self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['id'] == self.matricula.id
    
    def test_api_detalhe_matricula(self):
        """Teste da API de detalhes da matrícula."""
        url = reverse('matriculas:api_detalhe', kwargs={'pk': self.matricula.id})
        response = self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == self.matricula.id
        assert data['aluno'] == self.aluno.nome
        assert data['curso'] == self.curso.nome
    
    def test_api_criar_matricula(self):
        """Teste da API de criação de matrícula."""
        novo_aluno = AlunoFactory()
        novo_curso = CursoFactory()
        
        url = reverse('matriculas:api_criar')
        data = {
            'aluno': novo_aluno.id,
            'curso': novo_curso.id,
            'status': self.status.id,
            'valor_pago': '199.99',
            'observacoes': 'Matrícula via API'
        }
        
        response = self.client.post(url, data, content_type='application/json')
        
        assert response.status_code == 201
        assert Matricula.objects.filter(
            aluno=novo_aluno, curso=novo_curso
        ).exists()
    
    def test_api_estatisticas_matriculas(self):
        """Teste da API de estatísticas de matrículas."""
        url = reverse('matriculas:api_estatisticas')
        response = self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert 'total' in data
        assert 'ativas' in data
        assert 'inativas' in data


@pytest.mark.django_db
class MatriculaIntegrationTest:
    """Testes de integração para Matricula."""
    
    def test_fluxo_completo_matricula(self):
        """Teste do fluxo completo de matrícula."""
        # Criar dependências
        aluno = AlunoFactory()
        curso = CursoFactory()
        status = StatusMatriculaFactory()
        
        # Criar matrícula
        matricula = MatriculaFactory(
            aluno=aluno,
            curso=curso,
            status=status
        )
        
        # Verificar criação
        assert Matricula.objects.filter(id=matricula.id).exists()
        
        # Atualizar matrícula
        novo_status = StatusMatriculaFactory(nome='Concluída')
        matricula.status = novo_status
        matricula.save()
        
        # Verificar atualização
        matricula.refresh_from_db()
        assert matricula.status == novo_status
        
        # Desativar matrícula
        matricula.ativo = False
        matricula.save()
        
        # Verificar desativação
        matricula.refresh_from_db()
        assert matricula.ativo is False
    
    def test_relacionamentos_matricula(self):
        """Teste dos relacionamentos da matrícula."""
        aluno = AlunoFactory()
        curso = CursoFactory()
        status = StatusMatriculaFactory()
        
        matricula = MatriculaFactory(
            aluno=aluno,
            curso=curso,
            status=status
        )
        
        # Verificar relacionamentos
        assert matricula.aluno == aluno
        assert matricula.curso == curso
        assert matricula.status == status
        
        # Verificar relacionamentos reversos
        assert aluno.matricula_set.count() == 1
        assert curso.matricula_set.count() == 1
        assert status.matricula_set.count() == 1
    
    def test_unicidade_aluno_curso(self):
        """Teste da unicidade aluno-curso."""
        aluno = AlunoFactory()
        curso = CursoFactory()
        
        # Criar primeira matrícula
        MatriculaFactory(aluno=aluno, curso=curso)
        
        # Tentar criar segunda matrícula com mesmo aluno e curso
        with pytest.raises(Exception):
            MatriculaFactory(aluno=aluno, curso=curso)
    
    def test_performance_listagem_matriculas(self):
        """Teste de performance na listagem de matrículas."""
        import time
        
        # Criar muitas matrículas
        MatriculaFactory.create_batch(100)
        
        # Medir tempo de listagem
        start_time = time.time()
        matriculas = list(Matricula.objects.select_related(
            'aluno', 'curso', 'status'
        ).all())
        end_time = time.time()
        
        # Verificar que a consulta é rápida (< 1 segundo)
        assert end_time - start_time < 1.0
        assert len(matriculas) == 100
    
    def test_calculo_valor_pendente(self):
        """Teste do cálculo do valor pendente."""
        curso = CursoFactory(preco=Decimal('500.00'))
        matricula = MatriculaFactory(
            curso=curso,
            valor_pago=Decimal('200.00')
        )
        
        valor_pendente = curso.preco - matricula.valor_pago
        assert valor_pendente == Decimal('300.00')
        
        # Testar com valor pago igual ao preço do curso
        matricula.valor_pago = curso.preco
        matricula.save()
        
        valor_pendente = curso.preco - matricula.valor_pago
        assert valor_pendente == Decimal('0.00')
