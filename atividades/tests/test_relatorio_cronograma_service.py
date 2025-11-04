"""Testes para o serviço do relatório Cronograma Curso × Turmas."""

from datetime import date, time

from django.test import TestCase

from atividades.models import Atividade
from atividades.services.relatorios_cronograma import (
    CronogramaFiltros,
    gerar_relatorio_cronograma,
    normalizar_filtros_cronograma,
    obter_opcoes_filtros_cronograma,
)
from cursos.models import Curso
from turmas.models import Turma


class RelatorioCronogramaServiceTest(TestCase):
    """Garante métricas e filtros básicos do relatório de cronograma."""

    def setUp(self):
        """Cria curso, turmas e atividades com situações distintas."""

        self.curso = Curso.objects.create(nome="Curso Cronograma Teste")
        self.outro_curso = Curso.objects.create(nome="Curso Secundário")

        self.turma_alpha = Turma.objects.create(nome="Turma Alpha", curso=self.curso)
        self.turma_beta = Turma.objects.create(nome="Turma Beta", curso=self.curso)
        self.turma_extra = Turma.objects.create(
            nome="Turma Extra", curso=self.outro_curso
        )

        self.atividade_atrasada = Atividade.objects.create(
            nome="Atividade Atrasada",
            tipo_atividade="AULA",
            data_inicio=date(2025, 1, 10),
            data_fim=date(2025, 1, 12),
            hora_inicio=time(19, 0),
            hora_fim=time(21, 0),
            curso=self.curso,
            status="REALIZADA",
            responsavel="Instrutora Alpha",
        )
        self.atividade_atrasada.turmas.add(self.turma_alpha)

        self.atividade_adiantada = Atividade.objects.create(
            nome="Atividade Adiantada",
            tipo_atividade="AULA",
            data_inicio=date(2025, 2, 20),
            data_fim=date(2025, 2, 19),
            hora_inicio=time(18, 30),
            curso=self.curso,
            status="REALIZADA",
            responsavel="Instrutor Beta",
        )
        self.atividade_adiantada.turmas.add(self.turma_alpha, self.turma_beta)

        self.atividade_confirmada = Atividade.objects.create(
            nome="Atividade Confirmada",
            tipo_atividade="WORKSHOP",
            data_inicio=date(2025, 3, 5),
            hora_inicio=time(20, 0),
            curso=self.curso,
            status="CONFIRMADA",
            responsavel="Instrutor Beta",
        )
        self.atividade_confirmada.turmas.add(self.turma_beta)

    def test_gerar_relatorio_cronograma_agrega_metricas(self):
        """Confere contagens e indicadores de atraso/adiantamento."""

        filtros = CronogramaFiltros()
        relatorio = gerar_relatorio_cronograma(filtros)

        self.assertEqual(relatorio.resumo.total_atividades, 3)
        self.assertEqual(relatorio.resumo.atividades_atrasadas, 1)
        self.assertEqual(relatorio.resumo.atividades_adiantadas, 1)

        linhas_por_id = {linha.atividade_id: linha for linha in relatorio.linhas}

        linha_atrasada = linhas_por_id[self.atividade_atrasada.id]
        self.assertEqual(linha_atrasada.atraso_dias, 2)
        self.assertIsNone(linha_atrasada.adiantamento_dias)
        self.assertListEqual(linha_atrasada.turmas, [self.turma_alpha.nome])

        linha_adiantada = linhas_por_id[self.atividade_adiantada.id]
        self.assertEqual(linha_adiantada.adiantamento_dias, 1)
        self.assertIsNone(linha_adiantada.atraso_dias)
        self.assertIn(self.turma_beta.nome, linha_adiantada.turmas)

    def test_normalizar_filtros_cronograma(self):
        """Valida conversão de filtros recebidos da camada de apresentação."""

        filtros = normalizar_filtros_cronograma(
            {
                "curso": str(self.curso.id),
                "turma": str(self.turma_alpha.id),
                "responsavel": " Instrutora Alpha ",
                "status": "REALIZADA",
                "data_inicio": "2025-01-01",
                "data_fim": "2025-01-31",
            }
        )

        self.assertEqual(filtros.curso_id, self.curso.id)
        self.assertEqual(filtros.turma_id, self.turma_alpha.id)
        self.assertEqual(filtros.responsavel, "Instrutora Alpha")
        self.assertEqual(filtros.status, "REALIZADA")
        self.assertEqual(filtros.data_inicio, date(2025, 1, 1))
        self.assertEqual(filtros.data_fim, date(2025, 1, 31))

    def test_obter_opcoes_filtros_respeita_curso(self):
        """Garante que turmas retornadas respeitam o curso informado."""

        opcoes = obter_opcoes_filtros_cronograma(self.curso.id)
        turmas_ids = {turma["id"] for turma in opcoes["turmas"]}

        self.assertIn(self.turma_alpha.id, turmas_ids)
        self.assertNotIn(self.turma_extra.id, turmas_ids)
        self.assertTrue(opcoes["status"])
        self.assertTrue(opcoes["responsaveis"])
