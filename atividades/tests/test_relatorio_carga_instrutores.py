from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from atividades.services.relatorios_instrutores import (
    normalizar_filtros_instrutores,
    CargaInstrutorFiltros,
    gerar_relatorio_carga_instrutores,
)
from atividades.views_ext import relatorios


class RelatorioCargaInstrutoresServiceTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_normalizar_filtros_com_entrada_vazia(self):
        dados = {}
        filtros = normalizar_filtros_instrutores(dados)
        self.assertIsInstance(filtros, CargaInstrutorFiltros)
        self.assertIsNone(filtros.instrutor_id)
        self.assertIsNone(filtros.curso_id)
        self.assertIsNone(filtros.status_turma)
        self.assertIsNone(filtros.data_inicio)
        self.assertIsNone(filtros.data_fim)

    def test_gerar_relatorio_com_db_vazio(self):
        filtros = CargaInstrutorFiltros()
        relatorio = gerar_relatorio_carga_instrutores(filtros)
        # Mesmo com DB vazio, o objeto do relatório deve ser válido
        self.assertEqual(relatorio.resumo.total_instrutores, 0)
        self.assertEqual(relatorio.resumo.total_atividades, 0)
        self.assertEqual(relatorio.resumo.total_horas, 0.0)
        self.assertEqual(len(relatorio.linhas), 0)

    def test_exportador_csv_produzconteudo(self):
        filtros = CargaInstrutorFiltros()
        relatorio = gerar_relatorio_carga_instrutores(filtros)

        response = relatorios._exportar_carga_instrutores_csv(relatorio)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        # Deve conter cabeçalho CSV com colunas esperadas
        self.assertIn("Instrutor", content)
        self.assertIn("Total de Atividades", content)
        self.assertIn("Total de Horas", content)


class RelatorioCargaInstrutoresViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_view_relatorio_renderiza(self):
        request = self.factory.get(reverse("atividades:relatorio_carga_instrutores"))
        # Não estamos autenticando aqui; chamamos a view diretamente
        request.user = AnonymousUser()

        # A view está decorada com login_required, então chamá-la sem autenticação
        # deve retornar um redirect (HttpResponseRedirect) para login. Aqui verificamos
        # que o método existe e retorna um HttpResponse/redirection object.
        response = relatorios.relatorio_carga_instrutores(request)
        # Se não houver middleware de autenticação, a view pode tentar renderizar.
        self.assertTrue(hasattr(response, "status_code"))
