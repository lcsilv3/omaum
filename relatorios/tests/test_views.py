from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from alunos.services import criar_aluno
from alunos.models import Aluno, TipoCodigo, Codigo, RegistroHistorico
from presencas.models import PresencaAcademica
from datetime import date, time


class RelatorioViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Criar usuário de teste com permissões
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Adicionar permissões necessárias
        content_type_aluno = ContentType.objects.get_for_model(Aluno)
        permission_view_aluno = Permission.objects.get(
            content_type=content_type_aluno, codename="view_aluno"
        )
        self.user.user_permissions.add(permission_view_aluno)

        ct_presenca = ContentType.objects.get_for_model(PresencaAcademica)
        perm_view_presenca = Permission.objects.get(
            content_type=ct_presenca, codename="view_presencaacademica"
        )
        self.user.user_permissions.add(perm_view_presenca)

        # Fazer login
        self.client.login(username="testuser", password="testpassword")

        # Criar aluno de teste
        aluno_data = {
            "cpf": "12345678901",
            "nome": "Maria Oliveira",
            "data_nascimento": date(1985, 5, 15),
            "hora_nascimento": time(14, 30),
            "email": "maria@example.com",
            "sexo": "F",
            "nacionalidade": "Brasileira",
            "naturalidade": "São Paulo",
            "rua": "Rua Test",
            "numero_imovel": "123",
            "cidade": "São Paulo",
            "estado": "SP",
            "bairro": "Centro",
            "cep": "01234567",
            "nome_primeiro_contato": "João Oliveira",
            "celular_primeiro_contato": "11999999999",
            "tipo_relacionamento_primeiro_contato": "Pai",
            "nome_segundo_contato": "Ana Oliveira",
            "celular_segundo_contato": "11988888888",
            "tipo_relacionamento_segundo_contato": "Mãe",
            "tipo_sanguineo": "A",
            "fator_rh": "+",
        }
        self.aluno = criar_aluno(aluno_data)

        # Criar dados de teste para presenças
        self.presenca = PresencaAcademica.objects.create(
            aluno=self.aluno, data=date.today(), presente=True
        )

        # Criar dados de teste para histórico
        self.tipo_codigo = TipoCodigo.objects.create(nome="Punição")
        self.codigo = Codigo.objects.create(tipo_codigo=self.tipo_codigo, nome="Advertência")
        self.registro_historico = RegistroHistorico.objects.create(
            aluno=self.aluno,
            codigo=self.codigo,
            data_os=date.today(),
            ordem_servico="OS-001"
        )

    def test_relatorio_alunos(self):
        response = self.client.get(reverse("relatorio_alunos"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maria Oliveira")

        # Testar filtros
        response = self.client.get(f"{reverse('relatorio_alunos')}?nome=Maria")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maria Oliveira")

        response = self.client.get(
            f"{reverse('relatorio_alunos')}?nome=Inexistente"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Maria Oliveira")

    def test_relatorio_alunos_pdf(self):
        response = self.client.get(reverse("relatorio_alunos_pdf"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

        # Testar com filtros
        response = self.client.get(
            f"{reverse('relatorio_alunos_pdf')}?nome=Maria"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_relatorio_presencas(self):
        response = self.client.get(reverse("relatorio_presencas"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maria Oliveira")

        # Testar filtros
        response = self.client.get(
            f"{reverse('relatorio_presencas')}?aluno={self.aluno.id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maria Oliveira")

        # Testar filtro de data
        data_hoje = date.today().strftime("%Y-%m-%d")
        response = self.client.get(
            f"{reverse('relatorio_presencas')}?data_inicio={data_hoje}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maria Oliveira")

    def test_relatorio_presencas_pdf(self):
        response = self.client.get(reverse("relatorio_presencas_pdf"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

        # Testar com filtros
        response = self.client.get(
            f"{reverse('relatorio_presencas_pdf')}?aluno={self.aluno.id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_relatorio_historico(self):
        response = self.client.get(reverse("relatorios:relatorio_historico"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maria Oliveira")
        self.assertContains(response, "Advertência")

    def test_relatorio_historico_pdf(self):
        response = self.client.get(reverse("relatorios:relatorio_historico_pdf"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
