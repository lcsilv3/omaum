from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from alunos.models import Aluno
from datetime import date


class AlunoUITest(LiveServerTestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        User.objects.create_superuser(
            username="admin", password="admin123", email="admin@example.com"
        )
        Aluno.objects.create(
            cpf="12345678901",
            nome="Maria Test",
            data_nascimento=date(2000, 1, 1),
            email="maria@test.com",
            sexo="F",
            situacao="ATIVO",
        )
        self.browser = webdriver.Chrome()

    def tearDown(self):
        pass

    def test_listar_alunos(self):
        # Realizar login antes de acessar a página de alunos
        self.browser.get(f"{self.live_server_url}/admin/login/")
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("admin123")
        self.browser.find_element(By.XPATH, "//input[@type='submit']").click()

        # Abrir a página de listagem de alunos
        self.browser.get(f"{self.live_server_url}/alunos/")

        # Check page title
        self.assertIn("Lista de Alunos", self.browser.title)

        # Check header
        header = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text, "Lista de Alunos")

        # Check if test student is listed
        student_element = self.browser.find_element(
            By.XPATH, "//span[text()='Maria Test']"
        )
        self.assertEqual(student_element.text, "Maria Test")
