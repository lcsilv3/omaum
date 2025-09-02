from django.test import TestCase
from alunos.models import Aluno, Pais, Estado, Cidade, Bairro
from datetime import date, time, timedelta
from django.core.exceptions import ValidationError


class AlunoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
            cep="01234567",
            nome_primeiro_contato="Maria Test",
            celular_primeiro_contato="11999999999",
            tipo_relacionamento_primeiro_contato="Mãe",
            nome_segundo_contato="José Test",
            celular_segundo_contato="11988888888",
            tipo_relacionamento_segundo_contato="Pai",
            tipo_sanguineo="A",
        )
        self.assertEqual(aluno.nome, "João Test")
        self.assertEqual(aluno.cidade_ref, self.cidade)


class AlunoValidationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
            nome="Consolação", defaults={"cidade": cls.cidade}
        )

    def setUp(self):
        self.valid_data = {
            "cpf": "12345678901",
            "nome": "Carlos Souza",
            "data_nascimento": date(1975, 12, 25),
            "hora_nascimento": time(8, 30),
            "email": "carlos@example.com",
            "sexo": "M",
            "pais_nacionalidade": self.pais,
            "cidade_naturalidade": self.cidade,
            "rua": "Rua Augusta",
            "numero_imovel": "789",
            "cidade_ref": self.cidade,
            "bairro_ref": self.bairro,
            "cep": "01234567",
            "nome_primeiro_contato": "Pedro Souza",
            "celular_primeiro_contato": "11999999999",
            "tipo_relacionamento_primeiro_contato": "Pai",
            "nome_segundo_contato": "Julia Souza",
            "celular_segundo_contato": "11988888888",
            "tipo_relacionamento_segundo_contato": "Mãe",
            "tipo_sanguineo": "B",
        }

    def test_cpf_invalido(self):
        self.valid_data["cpf"] = "123"
        aluno = Aluno(**self.valid_data)
        with self.assertRaises(ValidationError):
            aluno.full_clean()

    def test_email_invalido(self):
        self.valid_data["email"] = "email_invalido"
        aluno = Aluno(**self.valid_data)
        with self.assertRaises(ValidationError):
            aluno.full_clean()

    def test_sexo_invalido(self):
        self.valid_data["sexo"] = "X"
        aluno = Aluno(**self.valid_data)
        with self.assertRaises(ValidationError):
            aluno.full_clean()

    def test_data_futura_invalida(self):
        self.valid_data["data_nascimento"] = date.today() + timedelta(days=1)
        aluno = Aluno(**self.valid_data)
        try:
            aluno.full_clean()
            self.fail("ValidationError não foi levantado para data_nascimento futura")
        except ValidationError as e:
            self.assertIn("data_nascimento", e.message_dict)


class SeleniumTestCase(TestCase):
    """Classe base para testes Selenium com configuração robusta."""

    def setUp(self):
        self.skipTest("Ignorando temporariamente os testes Selenium.")
