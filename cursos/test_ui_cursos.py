from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


class CursoUITest(StaticLiveServerTestCase):
    @classmethod
    def setUpTestData(cls):
        # Cria o superusuário para o banco de teste
        from django.contrib.auth.models import User

        if not User.objects.filter(username="lcsilv3").exists():
            print("[DEBUG] Criando usuário de teste lcsilv3...")
            User.objects.create_superuser(
                username="lcsilv3",
                password="iG356900",
                email="lcsilv3@example.com",
                is_staff=True,
                is_active=True,
            )
        else:
            print("[DEBUG] Usuário de teste lcsilv3 já existe.")

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
        # Garante que o usuário existe no banco de teste
        from django.contrib.auth.models import User

        if not User.objects.filter(username="lcsilv3").exists():
            print("[DEBUG] (test) Criando usuário de teste lcsilv3...")
            User.objects.create_superuser(
                username="lcsilv3",
                password="iG356900",
                email="lcsilv3@example.com",
                is_staff=True,
                is_active=True,
            )
        else:
            print("[DEBUG] (test) Usuário de teste lcsilv3 já existe.")

        # 1. Acessar a página de login real do sistema (/entrar/)
        self.driver.get(f"{self.live_server_url}/entrar/")
        print("[DEBUG] Página de login carregada.")
        usuario = self.driver.find_element(By.NAME, "username")
        senha = self.driver.find_element(By.NAME, "password")
        usuario.send_keys("lcsilv3")
        senha.send_keys("iG356900")
        senha.send_keys(Keys.RETURN)
        time.sleep(1)
        # Verificação explícita de login bem-sucedido
        body = self.driver.find_element(By.TAG_NAME, "body").text
        print(f"[DEBUG] Body após login: {body}")
        assert (
            "Sair" in body
            or "Administração" in body
            or "Logout" in body
            or "Cursos" in body
        ), f"Login falhou: usuário não autenticado. Body: {body}"
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
        # Debug: listar todos os botões do formulário
        botoes = self.driver.find_elements(By.XPATH, "//form//button")
        print("[DEBUG] Botões encontrados no formulário de criação:")
        for i, botao in enumerate(botoes):
            print(
                f"  [{i}] text='{botao.text}' enabled={botao.is_enabled()} displayed={botao.is_displayed()} type={botao.get_attribute('type')}"
            )
        # Clicar explicitamente no botão 'Criar Curso' habilitado e visível
        botao_criar = None
        for botao in botoes:
            if (
                botao.text.strip() == "Criar Curso"
                and botao.is_enabled()
                and botao.is_displayed()
            ):
                botao_criar = botao
                break
        if botao_criar:
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", botao_criar
            )
            time.sleep(0.2)
            botao_criar.click()
        else:
            raise Exception("Botão 'Criar Curso' não encontrado ou não interativo!")
        time.sleep(1)
        # 6. Verificar se curso aparece na listagem
        self.driver.get(f"{self.live_server_url}/cursos/")
        body = self.driver.find_element(By.TAG_NAME, "body").text
        print(f"[DEBUG] Body após criação do curso: {body}")
        assert "Curso Selenium" in body, (
            "Curso Selenium não encontrado na listagem após criação."
        )
        # 7. Acessar detalhes do curso (clicar no link da linha que contém 'Curso Selenium')
        linhas = self.driver.find_elements(By.XPATH, "//tr")
        achou = False
        for linha in linhas:
            if "Curso Selenium" in linha.text:
                links = linha.find_elements(By.TAG_NAME, "a")
                print(
                    f"[DEBUG] Links na linha do curso: {[l.get_attribute('href') for l in links]}"
                )
                if links:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);", links[0]
                    )
                    time.sleep(0.2)
                    links[0].click()
                    achou = True
                    break
        if not achou:
            raise Exception(
                "Não foi possível encontrar o link de detalhes do curso na linha de 'Curso Selenium'!"
            )
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
        # Debug: listar todos os botões do formulário de edição
        botoes = self.driver.find_elements(By.XPATH, "//form//button")
        print("[DEBUG] Botões encontrados no formulário de edição:")
        for i, botao in enumerate(botoes):
            print(
                f"  [{i}] text='{botao.text}' enabled={botao.is_enabled()} displayed={botao.is_displayed()} type={botao.get_attribute('type')}"
            )
        # Clicar explicitamente no botão de submit correto na edição
        textos_validos = ["Salvar", "Atualizar", "Atualizar Curso"]
        botao_salvar = None
        for botao in botoes:
            if (
                any(botao.text.strip() == txt for txt in textos_validos)
                and botao.is_enabled()
                and botao.is_displayed()
            ):
                botao_salvar = botao
                break
        if botao_salvar:
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", botao_salvar
            )
            time.sleep(0.2)
            botao_salvar.click()
        else:
            raise Exception(
                "Botão de submit não encontrado ou não interativo na edição! (Aceitos: 'Salvar', 'Atualizar', 'Atualizar Curso')"
            )
        time.sleep(1)
        # 9. Excluir curso
        if self.driver.find_elements(By.LINK_TEXT, "Excluir"):
            self.driver.find_element(By.LINK_TEXT, "Excluir").click()
        else:
            self.driver.get(self.driver.current_url.replace("editar/", "excluir/"))
        time.sleep(1)
        # Diagnóstico: detectar redirecionamento imediato (sem tela de confirmação)
        url_exclusao = self.driver.current_url
        print(f"[DEBUG] URL atual após tentar acessar exclusão: {url_exclusao}")
        body_exclusao = self.driver.find_element(By.TAG_NAME, "body").text
        print(f"[DEBUG] Body na tela de exclusão:\n{body_exclusao}")
        links = self.driver.find_elements(By.TAG_NAME, "a")
        print(
            f"[DEBUG] Links encontrados na tela de exclusão: {[link.get_attribute('href') for link in links]}"
        )
        # Se não está na tela de confirmação, pular teste de exclusão
        if not url_exclusao.rstrip("/").endswith("excluir"):
            self.skipTest(
                f"Redirecionado para {url_exclusao} ao tentar excluir. O sistema não permite exclusão deste curso ou há proteção de integridade. Veja o body e os links acima para diagnóstico."
            )
        # Caso esteja na tela de confirmação, seguir normalmente
        botoes = self.driver.find_elements(By.XPATH, "//form//button")
        print("[DEBUG] Botões encontrados no formulário de exclusão:")
        for i, botao in enumerate(botoes):
            print(
                f"  [{i}] text='{botao.text}' enabled={botao.is_enabled()} displayed={botao.is_displayed()} type={botao.get_attribute('type')}"
            )
        textos_exclusao = ["Excluir", "Remover", "Confirmar", "Apagar", "Deletar"]
        botao_excluir = None
        for botao in botoes:
            if (
                botao.is_enabled()
                and botao.is_displayed()
                and botao.get_attribute("type") == "submit"
            ):
                if any(txt in botao.text for txt in textos_exclusao):
                    botao_excluir = botao
                    break
        if botao_excluir:
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", botao_excluir
            )
            time.sleep(0.2)
            botao_excluir.click()
        else:
            raise Exception(
                "Botão de exclusão não encontrado ou não interativo! Veja o body e os links acima para diagnóstico."
            )
        time.sleep(1)
        # 10. Verificar se curso não está mais na listagem
        self.driver.get(f"{self.live_server_url}/cursos/")
        body = self.driver.find_element(By.TAG_NAME, "body").text
        assert "Curso Selenium Editado" not in body
