from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from alunos.models import Aluno, Pais, Estado, Cidade, Bairro
from django.contrib.auth.models import User
from datetime import date


class AlunoUITest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()
        try:
            User.objects.get(username="lcsilv3")
        except User.DoesNotExist:
            User.objects.create_superuser(
                username="lcsilv3", password="iG356900", email="lcsilv3@example.com"
            )
        # Criar dados de localização
        pais, _ = Pais.objects.get_or_create(
            nome="Brasil", defaults={"nacionalidade": "Brasileira"}
        )
        estado, _ = Estado.objects.get_or_create(
            nome="Bahia", defaults={"codigo": "BA"}
        )
        cidade, _ = Cidade.objects.get_or_create(
            nome="Salvador", defaults={"estado": estado}
        )
        bairro, _ = Bairro.objects.get_or_create(
            nome="Barra", defaults={"cidade": cidade}
        )

        Aluno.objects.get_or_create(
            cpf="12345678901",
            defaults={
                "nome": "Maria Test",
                "data_nascimento": date(2000, 1, 1),
                "email": "maria@test.com",
                "sexo": "F",
                "situacao": "ATIVO",
                "pais_nacionalidade": pais,
                "cidade_naturalidade": cidade,
                "cidade_ref": cidade,
                "bairro_ref": bairro,
            },
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        pass

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
                self.browser.find_element(By.XPATH, "//button[@type='submit']").click()
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
        wait = WebDriverWait(self.browser, 10)  # Espera até 10 segundos
        student_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Maria Test')]"))
        )
        self.assertIn("Maria Test", student_element.text)
