from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from iniciacoes.models import Iniciacao
from alunos.models import Aluno
from datetime import date, time


class IniciacaoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Criar um usuário de teste e fazer login
        self.usuario = User.objects.create_user(
            username="usuarioteste", password="12345"
        )
        self.client.login(username="usuarioteste", password="12345")

        self.aluno = Aluno.objects.create(
            cpf="12345678901",
            nome="João Silva",
            data_nascimento=date(1990, 1, 1),
            hora_nascimento=time(14, 30),
            email="joao@example.com",
            sexo="M",
            nacionalidade="Brasileira",
            naturalidade="São Paulo",
            rua="Rua Test",
            numero_imovel="123",
            cidade="São Paulo",
            estado="SP",
            bairro="Centro",
            cep="01234567",
            nome_primeiro_contato="Maria Silva",
            celular_primeiro_contato="11999999999",
            tipo_relacionamento_primeiro_contato="Mãe",
            nome_segundo_contato="José Silva",
            celular_segundo_contato="11988888888",
            tipo_relacionamento_segundo_contato="Pai",
            tipo_sanguineo="A",
            fator_rh="+",
        )
        self.iniciacao = Iniciacao.objects.create(
            aluno=self.aluno,
            nome_curso="Curso de Iniciação",
            data_iniciacao=date(2023, 10, 1),
        )

    def test_listar_iniciacoes(self):
        response = self.client.get(reverse("iniciacoes:listar_iniciacoes"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "João Silva")
        self.assertContains(response, "Curso de Iniciação")
