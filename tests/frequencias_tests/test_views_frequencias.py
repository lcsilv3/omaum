import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from frequencias.models import FrequenciaMensal, Carencia
from alunos.services import criar_aluno
from turmas.models import Turma
from atividades.models import Atividade
from matriculas.models import Matricula


@pytest.mark.django_db
class FrequenciasViewsTestCase(TestCase):
    """Testes de integração para as views do módulo de frequências."""

    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Criar uma turma para os testes
        self.turma = Turma.objects.create(nome="Turma de Teste", status="A")

        # Criar uma atividade para os testes
        self.atividade = Atividade.objects.create(
            nome="Atividade de Teste",
            descricao="Descrição da atividade",
            data_inicio=timezone.now(),
            responsavel="Professor Teste",
            tipo_atividade="aula",
            status="agendada",
        )
        self.atividade.turmas.add(self.turma)

        # Criar alunos para os testes usando o serviço
        self.aluno1 = criar_aluno(
            {
                "cpf": "12345678900",
                "nome": "Aluno Teste 1",
                "email": "aluno1@teste.com",
                "data_nascimento": "1990-01-01",
            }
        )

        self.aluno2 = criar_aluno(
            {
                "cpf": "98765432100",
                "nome": "Aluno Teste 2",
                "email": "aluno2@teste.com",
                "data_nascimento": "1992-05-15",
            }
        )

        # Matricular alunos na turma
        Matricula.objects.create(
            aluno=self.aluno1,
            turma=self.turma,
            data_matricula=timezone.now().date(),
            status="A",
        )

        Matricula.objects.create(
            aluno=self.aluno2,
            turma=self.turma,
            data_matricula=timezone.now().date(),
            status="A",
        )

        # Criar uma frequência mensal para os testes
        self.frequencia = FrequenciaMensal.objects.create(
            turma=self.turma, mes=timezone.now().month, ano=timezone.now().year
        )
        # Criar carências para os alunos
        Carencia.objects.create(
            frequencia_mensal=self.frequencia,
            aluno=self.aluno1,
            total_presencas=5,
            total_atividades=6,
            percentual_presenca=83.3,
            numero_carencias=1,
            liberado=True,
            data_identificacao=timezone.now().date(),
            status="RESOLVIDO",
        )
        Carencia.objects.create(
            frequencia_mensal=self.frequencia,
            aluno=self.aluno2,
            total_presencas=2,
            total_atividades=6,
            percentual_presenca=33.3,
            numero_carencias=4,
            liberado=False,
            data_identificacao=timezone.now().date(),
            status="PENDENTE",
        )

        # Cliente para fazer requisições
        self.client = Client()

    def test_listar_frequencias_view(self):
        """Testa se a view de listagem de frequências funciona corretamente."""
        # Fazer login
        self.client.login(username="testuser", password="testpassword")

        # Acessar a página de listagem de frequências
        response = self.client.get(reverse("frequencias:listar_frequencias"))

        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verificar se as frequências estão no contexto
        self.assertIn("frequencias", response.context)
        self.assertEqual(len(response.context["frequencias"]), 1)

        # Verificar se a frequência está na página
        self.assertContains(response, self.atividade.nome)
        self.assertContains(response, self.frequencia.data.strftime("%d/%m/%Y"))

    def test_criar_frequencia_view(self):
        """Testa se a view de criação de frequência funciona corretamente."""
        # Fazer login
        self.client.login(username="testuser", password="testpassword")

        # Acessar a página de criação de frequência
        response = self.client.get(reverse("frequencias:criar_frequencia"))

        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verificar se o formulário está no contexto
        self.assertIn("form", response.context)

        # Dados para a nova frequência
        nova_frequencia_data = {
            "atividade": self.atividade.id,
            "data": timezone.now().date().strftime("%Y-%m-%d"),
            "observacoes": "Nova frequência de teste",
        }

        # Enviar o formulário para criar uma nova frequência
        response = self.client.post(
            reverse("frequencias:criar_frequencia"),
            data=nova_frequencia_data,
            follow=True,
        )

        # Verificar se o redirecionamento foi bem-sucedido
        self.assertEqual(response.status_code, 200)

        # Verificar se a frequência foi criada no banco de dados
        self.assertTrue(
            Frequencia.objects.filter(observacoes="Nova frequência de teste").exists()
        )

        # Verificar se a mensagem de sucesso está na página
        self.assertContains(response, "Frequência criada com sucesso")

    def test_registrar_frequencia_view(self):
        """Testa se a view de registro de frequência funciona corretamente."""
        # Fazer login
        self.client.login(username="testuser", password="testpassword")

        # Acessar a página de registro de frequência
        response = self.client.get(
            reverse("frequencias:registrar_frequencia", args=[self.frequencia.id])
        )

        # Verificar se a resposta foi bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verificar se o formset está no contexto
        self.assertIn("formset", response.context)

        # Dados para o registro de frequência
        registro_data = {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "2",
            "form-MAX_NUM_FORMS": "",
            "form-0-id": RegistroFrequencia.objects.get(aluno=self.aluno1).id,
            "form-0-aluno": self.aluno1.cpf,
            "form-0-presente": "False",
            "form-0-justificativa": "Faltou por motivo de saúde",
            "form-1-id": RegistroFrequencia.objects.get(aluno=self.aluno2).id,
            "form-1-aluno": self.aluno2.cpf,
            "form-1-presente": "True",
            "form-1-justificativa": "",
        }

        # Enviar o formulário para atualizar os registros de frequência
        response = self.client.post(
            reverse("frequencias:registrar_frequencia", args=[self.frequencia.id]),
            data=registro_data,
            follow=True,
        )

        # Verificar se o redirecionamento foi bem-sucedido
        self.assertEqual(response.status_code, 200)

        # Verificar se os registros foram atualizados no banco de dados
        registro1 = RegistroFrequencia.objects.get(aluno=self.aluno1)
        self.assertFalse(registro1.presente)
        self.assertEqual(registro1.justificativa, "Faltou por motivo de saúde")

        registro2 = RegistroFrequencia.objects.get(aluno=self.aluno2)
        self.assertTrue(registro2.presente)
        self.assertEqual(registro2.justificativa, "")

        # Verificar se a mensagem de sucesso está na página
        self.assertContains(response, "Frequência registrada com sucesso")  # Verific
