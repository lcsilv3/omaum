"""
Testes para os services do app relatorios_presenca.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from unittest.mock import Mock, patch, MagicMock

from ..services.relatorio_service import RelatorioPresencaService


class RelatorioPresencaServiceTestCase(TestCase):
    """Testes para o RelatorioPresencaService."""

    def setUp(self):
        """Configuração inicial dos testes."""
        self.service = RelatorioPresencaService()

        # Mock dos modelos para evitar dependências
        self.mock_turma = Mock()
        self.mock_turma.id = 1
        self.mock_turma.nome = "Turma Teste"
        self.mock_turma.curso.nome = "Curso Teste"
        self.mock_turma.instrutor.nome = "Instrutor Teste"
        self.mock_turma.get_status_display.return_value = "Ativa"

        self.mock_aluno = Mock()
        self.mock_aluno.id = 1
        self.mock_aluno.nome = "Aluno Teste"
        self.mock_aluno.numero_iniciatico = "001"
        self.mock_aluno.get_situacao_display.return_value = "Ativo"

        self.mock_atividade = Mock()
        self.mock_atividade.id = 1
        self.mock_atividade.nome = "Atividade Teste"

    @patch("relatorios_presenca.services.relatorio_service.import_module")
    def test_carregar_modelos_sucesso(self, mock_import):
        """Testa carregamento bem-sucedido dos modelos."""
        # Mock dos módulos
        mock_presencas_module = Mock()
        mock_presencas_module.RegistroPresenca = Mock()
        mock_alunos_module = Mock()
        mock_alunos_module.Aluno = Mock()
        mock_turmas_module = Mock()
        mock_turmas_module.Turma = Mock()
        mock_atividades_module = Mock()
        mock_atividades_module.Atividade = Mock()

        mock_import.side_effect = [
            mock_presencas_module,
            mock_alunos_module,
            mock_turmas_module,
            mock_atividades_module,
        ]

        # Criar novo service para testar carregamento
        service = RelatorioPresencaService()

        # Verificar se modelos foram carregados
        self.assertEqual(
            service.RegistroPresenca, mock_presencas_module.RegistroPresenca
        )
        self.assertEqual(service.Aluno, mock_alunos_module.Aluno)
        self.assertEqual(service.Turma, mock_turmas_module.Turma)
        self.assertEqual(service.Atividade, mock_atividades_module.Atividade)

    @patch("relatorios_presenca.services.relatorio_service.import_module")
    def test_carregar_modelos_erro(self, mock_import):
        """Testa erro no carregamento dos modelos."""
        mock_import.side_effect = ImportError("Módulo não encontrado")

        with self.assertRaises(ImportError):
            RelatorioPresencaService()

    def test_obter_dados_turma(self):
        """Testa obtenção de dados básicos da turma."""
        dados = self.service._obter_dados_turma(self.mock_turma)

        expected = {
            "id": 1,
            "nome": "Turma Teste",
            "curso": "Curso Teste",
            "status": "Ativa",
            "instrutor": "Instrutor Teste",
        }

        self.assertEqual(dados, expected)

    def test_gerar_lista_meses(self):
        """Testa geração de lista de meses."""
        data_inicio = date(2023, 1, 15)
        data_fim = date(2023, 3, 10)

        meses = self.service._gerar_lista_meses(data_inicio, data_fim)

        self.assertEqual(len(meses), 3)  # Janeiro, Fevereiro, Março

        # Verificar primeiro mês
        self.assertEqual(meses[0]["mes"], 1)
        self.assertEqual(meses[0]["ano"], 2023)
        self.assertEqual(meses[0]["nome"], "Janeiro")
        self.assertEqual(meses[0]["chave"], "01/2023")

        # Verificar último mês
        self.assertEqual(meses[2]["mes"], 3)
        self.assertEqual(meses[2]["ano"], 2023)
        self.assertEqual(meses[2]["nome"], "Março")
        self.assertEqual(meses[2]["chave"], "03/2023")

    def test_gerar_dias_mes(self):
        """Testa geração de dias do mês."""
        dias = self.service._gerar_dias_mes(2023, 2)  # Fevereiro 2023

        self.assertEqual(len(dias), 28)  # Fevereiro não bissexto

        # Verificar primeiro dia
        self.assertEqual(dias[0]["dia"], 1)
        self.assertEqual(dias[0]["data"], date(2023, 2, 1))

        # Verificar último dia
        self.assertEqual(dias[27]["dia"], 28)
        self.assertEqual(dias[27]["data"], date(2023, 2, 28))

    def test_obter_nome_mes(self):
        """Testa obtenção do nome do mês."""
        self.assertEqual(self.service._obter_nome_mes(1), "Janeiro")
        self.assertEqual(self.service._obter_nome_mes(6), "Junho")
        self.assertEqual(self.service._obter_nome_mes(12), "Dezembro")

    def test_calcular_estatisticas_consolidado(self):
        """Testa cálculo de estatísticas do consolidado."""
        dados_alunos = [
            {
                "aluno": self.mock_aluno,
                "totais": {"P": 8, "F": 2, "J": 1, "V1": 0, "V2": 0},
            },
            {
                "aluno": self.mock_aluno,
                "totais": {"P": 6, "F": 3, "J": 0, "V1": 1, "V2": 0},
            },
        ]

        estatisticas = self.service._calcular_estatisticas_consolidado(dados_alunos)

        expected = {
            "total_alunos": 2,
            "total_presencas": 14,  # 8 + 6
            "total_faltas": 5,  # 2 + 3
            "total_atividades": 21,  # 11 + 10
            "percentual_geral": 66.67,  # 14/21 * 100
        }

        self.assertEqual(estatisticas, expected)

    def test_calcular_estatisticas_consolidado_vazio(self):
        """Testa cálculo de estatísticas com dados vazios."""
        estatisticas = self.service._calcular_estatisticas_consolidado([])

        self.assertEqual(estatisticas, {})

    @patch.object(RelatorioPresencaService, "_carregar_modelos")
    def test_processar_dados_consolidado(self, mock_carregar):
        """Testa processamento de dados para consolidado."""
        # Mock do registro de presença
        mock_registro = Mock()
        mock_registro.aluno = self.mock_aluno
        mock_registro.data = date(2023, 1, 15)
        mock_registro.status = "P"

        registros = [mock_registro]
        data_inicio = date(2023, 1, 1)
        data_fim = date(2023, 1, 31)

        # Configurar service com modelo mockado
        service = RelatorioPresencaService()
        service.RegistroPresenca = Mock()

        dados = service._processar_dados_consolidado(registros, data_inicio, data_fim)

        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]["aluno"], self.mock_aluno)
        self.assertEqual(dados[0]["totais"]["P"], 1)
        self.assertEqual(dados[0]["meses"]["01/2023"]["P"], 1)

    @patch.object(RelatorioPresencaService, "_carregar_modelos")
    def test_processar_dados_mensais(self, mock_carregar):
        """Testa processamento de dados mensais."""
        # Mock do registro de presença
        mock_registro = Mock()
        mock_registro.aluno = self.mock_aluno
        mock_registro.data = date(2023, 1, 15)
        mock_registro.status = "P"

        registros = [mock_registro]
        data_inicio = date(2023, 1, 1)
        data_fim = date(2023, 1, 31)

        # Configurar service com modelo mockado
        service = RelatorioPresencaService()
        service.RegistroPresenca = Mock()

        dados = service._processar_dados_mensais(registros, data_inicio, data_fim)

        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]["aluno"], self.mock_aluno)
        self.assertEqual(dados[0]["totais"]["P"], 1)
        self.assertEqual(dados[0]["dias"][15]["status"], "P")
        self.assertEqual(dados[0]["dias"][15]["registro"], mock_registro)
