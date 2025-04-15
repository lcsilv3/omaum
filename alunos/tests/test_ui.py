from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class AlunoUITest(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.add_argument(
            "--headless"
        )  # Run in headless mode for CI environments
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        try:
            self.browser = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options,
            )
        except Exception as e:
            print(f"Could not initialize Chrome driver: {e}")
            self.skipTest("Webdriver not available")

    def tearDown(self):
        if hasattr(self, "browser"):
            self.browser.quit()

    def test_listar_alunos(self):
        self.browser.get(self.live_server_url + reverse("alunos:listar"))
        self.assertIn("Lista de Alunos", self.browser.title)

    def test_criar_aluno(self):
        self.browser.get(self.live_server_url + reverse("alunos:cadastrar"))
        self.assertIn("Cadastrar Novo Aluno", self.browser.page_source)

        # Fill form and submit
        self.browser.find_element(By.NAME, "nome").send_keys("João Test")
        self.browser.find_element(By.NAME, "cpf").send_keys("98765432100")
        # Add other form fields...

        self.browser.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        ).click()

        # Verify success        self.assertIn('Aluno criado com sucesso', self.browser.page_source)        self.assertIn('Lista de Alunos', self.browser.title)
