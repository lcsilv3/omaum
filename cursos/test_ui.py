from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


class CursoUITest(StaticLiveServerTestCase):
    """Testes de UI automatizados para o app cursos usando Selenium."""

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
        """Fluxo completo: login, criar, visualizar, editar e excluir curso."""
        # 1. Acessar a página de login
        self.driver.get(f"{self.live_server_url}/admin/login/")
        # 2. Login
        usuario = self.driver.find_element(By.NAME, "username")
        senha = self.driver.find_element(By.NAME, "password")
        usuario.send_keys("lcsilv3")
        senha.send_keys("iG356900")
        senha.send_keys(Keys.RETURN)
        time.sleep(1)
        # 3. Ir para a página de cursos
        self.driver.get(f"{self.live_server_url}/cursos/")
        time.sleep(1)
        # Verificação robusta de header
        header = None
        try:
            header = self.driver.find_element(
                By.XPATH, "//h1[contains(text(), 'Curso')]"
            )
        except Exception:
            try:
                header = self.driver.find_element(
                    By.XPATH, "//*[self::h2 or self::h3][contains(text(), 'Curso')]"
                )
            except Exception:
                body = self.driver.find_element(By.TAG_NAME, "body").text
                assert "Curso" in body
        if header:
            assert "Curso" in header.text
        # 4. Clicar em "Criar Curso" (ajustar seletor conforme template)
        if self.driver.find_elements(By.LINK_TEXT, "Criar Curso"):
            self.driver.find_element(By.LINK_TEXT, "Criar Curso").click()
        else:
            self.driver.get(f"{self.live_server_url}/cursos/criar/")
        time.sleep(1)
        # 5. Preencher formulário de criação
        self.driver.find_element(By.NAME, "nome").send_keys("Curso Selenium")
        self.driver.find_element(By.NAME, "descricao").send_keys(
            "Curso criado via Selenium"
        )
        self.driver.find_element(
            By.XPATH,
            '//form//button[@type="submit" or @type="button" and (text()="Salvar" or text()="Criar")]',
        ).click()
        time.sleep(1)
        # 6. Verificar se curso aparece na listagem
        self.driver.get(f"{self.live_server_url}/cursos/")
        body = self.driver.find_element(By.TAG_NAME, "body").text
        assert "Curso Selenium" in body
        # 7. Acessar detalhes do curso
        self.driver.find_element(By.LINK_TEXT, "Curso Selenium").click()
        time.sleep(1)
        assert "Curso Selenium" in self.driver.page_source
        # 8. Editar curso
        if self.driver.find_elements(By.LINK_TEXT, "Editar"):
            self.driver.find_element(By.LINK_TEXT, "Editar").click()
        else:
            self.driver.get(self.driver.current_url + "editar/")
        time.sleep(1)
        campo_nome = self.driver.find_element(By.NAME, "nome")
        campo_nome.clear()
        campo_nome.send_keys("Curso Selenium Editado")
        self.driver.find_element(
            By.XPATH,
            '//form//button[@type="submit" or @type="button" and (text()="Salvar" or text()="Atualizar")]',
        ).click()
        time.sleep(1)
        # 9. Excluir curso
        if self.driver.find_elements(By.LINK_TEXT, "Excluir"):
            self.driver.find_element(By.LINK_TEXT, "Excluir").click()
        else:
            self.driver.get(self.driver.current_url.replace("editar/", "excluir/"))
        time.sleep(1)
        # Confirmar exclusão se houver botão
        botoes = self.driver.find_elements(By.XPATH, "//form//button")
        if botoes:
            botoes[0].click()
        time.sleep(1)
        # 10. Verificar se curso não está mais na listagem
        self.driver.get(f"{self.live_server_url}/cursos/")
        body = self.driver.find_element(By.TAG_NAME, "body").text
        assert "Curso Selenium Editado" not in body
