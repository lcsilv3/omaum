"""Testes para o serviço do relatório histórico do aluno."""

from datetime import date, time

from django.test import TestCase

from atividades.models import Atividade
from atividades.services.relatorios_historico_aluno import (
    HistoricoFiltros,
    gerar_relatorio_historico_aluno,
    normalizar_filtros_historico,
    obter_opcoes_filtros_historico,
)
from alunos.models import Aluno
from cursos.models import Curso
from presencas.models import RegistroPresenca
from turmas.models import Turma


class RelatorioHistoricoServiceTest(TestCase):
    """Garante a consolidação de eventos e filtros do histórico."""

    def setUp(self):
        """Cria aluno, curso, turmas e registros de presença variados."""

        self.curso = Curso.objects.create(nome="Curso Histórico")
        self.outro_curso = Curso.objects.create(nome="Curso Externo")

        self.turma = Turma.objects.create(nome="Turma Histórica", curso=self.curso)
        self.turma.instrutor = None
        self.turma.save()

        self.turma_externa = Turma.objects.create(
            nome="Turma Externa", curso=self.outro_curso
        )

        self.aluno = Aluno.objects.create(
            cpf="12345678901",
            nome="Aluno Histórico",
            data_nascimento=date(2000, 1, 1),
            email="historico@example.com",
            numero_iniciatico="A123",
        )
        self.outro_aluno = Aluno.objects.create(
            cpf="10987654321",
            nome="Aluno Externo",
            data_nascimento=date(1999, 5, 5),
            email="externo@example.com",
            numero_iniciatico="B321",
        )

        self.atividade_aula = Atividade.objects.create(
            nome="Aula Presencial",
            tipo_atividade="AULA",
            data_inicio=date(2025, 1, 10),
            hora_inicio=time(19, 0),
            status="REALIZADA",
            curso=self.curso,
        )
        self.atividade_aula.turmas.add(self.turma)

        self.atividade_voluntaria = Atividade.objects.create(
            nome="Atuação Voluntária",
            tipo_atividade="WORKSHOP",
            data_inicio=date(2025, 2, 15),
            hora_inicio=time(18, 30),
            status="REALIZADA",
            curso=self.curso,
        )
        self.atividade_voluntaria.turmas.add(self.turma)

        self.atividade_instrucao = Atividade.objects.create(
            nome="Oficina Instrucional",
            tipo_atividade="SEMINARIO",
            data_inicio=date(2025, 3, 20),
            hora_inicio=time(20, 0),
            status="CONFIRMADA",
            curso=self.curso,
        )
        self.atividade_instrucao.turmas.add(self.turma)

        self.turma.instrutor = self.aluno
        self.turma.save()

        RegistroPresenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade_aula,
            data=date(2025, 1, 10),
            status="P",
        )
        RegistroPresenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade_aula,
            data=date(2025, 1, 11),
            status="F",
        )
        RegistroPresenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade_voluntaria,
            data=date(2025, 2, 15),
            status="V1",
        )

        atividade_externa = Atividade.objects.create(
            nome="Atividade Externa",
            tipo_atividade="AULA",
            data_inicio=date(2025, 1, 5),
            hora_inicio=time(18, 0),
            status="REALIZADA",
            curso=self.outro_curso,
        )
        atividade_externa.turmas.add(self.turma_externa)
        RegistroPresenca.objects.create(
            aluno=self.outro_aluno,
            turma=self.turma_externa,
            atividade=atividade_externa,
            data=date(2025, 1, 5),
            status="P",
        )

    def test_gerar_relatorio_historico_agrega_resumo(self):
        """Confere totais e distribuição de papéis para o aluno principal."""

        filtros = HistoricoFiltros(aluno_id=self.aluno.id)
        relatorio = gerar_relatorio_historico_aluno(filtros)

        self.assertEqual(relatorio.resumo.total_eventos, 4)
        self.assertEqual(relatorio.resumo.total_participacoes, 3)
        self.assertEqual(relatorio.resumo.total_presencas, 1)
        self.assertEqual(relatorio.resumo.total_faltas, 1)
        self.assertEqual(relatorio.resumo.total_voluntarios, 1)
        self.assertEqual(relatorio.resumo.total_instrucao, 1)

        distribuicao = relatorio.resumo.eventos_por_papel
        self.assertEqual(distribuicao.get("Participante"), 2)
        self.assertEqual(distribuicao.get("Voluntário Extra"), 1)
        self.assertEqual(distribuicao.get("Instrutor Principal"), 1)

        datas = [evento.data for evento in relatorio.eventos]
        self.assertTrue(all(datas[i] >= datas[i + 1] for i in range(len(datas) - 1)))

    def test_normalizar_filtros_historico_trata_alias(self):
        """Garante conversão segura dos filtros vindos da camada de apresentação."""

        filtros = normalizar_filtros_historico(
            {
                "aluno": str(self.aluno.id),
                "curso": str(self.curso.id),
                "papel": "voluntario",
                "data_inicio": "2025-01-01",
                "data_fim": "2025-12-31",
            }
        )

        self.assertEqual(filtros.aluno_id, self.aluno.id)
        self.assertEqual(filtros.curso_id, self.curso.id)
        self.assertEqual(filtros.papel, "voluntario")
        self.assertEqual(filtros.data_inicio, date(2025, 1, 1))
        self.assertEqual(filtros.data_fim, date(2025, 12, 31))

    def test_obter_opcoes_filtros_restringe_por_curso(self):
        """Verifica que apenas alunos do curso informado aparecem nas opções."""

        opcoes = obter_opcoes_filtros_historico(curso_id=self.curso.id)
        alunos_ids = {item["id"] for item in opcoes["alunos"]}

        self.assertIn(self.aluno.id, alunos_ids)
        self.assertNotIn(self.outro_aluno.id, alunos_ids)
        self.assertTrue(opcoes["papeis"])
