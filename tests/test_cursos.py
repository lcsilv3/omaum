"""
Testes unitários para o módulo de cursos.
"""

import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

from cursos.models import Curso
from cursos.forms import CursoForm
from cursos.services import CursoService
from tests.factories import CursoFactory, UserFactory


class TipoCursoModelTest(TestCase):
    """Testes para o modelo TipoCurso."""
    
    def setUp(self):
        self.tipo_curso = TipoCursoFactory()
    
    def test_str_representation(self):
        """Teste da representação string do TipoCurso."""
        assert str(self.tipo_curso) == self.tipo_curso.nome
    
    def test_tipo_curso_creation(self):
        """Teste da criação de TipoCurso."""
        assert self.tipo_curso.nome
        assert self.tipo_curso.ativo is True
        assert self.tipo_curso.descricao
    
    def test_tipo_curso_unique_name(self):
        """Teste da unicidade do nome do TipoCurso."""
        with pytest.raises(Exception):
            TipoCursoFactory(nome=self.tipo_curso.nome)
    
    def test_tipo_curso_deactivation(self):
        """Teste da desativação do TipoCurso."""
        self.tipo_curso.ativo = False
        self.tipo_curso.save()
        assert self.tipo_curso.ativo is False


class CursoModelTest(TestCase):
    """Testes para o modelo Curso."""
    
    def setUp(self):
        self.tipo_curso = TipoCursoFactory()
        self.curso = CursoFactory(tipo_curso=self.tipo_curso)
    
    def test_str_representation(self):
        """Teste da representação string do Curso."""
        assert str(self.curso) == self.curso.nome
    
    def test_curso_creation(self):
        """Teste da criação de Curso."""
        assert self.curso.nome
        assert self.curso.tipo_curso == self.tipo_curso
        assert self.curso.ativo is True
        assert self.curso.carga_horaria > 0
        assert self.curso.preco > 0
        assert self.curso.data_criacao
    
    def test_curso_price_validation(self):
        """Teste da validação do preço do curso."""
        curso = CursoFactory.build(preco=Decimal('-10.00'))
        with pytest.raises(ValidationError):
            curso.full_clean()
    
    def test_curso_carga_horaria_validation(self):
        """Teste da validação da carga horária."""
        curso = CursoFactory.build(carga_horaria=-5)
        with pytest.raises(ValidationError):
            curso.full_clean()
    
    def test_curso_deactivation(self):
        """Teste da desativação do curso."""
        self.curso.ativo = False
        self.curso.save()
        assert self.curso.ativo is False
    
    def test_curso_with_tipo_curso_relation(self):
        """Teste da relação com TipoCurso."""
        assert self.curso.tipo_curso.nome
        assert self.curso.tipo_curso.ativo is True


class CursoFormTest(TestCase):
    """Testes para o formulário de Curso."""
    
    def setUp(self):
        self.tipo_curso = TipoCursoFactory()
        self.valid_data = {
            'nome': 'Curso de Teste',
            'descricao': 'Descrição do curso de teste',
            'tipo_curso': self.tipo_curso.id,
            'carga_horaria': 40,
            'preco': '299.99',
            'ativo': True
        }
    
    def test_valid_form(self):
        """Teste de formulário válido."""
        form = CursoForm(data=self.valid_data)
        assert form.is_valid()
    
    def test_form_missing_required_fields(self):
        """Teste de formulário com campos obrigatórios ausentes."""
        data = self.valid_data.copy()
        del data['nome']
        form = CursoForm(data=data)
        assert not form.is_valid()
        assert 'nome' in form.errors
    
    def test_form_invalid_price(self):
        """Teste de formulário com preço inválido."""
        data = self.valid_data.copy()
        data['preco'] = '-10.00'
        form = CursoForm(data=data)
        assert not form.is_valid()
    
    def test_form_invalid_carga_horaria(self):
        """Teste de formulário com carga horária inválida."""
        data = self.valid_data.copy()
        data['carga_horaria'] = -5
        form = CursoForm(data=data)
        assert not form.is_valid()
    
    def test_form_save(self):
        """Teste de salvamento do formulário."""
        form = CursoForm(data=self.valid_data)
        assert form.is_valid()
        curso = form.save()
        assert curso.nome == self.valid_data['nome']
        assert curso.tipo_curso == self.tipo_curso


class CursoServiceTest(TestCase):
    """Testes para o serviço de Curso."""
    
    def setUp(self):
        self.tipo_curso = TipoCursoFactory()
        self.curso = CursoFactory(tipo_curso=self.tipo_curso)
        self.service = CursoService()
    
    def test_listar_cursos_ativos(self):
        """Teste da listagem de cursos ativos."""
        CursoFactory(ativo=False)  # Curso inativo
        cursos_ativos = self.service.listar_cursos_ativos()
        assert len(cursos_ativos) == 1
        assert self.curso in cursos_ativos
    
    def test_obter_curso_por_id(self):
        """Teste da obtenção de curso por ID."""
        curso = self.service.obter_curso_por_id(self.curso.id)
        assert curso == self.curso
    
    def test_obter_curso_inexistente(self):
        """Teste da obtenção de curso inexistente."""
        curso = self.service.obter_curso_por_id(99999)
        assert curso is None
    
    def test_criar_curso(self):
        """Teste da criação de curso."""
        dados = {
            'nome': 'Novo Curso',
            'descricao': 'Descrição do novo curso',
            'tipo_curso': self.tipo_curso,
            'carga_horaria': 30,
            'preco': Decimal('199.99')
        }
        
        novo_curso = self.service.criar_curso(dados)
        assert novo_curso.nome == dados['nome']
        assert novo_curso.tipo_curso == self.tipo_curso
    
    def test_atualizar_curso(self):
        """Teste da atualização de curso."""
        novos_dados = {
            'nome': 'Curso Atualizado',
            'preco': Decimal('399.99')
        }
        
        curso_atualizado = self.service.atualizar_curso(self.curso.id, novos_dados)
        assert curso_atualizado.nome == novos_dados['nome']
        assert curso_atualizado.preco == novos_dados['preco']
    
    def test_desativar_curso(self):
        """Teste da desativação de curso."""
        self.service.desativar_curso(self.curso.id)
        self.curso.refresh_from_db()
        assert self.curso.ativo is False
    
    def test_filtrar_cursos_por_tipo(self):
        """Teste da filtragem de cursos por tipo."""
        outro_tipo = TipoCursoFactory()
        CursoFactory(tipo_curso=outro_tipo)
        
        cursos_filtrados = self.service.filtrar_cursos_por_tipo(self.tipo_curso.id)
        assert len(cursos_filtrados) == 1
        assert self.curso in cursos_filtrados
    
    def test_buscar_cursos_por_nome(self):
        """Teste da busca de cursos por nome."""
        self.curso.nome = 'Curso de Python'
        self.curso.save()
        
        cursos_encontrados = self.service.buscar_cursos_por_nome('Python')
        assert len(cursos_encontrados) == 1
        assert self.curso in cursos_encontrados
    
    def test_calcular_preco_com_desconto(self):
        """Teste do cálculo de preço com desconto."""
        preco_original = self.curso.preco
        desconto = 10  # 10%
        
        preco_com_desconto = self.service.calcular_preco_com_desconto(
            self.curso.id, desconto
        )
        
        preco_esperado = preco_original * (1 - desconto / 100)
        assert preco_com_desconto == preco_esperado


class CursoViewTest(TestCase):
    """Testes para as views de Curso."""
    
    def setUp(self):
        self.user = UserFactory()
        self.tipo_curso = TipoCursoFactory()
        self.curso = CursoFactory(tipo_curso=self.tipo_curso)
        self.client.force_login(self.user)
    
    def test_lista_cursos_view(self):
        """Teste da view de listagem de cursos."""
        url = reverse('cursos:lista')
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert self.curso in response.context['cursos']
    
    def test_detalhe_curso_view(self):
        """Teste da view de detalhes do curso."""
        url = reverse('cursos:detalhe', kwargs={'pk': self.curso.id})
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert response.context['curso'] == self.curso
    
    def test_criar_curso_view_get(self):
        """Teste da view de criação de curso (GET)."""
        url = reverse('cursos:criar')
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_criar_curso_view_post(self):
        """Teste da view de criação de curso (POST)."""
        url = reverse('cursos:criar')
        data = {
            'nome': 'Novo Curso',
            'descricao': 'Descrição do novo curso',
            'tipo_curso': self.tipo_curso.id,
            'carga_horaria': 40,
            'preco': '299.99',
            'ativo': True
        }
        
        response = self.client.post(url, data)
        
        assert response.status_code == 302  # Redirect após sucesso
        assert Curso.objects.filter(nome='Novo Curso').exists()
    
    def test_editar_curso_view(self):
        """Teste da view de edição de curso."""
        url = reverse('cursos:editar', kwargs={'pk': self.curso.id})
        data = {
            'nome': 'Curso Editado',
            'descricao': self.curso.descricao,
            'tipo_curso': self.tipo_curso.id,
            'carga_horaria': self.curso.carga_horaria,
            'preco': str(self.curso.preco),
            'ativo': True
        }
        
        response = self.client.post(url, data)
        
        assert response.status_code == 302
        self.curso.refresh_from_db()
        assert self.curso.nome == 'Curso Editado'
    
    def test_deletar_curso_view(self):
        """Teste da view de exclusão de curso."""
        url = reverse('cursos:deletar', kwargs={'pk': self.curso.id})
        response = self.client.post(url)
        
        assert response.status_code == 302
        self.curso.refresh_from_db()
        assert self.curso.ativo is False
    
    def test_buscar_cursos_view(self):
        """Teste da view de busca de cursos."""
        url = reverse('cursos:buscar')
        response = self.client.get(url, {'q': self.curso.nome[:5]})
        
        assert response.status_code == 200
        assert self.curso in response.context['cursos']
    
    def test_filtrar_cursos_por_tipo_view(self):
        """Teste da view de filtro por tipo."""
        url = reverse('cursos:filtrar_por_tipo')
        response = self.client.get(url, {'tipo': self.tipo_curso.id})
        
        assert response.status_code == 200
        assert self.curso in response.context['cursos']


class CursoAPITest(TestCase):
    """Testes para a API de Curso."""
    
    def setUp(self):
        self.user = UserFactory()
        self.tipo_curso = TipoCursoFactory()
        self.curso = CursoFactory(tipo_curso=self.tipo_curso)
        self.client.force_login(self.user)
    
    def test_api_lista_cursos(self):
        """Teste da API de listagem de cursos."""
        url = reverse('cursos:api_lista')
        response = self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['nome'] == self.curso.nome
    
    def test_api_detalhe_curso(self):
        """Teste da API de detalhes do curso."""
        url = reverse('cursos:api_detalhe', kwargs={'pk': self.curso.id})
        response = self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data['nome'] == self.curso.nome
        assert data['preco'] == str(self.curso.preco)
    
    def test_api_criar_curso(self):
        """Teste da API de criação de curso."""
        url = reverse('cursos:api_criar')
        data = {
            'nome': 'Curso API',
            'descricao': 'Curso criado via API',
            'tipo_curso': self.tipo_curso.id,
            'carga_horaria': 30,
            'preco': '199.99'
        }
        
        response = self.client.post(url, data, content_type='application/json')
        
        assert response.status_code == 201
        assert Curso.objects.filter(nome='Curso API').exists()


@pytest.mark.django_db
class CursoIntegrationTest:
    """Testes de integração para Curso."""
    
    def test_fluxo_completo_curso(self):
        """Teste do fluxo completo de curso."""
        # Criar tipo de curso
        tipo_curso = TipoCursoFactory()
        
        # Criar curso
        curso = CursoFactory(tipo_curso=tipo_curso)
        
        # Verificar criação
        assert Curso.objects.filter(id=curso.id).exists()
        
        # Atualizar curso
        curso.nome = 'Curso Atualizado'
        curso.save()
        
        # Verificar atualização
        curso.refresh_from_db()
        assert curso.nome == 'Curso Atualizado'
        
        # Desativar curso
        curso.ativo = False
        curso.save()
        
        # Verificar desativação
        curso.refresh_from_db()
        assert curso.ativo is False
    
    def test_relacionamento_tipo_curso(self):
        """Teste do relacionamento com TipoCurso."""
        tipo_curso = TipoCursoFactory()
        cursos = CursoFactory.create_batch(3, tipo_curso=tipo_curso)
        
        # Verificar relacionamento
        assert tipo_curso.curso_set.count() == 3
        for curso in cursos:
            assert curso.tipo_curso == tipo_curso
    
    def test_performance_listagem_cursos(self):
        """Teste de performance na listagem de cursos."""
        import time
        
        # Criar muitos cursos
        CursoFactory.create_batch(100)
        
        # Medir tempo de listagem
        start_time = time.time()
        cursos = list(Curso.objects.select_related('tipo_curso').all())
        end_time = time.time()
        
        # Verificar que a consulta é rápida (< 1 segundo)
        assert end_time - start_time < 1.0
        assert len(cursos) == 100
