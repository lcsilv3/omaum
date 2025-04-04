# Código da Funcionalidade: turmas - Parte 3/3
*Gerado automaticamente*



## turmas\tests\test_views.py

python
from django.test import TestCase, Client
from django.urls import reverse
from turmas.models import Turma
from cursos.models import Curso
from datetime import date

class TurmaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )
        self.turma = Turma.objects.create(
            nome='Turma de Teste',
            curso=self.curso,
            data_inicio=date(2023, 10, 1),
            data_fim=date(2023, 12, 31)
        )

    def test_listar_turmas(self):
        response = self.client.get(reverse('turmas:turma_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Turma de Teste')
        self.assertContains(response, 'Curso de Teste')

    def test_criar_turma(self):
        response = self.client.post(reverse('turmas:turma_create'), {
            'nome': 'Nova Turma',
            'curso': self.curso.id,
            'data_inicio': '2024-01-01',
            'data_fim': '2024-03-31'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Turma.objects.filter(nome='Nova Turma').exists())

    def test_atualizar_turma(self):
        response = self.client.post(reverse('turmas:turma_update', args=[self.turma.id]), {
            'nome': 'Turma Atualizada',
            'curso': self.curso.id,
            'data_inicio': '2023-11-01',
            'data_fim': '2024-01-31'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.turma.refresh_from_db()
        self.assertEqual(self.turma.nome, 'Turma Atualizada')

    def test_deletar_turma(self):
        response = self.client.post(reverse('turmas:turma_delete', args=[self.turma.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Turma.objects.filter(id=self.turma.id).exists())

class CursoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            nome='Curso de Teste',
            descricao='Descrição do curso de teste'
        )

    def test_listar_cursos(self):
        response = self.client.get(reverse('turmas:curso_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Curso de Teste')

    def test_criar_curso(self):
        response = self.client.post(reverse('turmas:curso_create'), {
            'nome': 'Novo Curso',
            'descricao': 'Descrição do novo curso'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Curso.objects.filter(nome='Novo Curso').exists())

    def test_atualizar_curso(self):
        response = self.client.post(reverse('turmas:curso_update', args=[self.curso.id]), {
            'nome': 'Curso Atualizado',
            'descricao': 'Descrição atualizada'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.curso.refresh_from_db()
        self.assertEqual(self.curso.nome, 'Curso Atualizado')

    def test_deletar_curso(self):
        response = self.client.post(reverse('turmas:curso_delete', args=[self.curso.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Curso.objects.filter(id=self.curso.id).exists())



