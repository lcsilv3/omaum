"""
Testes unitários simplificados para o módulo de cursos.
"""

import pytest
from django.test import TestCase

from cursos.forms import CursoForm
from tests.factories import UserFactory


@pytest.mark.django_db
class CursoModelTest(TestCase):
    """Testes para o formulário de Curso."""

    def setUp(self):
        self.user = UserFactory()

    def test_curso_form_valid(self):
        form_data = {
            "nome": "Curso Teste",
            "descricao": "Descrição do curso",
            "ativo": True,
        }
        form = CursoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_curso_form_invalid_nome_required(self):
        form_data = {"descricao": "Descrição do curso", "ativo": True}
        form = CursoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("nome", form.errors)

    def test_curso_form_save(self):
        form_data = {
            "nome": "Curso Teste",
            "descricao": "Descrição do curso",
            "ativo": True,
        }
        form = CursoForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_valid())
        curso = form.save()
        self.assertEqual(curso.nome, "Curso Teste")
        self.assertEqual(curso.descricao, "Descrição do curso")
        self.assertTrue(curso.ativo)


@pytest.mark.django_db
class CursoViewTest(TestCase):
    """Testes para views de Curso."""

    def setUp(self):
        # ...apenas testes de formulário válidos acima...
        self.assertEqual(Curso.objects.count(), 100)

        # Teste de consulta em lote
        cursos_ativos = Curso.objects.filter(ativo=True)
        self.assertEqual(cursos_ativos.count(), 100)

        # Teste de atualização em lote
        Curso.objects.filter(nome__startswith="Curso").update(ativo=False)
        cursos_inativos = Curso.objects.filter(ativo=False)
        self.assertEqual(cursos_inativos.count(), 100)


@pytest.mark.unit
@pytest.mark.django_db
class CursoUnitTest(TestCase):
    """Testes unitários específicos para o módulo de cursos."""

    def test_curso_defaults(self):
        """Teste valores padrão do curso."""
        curso = Curso.objects.create(nome="Teste")
        self.assertTrue(curso.ativo)
        self.assertEqual(curso.descricao, "")

    def test_curso_ordering(self):
        """Teste ordenação de cursos."""
        curso1 = CursoFactory(nome="Curso Z")
        curso2 = CursoFactory(nome="Curso A")

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
            curso = Curso(nome="", descricao="Teste")
            curso.full_clean()

    def test_curso_max_length_validation(self):
        """Teste validação de tamanho máximo do nome."""
        long_name = "A" * 101  # Maior que 100 caracteres
        with self.assertRaises(ValidationError):
            curso = Curso(nome=long_name)
            curso.full_clean()
