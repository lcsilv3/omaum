from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from alunos.models import Aluno
from datetime import date


class AlunoUITest(LiveServerTestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        User.objects.create_superuser(
            username="lcsilv3", password="iG356900", email="lcsilv3@example.com"
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
        login_urls = ["/accounts/login/"]
        logged_in = False
        for url in login_urls:
            self.browser.get(f"{self.live_server_url}{url}")
            try:
                self.browser.find_element(By.NAME, "username").send_keys("lcsilv3")
                self.browser.find_element(By.NAME, "password").send_keys("iG356900")
                self.browser.find_element(By.XPATH, "//input[@type='submit']").click()
                logged_in = True
                break
            except Exception:
                # Captura HTML para debug
                with open("saida_login_debug.html", "w", encoding="utf-8") as f:
                    f.write(self.browser.page_source)
        if not logged_in:
            raise AssertionError(
                "Não foi possível encontrar o formulário de login. "
                "Veja saida_login_debug.html para depuração."
            )

        # Abrir a página de listagem de alunos
        self.browser.get(f"{self.live_server_url}/alunos/")

        # Verificação robusta de header
        header = None
        try:
            header = self.browser.find_element(
                By.XPATH, "//h1[contains(text(), 'Aluno')]"
            )
        except Exception:
            try:
                header = self.browser.find_element(
                    By.XPATH, "//*[self::h2 or self::h3][contains(text(), 'Aluno')]"
                )
            except Exception:
                body = self.browser.find_element(By.TAG_NAME, "body").text
                self.assertIn("Aluno", body)
        if header:
            self.assertIn("Aluno", header.text)

        # Check if test student is listed
        student_element = self.browser.find_element(
            By.XPATH, "//*[text()='Maria Test']"
        )
        self.assertEqual(student_element.text, "Maria Test")
