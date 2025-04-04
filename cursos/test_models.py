from django.test import TestCase
from django.core.exceptions import ValidationError
from cursos.models import Curso

class CursoModelTest(TestCase):
    """Testes para o modelo Curso"""
    
    def test_criar_curso_com_dados_validos(self):
        """Teste de criação de curso com dados válidos"""
        curso = Curso.objects.create(
            codigo_curso=101,
            nome="Curso de Teste",
            descricao="Descrição do curso de teste",
            duracao=6
        )
        self.assertEqual(curso.nome, "Curso de Teste")
        self.assertEqual(curso.codigo_curso, 101)
        self.assertEqual(curso.duracao, 6)
        self.assertEqual(curso.descricao, "Descrição do curso de teste")
    
    def test_str_representation(self):
        """Teste da representação string do modelo"""
        curso = Curso.objects.create(
            codigo_curso=102,
            nome="Curso de Python",
            descricao="Aprenda Python do zero",
            duracao=3
        )
        self.assertEqual(str(curso), "102 - Curso de Python")
    
    def test_ordering(self):
        """Teste para verificar a ordenação dos cursos"""
        Curso.objects.create(codigo_curso=105, nome="Curso Z", duracao=6)
        Curso.objects.create(codigo_curso=103, nome="Curso A", duracao=6)
        Curso.objects.create(codigo_curso=104, nome="Curso M", duracao=6)
        
        cursos = Curso.objects.all()
        self.assertEqual(cursos[0].codigo_curso, 103)  # Primeiro curso (ordenado por codigo_curso)
        self.assertEqual(cursos[1].codigo_curso, 104)  # Segundo curso
        self.assertEqual(cursos[2].codigo_curso, 105)  # Terceiro curso
