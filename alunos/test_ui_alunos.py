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

        # Verificação robusta de header
        header = None
        try:
            header = self.browser.find_element(By.XPATH, "//h1[contains(text(), 'Aluno')]")
        except Exception:
            try:
                header = self.browser.find_element(By.XPATH, "//*[self::h2 or self::h3][contains(text(), 'Aluno')]")
            except Exception:
                body = self.browser.find_element(By.TAG_NAME, "body").text
                self.assertIn('Aluno', body)
        if header:
            self.assertIn('Aluno', header.text)

        # Check if test student is listed
        student_element = self.browser.find_element(
            By.XPATH, "//*[text()='Maria Test']"
        )
        self.assertEqual(student_element.text, "Maria Test")
