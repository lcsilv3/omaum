from django.test import TestCase
from cursos.forms import CursoForm


class CursoFormTest(TestCase):
    """Testes para o formulário CursoForm"""

    def test_form_valid(self):
        """Teste com dados válidos no formulário"""
        form_data = {
            "nome": "Curso de Teste",
            "descricao": "Descrição do curso de teste",
        }
        form = CursoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_campos_obrigatorios(self):
        """Teste para verificar campos obrigatórios"""
        form_data = {}  # Formulário vazio
        form = CursoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("nome", form.errors)
