import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException  # type: ignore
from django.urls import reverse  # type: ignore


@pytest.mark.django_db
class TestAlunosE2E:
    """Testes de ponta a ponta para o fluxo de alunos."""

    def test_login_e_listar_alunos(self, browser, live_server_with_data):
        """Testa o login e a listagem de alunos."""
        # Acessar a página de login
        browser.get(f"{live_server_with_data.url}/entrar/")

        # Preencher o formulário de login
        browser.find_element(By.NAME, "username").send_keys("desenv")
        browser.find_element(By.NAME, "password").send_keys("desenv123")
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Verificar se o login foi bem-sucedido
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar-brand"))
        )

        # Acessar a página de listagem de alunos
        browser.get(f"{live_server_with_data.url}{reverse('alunos:listar_alunos')}")

        # Verificar se a página carregou corretamente
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        # Verificar se os alunos estão na página
        assert "João da Silva" in browser.page_source
        assert "Maria Souza" in browser.page_source

    def test_criar_aluno(self, browser, live_server_with_data):
        """Testa a criação de um novo aluno."""
        # Fazer login
        browser.get(f"{live_server_with_data.url}/entrar/")
        browser.find_element(By.NAME, "username").send_keys("desenv")
        browser.find_element(By.NAME, "password").send_keys("desenv123")
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar"))
        )

        # Acessar a página de criação de aluno
        browser.get(f"{live_server_with_data.url}{reverse('alunos:criar_aluno')}")

        # Verificar se a página carregou corretamente
        WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.ID, "id_cpf"))
        )

        # Preencher o formulário
        browser.find_element(By.ID, "id_cpf").send_keys("11122233344")
        browser.find_element(By.ID, "id_nome").send_keys("Carlos Pereira")
        browser.find_element(By.ID, "id_email").send_keys("carlos@exemplo.com")
        data_input = browser.find_element(By.ID, "id_data_nascimento")
        data_input.clear()
        data_input.send_keys("15/03/1988")
        browser.find_element(By.ID, "id_numero_iniciatico").send_keys("N-111222")

        # Selecionar sexo
        browser.find_element(
            By.CSS_SELECTOR, "select#id_sexo option[value='M']"
        ).click()

        # Enviar o formulário (garante botão clicável mesmo com colapsos)
        submit_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "btn-salvar"))
        )
        browser.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        browser.execute_script("arguments[0].click();", submit_btn)

        # Verificar se o aluno foi criado com sucesso
        WebDriverWait(browser, 10).until(
            EC.url_contains("/detalhes/")
        )
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//h1[contains(., 'Aluno')]"
                    "|//h2[contains(., 'Aluno')]"
                    "|//h3[contains(., 'Aluno')]",
                )
            )
        )

        # Verificar se o aluno aparece na listagem
        browser.get(f"{live_server_with_data.url}{reverse('alunos:listar_alunos')}")

        # Verificar se a página carregou corretamente (header robusto)
        header = None
        try:
            header = browser.find_element(By.XPATH, "//h1[contains(text(), 'Aluno')]")
        except NoSuchElementException:
            try:
                header = browser.find_element(
                    By.XPATH, "//*[self::h2 or self::h3][contains(text(), 'Aluno')]"
                )
            except NoSuchElementException:
                body = browser.find_element(By.TAG_NAME, "body").text
                assert "Aluno" in body
        if header:
            assert "Aluno" in header.text

        assert "Carlos Pereira" in browser.page_source
