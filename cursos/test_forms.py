from django.test import TestCase
from cursos.forms import CursoForm

class CursoFormTest(TestCase):
    """Testes para o formulário CursoForm"""
    
    def test_form_valid(self):
        """Teste com dados válidos no formulário"""
        form_data = {
            'codigo_curso': 201,
            'nome': 'Curso de Teste',
            'descricao': 'Descrição do curso de teste',
            'duracao': 6
        }
        form = CursoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_codigo_negativo(self):
        """Teste com código de curso negativo (inválido)"""
        form_data = {
            'codigo_curso': -1,
            'nome': 'Curso de Teste',
            'descricao': 'Descrição do curso de teste',
            'duracao': 6
        }
        form = CursoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('codigo_curso', form.errors)
    
    def test_form_campos_obrigatorios(self):
        """Teste para verificar campos obrigatórios"""
        form_data = {}  # Formulário vazio
        form = CursoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('codigo_curso', form.errors)
        self.assertIn('nome', form.errors)
        self.assertIn('duracao', form.errors)
