"""Testes das views do relatório Cronograma Curso × Turmas."""

from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from atividades.services.relatorios_cronograma import CronogramaFiltros
from atividades.views_ext.relatorios import _montar_descricao_filtros_cronograma


class RelatorioCronogramaViewsTest(TestCase):
    """Verifica endpoints, exportações e helpers do relatório de cronograma."""

    def setUp(self):
        """Cria usuário autenticado para os cenários de teste."""

        self.usuario = get_user_model().objects.create_user(
            username="cronograma-tester",
            email="cronograma@example.com",
            password="senha123",
        )

    def test_view_principal_autenticada(self):
        """Confere a renderização da página principal autenticada."""

        self.client.login(username="cronograma-tester", password="senha123")
        resposta = self.client.get(
            reverse("atividades:relatorio_cronograma_curso_turmas")
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Relatório Cronograma Curso × Turmas")

    def test_ajax_tabela(self):
        """Garante que a rota AJAX da tabela responde com HTML."""

        self.client.login(username="cronograma-tester", password="senha123")
        resposta = self.client.get(
            reverse("atividades:ajax_relatorio_cronograma_tabela"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("text/html", resposta.headers.get("Content-Type", ""))

    def test_ajax_opcoes(self):
        """Valida o retorno JSON das opções dinâmicas."""

        self.client.login(username="cronograma-tester", password="senha123")
        resposta = self.client.get(
            reverse("atividades:ajax_relatorio_cronograma_opcoes"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertJSONEqual(resposta.content, resposta.json())

    def test_exportacoes(self):
        """Confere exportações CSV, Excel e PDF do relatório."""

        self.client.login(username="cronograma-tester", password="senha123")
        formatos_esperados = [
            ("csv", "text/csv"),
            (
                "excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
            ("pdf", "text/html"),
        ]
        for formato, content_type in formatos_esperados:
            resposta = self.client.get(
                reverse("atividades:exportar_relatorio_cronograma", args=[formato])
            )
            self.assertEqual(resposta.status_code, 200)
            self.assertIn(content_type, resposta.headers.get("Content-Type", ""))

    def test_montar_descricao_filtros_helper(self):
        """Garante descrição amigável dos filtros aplicados."""

        opcoes = {
            "cursos": [{"id": 1, "nome": "Curso Teste"}],
            "turmas": [{"id": 2, "nome": "Turma X"}],
            "status": [{"value": "REALIZADA", "label": "Realizada"}],
            "responsaveis": [{"value": "Instrutor", "label": "Instrutor"}],
        }
        filtros = CronogramaFiltros(
            curso_id=1,
            turma_id=2,
            status="REALIZADA",
            responsavel="Instrutor",
            data_inicio=date(2025, 1, 1),
            data_fim=date(2025, 1, 31),
        )
        descricao = _montar_descricao_filtros_cronograma(filtros, opcoes)
        self.assertEqual(descricao["curso"], "Curso Teste")
        self.assertEqual(descricao["turma"], "Turma X")
        self.assertEqual(descricao["status"], "Realizada")
        self.assertEqual(descricao["responsavel"], "Instrutor")
        self.assertEqual(descricao["periodo"], "01/01/2025 a 31/01/2025")
