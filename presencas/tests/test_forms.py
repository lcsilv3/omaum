from django.test import TestCase
from presencas.forms import PresencaForm
from alunos.services import criar_aluno
from turmas.models import Turma
from datetime import date, timedelta


class PresencaFormTest(TestCase):
    def setUp(self):
        self.turma = Turma.objects.create(codigo_turma="TURMA001", nome="Turma de Teste")
        self.aluno = criar_aluno({
            "cpf": "12345678901",
            "nome": "João Silva",
            "data_nascimento": "1990-01-01",
            "hora_nascimento": "14:30",
            "email": "joao@example.com",
            "sexo": "M",
            "nacionalidade": "Brasileira",
            "naturalidade": "São Paulo",
            "rua": "Rua Test",
            "numero_imovel": "123",
            "cidade": "São Paulo",
            "estado": "SP",
            "bairro": "Centro",
            "cep": "01234567",
            "nome_primeiro_contato": "Maria Silva",
            "celular_primeiro_contato": "11999999999",
            "tipo_relacionamento_primeiro_contato": "Mãe",
            "nome_segundo_contato": "José Silva",
            "celular_segundo_contato": "11988888888",
            "tipo_relacionamento_segundo_contato": "Pai",
            "tipo_sanguineo": "A",
            "fator_rh": "+",
        })

    def test_form_valido(self):
        data = {
            "aluno": self.aluno.id,
            "turma": self.turma.id,
            "data": date.today(),
            "presente": True,
        }
        form = PresencaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_data_futura(self):
        data = {
            "aluno": self.aluno.id,
            "turma": self.turma.id,
            "data": date.today() + timedelta(days=1),
            "presente": True,
        }
        form = PresencaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("data", form.errors)

    def test_form_duplicado(self):
        # Criar uma presença inicial
        data = {
            "aluno": self.aluno.id,
            "turma": self.turma.id,
            "data": date.today(),
            "presente": True,
        }
        form = PresencaForm(data=data)
        form.is_valid()
