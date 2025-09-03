import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse


@pytest.mark.django_db
class TestAlunosE2E:
    """Testes de ponta a ponta para o fluxo de alunos."""

    def test_login_e_listar_alunos(self, browser, live_server_with_data):
        """Testa o login e a listagem de alunos."""
        # Acessar a página de login
        browser.get(f"{live_server_with_data.url}/login/")

        # Preencher o formulário de login
        browser.find_element(By.NAME, "username").send_keys("testuser")
        browser.find_element(By.NAME, "password").send_keys("testpassword")
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
        browser.get(f"{live_server_with_data.url}/login/")
        browser.find_element(By.NAME, "username").send_keys("testuser")
        browser.find_element(By.NAME, "password").send_keys("testpassword")
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Acessar a página de criação de aluno
        browser.get(f"{live_server_with_data.url}{reverse('alunos:criar_aluno')}")

        # Verificar se a página carregou corretamente
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "id_cpf"))
        )

        # Preencher o formulário
        browser.find_element(By.ID, "id_cpf").send_keys("11122233344")
        browser.find_element(By.ID, "id_nome").send_keys("Carlos Pereira")
        browser.find_element(By.ID, "id_email").send_keys("carlos@exemplo.com")
        browser.find_element(By.ID, "id_data_nascimento").send_keys("1988-03-15")

        # Selecionar sexo
        browser.find_element(
            By.CSS_SELECTOR, "select#id_sexo option[value='M']"
        ).click()

        # Enviar o formulário
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Verificar se o aluno foi criado com sucesso
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )

        # Verificar se o aluno aparece na listagem
        browser.get(f"{live_server_with_data.url}{reverse('alunos:listar_alunos')}")

        # Verificar se a página carregou corretamente (header robusto)
        header = None
        try:
            header = browser.find_element(By.XPATH, "//h1[contains(text(), 'Aluno')]")
        except Exception:
            try:
                header = browser.find_element(
                    By.XPATH, "//*[self::h2 or self::h3][contains(text(), 'Aluno')]"
                )
            except Exception:
                body = browser.find_element(By.TAG_NAME, "body").text
                assert "Aluno" in body
        if header:
            assert "Aluno" in header.text

        assert "Carlos Pereira" in browser.page_source
