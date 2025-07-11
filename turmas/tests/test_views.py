from django.test import TestCase, Client
from django.urls import reverse
from turmas.models import Turma
from cursos.models import Curso


class TurmaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            nome="Curso de Teste", descricao="Descrição do curso de teste"
        )
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            curso=self.curso,
        )

    def test_listar_turmas(self):
        response = self.client.get(reverse("turmas:listar_turmas"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Turma de Teste")

    def test_criar_turma(self):
        response = self.client.post(
            reverse("turmas:criar_turma"),
            {
                "nome": "Nova Turma",
                "curso": self.curso.id,
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful creation
        self.assertTrue(Turma.objects.filter(nome="Nova Turma").exists())

    def test_atualizar_turma(self):
        response = self.client.post(
            reverse("turmas:editar_turma", args=[self.turma.id]),
            {
                "nome": "Turma Atualizada",
                "curso": self.curso.id,
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful update
        self.turma.refresh_from_db()
        self.assertEqual(self.turma.nome, "Turma Atualizada")

    def test_deletar_turma(self):
        response = self.client.post(
            reverse("turmas:excluir_turma", args=[self.turma.id])
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful deletion
        self.assertFalse(Turma.objects.filter(id=self.turma.id).exists())
