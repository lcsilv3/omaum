from django.test import TestCase
from django.urls import reverse
from presencas.models import Presenca
from turmas.models import Turma
from alunos.models import Aluno
from atividades.models import Atividade


class PresencaViewsTest(TestCase):
    def setUp(self):
        self.turma = Turma.objects.create(nome="Turma Teste")
        self.aluno = Aluno.objects.create(nome="Aluno Teste", cpf="12345678900")
        self.atividade = Atividade.objects.create(nome="Atividade Teste")
        self.presenca = Presenca.objects.create(
            aluno=self.aluno,
            turma=self.turma,
            atividade=self.atividade,
            data="2025-08-13",
            presente=True,
        )

    def test_excluir_presenca(self):
        url = reverse("presencas:excluir_presenca")
        response = self.client.post(
            url,
            {
                "presenca_id": self.presenca.id,
                "turma_id": self.turma.id,
                "ano": 2025,
                "mes": 8,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Presenca.objects.filter(id=self.presenca.id).exists())
