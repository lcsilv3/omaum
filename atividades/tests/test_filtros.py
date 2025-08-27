from django.test import TestCase, Client
from django.urls import reverse
from importlib import import_module
import json


class FiltrosAtividadesAcademicasTestCase(TestCase):
    """Testes para os filtros de atividades acadêmicas."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.client = Client()

        # Obter modelos dinamicamente
        atividades_module = import_module("atividades.models")
        cursos_module = import_module("cursos.models")
        turmas_module = import_module("turmas.models")

        self.AtividadeAcademica = getattr(atividades_module, "AtividadeAcademica")
        self.Curso = getattr(cursos_module, "Curso")
        self.Turma = getattr(turmas_module, "Turma")

        # Criar dados de teste
        self.curso1 = self.Curso.objects.create(
            nome="Curso de Teste 1", codigo_curso="CT1"
        )

        self.curso2 = self.Curso.objects.create(
            nome="Curso de Teste 2", codigo_curso="CT2"
        )

        self.turma1 = self.Turma.objects.create(
            nome="Turma 1", curso=self.curso1, status="A"
        )

        self.turma2 = self.Turma.objects.create(
            nome="Turma 2", curso=self.curso2, status="A"
        )

        self.atividade1 = self.AtividadeAcademica.objects.create(
            nome="Atividade 1",
            descricao="Descrição da Atividade 1",
            curso=self.curso1,
            tipo="A",
            status="A",
        )
        self.atividade1.turmas.add(self.turma1)

        self.atividade2 = self.AtividadeAcademica.objects.create(
            nome="Atividade 2",
            descricao="Descrição da Atividade 2",
            curso=self.curso2,
            tipo="A",
            status="A",
        )
        self.atividade2.turmas.add(self.turma2)

    def test_listar_atividades_sem_filtro(self):
        """Testa a listagem de atividades sem filtros."""
        response = self.client.get(reverse("atividades:listar_atividades_academicas"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Atividade 1")
        self.assertContains(response, "Atividade 2")

    def test_filtro_por_nome(self):
        """Testa o filtro por nome."""
        response = self.client.get(
            reverse("atividades:listar_atividades_academicas"), {"q": "Atividade 1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Atividade 1")
        self.assertNotContains(response, "Atividade 2")

    def test_filtro_por_curso(self):
        """Testa o filtro por curso."""
        response = self.client.get(
            reverse("atividades:listar_atividades_academicas"),
            {"curso": self.curso1.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Atividade 1")
        self.assertNotContains(response, "Atividade 2")

    def test_filtro_por_turma(self):
        """Testa o filtro por turma."""
        response = self.client.get(
            reverse("atividades:listar_atividades_academicas"),
            {"turma": self.turma1.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Atividade 1")
        self.assertNotContains(response, "Atividade 2")

    def test_api_turmas_por_curso(self):
        """Testa a API de turmas por curso."""
        response = self.client.get(
            reverse("atividades:api_get_turmas_por_curso"), {"curso_id": self.curso1.id}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data["turmas"]), 1)
        self.assertEqual(data["turmas"][0]["nome"], "Turma 1")

    def test_api_cursos_por_turma(self):
        """Testa a API de cursos por turma."""
        response = self.client.get(
            reverse("atividades:api_get_cursos_por_turma"), {"turma_id": self.turma1.id}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data["cursos"]), 1)
        self.assertEqual(data["cursos"][0]["nome"], "Curso de Teste 1")

    def test_api_erro_id_invalido(self):
        """Testa o tratamento de erro para IDs inválidos."""
        response = self.client.get(
            reverse("atividades:api_get_turmas_por_curso"),
            {"curso_id": "abc"},  # ID inválido
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)

        response = self.client.get(
            reverse("atividades:api_get_cursos_por_turma"),
            {"turma_id": "abc"},  # ID inválido
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_api_turma_nao_encontrada(self):
        """Testa o tratamento de erro para turma não encontrada."""
        response = self.client.get(
            reverse("atividades:api_get_cursos_por_turma"),
            {"turma_id": 9999},  # ID inexistente
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn("error", data)
        self.assertEqual(data["cursos"][0]["nome"], "Curso de Teste 1")
