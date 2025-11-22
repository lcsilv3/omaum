from __future__ import annotations

import os
import time

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.selenium_driver import get_chrome_service


class FrequenciasUITest(StaticLiveServerTestCase):
    """Testes de UI automatizados para o app frequencias usando Selenium."""

    SUPERUSER = os.getenv("SELENIUM_SUPERUSER", "selenium_admin")
    SUPERPASS = os.getenv("SELENIUM_SUPERUSER_PASSWORD", "Teste@123")

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls._ensure_superuser()

    @classmethod
    def _ensure_superuser(cls):
        """Garante a existência do usuário usado pelo Selenium."""

        User = get_user_model()
        usuario, _ = User.objects.get_or_create(
            username=cls.SUPERUSER,
            defaults={
                "email": "selenium@example.com",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.is_active = True
        usuario.email = usuario.email or "selenium@example.com"
        usuario.set_password(cls.SUPERPASS)
        usuario.save()
        return usuario

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(
            service=get_chrome_service(), options=chrome_options
        )
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def _login_and_go_to_frequencias(self) -> None:
        """Autentica via Django test client e reutiliza a sessão no navegador."""

        client = Client()
        usuario = self._ensure_superuser()

        client.force_login(usuario)
        session_cookie = client.cookies.get("sessionid")
        assert session_cookie, "Sessão não foi gerada para o usuário autenticado."

        # O navegador precisa conhecer o domínio antes de receber o cookie.
        # Necessário visitar o host para que Selenium permita inserir cookies.
        self.driver.get(self.live_server_url)
        self.driver.add_cookie(
            {
                "name": "sessionid",
                "value": session_cookie.value,
                "path": "/",
                "domain": "localhost",
                "httponly": True,
            }
        )
        self.driver.get(f"{self.live_server_url}/frequencias/")

        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        assert (
            "Entrar no Sistema" not in body_text
        ), "Login falhou: usuário não autenticado."

    def _assert_frequencia_header(self) -> None:
        """Confirma se algum título ou corpo contém 'Frequência'."""

        wait = WebDriverWait(self.driver, 15)
        try:
            header = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h1[contains(text(), 'Frequência')]")
                )
            )
            assert "Frequência" in header.text
            return
        except Exception:
            try:
                header = self.driver.find_element(
                    By.XPATH,
                    "//*[self::h2 or self::h3][contains(text(), 'Frequência')]",
                )
                assert "Frequência" in header.text
                return
            except Exception:
                body = self.driver.find_element(By.TAG_NAME, "body").text
                assert "Frequência" in body

    def test_fluxo_completo_usuario(self):
        self._login_and_go_to_frequencias()
        self._assert_frequencia_header()
        wait = WebDriverWait(self.driver, 15)

        if self.driver.find_elements(By.LINK_TEXT, "Criar Frequência"):
            self.driver.find_element(By.LINK_TEXT, "Criar Frequência").click()
        else:
            self.driver.get(f"{self.live_server_url}/frequencias/criar/")

        campo_nome = wait.until(EC.presence_of_element_located((By.NAME, "nome")))
        campo_nome.send_keys("Frequência Selenium")
        self.driver.find_element(By.NAME, "descricao").send_keys(
            "Frequência criada via Selenium"
        )
        self.driver.find_element(
            By.XPATH,
            '//form//button[@type="submit" or @type="button" and (text()="Salvar" or text()="Criar")]',
        ).click()

        self.driver.get(f"{self.live_server_url}/frequencias/")
        body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text
        assert "Frequência Selenium" in body
        self.driver.find_element(By.LINK_TEXT, "Frequência Selenium").click()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "Frequência Selenium" in self.driver.page_source

        if self.driver.find_elements(By.LINK_TEXT, "Editar"):
            self.driver.find_element(By.LINK_TEXT, "Editar").click()
        else:
            self.driver.get(self.driver.current_url + "editar/")

        campo_nome = wait.until(EC.element_to_be_clickable((By.NAME, "nome")))
        campo_nome.clear()
        campo_nome.send_keys("Frequência Selenium Editada")
        self.driver.find_element(
            By.XPATH,
            '//form//button[@type="submit" or @type="button" and (text()="Salvar" or text()="Atualizar")]',
        ).click()

        if self.driver.find_elements(By.LINK_TEXT, "Excluir"):
            self.driver.find_element(By.LINK_TEXT, "Excluir").click()
        else:
            self.driver.get(self.driver.current_url.replace("editar/", "excluir/"))

        botoes = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//form//button"))
        )
        botoes[0].click()
        self.driver.get(f"{self.live_server_url}/frequencias/")
        body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text
        assert "Frequência Selenium Editada" not in body
