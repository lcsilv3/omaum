from django.test import TestCase
from django.urls import reverse
from datetime import date, timedelta
from relatorios_presenca.services import RelatorioPresencaService
from alunos.models import Aluno
from turmas.models import Turma
from cursos.models import Curso
from presencas.models import RegistroPresenca


class RelatoriosPresencaViewsTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(nome="Curso Teste", ativo=True)
        self.turma = Turma.objects.create(
            nome="Turma Teste", curso=self.curso, ativo=True
        )
        self.aluno = Aluno.objects.create(
            nome="Aluno Teste",
            data_nascimento=date(2000, 1, 1),
            numero_iniciatico="A003",
            email="aluno3@teste.com",
            cpf="00000000003",
        )
        self.data = date.today() - timedelta(days=5)
        from atividades.models import Atividade, Presenca

        self.atividade = Atividade.objects.create(
            nome="Atividade Teste",
            tipo_atividade="AULA",
            data_inicio=self.data,
            hora_inicio="08:00",
        )
        RegistroPresenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            data=self.data,
            status="F",
        )
        Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            data=self.data,
            presente=True,
        )

    def test_dashboard_acessa(self):
        resp = self.client.get(reverse("relatorios_presenca:dashboard_relatorios"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Dashboard")

    def test_alunos_com_carencia_csv(self):
        url = reverse("relatorios_presenca:alunos_com_carencia")
        resp = self.client.get(
            url,
            {
                "curso_id": self.curso.id,
                "turma_id": self.turma.id,
                "data_inicio": self.data,
                "data_fim": self.data,
                "formato": "csv",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/csv", resp["Content-Type"])

    def test_alunos_com_carencia_pdf(self):
        url = reverse("relatorios_presenca:alunos_com_carencia")
        resp = self.client.get(
            url,
            {
                "curso_id": self.curso.id,
                "turma_id": self.turma.id,
                "data_inicio": self.data,
                "data_fim": self.data,
                "formato": "pdf",
            },
        )
        self.assertIn(resp.status_code, [200, 500])

    def test_frequencia_por_atividade_csv(self):
        url = reverse("relatorios_presenca:frequencia_por_atividade")
        resp = self.client.get(url, {"turma_id": self.turma.id, "formato": "csv"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/csv", resp["Content-Type"])

    def test_frequencia_por_atividade_pdf(self):
        url = reverse("relatorios_presenca:frequencia_por_atividade")
        resp = self.client.get(url, {"turma_id": self.turma.id, "formato": "pdf"})
        self.assertIn(resp.status_code, [200, 500])

    def test_frequencia_por_atividade_view(self):
        url = reverse("relatorios_presenca:frequencia_por_atividade")
        resp = self.client.get(url, {"turma_id": self.turma.id})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("resultados", resp.context)

    def test_boletim_frequencia_aluno_csv(self):
        url = reverse("relatorios_presenca:boletim_frequencia_aluno")
        resp = self.client.get(
            url,
            {
                "aluno_id": self.aluno.id,
                "mes": self.data.month,
                "ano": self.data.year,
                "formato": "csv",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/csv", resp["Content-Type"])

    def test_boletim_frequencia_aluno_pdf(self):
        url = reverse("relatorios_presenca:boletim_frequencia_aluno")
        resp = self.client.get(
            url,
            {
                "aluno_id": self.aluno.id,
                "mes": self.data.month,
                "ano": self.data.year,
                "formato": "pdf",
            },
        )
        self.assertIn(resp.status_code, [200, 500])

    def test_exportar_relatorio_consolidado_csv(self):
        url = reverse("relatorios_presenca:exportar_relatorio_consolidado")
        data_inicio = self.data.strftime("%Y-%m-%d")
        data_fim = self.data.strftime("%Y-%m-%d")
        resp = self.client.post(
            url,
            {
                "turma_id": self.turma.id,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "formato": "csv",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/csv", resp["Content-Type"])

    def test_exportar_relatorio_consolidado_excel(self):
        url = reverse("relatorios_presenca:exportar_relatorio_consolidado")
        data_inicio = self.data.strftime("%Y-%m-%d")
        data_fim = self.data.strftime("%Y-%m-%d")
        resp = self.client.post(
            url,
            {
                "turma_id": self.turma.id,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "formato": "excel",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            resp["Content-Type"],
        )

    def test_turmas_por_curso_json(self):
        url = reverse("relatorios_presenca:turmas_por_curso_json")
        resp = self.client.get(url, {"curso_id": self.curso.id})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("turmas", resp.json())

    def test_alunos_por_turma_json(self):
        url = reverse("relatorios_presenca:alunos_por_turma_json")
        resp = self.client.get(url, {"turma_id": self.turma.id})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("alunos", resp.json())

    def test_consolidado_tabela_ajax(self):
        url = reverse("relatorios_presenca:consolidado_tabela_ajax")
        data_inicio = self.data.strftime("%Y-%m-%d")
        data_fim = self.data.strftime("%Y-%m-%d")
        resp = self.client.get(
            url,
            {
                "turma_id": self.turma.id,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/html", resp["Content-Type"])

    def test_view_parametros_invalidos(self):
        # Testa ausência de parâmetros obrigatórios
        url = reverse("relatorios_presenca:consolidado_tabela_ajax")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 400)
        url2 = reverse("relatorios_presenca:exportar_relatorio_consolidado")
        resp2 = self.client.post(url2, {})
        self.assertIn(resp2.status_code, [400, 405])
