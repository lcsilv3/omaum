"""Testes das views relacionadas ao relatório de frequência."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from atividades.services.relatorios_frequencia import FrequenciaFiltros
from atividades.views_ext.relatorios import _montar_descricao_filtros_frequencia


class RelatorioFrequenciaViewsTest(TestCase):
    """Valida endpoints principais e AJAX do relatório de frequência."""

    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username="tester",
            email="tester@example.com",
            password="123456",
        )

    def test_view_principal_autenticada(self):
        self.client.login(username="tester", password="123456")
        resposta = self.client.get(reverse("atividades:relatorio_frequencia_turmas"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Relatório de Carências e Frequência por Turma")

    def test_ajax_tabela(self):
        self.client.login(username="tester", password="123456")
        resposta = self.client.get(
            reverse("atividades:ajax_relatorio_frequencia_tabela"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("text/html", resposta.headers.get("Content-Type", ""))

    def test_ajax_opcoes(self):
        self.client.login(username="tester", password="123456")
        resposta = self.client.get(
            reverse("atividades:ajax_relatorio_frequencia_opcoes"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertJSONEqual(resposta.content, resposta.json())

    def test_exportacoes(self):
        self.client.login(username="tester", password="123456")
        for formato, content_type in [
            ("csv", "text/csv"),
            (
                "excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ),
            ("pdf", "text/html"),
        ]:
            resposta = self.client.get(
                reverse("atividades:exportar_relatorio_frequencia", args=[formato])
            )
            self.assertEqual(resposta.status_code, 200)
            self.assertIn(content_type, resposta.headers.get("Content-Type", ""))

    def test_montar_descricao_filtros_helper(self):
        opcoes = {
            "cursos": [{"id": 1, "nome": "Curso Teste"}],
            "turmas": [{"id": 2, "nome": "Turma X"}],
            "meses": [{"value": "10", "label": "Outubro"}],
            "anos": [{"value": "2025", "label": "2025"}],
            "status": [{"value": "PENDENTE", "label": "Pendente"}],
        }
        filtros = FrequenciaFiltros(
            curso_id=1, turma_id=2, mes=10, ano=2025, status_carencia="PENDENTE"
        )
        descricao = _montar_descricao_filtros_frequencia(filtros, opcoes)
        self.assertEqual(descricao["curso"], "Curso Teste")
        self.assertEqual(descricao["turma"], "Turma X")
        self.assertEqual(descricao["periodo"], "Outubro / 2025")
        self.assertEqual(descricao["status_carencia"], "Pendente")
