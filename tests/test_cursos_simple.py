"""
Testes unitários simplificados para o módulo de cursos.
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
from tests.factories import CursoFactory, UserFactory


@pytest.mark.django_db
class CursoModelTest(TestCase):
    """Testes para o modelo Curso."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = UserFactory()
        
    def test_curso_creation(self):
        """Teste criação de curso."""
        curso = CursoFactory(
            nome="Curso Teste",
            descricao="Descrição do curso teste"
        )
        self.assertEqual(curso.nome, "Curso Teste")
        self.assertEqual(curso.descricao, "Descrição do curso teste")
        self.assertTrue(curso.ativo)
        
    def test_curso_str(self):
        """Teste representação string do curso."""
        curso = CursoFactory(nome="Curso Teste")
        self.assertEqual(str(curso), "Curso Teste")
        
    def test_curso_meta(self):
        """Teste meta configurações do curso."""
        curso = CursoFactory()
        self.assertEqual(curso._meta.verbose_name, "Curso")
        self.assertEqual(curso._meta.verbose_name_plural, "Cursos")
        self.assertEqual(curso._meta.ordering, ["id"])


@pytest.mark.django_db
class CursoFormTest(TestCase):
    """Testes para o formulário de Curso."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = UserFactory()
        
    def test_curso_form_valid(self):
        """Teste formulário válido."""
        form_data = {
            'nome': 'Curso Teste',
            'descricao': 'Descrição do curso',
            'ativo': True
        }
        form = CursoForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_curso_form_invalid_nome_required(self):
        """Teste formulário inválido - nome obrigatório."""
        form_data = {
            'descricao': 'Descrição do curso',
            'ativo': True
        }
        form = CursoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        
    def test_curso_form_save(self):
        """Teste save do formulário."""
        form_data = {
            'nome': 'Curso Teste',
            'descricao': 'Descrição do curso',
            'ativo': True
        }
        form = CursoForm(data=form_data)
        self.assertTrue(form.is_valid())
        curso = form.save()
        self.assertEqual(curso.nome, 'Curso Teste')
        self.assertEqual(curso.descricao, 'Descrição do curso')
        self.assertTrue(curso.ativo)


@pytest.mark.django_db
class CursoViewTest(TestCase):
    """Testes para views de Curso."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = UserFactory()
        self.curso = CursoFactory()
        
    def test_curso_list_view(self):
        """Teste view de listagem de cursos."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('cursos:curso_list'))
        self.assertEqual(response.status_code, 200)
        
    def test_curso_detail_view(self):
        """Teste view de detalhes do curso."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('cursos:curso_detail', kwargs={'pk': self.curso.pk})
        )
        self.assertEqual(response.status_code, 200)
        
    def test_curso_create_view_get(self):
        """Teste view de criação de curso - GET."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('cursos:curso_create'))
        self.assertEqual(response.status_code, 200)
        
    def test_curso_create_view_post(self):
        """Teste view de criação de curso - POST."""
        self.client.force_login(self.user)
        data = {
            'nome': 'Novo Curso',
            'descricao': 'Descrição do novo curso',
            'ativo': True
        }
        response = self.client.post(reverse('cursos:curso_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect após sucesso
        
        # Verificar se o curso foi criado
        self.assertTrue(Curso.objects.filter(nome='Novo Curso').exists())
        
    def test_curso_update_view_get(self):
        """Teste view de atualização de curso - GET."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('cursos:curso_update', kwargs={'pk': self.curso.pk})
        )
        self.assertEqual(response.status_code, 200)
        
    def test_curso_update_view_post(self):
        """Teste view de atualização de curso - POST."""
        self.client.force_login(self.user)
        data = {
            'nome': 'Curso Atualizado',
            'descricao': 'Descrição atualizada',
            'ativo': True
        }
        response = self.client.post(
            reverse('cursos:curso_update', kwargs={'pk': self.curso.pk}), 
            data
        )
        self.assertEqual(response.status_code, 302)  # Redirect após sucesso
        
        # Verificar se o curso foi atualizado
        self.curso.refresh_from_db()
        self.assertEqual(self.curso.nome, 'Curso Atualizado')
        
    def test_curso_delete_view_get(self):
        """Teste view de exclusão de curso - GET."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('cursos:curso_delete', kwargs={'pk': self.curso.pk})
        )
        self.assertEqual(response.status_code, 200)
        
    def test_curso_delete_view_post(self):
        """Teste view de exclusão de curso - POST."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('cursos:curso_delete', kwargs={'pk': self.curso.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redirect após sucesso
        
        # Verificar se o curso foi excluído
        self.assertFalse(Curso.objects.filter(pk=self.curso.pk).exists())


@pytest.mark.django_db
class CursoIntegrationTest(TestCase):
    """Testes de integração para o módulo de cursos."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = UserFactory()
        
    def test_curso_crud_complete_flow(self):
        """Teste fluxo completo CRUD de curso."""
        self.client.force_login(self.user)
        
        # Criar curso
        data = {
            'nome': 'Curso Integração',
            'descricao': 'Descrição para teste de integração',
            'ativo': True
        }
        response = self.client.post(reverse('cursos:curso_create'), data)
        self.assertEqual(response.status_code, 302)
        
        # Verificar se foi criado
        curso = Curso.objects.get(nome='Curso Integração')
        self.assertEqual(curso.descricao, 'Descrição para teste de integração')
        
        # Listar cursos
        response = self.client.get(reverse('cursos:curso_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Curso Integração')
        
        # Visualizar detalhes
        response = self.client.get(
            reverse('cursos:curso_detail', kwargs={'pk': curso.pk})
        )
        self.assertEqual(response.status_code, 200)
        
        # Atualizar curso
        data_update = {
            'nome': 'Curso Integração Atualizado',
            'descricao': 'Descrição atualizada',
            'ativo': True
        }
        response = self.client.post(
            reverse('cursos:curso_update', kwargs={'pk': curso.pk}), 
            data_update
        )
        self.assertEqual(response.status_code, 302)
        
        # Verificar atualização
        curso.refresh_from_db()
        self.assertEqual(curso.nome, 'Curso Integração Atualizado')
        
        # Excluir curso
        response = self.client.post(
            reverse('cursos:curso_delete', kwargs={'pk': curso.pk})
        )
        self.assertEqual(response.status_code, 302)
        
        # Verificar exclusão
        self.assertFalse(Curso.objects.filter(pk=curso.pk).exists())
        
    def test_performance_listagem_cursos(self):
        """Teste de performance para listagem de cursos."""
        # Criar vários cursos
        cursos = [CursoFactory() for _ in range(50)]
        
        self.client.force_login(self.user)
        
        # Medir tempo de resposta
        import time
        start_time = time.time()
        
        response = self.client.get(reverse('cursos:curso_list'))
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Verificar se a resposta é rápida (menos de 1 segundo)
        self.assertLess(response_time, 1.0)
        self.assertEqual(response.status_code, 200)
        
        # Verificar se todos os cursos estão na página
        self.assertEqual(len(response.context['object_list']), 50)


# Testes de marcação para diferentes tipos
@pytest.mark.django_db
class CursoSlowTest(TestCase):
    """Testes mais lentos para o módulo de cursos."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = UserFactory()
        
    @pytest.mark.slow
    def test_curso_bulk_operations(self):
        """Teste operações em lote com muitos cursos."""
        # Criar 100 cursos
        cursos = []
        for i in range(100):
            cursos.append(CursoFactory(nome=f'Curso {i}'))
        
        # Verificar se todos foram criados
        self.assertEqual(Curso.objects.count(), 100)
        
        # Teste de consulta em lote
        cursos_ativos = Curso.objects.filter(ativo=True)
        self.assertEqual(cursos_ativos.count(), 100)
        
        # Teste de atualização em lote
        Curso.objects.filter(nome__startswith='Curso').update(ativo=False)
        cursos_inativos = Curso.objects.filter(ativo=False)
        self.assertEqual(cursos_inativos.count(), 100)


@pytest.mark.unit
@pytest.mark.django_db
class CursoUnitTest(TestCase):
    """Testes unitários específicos para o módulo de cursos."""
    
    def test_curso_defaults(self):
        """Teste valores padrão do curso."""
        curso = Curso.objects.create(nome='Teste')
        self.assertTrue(curso.ativo)
        self.assertEqual(curso.descricao, '')
        
    def test_curso_ordering(self):
        """Teste ordenação de cursos."""
        curso1 = CursoFactory(nome='Curso Z')
        curso2 = CursoFactory(nome='Curso A')
        
        cursos = Curso.objects.all()
        # Ordenação por ID (primeiro criado vem primeiro)
        self.assertEqual(cursos.first(), curso1)
        self.assertEqual(cursos.last(), curso2)


@pytest.mark.critical
@pytest.mark.django_db
class CursoCriticalTest(TestCase):
    """Testes críticos para o módulo de cursos."""
    
    def test_curso_cannot_be_empty_name(self):
        """Teste que nome não pode ser vazio."""
        with self.assertRaises(ValidationError):
            curso = Curso(nome='', descricao='Teste')
            curso.full_clean()
            
    def test_curso_max_length_validation(self):
        """Teste validação de tamanho máximo do nome."""
        long_name = 'A' * 101  # Maior que 100 caracteres
        with self.assertRaises(ValidationError):
            curso = Curso(nome=long_name)
            curso.full_clean()
