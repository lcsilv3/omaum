"""Testes para o serviço de relatório de participação por atividade."""

from datetime import date, time

from django.test import TestCase

from alunos.models import Aluno
from atividades.models import Atividade
from atividades.services.relatorios_participacao import (
    ParticipacaoFiltros,
    gerar_relatorio_participacao,
    normalizar_filtros,
)
from cursos.models import Curso
from presencas.models import RegistroPresenca
from turmas.models import Turma


class RelatorioParticipacaoServiceTest(TestCase):
    """Cobertura básica para o relatório de participação por atividade."""

    def setUp(self):
        """Monta grafo de dados mínimo para os cenários de teste."""

        self.curso = Curso.objects.create(nome="Curso Teste")
        self.turma = Turma.objects.create(nome="Turma Alfa", curso=self.curso)

        self.alunos = [
            Aluno.objects.create(
                cpf=f"0000000000{i}",
                nome=f"Aluno {i}",
                data_nascimento=date(1990, 1, 1),
                email=f"aluno{i}@teste.com",
                numero_iniciatico=f"INI{i:03d}",
            )
            for i in range(1, 6)
        ]

        self.atividade = Atividade.objects.create(
            nome="Atividade Base",
            tipo_atividade="AULA",
            data_inicio=date(2025, 10, 10),
            data_fim=date(2025, 10, 10),
            hora_inicio=time(19, 0),
            hora_fim=time(21, 0),
            curso=self.curso,
            status="REALIZADA",
        )
        self.atividade.turmas.add(self.turma)

        status_map = ["P", "F", "J", "V1", "V2"]
        for aluno, status in zip(self.alunos, status_map):
            RegistroPresenca.objects.create(
                aluno=aluno,
                turma=self.turma,
                atividade=self.atividade,
                data=self.atividade.data_inicio,
                status=status,
            )

        self.atividade_sem_dados = Atividade.objects.create(
            nome="Atividade Sem Dados",
            tipo_atividade="PALESTRA",
            data_inicio=date(2025, 10, 12),
            hora_inicio=time(18, 0),
            curso=self.curso,
            status="CONFIRMADA",
        )
        self.atividade_sem_dados.turmas.add(self.turma)

    def test_gerar_relatorio_participacao_consolida_metricas(self):
        """Garante que métricas de participação são agregadas corretamente."""

        filtros = ParticipacaoFiltros()
        relatorio = gerar_relatorio_participacao(filtros)

        self.assertEqual(relatorio.resumo.total_convocados, 5)
        self.assertEqual(relatorio.resumo.total_presentes, 1)
        self.assertEqual(relatorio.resumo.total_faltas, 1)
        self.assertEqual(relatorio.resumo.total_faltas_justificadas, 1)
        self.assertEqual(relatorio.resumo.total_voluntario_extra, 1)
        self.assertEqual(relatorio.resumo.total_voluntario_simples, 1)
        self.assertGreaterEqual(len(relatorio.linhas), 2)

        linhas_por_atividade = {
            linha.atividade_id: linha for linha in relatorio.linhas
        }

        linha_base = linhas_por_atividade[self.atividade.id]
        self.assertAlmostEqual(linha_base.percentual_presenca, 20.0)
        self.assertEqual(linha_base.total_voluntarios, 2)
        self.assertListEqual(linha_base.turmas, [self.turma.nome])

        linha_sem_dados = linhas_por_atividade[self.atividade_sem_dados.id]
        self.assertEqual(linha_sem_dados.total_convocados, 0)
        self.assertEqual(linha_sem_dados.percentual_presenca, 0.0)

    def test_normalizar_filtros_converte_valores(self):
        """Verifica parsing de filtros enviados pela camada de view."""

        filtros = normalizar_filtros(
            {
                "curso": str(self.curso.id),
                "turma": str(self.turma.id),
                "tipo_atividade": "AULA",
                "status": "REALIZADA",
                "data_inicio": "2025-10-01",
                "data_fim": "2025-10-31",
            }
        )

        self.assertEqual(filtros.curso_id, self.curso.id)
        self.assertEqual(filtros.turma_id, self.turma.id)
        self.assertEqual(filtros.tipo_atividade, "AULA")
        self.assertEqual(filtros.status_atividade, "REALIZADA")
        self.assertEqual(filtros.data_inicio, date(2025, 10, 1))
        self.assertEqual(filtros.data_fim, date(2025, 10, 31))
