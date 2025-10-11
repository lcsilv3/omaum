"""Testes atualizados para o fluxo unificado de presenças."""

from __future__ import annotations

from datetime import date, timedelta, time
from importlib import import_module

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from alunos.models import Aluno
from presencas.models import RegistroPresenca


class PresencasViewsSmokeTest(TestCase):
    """Valida o funcionamento mínimo das views principais e placeholders."""

    def setUp(self) -> None:
        user_model = get_user_model()
        self.usuario = user_model.objects.create_user(
            username="testuser", password="12345"
        )

        cursos_module = import_module("cursos.models")
        self.Curso = getattr(cursos_module, "Curso")
        self.curso = self.Curso.objects.create(
            nome="Curso Teste", descricao="Curso para testes", ativo=True
        )

        self.aluno = Aluno.objects.create(
            nome="Aluno Teste",
            cpf="12345678901",
            email="aluno@teste.com",
            data_nascimento=date(1990, 1, 1),
        )

        turmas_module = import_module("turmas.models")
        self.Turma = getattr(turmas_module, "Turma")
        self.turma = self.Turma.objects.create(
            nome="Turma Teste",
            curso=self.curso,
            vagas=20,
            data_inicio_ativ=date(2024, 1, 15),
            ativo=True,
        )

        atividades_module = import_module("atividades.models")
        self.Atividade = getattr(atividades_module, "Atividade")
        self.atividade = self.Atividade.objects.create(
            nome="Aula Magna",
            descricao="Atividade de teste",
            tipo_atividade="AULA",
            data_inicio=date.today(),
            data_fim=date.today(),
            hora_inicio=time(19, 0),
            hora_fim=time(20, 0),
            status="CONFIRMADA",
            curso=self.curso,
        )
        self.atividade.turmas.add(self.turma)

        self.presenca = RegistroPresenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            data=date.today(),
            status="P",
            registrado_por=self.usuario.username,
        )

    def test_listagem_exige_autenticacao(self) -> None:
        """Usuário não autenticado deve ser redirecionado para login."""

        response = self.client.get(reverse("presencas:listar_presencas"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))

    def test_listagem_autenticada_exibe_registros(self) -> None:
        """Usuário autenticado visualiza listagem com dados básicos."""

        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("presencas:listar_presencas"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "presencas/academicas/listar_presencas_academicas.html"
        )
        self.assertContains(response, self.aluno.nome)

    def test_placeholder_fluxo_guiado_redireciona(self) -> None:
        """Views placeholder informam indisponibilidade e redirecionam."""

        self.client.login(username="testuser", password="12345")
        response = self.client.get(
            reverse("presencas:registrar_presenca_dados_basicos")
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("presencas:listar_presencas_academicas"))

    def test_placeholder_ajax_retorna_json(self) -> None:
        """Endpoints AJAX placeholders retornam resposta JSON 501."""

        self.client.login(username="testuser", password="12345")
        response = self.client.get(
            reverse("presencas:registrar_presenca_dados_basicos_ajax")
        )
        self.assertEqual(response.status_code, 501)
        self.assertFalse(response.json()["success"])  # type: ignore[index]

    def test_registro_rapido_cria_registro_presenca(self) -> None:
        """Formulário rápido deve criar ou atualizar registros de presença."""

        self.client.login(username="testuser", password="12345")
        nova_data = date.today() + timedelta(days=1)
        response = self.client.post(
            reverse("presencas:registrar_presenca_academica"),
            {
                "aluno": self.aluno.cpf,
                "turma": str(self.turma.id),
                "atividade": str(self.atividade.id),
                "data": nova_data.isoformat(),
                "presente": "on",
                "observacao": "Teste automatizado",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("presencas:listar_presencas_academicas"))
        self.assertTrue(
            RegistroPresenca.objects.filter(
                aluno=self.aluno,
                turma=self.turma,
                atividade=self.atividade,
                data=nova_data,
            ).exists()
        )
