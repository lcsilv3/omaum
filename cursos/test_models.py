from django.test import TestCase
from cursos.models import Curso


class CursoModelTest(TestCase):
    """Testes para o modelo Curso"""

    def test_criar_curso_com_dados_validos(self):
        """Teste de criação de curso com dados válidos"""
        curso = Curso.objects.create(
            nome="Curso de Teste",
            descricao="Descrição do curso de teste",
        )
        self.assertEqual(curso.nome, "Curso de Teste")
        self.assertEqual(curso.descricao, "Descrição do curso de teste")

    def test_str_representation(self):
        """Teste da representação string do modelo"""
        curso = Curso.objects.create(
            nome="Curso de Python",
            descricao="Aprenda Python do zero",
        )
        self.assertEqual(str(curso), "Curso de Python")

    # Removidas referências a codigo_curso e duracao dos testes
    # Ajustado para refletir apenas os campos atuais do modelo Curso
