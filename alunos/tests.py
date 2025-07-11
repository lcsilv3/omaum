from django.test import TestCase
from alunos.models import Aluno
from datetime import date, time
from django.core.exceptions import ValidationError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


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


class SeleniumTestCase(TestCase):
    def setUp(self):
        """Configurar o driver do Selenium com webdriver-manager"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Executar sem interface gráfica
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            # Se falhar, pular os testes Selenium
            self.skipTest(f"Selenium não disponível: {str(e)}")

    def tearDown(self):
        """Fechar o driver do Selenium"""
        if hasattr(self, 'driver'):
            self.driver.quit()
