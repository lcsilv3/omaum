# Arquivo de teste esvaziado para evitar erro de coleta pytest


import pytest
from turmas.forms import TurmaForm
from django.utils import timezone


@pytest.mark.django_db
class TestTurmaForm:
    """Testes para o formulário de Turma."""

    def test_form_valido(self):
        """Testa se o formulário é válido com dados corretos."""
        form_data = {
            "nome": "Turma de Filosofia 2023",
            "codigo": "FIL-2023",
            "data_inicio": timezone.now().date().strftime("%Y-%m-%d"),
            "status": "A",
        }

        form = TurmaForm(data=form_data)
        assert form.is_valid(), f"Formulário inválido: {form.errors}"

    def test_form_invalido_campos_obrigatorios(self):
        """Testa se o formulário é inválido quando campos obrigatórios estão ausentes."""
        form_data = {
            "status": "A",
        }

        form = TurmaForm(data=form_data)
        assert not form.is_valid()
        assert "nome" in form.errors
        assert "codigo" in form.errors

    def test_form_data_fim_anterior_data_inicio(self):
        """Testa se o formulário rejeita data de fim anterior à data de início."""
        form_data = {
            "nome": "Turma de Filosofia 2023",
            "codigo": "FIL-2023",
            "data_inicio": timezone.now().date().strftime("%Y-%m-%d"),
            "data_fim": (timezone.now().date() - timezone.timedelta(days=1)).strftime(
                "%Y-%m-%d"
            ),
            "status": "A",
        }

        form = TurmaForm(data=form_data)
        assert not form.is_valid()
        assert "data_fim" in form.errors or "__all__" in form.errors
