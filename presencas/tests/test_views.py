from django.test import TestCase, Client
from django.urls import reverse
from presencas.models import PresencaAcademica
from turmas.models import Turma
from alunos.services import criar_aluno
from datetime import date


class PresencaViewTest(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.presenca = PresencaAcademica.objects.create(
            turma=self.turma,
            aluno=self.aluno,
            data=date(2023, 10, 1),
            presente=True,
        )

    def test_listar_presencas(self):
        response = self.client.get(reverse("lista_presencas"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "João Silva")
