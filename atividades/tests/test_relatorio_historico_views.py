"""Testes das views do relatório histórico do aluno."""

from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from atividades.services.relatorios_historico_aluno import HistoricoFiltros
from atividades.views_ext.relatorios import _montar_descricao_filtros_historico


class RelatorioHistoricoViewsTest(TestCase):
    """Valida endpoints, exportações e helpers do relatório histórico."""

    def setUp(self):
        """Cria usuário autenticado para acessar as rotas protegidas."""

        self.usuario = get_user_model().objects.create_user(
            username="historico-tester",
            email="historico@example.com",
            password="senha123",
        )

    def test_view_principal_autenticada(self):
        """Confere renderização da página principal do relatório."""

        self.client.login(username="historico-tester", password="senha123")
        resposta = self.client.get(reverse("atividades:relatorio_historico_aluno"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Relatório Histórico de Participação do Aluno")

    def test_ajax_tabela(self):
        """Garante resposta HTML da rota AJAX da timeline."""

        self.client.login(username="historico-tester", password="senha123")
        resposta = self.client.get(
            reverse("atividades:ajax_relatorio_historico_tabela"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("text/html", resposta.headers.get("Content-Type", ""))

    def test_ajax_opcoes(self):
        """Confere retorno JSON da rota AJAX de opções."""

        self.client.login(username="historico-tester", password="senha123")
        resposta = self.client.get(
            reverse("atividades:ajax_relatorio_historico_opcoes"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertJSONEqual(resposta.content, resposta.json())

    def test_exportacoes(self):
        """Verifica exportações CSV, Excel e PDF do relatório."""

        self.client.login(username="historico-tester", password="senha123")
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
                reverse("atividades:exportar_relatorio_historico_aluno", args=[formato])
            )
            self.assertEqual(resposta.status_code, 200)
            self.assertIn(content_type, resposta.headers.get("Content-Type", ""))

    def test_montar_descricao_filtros_helper(self):
        """Valida descrição amigável dos filtros selecionados."""

        opcoes = {
            "alunos": [{"id": 1, "nome": "Aluno Teste"}],
            "cursos": [{"id": 2, "nome": "Curso Exemplo"}],
            "papeis": [{"value": "voluntario", "label": "Voluntário"}],
        }
        filtros = HistoricoFiltros(
            aluno_id=1,
            curso_id=2,
            papel="voluntario",
            data_inicio=date(2025, 1, 1),
            data_fim=date(2025, 1, 31),
        )
        descricao = _montar_descricao_filtros_historico(filtros, opcoes)
        self.assertEqual(descricao["aluno"], "Aluno Teste")
        self.assertEqual(descricao["curso"], "Curso Exemplo")
        self.assertEqual(descricao["papel"], "Voluntário")
        self.assertEqual(descricao["periodo"], "01/01/2025 a 31/01/2025")
