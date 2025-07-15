"""
Tests para views do consolidado de presenças.
"""

import json
from datetime import date
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import PresencaDetalhada
from cursos.models import Curso
from turmas.models import Turma
from alunos.models import Aluno
from atividades.models import AtividadeAcademica


class ConsolidadoPresencasViewTestCase(TestCase):
    """
    Tests para a view principal do consolidado.
    """

    def setUp(self):
        """Configuração inicial dos testes."""
        self.client = Client()

        # Criar usuário
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        # Criar dados de teste
        self.curso = Curso.objects.create(
            nome="Curso Teste", codigo="CT001", ativo=True
        )

        self.turma = Turma.objects.create(
            nome="Turma Teste", curso=self.curso, status="A"
        )

        self.aluno = Aluno.objects.create(
            nome="Aluno Teste", cpf="12345678901", email="aluno@teste.com"
        )

        self.atividade = AtividadeAcademica.objects.create(
            nome="Atividade Teste", codigo="AT001", ativo=True
        )

        # Criar presença detalhada
        self.presenca = PresencaDetalhada.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=10,
            presencas=8,
            faltas=2,
            voluntario_extra=1,
            voluntario_simples=2,
        )

        # URLs
        self.consolidado_url = reverse("presencas:consolidado")
        self.filtros_url = reverse("presencas:filtros_consolidado")
        self.exportar_url = reverse("presencas:exportar_consolidado")

    def test_consolidado_requires_login(self):
        """Testa se a view requer login."""
        response = self.client.get(self.consolidado_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.consolidado_url}")

    def test_consolidado_get_success(self):
        """Testa GET bem-sucedido da view consolidado."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(self.consolidado_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Consolidado de Presenças")
        self.assertIn("dados_consolidados", response.context)
        self.assertIn("estatisticas", response.context)
        self.assertIn("filtros", response.context)

    def test_consolidado_with_filters(self):
        """Testa consolidado com filtros aplicados."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(
            self.consolidado_url,
            {
                "turma_id": self.turma.id,
                "periodo_inicio": "2024-01-01",
                "periodo_fim": "2024-12-31",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("dados_consolidados", response.context)

        # Verificar se os filtros foram aplicados
        filtros = response.context["filtros"]
        self.assertEqual(filtros["turma_id"], str(self.turma.id))

    def test_consolidado_ajax_salvar_celula(self):
        """Testa salvamento AJAX de célula."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            self.consolidado_url,
            {
                "acao": "salvar_celula",
                "presenca_id": self.presenca.id,
                "campo": "convocacoes",
                "valor": "12",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)

        # Verificar resposta JSON
        data = json.loads(response.content)
        self.assertTrue(data["success"])
        self.assertIn("nova_presenca", data)

        # Verificar se foi salvo no banco
        self.presenca.refresh_from_db()
        self.assertEqual(self.presenca.convocacoes, 12)

    def test_consolidado_ajax_salvar_celula_valor_invalido(self):
        """Testa salvamento AJAX com valor inválido."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            self.consolidado_url,
            {
                "acao": "salvar_celula",
                "presenca_id": self.presenca.id,
                "campo": "convocacoes",
                "valor": "-1",  # Valor inválido
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)

        # Verificar resposta JSON
        data = json.loads(response.content)
        self.assertFalse(data["success"])
        self.assertIn("error", data)

    def test_consolidado_ajax_carregar_turmas(self):
        """Testa carregamento AJAX de turmas."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(
            self.consolidado_url,
            {"acao": "carregar_filtros", "tipo": "turmas", "curso_id": self.curso.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)

        # Verificar resposta JSON
        data = json.loads(response.content)
        self.assertTrue(data["success"])
        self.assertIn("turmas", data)
        self.assertEqual(len(data["turmas"]), 1)
        self.assertEqual(data["turmas"][0]["nome"], "Turma Teste")

    def test_filtros_consolidado_get(self):
        """Testa GET da view de filtros."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(self.filtros_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Filtros Avançados")
        self.assertIn("cursos", response.context)
        self.assertIn("turmas", response.context)
        self.assertIn("atividades", response.context)

    def test_filtros_consolidado_post(self):
        """Testa POST da view de filtros."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            self.filtros_url,
            {
                "turma_id": self.turma.id,
                "periodo_inicio": "2024-01-01",
                "periodo_fim": "2024-12-31",
            },
        )

        # Deve redirecionar para consolidado com filtros
        self.assertEqual(response.status_code, 302)
        self.assertIn("consolidado", response.url)
        self.assertIn("turma_id", response.url)

    def test_exportar_consolidado_get(self):
        """Testa exportação do consolidado."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(self.exportar_url)

        # Deve retornar arquivo ou redirecionar em caso de erro
        self.assertIn(response.status_code, [200, 302])

        if response.status_code == 200:
            # Verificar headers do Excel
            self.assertIn("application/vnd.openxmlformats", response["Content-Type"])
            self.assertIn("attachment", response["Content-Disposition"])

    def test_consolidado_with_no_data(self):
        """Testa consolidado sem dados."""
        # Remover presença de teste
        self.presenca.delete()

        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(self.consolidado_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhum registro encontrado")

    def test_consolidado_pagination(self):
        """Testa paginação de atividades."""
        # Criar mais atividades
        for i in range(15):
            AtividadeAcademica.objects.create(
                nome=f"Atividade {i}", codigo=f"AT{i:03d}", ativo=True
            )

        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(self.consolidado_url, {"pagina_atividade": 2})

        self.assertEqual(response.status_code, 200)
        self.assertIn("atividades_paginadas", response.context)

        # Verificar se tem paginação
        page_obj = response.context["atividades_paginadas"]
        if page_obj.has_other_pages:
            self.assertEqual(page_obj.number, 2)

    def test_consolidado_statistics(self):
        """Testa cálculo de estatísticas."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(self.consolidado_url)

        estatisticas = response.context["estatisticas"]

        self.assertEqual(estatisticas["total_registros"], 1)
        self.assertEqual(estatisticas["alunos_unicos"], 1)
        self.assertEqual(estatisticas["atividades_unicas"], 1)
        self.assertEqual(estatisticas["total_convocacoes"], 10)
        self.assertEqual(estatisticas["total_presencas"], 8)

    def test_consolidado_ordering(self):
        """Testa ordenação dos dados."""
        # Criar mais um aluno
        aluno2 = Aluno.objects.create(
            nome="Aluno B", cpf="98765432100", email="aluno2@teste.com"
        )

        PresencaDetalhada.objects.create(
            aluno=aluno2,
            turma=self.turma,
            atividade=self.atividade,
            periodo=date(2024, 1, 1),
            convocacoes=5,
            presencas=4,
            faltas=1,
        )

        self.client.login(username="testuser", password="testpass123")

        # Testar ordenação por nome
        response = self.client.get(
            self.consolidado_url, {"ordenar_por": "aluno__nome", "ordem": "asc"}
        )

        self.assertEqual(response.status_code, 200)
        # Verificar se os dados estão ordenados
        dados = response.context["dados_consolidados"]
        nomes = [dados[k]["aluno"].nome for k in dados.keys()]
        self.assertEqual(nomes, sorted(nomes))


class ConsolidadoIntegrationTestCase(TestCase):
    """
    Tests de integração para o consolidado.
    """

    def setUp(self):
        """Configuração inicial."""
        self.client = Client()

        # Criar usuário staff
        self.user = User.objects.create_user(
            username="staff", password="testpass123", is_staff=True
        )

        # Criar dados mais complexos
        self.curso = Curso.objects.create(
            nome="Curso Integração", codigo="CI001", ativo=True
        )
        self.turma = Turma.objects.create(
            nome="Turma Integração", curso=self.curso, status="A"
        )

        # Criar múltiplos alunos
        self.alunos = []
        for i in range(5):
            aluno = Aluno.objects.create(
                nome=f"Aluno {i + 1}",
                cpf=f"1234567890{i}",
                email=f"aluno{i + 1}@teste.com",
            )
            self.alunos.append(aluno)

        # Criar múltiplas atividades
        self.atividades = []
        for i in range(3):
            atividade = AtividadeAcademica.objects.create(
                nome=f"Atividade {i + 1}", codigo=f"AI{i + 1:03d}", ativo=True
            )
            self.atividades.append(atividade)

        # Criar presenças detalhadas
        for aluno in self.alunos:
            for atividade in self.atividades:
                PresencaDetalhada.objects.create(
                    aluno=aluno,
                    turma=self.turma,
                    atividade=atividade,
                    periodo=date(2024, 1, 1),
                    convocacoes=10,
                    presencas=8,
                    faltas=2,
                    voluntario_extra=1,
                    voluntario_simples=1,
                )

    def test_consolidado_full_workflow(self):
        """Testa workflow completo do consolidado."""
        self.client.login(username="staff", password="testpass123")

        # 1. Carregar consolidado
        response = self.client.get(reverse("presencas:consolidado"))
        self.assertEqual(response.status_code, 200)

        # 2. Aplicar filtros
        response = self.client.get(
            reverse("presencas:consolidado"),
            {
                "turma_id": self.turma.id,
                "periodo_inicio": "2024-01-01",
                "periodo_fim": "2024-12-31",
            },
        )
        self.assertEqual(response.status_code, 200)

        # 3. Editar célula via AJAX
        presenca = PresencaDetalhada.objects.first()
        response = self.client.post(
            reverse("presencas:consolidado"),
            {
                "acao": "salvar_celula",
                "presenca_id": presenca.id,
                "campo": "presencas",
                "valor": "9",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)

        # 4. Exportar dados
        response = self.client.get(reverse("presencas:exportar_consolidado"))
        self.assertIn(response.status_code, [200, 302])

        # 5. Verificar se alteração foi salva
        presenca.refresh_from_db()
        self.assertEqual(presenca.presencas, 9)

    def test_consolidado_performance(self):
        """Testa performance com muitos dados."""
        self.client.login(username="staff", password="testpass123")

        # Medir tempo de carregamento
        import time

        start_time = time.time()

        response = self.client.get(reverse("presencas:consolidado"))

        end_time = time.time()
        load_time = end_time - start_time

        self.assertEqual(response.status_code, 200)
        self.assertLess(load_time, 5.0)  # Deve carregar em menos de 5 segundos
