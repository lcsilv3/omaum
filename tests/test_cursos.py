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
 ## CursoService removido
from tests.factories import CursoFactory, UserFactory


@pytest.mark.django_db



    


@pytest.mark.django_db


@pytest.mark.django_db
class CursoViewTest(TestCase):
    """Testes para as views de Curso."""
    
    def setUp(self):
        self.user = UserFactory()
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


@pytest.mark.django_db
class CursoAPITest(TestCase):
    """Testes para a API de Curso."""
    
    def setUp(self):
        self.user = UserFactory()
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
