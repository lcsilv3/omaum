"""
Testes para os modelos do app relatorios_presenca.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
import json

from ..models import ConfiguracaoRelatorio, HistoricoRelatorio, AgendamentoRelatorio


class ConfiguracaoRelatorioTestCase(TestCase):
    """Testes para o modelo ConfiguracaoRelatorio."""

    def setUp(self):
        """Configuração inicial dos testes."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_criar_configuracao_valida(self):
        """Testa criação de configuração válida."""
        config = ConfiguracaoRelatorio.objects.create(
            nome="Teste Consolidado",
            tipo_relatorio="consolidado",
            formato_saida="excel",
            criado_por=self.user,
        )

        self.assertEqual(config.nome, "Teste Consolidado")
        self.assertEqual(config.tipo_relatorio, "consolidado")
        self.assertEqual(config.formato_saida, "excel")
        self.assertTrue(config.ativo)
        self.assertEqual(config.criado_por, self.user)

    def test_parametros_padrao_json_valido(self):
        """Testa validação de parâmetros JSON."""
        parametros = {"filtro_ativo": True, "limite": 100}

        config = ConfiguracaoRelatorio.objects.create(
            nome="Teste JSON",
            tipo_relatorio="mensal",
            parametros_padrao=parametros,
            criado_por=self.user,
        )

        self.assertEqual(config.parametros_padrao, parametros)

    def test_str_representation(self):
        """Testa representação string do modelo."""
        config = ConfiguracaoRelatorio.objects.create(
            nome="Teste String", tipo_relatorio="consolidado", criado_por=self.user
        )

        expected = "Teste String (Consolidado por Período (grau))"
        self.assertEqual(str(config), expected)


class HistoricoRelatorioTestCase(TestCase):
    """Testes para o modelo HistoricoRelatorio."""

    def setUp(self):
        """Configuração inicial dos testes."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.config = ConfiguracaoRelatorio.objects.create(
            nome="Config Teste", tipo_relatorio="consolidado", criado_por=self.user
        )

    def test_criar_historico_valido(self):
        """Testa criação de histórico válido."""
        parametros = {"turma_id": 1, "data_inicio": "2023-01-01"}

        historico = HistoricoRelatorio.objects.create(
            usuario=self.user,
            configuracao=self.config,
            tipo_relatorio="consolidado",
            parametros=parametros,
        )

        self.assertEqual(historico.usuario, self.user)
        self.assertEqual(historico.configuracao, self.config)
        self.assertEqual(historico.tipo_relatorio, "consolidado")
        self.assertEqual(historico.parametros, parametros)
        self.assertEqual(historico.status, "processando")

    def test_tamanho_arquivo_formatado(self):
        """Testa formatação do tamanho do arquivo."""
        historico = HistoricoRelatorio.objects.create(
            usuario=self.user,
            tipo_relatorio="consolidado",
            parametros={},
            tamanho_arquivo=1024,
        )

        self.assertEqual(historico.tamanho_arquivo_formatado, "1.0 KB")

        # Teste com arquivo maior
        historico.tamanho_arquivo = 1048576  # 1 MB
        historico.save()
        self.assertEqual(historico.tamanho_arquivo_formatado, "1.0 MB")

        # Teste sem arquivo
        historico.tamanho_arquivo = None
        historico.save()
        self.assertEqual(historico.tamanho_arquivo_formatado, "N/A")

    def test_marcar_como_concluido(self):
        """Testa marcação como concluído."""
        historico = HistoricoRelatorio.objects.create(
            usuario=self.user, tipo_relatorio="consolidado", parametros={}
        )

        historico.marcar_como_concluido("arquivo.xlsx", 2048)

        self.assertEqual(historico.status, "concluido")
        self.assertEqual(historico.arquivo_gerado, "arquivo.xlsx")
        self.assertEqual(historico.tamanho_arquivo, 2048)

    def test_marcar_como_erro(self):
        """Testa marcação como erro."""
        historico = HistoricoRelatorio.objects.create(
            usuario=self.user, tipo_relatorio="consolidado", parametros={}
        )

        mensagem_erro = "Erro de teste"
        historico.marcar_como_erro(mensagem_erro)

        self.assertEqual(historico.status, "erro")
        self.assertEqual(historico.mensagem_erro, mensagem_erro)


class AgendamentoRelatorioTestCase(TestCase):
    """Testes para o modelo AgendamentoRelatorio."""

    def setUp(self):
        """Configuração inicial dos testes."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        self.config = ConfiguracaoRelatorio.objects.create(
            nome="Config Teste", tipo_relatorio="consolidado", criado_por=self.user
        )

    def test_criar_agendamento_valido(self):
        """Testa criação de agendamento válido."""
        agendamento = AgendamentoRelatorio.objects.create(
            nome="Agendamento Teste",
            configuracao=self.config,
            usuario=self.user,
            frequencia="mensal",
            emails_destino="test@example.com",
        )

        self.assertEqual(agendamento.nome, "Agendamento Teste")
        self.assertEqual(agendamento.configuracao, self.config)
        self.assertEqual(agendamento.usuario, self.user)
        self.assertEqual(agendamento.frequencia, "mensal")
        self.assertTrue(agendamento.ativo)
        self.assertIsNotNone(agendamento.proxima_execucao)

    def test_calcular_proxima_execucao_diario(self):
        """Testa cálculo de próxima execução diária."""
        agendamento = AgendamentoRelatorio(
            nome="Teste Diário",
            configuracao=self.config,
            usuario=self.user,
            frequencia="diario",
            emails_destino="test@example.com",
        )

        agendamento.calcular_proxima_execucao()

        self.assertIsNotNone(agendamento.proxima_execucao)
        # Próxima execução deve ser hoje ou amanhã
        hoje = timezone.now().date()
        amanha = hoje + timedelta(days=1)
        self.assertIn(agendamento.proxima_execucao.date(), [hoje, amanha])

    def test_calcular_proxima_execucao_semanal(self):
        """Testa cálculo de próxima execução semanal."""
        agendamento = AgendamentoRelatorio(
            nome="Teste Semanal",
            configuracao=self.config,
            usuario=self.user,
            frequencia="semanal",
            emails_destino="test@example.com",
        )

        agendamento.calcular_proxima_execucao()

        self.assertIsNotNone(agendamento.proxima_execucao)
        # Próxima execução deve ser dentro de 7 dias
        hoje = timezone.now().date()
        limite = hoje + timedelta(days=7)
        self.assertLessEqual(agendamento.proxima_execucao.date(), limite)

    def test_str_representation(self):
        """Testa representação string do modelo."""
        agendamento = AgendamentoRelatorio.objects.create(
            nome="Teste String",
            configuracao=self.config,
            usuario=self.user,
            frequencia="mensal",
            emails_destino="test@example.com",
        )

        expected = "Teste String - Mensal"
        self.assertEqual(str(agendamento), expected)
