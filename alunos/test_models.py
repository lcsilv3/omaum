from django.test import TestCase
from alunos.models import Aluno, Pais, Estado, Cidade, Bairro
from datetime import date, time


class AlunoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Usar get_or_create para evitar erros de constraint em execuções de teste repetidas
        cls.pais, _ = Pais.objects.get_or_create(
            nome="Brasil", defaults={"nacionalidade": "Brasileira"}
        )
        cls.estado, _ = Estado.objects.get_or_create(
            nome="São Paulo", defaults={"codigo": "SP"}
        )
        cls.cidade, _ = Cidade.objects.get_or_create(
            nome="São Paulo", defaults={"estado": cls.estado}
        )
        cls.bairro, _ = Bairro.objects.get_or_create(
            nome="Centro", defaults={"cidade": cls.cidade}
        )

    def test_criar_aluno(self):
        aluno = Aluno.objects.create(
            cpf="12345678901",
            nome="João Test",
            data_nascimento=date(1995, 5, 15),
            hora_nascimento=time(14, 30),
            email="joao@test.com",
            sexo="M",
            pais_nacionalidade=self.pais,
            cidade_naturalidade=self.cidade,
            rua="Rua Test",
            numero_imovel="123",
            cidade_ref=self.cidade,
            bairro_ref=self.bairro,
            cep="12345678",
        )
        self.assertEqual(aluno.nome, "João Test")
        self.assertEqual(aluno.nacionalidade_display, "Brasileira")
        # Acessar o estado através da cidade para a asserção
        self.assertEqual(
            aluno.naturalidade_display, "São Paulo, São Paulo"
        )  # Ajustado para não incluir país
        self.assertEqual(aluno.cidade_ref.nome, "São Paulo")
        self.assertEqual(aluno.bairro_ref.nome, "Centro")

    def test_aluno_str(self):
        aluno = Aluno.objects.create(
            nome="Maria Silva",
            cpf="98765432109",
            data_nascimento=date(1990, 1, 1),  # Campo obrigatório
            sexo="F",  # Campo obrigatório
        )
        self.assertEqual(str(aluno), "Maria Silva")
