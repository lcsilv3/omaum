"""Testes para o serviço de relatório de carências e frequência."""

from datetime import date

from django.test import TestCase

from alunos.models import Aluno
from atividades.models import Atividade
from atividades.services.relatorios_frequencia import (
    FrequenciaFiltros,
    gerar_relatorio_frequencia,
    normalizar_filtros_frequencia,
)
from cursos.models import Curso
from frequencias.models import Carencia, FrequenciaMensal
from matriculas.models import Matricula
from presencas.models import RegistroPresenca
from turmas.models import Turma


class RelatorioFrequenciaServiceTest(TestCase):
    """Cobertura mínima para fluxo de relatório de frequência."""

    def setUp(self):
        """Configura curso, turma, alunos e registros para os cenários."""

        self.curso = Curso.objects.create(nome="Curso Frequência")
        self.turma = Turma.objects.create(nome="Turma Frequência", curso=self.curso)

        self.aluno_presenca = Aluno.objects.create(
            cpf="00000000001",
            nome="Aluno Presença",
            data_nascimento=date(1990, 1, 1),
            email="presenca@example.com",
            numero_iniciatico="INI001",
        )
        self.aluno_faltoso = Aluno.objects.create(
            cpf="00000000002",
            nome="Aluno Faltoso",
            data_nascimento=date(1990, 1, 2),
            email="faltoso@example.com",
            numero_iniciatico="INI002",
        )

        Matricula.objects.bulk_create(
            [
                Matricula(
                    aluno=self.aluno_presenca,
                    turma=self.turma,
                    data_matricula=date(2025, 1, 10),
                ),
                Matricula(
                    aluno=self.aluno_faltoso,
                    turma=self.turma,
                    data_matricula=date(2025, 1, 10),
                ),
            ]
        )

        self.atividade = Atividade.objects.create(
            nome="Atividade Frequência",
            curso=self.curso,
            data_inicio=date(2025, 10, 5),
            status="REALIZADA",
        )
        self.atividade.turmas.add(self.turma)

        RegistroPresenca.objects.create(
            aluno=self.aluno_presenca,
            turma=self.turma,
            atividade=self.atividade,
            data=self.atividade.data_inicio,
            status="P",
        )

        RegistroPresenca.objects.create(
            aluno=self.aluno_faltoso,
            turma=self.turma,
            atividade=self.atividade,
            data=self.atividade.data_inicio,
            status="F",
        )

    def test_gerar_relatorio_sem_frequencia_mensal(self):
        """Relatório calcula dados diretamente quando carências não existem."""

        filtros = FrequenciaFiltros(
            curso_id=self.curso.id,
            turma_id=self.turma.id,
            mes=10,
            ano=2025,
        )

        relatorio = gerar_relatorio_frequencia(filtros)
        linhas = {linha.aluno_id: linha for linha in relatorio.linhas}

        self.assertEqual(relatorio.resumo.total_alunos, 2)
        self.assertEqual(relatorio.resumo.total_presencas, 1)
        self.assertEqual(relatorio.resumo.total_faltas, 1)
        self.assertGreaterEqual(relatorio.resumo.percentual_presenca_medio, 0)

        self.assertTrue(linhas[self.aluno_presenca.id].liberado)
        self.assertFalse(linhas[self.aluno_faltoso.id].liberado)
        self.assertEqual(linhas[self.aluno_faltoso.id].status_carencia, "PENDENTE")

    def test_gerar_relatorio_com_frequencia_mensal(self):
        """Quando frequências mensais existem, usa carências persistidas."""

        frequencia = FrequenciaMensal.objects.create(
            turma=self.turma,
            mes=10,
            ano=2025,
            percentual_minimo=75,
        )

        Carencia.objects.create(
            frequencia_mensal=frequencia,
            aluno=self.aluno_presenca,
            total_presencas=1,
            total_atividades=1,
            percentual_presenca=100,
            numero_carencias=0,
            liberado=True,
            status="RESOLVIDO",
        )
        Carencia.objects.create(
            frequencia_mensal=frequencia,
            aluno=self.aluno_faltoso,
            total_presencas=0,
            total_atividades=1,
            percentual_presenca=0,
            numero_carencias=1,
            liberado=False,
            status="PENDENTE",
        )

        filtros = FrequenciaFiltros(
            curso_id=self.curso.id,
            turma_id=self.turma.id,
            mes=10,
            ano=2025,
        )

        relatorio = gerar_relatorio_frequencia(filtros)
        linhas = {linha.aluno_id: linha for linha in relatorio.linhas}

        self.assertEqual(relatorio.resumo.total_alunos, 2)
        self.assertEqual(relatorio.resumo.total_presencas, 1)
        self.assertEqual(relatorio.resumo.total_faltas, 1)
        self.assertEqual(linhas[self.aluno_presenca.id].status_carencia, "RESOLVIDO")
        self.assertEqual(linhas[self.aluno_faltoso.id].status_carencia, "PENDENTE")

    def test_normalizar_filtros(self):
        """Verifica conversão de filtros em tipos adequados."""

        filtros = normalizar_filtros_frequencia(
            {
                "curso": str(self.curso.id),
                "turma": str(self.turma.id),
                "mes": "10",
                "ano": "2025",
                "status_carencia": "RESOLVIDO",
            }
        )

        self.assertEqual(filtros.curso_id, self.curso.id)
        self.assertEqual(filtros.turma_id, self.turma.id)
        self.assertEqual(filtros.mes, 10)
        self.assertEqual(filtros.ano, 2025)
        self.assertEqual(filtros.status_carencia, "RESOLVIDO")
