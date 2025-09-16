from django.test import TestCase
from datetime import date, timedelta
from relatorios_presenca.services import RelatorioPresencaService
from alunos.models import Aluno
from turmas.models import Turma
from cursos.models import Curso
from presencas.models import RegistroPresenca


class RelatorioPresencaServiceTest(TestCase):
    def setUp(self):
        # Criação de curso, turma e alunos
        self.curso = Curso.objects.create(nome="Curso Teste", ativo=True)
        self.turma = Turma.objects.create(
            nome="Turma Teste", curso=self.curso, ativo=True
        )
        self.aluno1 = Aluno.objects.create(
            nome="Aluno 1",
            data_nascimento=date(2000, 1, 1),
            numero_iniciatico="A001",
            email="aluno1@teste.com",
            cpf="00000000001",
        )
        self.aluno2 = Aluno.objects.create(
            nome="Aluno 2",
            data_nascimento=date(2000, 1, 2),
            numero_iniciatico="A002",
            email="aluno2@teste.com",
            cpf="00000000002",
        )
        # Datas
        self.data1 = date.today() - timedelta(days=10)
        self.data2 = date.today() - timedelta(days=5)
        # Criar atividade obrigatória
        from atividades.models import Atividade

        self.atividade = Atividade.objects.create(
            nome="Atividade Teste",
            tipo_atividade="AULA",
            data_inicio=self.data1,
            hora_inicio="08:00",
        )
        # Registros de presença e falta
        RegistroPresenca.objects.create(
            aluno=self.aluno1,
            turma=self.turma,
            atividade=self.atividade,
            data=self.data1,
            status="F",
        )
        RegistroPresenca.objects.create(
            aluno=self.aluno1,
            turma=self.turma,
            atividade=self.atividade,
            data=self.data2,
            status="P",
        )
        RegistroPresenca.objects.create(
            aluno=self.aluno2,
            turma=self.turma,
            atividade=self.atividade,
            data=self.data1,
            status="F",
        )
        RegistroPresenca.objects.create(
            aluno=self.aluno2,
            turma=self.turma,
            atividade=self.atividade,
            data=self.data2,
            status="F",
        )
        self.service = RelatorioPresencaService()

    def test_obter_alunos_mais_carencias(self):
        resultados = self.service.obter_alunos_mais_carencias(
            curso_id=self.curso.id,
            turma_id=self.turma.id,
            data_inicio=self.data1,
            data_fim=self.data2,
        )
        self.assertEqual(len(resultados), 2)
        # Aluno 2 deve ter mais faltas
        self.assertEqual(resultados[0]["aluno"].nome, "Aluno 2")
        self.assertEqual(resultados[0]["faltas"], 2)
        self.assertEqual(resultados[1]["aluno"].nome, "Aluno 1")
        self.assertEqual(resultados[1]["faltas"], 1)

    def test_obter_frequencia_por_atividade_com_dados(self):
        # Simula presença e falta em uma atividade
        from atividades.models import Atividade, Presenca

        atividade = Atividade.objects.create(
            nome="Ativ Teste",
            tipo_atividade="AULA",
            data_inicio=self.data1,
            hora_inicio="08:00",
        )
        Presenca.objects.create(
            aluno=self.aluno1,
            turma=self.turma,
            atividade=atividade,
            data=self.data1,
            presente=True,
        )
        Presenca.objects.create(
            aluno=self.aluno2,
            turma=self.turma,
            atividade=atividade,
            data=self.data1,
            presente=False,
        )
        resultados = self.service.obter_frequencia_por_atividade(
            turma_id=self.turma.id, atividade_id=atividade.id
        )
        self.assertEqual(len(resultados), 2)
        nomes = [r["aluno"].nome for r in resultados]
        self.assertIn("Aluno 1", nomes)
        self.assertIn("Aluno 2", nomes)
        for r in resultados:
            if r["aluno"].nome == "Aluno 1":
                self.assertEqual(r["presencas"], 1)
            if r["aluno"].nome == "Aluno 2":
                self.assertEqual(r["faltas"], 1)

    def test_obter_alunos_mais_carencias_sem_resultados(self):
        # Busca por turma inexistente
        resultados = self.service.obter_alunos_mais_carencias(turma_id=9999)
        self.assertEqual(resultados, [])
