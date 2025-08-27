import pytest
from django.test import TestCase
from django.utils import timezone
from frequencias.forms import FrequenciaMensalForm
from turmas.models import Turma
from atividades.models import Atividade


@pytest.mark.django_db
class FrequenciaFormTestCase(TestCase):
    """Testes unitários para o formulário de frequência."""

    def setUp(self):
        """Configuração inicial para os testes."""
        from cursos.models import Curso

        curso = Curso.objects.create(nome="Curso Teste")
        self.turma = Turma.objects.create(
            nome="Turma de Teste", curso=curso, status="A"
        )
        self.atividade = Atividade.objects.create(
            nome="Atividade de Teste",
            tipo_atividade="AULA",
            data_inicio=timezone.now().date(),
            hora_inicio=timezone.now().time(),
            status="PENDENTE",
        )
        self.atividade.turmas.add(self.turma)

    def test_frequencia_form_valido(self):
        """Testa se o formulário é válido com dados corretos."""
        form_data = {
            "atividade": self.atividade.id,
            "data": timezone.now().date(),
            "observacoes": "Teste de formulário",
        }
        form = FrequenciaMensalForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_frequencia_form_invalido(self):
        """Testa se o formulário é inválido com dados incorretos."""
        # Formulário sem turma
        form_data = {"mes": 8, "ano": 2025, "percentual_minimo": 75}
        form = FrequenciaMensalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("turma", form.errors)

        # Formulário sem mes
        form_data = {"turma": self.turma.id, "ano": 2025, "percentual_minimo": 75}
        form = FrequenciaMensalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("mes", form.errors)

        # Formulário sem ano
        form_data = {"turma": self.turma.id, "mes": 8, "percentual_minimo": 75}
        form = FrequenciaMensalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("ano", form.errors)

        # Formulário sem percentual_minimo
        form_data = {"turma": self.turma.id, "mes": 8, "ano": 2025}
        form = FrequenciaMensalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("percentual_minimo", form.errors)
