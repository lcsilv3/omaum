import json
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from alunos.models import Aluno, Codigo, RegistroHistorico, TipoCodigo
from alunos.services import HistoricoService


class HistoricoApiTestCase(TestCase):
    """Testa a criação e manutenção de registros de histórico via API."""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.tipo = TipoCodigo.objects.create(nome="Progressao", descricao="")
        cls.codigo = Codigo.objects.create(
            tipo_codigo=cls.tipo,
            nome="Grau II",
            descricao="Segundo grau",
        )
        cls.aluno = Aluno.objects.create(
            cpf="98765432100",
            nome="Maria Teste",
            data_nascimento=date(1992, 6, 20),
            email="maria@example.com",
            sexo="F",
            numero_iniciatico="0002",
        )

    def setUp(self) -> None:
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="senha@test",
            is_staff=True,
        )
        permissoes = Permission.objects.filter(
            codename__in=["add_registrohistorico", "change_registrohistorico"]
        )
        self.user.user_permissions.add(*permissoes)
        self.client.force_login(self.user)

    def test_criar_historico_api_sucesso(self) -> None:
        url = reverse("alunos:api_criar_historico_aluno", args=[self.aluno.id])
        payload = {
            "codigo_id": self.codigo.id,
            "data_os": date(2024, 9, 1).isoformat(),
            "ordem_servico": "OS/24",
            "observacoes": "Registro criado via API",
        }

        resposta = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(resposta.status_code, 201)
        corpo = resposta.json()
        self.assertEqual(corpo["status"], "success")
        self.assertEqual(RegistroHistorico.objects.count(), 1)
        registro = RegistroHistorico.objects.first()
        self.assertIsNotNone(registro)
        self.assertEqual(registro.ordem_servico, "OS/2024")
        self.assertEqual(registro.codigo, self.codigo)

    def test_criar_historico_api_data_invalida(self) -> None:
        url = reverse("alunos:api_criar_historico_aluno", args=[self.aluno.id])
        payload = {
            "codigo_id": self.codigo.id,
            "data_os": (date.today() + timedelta(days=1)).isoformat(),
        }

        resposta = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(resposta.status_code, 400)
        corpo = resposta.json()
        self.assertEqual(corpo["status"], "error")
        self.assertIn("data_os", corpo["errors"])
        self.assertEqual(RegistroHistorico.objects.count(), 0)

    def test_desativar_historico_api(self) -> None:
        registro = HistoricoService.criar_evento(
            self.aluno,
            {
                "codigo_id": self.codigo.id,
                "data_os": date(2023, 4, 10),
                "observacoes": "Ativo",
            },
        )

        url = reverse(
            "alunos:api_desativar_historico_aluno",
            args=[self.aluno.id, registro.id],
        )
        resposta = self.client.post(
            url,
            data=json.dumps({"motivo": "Correção de dados"}),
            content_type="application/json",
        )

        self.assertEqual(resposta.status_code, 200)
        corpo = resposta.json()
        self.assertEqual(corpo["status"], "success")
        registro.refresh_from_db()
        self.assertFalse(registro.ativo)
        self.assertIn("Correção de dados", registro.observacoes)

    def test_reativar_historico_api(self) -> None:
        registro = HistoricoService.criar_evento(
            self.aluno,
            {
                "codigo_id": self.codigo.id,
                "data_os": date(2022, 8, 5),
            },
        )
        HistoricoService.desativar_evento(registro, motivo="Inativado temporariamente")

        url = reverse(
            "alunos:api_reativar_historico_aluno",
            args=[self.aluno.id, registro.id],
        )
        resposta = self.client.post(url)

        self.assertEqual(resposta.status_code, 200)
        corpo = resposta.json()
        self.assertEqual(corpo["status"], "success")
        registro.refresh_from_db()
        self.assertTrue(registro.ativo)
