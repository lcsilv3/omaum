from django.test import TestCase
from django.urls import reverse, resolve
from cursos.views import listar_cursos, criar_curso, detalhar_curso, editar_curso, excluir_curso

class CursoUrlsTest(TestCase):
    """Testes para as URLs do aplicativo cursos"""
    
    def test_listar_cursos_url(self):
        """Teste da URL de listagem de cursos"""
        url = reverse('cursos:listar_cursos')
        self.assertEqual(url, '/cursos/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, listar_cursos)
    
    def test_criar_curso_url(self):
        """Teste da URL de criação de curso"""
        url = reverse('cursos:criar_curso')
        self.assertEqual(url, '/cursos/criar/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, criar_curso)
