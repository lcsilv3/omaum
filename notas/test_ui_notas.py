from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


class NotasUITest(StaticLiveServerTestCase):
    """Testes de UI automatizados para o app notas usando Selenium."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_fluxo_completo_usuario(self):
        self.driver.get(f"{self.live_server_url}/admin/login/")
        usuario = self.driver.find_element(By.NAME, "username")
        senha = self.driver.find_element(By.NAME, "password")
        usuario.send_keys("lcsilv3")
        senha.send_keys("iG356900")
        senha.send_keys(Keys.RETURN)
        time.sleep(1)
        # Verificação explícita de login bem-sucedido
        body = self.driver.find_element(By.TAG_NAME, "body").text
        assert (
            "Sair" in body or "Administração" in body or "Logout" in body
        ), "Login falhou: usuário não autenticado."
        self.driver.get(f"{self.live_server_url}/notas/")
        time.sleep(1)
        # Verificação robusta de header
        header = None
        try:
            header = self.driver.find_element(
                By.XPATH, "//h1[contains(text(), 'Nota')]"
            )
        except Exception:
            try:
                header = self.driver.find_element(
                    By.XPATH, "//*[self::h2 or self::h3][contains(text(), 'Nota')]"
                )
            except Exception:
                body = self.driver.find_element(By.TAG_NAME, "body").text
                assert "Nota" in body
        if header:
            assert "Nota" in header.text
        if self.driver.find_elements(By.LINK_TEXT, "Criar Nota"):
            self.driver.find_element(By.LINK_TEXT, "Criar Nota").click()
        else:
            self.driver.get(f"{self.live_server_url}/notas/criar/")
        time.sleep(1)
        self.driver.find_element(By.NAME, "aluno").send_keys("Aluno Selenium")
        self.driver.find_element(By.NAME, "valor").send_keys("10")
        self.driver.find_element(
            By.XPATH,
            '//form//button[@type="submit" or @type="button" and (text()="Salvar" or text()="Criar")]',
        ).click()
        time.sleep(1)
        self.driver.get(f"{self.live_server_url}/notas/")
        body = self.driver.find_element(By.TAG_NAME, "body").text
        assert "Aluno Selenium" in body
        self.driver.find_element(By.LINK_TEXT, "Aluno Selenium").click()
        time.sleep(1)
        assert "Aluno Selenium" in self.driver.page_source
        if self.driver.find_elements(By.LINK_TEXT, "Editar"):
            self.driver.find_element(By.LINK_TEXT, "Editar").click()
        else:
            self.driver.get(self.driver.current_url + "editar/")
        time.sleep(1)
        campo_valor = self.driver.find_element(By.NAME, "valor")
        campo_valor.clear()
        campo_valor.send_keys("9")
        self.driver.find_element(
            By.XPATH,
            '//form//button[@type="submit" or @type="button" and (text()="Salvar" or text()="Atualizar")]',
        ).click()
        time.sleep(1)
        if self.driver.find_elements(By.LINK_TEXT, "Excluir"):
            self.driver.find_element(By.LINK_TEXT, "Excluir").click()
        else:
            self.driver.get(self.driver.current_url.replace("editar/", "excluir/"))
        time.sleep(1)
        botoes = self.driver.find_elements(By.XPATH, "//form//button")
        if botoes:
            botoes[0].click()
        time.sleep(1)
        self.driver.get(f"{self.live_server_url}/notas/")
        body = self.driver.find_element(By.TAG_NAME, "body").text
        assert "Aluno Selenium" not in body
