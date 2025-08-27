from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import AtividadeAcademica
from turmas.models import Turma
from cursos.models import Curso
from datetime import date, timedelta
from django.utils import timezone


class AtividadeAcademicaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            codigo_curso="CUR01",
            nome="Curso de Teste",
            descricao="Descrição do curso de teste",
        )
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31),
        )
        self.data_inicio = timezone.now()
        self.data_fim = self.data_inicio + timedelta(days=7)
        self.atividade = AtividadeAcademica.objects.create(
            nome="Aula de Matemática",
            descricao="Aula introdutória sobre álgebra.",
            data_inicio=self.data_inicio,
            data_fim=self.data_fim,
            turma=self.turma,
        )

    def test_listar_atividades(self):
        response = self.client.get(reverse("atividades:academica_lista"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aula de Matemática")

    def test_filtrar_atividades_por_turma(self):
        # Criar outra turma e atividade
        turma2 = Turma.objects.create(
            nome="Turma 2",
            curso=self.curso,
            data_inicio=date(2023, 1, 1),
            data_fim=date(2023, 12, 31),
        )
        AtividadeAcademica.objects.create(
            nome="Aula de Física",
            descricao="Introdução à física",
            data_inicio=self.data_inicio,
            data_fim=self.data_fim,
            turma=turma2,
        )

        # Filtrar por turma1
        response = self.client.get(
            f"{reverse('atividades:academica_lista')}?turma={self.turma.id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aula de Matemática")
        self.assertNotContains(response, "Aula de Física")

        # Filtrar por turma2
        response = self.client.get(
            f"{reverse('atividades:academica_lista')}?turma={turma2.id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aula de Física")
        self.assertNotContains(response, "Aula de Matemática")

    def test_criar_atividade(self):
        response = self.client.get(reverse("atividades:academica_criar"))
        self.assertEqual(response.status_code, 200)

        # Testar POST para criar atividade
        data = {
            "nome": "Nova Atividade",
            "descricao": "Descrição da nova atividade",
            "data_inicio": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_fim": (timezone.now() + timedelta(days=7)).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "turma": self.turma.id,
        }
        response = self.client.post(reverse("atividades:academica_criar"), data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

        # Verificar se a atividade foi criada
        self.assertTrue(
            AtividadeAcademica.objects.filter(nome="Nova Atividade").exists()
        )

    def test_editar_atividade(self):
        response = self.client.get(
            reverse("atividades:academica_editar", args=[self.atividade.id])
        )
        self.assertEqual(response.status_code, 200)

        # Testar POST para editar atividade
        data = {
            "nome": "Aula de Matemática Atualizada",
            "descricao": "Descrição atualizada",
            "data_inicio": self.data_inicio.strftime("%Y-%m-%d %H:%M:%S"),
            "data_fim": self.data_fim.strftime("%Y-%m-%d %H:%M:%S"),
            "turma": self.turma.id,
        }
        response = self.client.post(
            reverse("atividades:academica_editar", args=[self.atividade.id]), data
        )
        self.assertEqual(response.status_code, 302)  # Redirecionamento após sucesso

        # Verificar se a atividade foi atualizada
        self.atividade.refresh_from_db()
        self.assertEqual(self.atividade.nome, "Aula de Matemática Atualizada")
        self.assertEqual(self.atividade.descricao, "Descrição atualizada")

    def test_excluir_atividade(self):
        response = self.client.get(
            reverse("atividades:academica_excluir", kwargs={"id": self.atividade.id})
        )
        self.assertEqual(response.status_code, 200)
