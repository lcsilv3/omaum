from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cursos.models import Curso
from turmas.forms import TurmaForm
from turmas.models import Turma
from presencas.forms import RegistrarPresencaForm
from frequencias.forms import FrequenciaMensalForm


class BaseTurmaTestCase(TestCase):
    """Helper base para montar dados mínimos de curso/turma."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            email="tester@example.com",
        )
        self.client.login(username="testuser", password="testpass123")
        self.curso = Curso.objects.create(nome="Curso Teste", descricao="Desc")
        self.turma = Turma.objects.create(
            nome="Turma Base",
            curso=self.curso,
            status="A",
            data_inicio=date.today(),
            vagas=20,
        )

    def payload_formulario(self, **override):
        base = {
            "curso": self.curso.id,
            "nome": override.get("nome", "Turma Form"),
            "descricao": "",
            "data_inicio": date.today().isoformat(),
            "data_fim": override.get("data_fim", ""),
            "num_livro": 1,
            "perc_presenca_minima": "75.00",
            "data_iniciacao": date.today().isoformat(),
            "data_inicio_ativ": date.today().isoformat(),
            "data_termino_atividades": "",
            "data_prim_aula": date.today().isoformat(),
            "dias_semana": "3ª e 5ª",
            "horario": '19:30 "às" 21:00',
            "local": "Sala 1",
            "vagas": 25,
            "status": "A",
            "confirmar_encerramento": override.get("confirmar_encerramento", ""),
        }
        base.update(override)
        return base


class TurmaFormEncerramentoTest(BaseTurmaTestCase):
    def test_confirmacao_obrigatoria_para_data_fim(self):
        form = TurmaForm(
            data=self.payload_formulario(
                data_fim=(date.today() + timedelta(days=7)).isoformat()
            ),
            usuario=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("confirmar_encerramento", form.errors)

    def test_flag_encerrar_eh_definida_quando_confirmado(self):
        form = TurmaForm(
            data=self.payload_formulario(
                data_fim=(date.today() + timedelta(days=7)).isoformat(),
                confirmar_encerramento="on",
            ),
            usuario=self.user,
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data.get("_encerrar"))


class TurmaViewsTest(BaseTurmaTestCase):
    def test_criar_turma_dispara_criacao_de_atividades(self):
        payload = self.payload_formulario(nome="Turma Nova")
        with patch(
            "turmas.views.turma_services.criar_atividades_basicas"
        ) as mock_criar, patch(
            "turmas.views.turma_services.encerrar_turma"
        ) as mock_encerrar:
            response = self.client.post(reverse("turmas:criar_turma"), payload)
        self.assertEqual(response.status_code, 302)
        mock_criar.assert_called_once()
        mock_encerrar.assert_not_called()

    def test_editar_turma_encerrando_registra_auditoria(self):
        payload = self.payload_formulario(
            nome="Turma Base",
            data_fim=(date.today() + timedelta(days=1)).isoformat(),
            confirmar_encerramento="on",
        )
        with patch("turmas.views.turma_services.encerrar_turma") as mock_encerrar:
            response = self.client.post(
                reverse("turmas:editar_turma", args=[self.turma.id]),
                payload,
            )
        self.assertEqual(response.status_code, 302)
        mock_encerrar.assert_called_once()

    def test_transferir_alunos_chama_service(self):
        turma_destino = Turma.objects.create(
            nome="Turma Destino",
            curso=self.curso,
            status="A",
            data_inicio=date.today(),
            vagas=30,
        )
        self.turma.data_fim = date.today()
        self.turma.encerrada_em = timezone.now()
        self.turma.encerrada_por = self.user
        self.turma.save()

        url = reverse("turmas:transferir_alunos_turma", args=[self.turma.id])
        payload = {"turma_destino": turma_destino.id, "confirmacao": "on"}
        with patch(
            "turmas.views.turma_services.transferir_matriculas_em_lote",
            return_value=0,
        ) as mock_transferir:
            response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        mock_transferir.assert_called_once_with(self.turma, turma_destino, self.user)


class IntegracoesBloqueioTest(TestCase):
    def setUp(self):
        self.curso = Curso.objects.create(nome="Curso Integracao", descricao="Desc")
        self.turma_encerrada = Turma.objects.create(
            nome="Turma Encerrada",
            curso=self.curso,
            status="A",
            data_inicio=date.today(),
            data_fim=date.today(),
            encerrada_em=timezone.now(),
            vagas=10,
        )
        self.turma_encerrada.encerrada_por = get_user_model().objects.create_user(
            username="auditor",
            password="teste123",
        )
        self.turma_encerrada.save()

    def test_form_presenca_recusa_turma_encerrada(self):
        form = RegistrarPresencaForm(
            data={
                "curso": self.curso.id,
                "turma": self.turma_encerrada.id,
                "ano": timezone.now().year,
                "mes": timezone.now().month,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("turma", form.errors)

    def test_form_frequencia_recusa_turma_encerrada(self):
        form = FrequenciaMensalForm(
            data={
                "turma": self.turma_encerrada.id,
                "mes": 1,
                "ano": timezone.now().year,
                "percentual_minimo": 70,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("turma", form.errors)
