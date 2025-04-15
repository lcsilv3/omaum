from django.test import TestCase
from alunos.models import Aluno
from datetime import date, time
from django.core.exceptions import (
    ValidationError,
)  # Adicionada importação faltante


class AlunoTest(TestCase):
    def test_criar_aluno(self):
        aluno = Aluno.objects.create(
            cpf="12345678901",
            nome="João Test",
            data_nascimento=date(1995, 5, 15),
            hora_nascimento=time(14, 30),
            email="joao@test.com",
            sexo="M",
            nacionalidade="Brasileira",
            naturalidade="São Paulo",
            rua="Rua Test",
            numero_imovel="123",
            cidade="São Paulo",
            estado="SP",
            bairro="Centro",
            cep="01234567",
            nome_primeiro_contato="Maria Test",
            celular_primeiro_contato="11999999999",
            tipo_relacionamento_primeiro_contato="Mãe",
            nome_segundo_contato="José Test",
            celular_segundo_contato="11988888888",
            tipo_relacionamento_segundo_contato="Pai",
            tipo_sanguineo="A",
            fator_rh="+",
        )
        self.assertEqual(aluno.nome, "João Test")


class AlunoValidationTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "cpf": "12345678901",
            "nome": "Carlos Souza",
            "data_nascimento": date(1975, 12, 25),
            "hora_nascimento": time(8, 30),
            "email": "carlos@example.com",
            "sexo": "M",
            "nacionalidade": "Brasileira",
            "naturalidade": "São Paulo",
            "rua": "Rua Augusta",
            "numero_imovel": "789",
            "cidade": "São Paulo",
            "estado": "SP",
            "bairro": "Consolação",
            "cep": "01234567",
            "nome_primeiro_contato": "Pedro Souza",
            "celular_primeiro_contato": "11999999999",
            "tipo_relacionamento_primeiro_contato": "Pai",
            "nome_segundo_contato": "Julia Souza",
            "celular_segundo_contato": "11988888888",
            "tipo_relacionamento_segundo_contato": "Mãe",
            "tipo_sanguineo": "B",
            "fator_rh": "+",
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
        self.valid_data["data_nascimento"] = date(2025, 1, 1)
        aluno = Aluno(**self.valid_data)
        with self.assertRaises(ValidationError):
            aluno.full_clean()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class SeleniumTestCase(TestCase):
    def setUp(self):
        service = Service("chromedriver.exe")  # Path to your chromedriver
        self.driver = webdriver.Chrome(service=service)

    def tearDown(self):
        self.driver.quit()
