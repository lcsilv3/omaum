import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse

@pytest.mark.django_db
class TestTurmasE2E:
    """Testes de ponta a ponta para o fluxo de turmas."""
    
    def test_listar_e_detalhar_turma(self, browser, live_server_with_data):
        """Testa a listagem e visualização de detalhes de uma turma."""
        # Fazer login
        browser.get(f"{live_server_with_data.url}/login/")
        browser.find_element(By.NAME, "username").send_keys("testuser")
        browser.find_element(By.NAME, "password").send_keys("testpassword")
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Acessar a página de listagem de turmas
        browser.get(f"{live_server_with_data.url}{reverse('turmas:listar_turmas')}")
        
        # Verificar se a página carregou corretamente
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        
        # Verificar se as turmas estão na página
        assert "Turma de Filosofia 2023" in browser.page_source
        assert "Turma de História 2023" in browser.page_source
        
        # Clicar no botão de detalhes da primeira turma
        browser.find_element(By.LINK_TEXT, "Detalhes").click()
        
        # Verificar se a página de detalhes carregou corretamente
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card-header"))
        )
        
        # Verificar se os detalhes da turma estão na página
        assert "Informações da Turma" in browser.page_source
    
    def test_criar_turma(self, browser, live_server_with_data):
        """Testa a criação de uma nova turma."""
        # Fazer login
        browser.get(f"{live_server_with_data.url}/login/")
        browser.find_element(By.NAME, "username").send_keys("testuser")
        browser.find_element(By.NAME, "password").send_keys("testpassword")
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Acessar a página de criação de turma
        browser.get(f"{live_server_with_data.url}{reverse('turmas:criar_turma')}")
        
        # Verificar se a página carregou corretamente
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "id_nome"))
        )
        
        # Preencher o formulário
        browser.find_element(By.ID, "id_nome").send_keys("Turma de Geografia 2023")
        browser.find_element(By.ID, "id_codigo").send_keys("GEO-2023")
        browser.find_element(By.ID, "id_data_inicio").send_keys("2023-01-15")
        
        # Selecionar status
        Select(browser.find_element(By.ID, "id_status")).select_by_value("A")
        
        # Enviar o formulário
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Verificar se a turma foi criada com sucesso
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        
        # Verificar se a turma aparece na listagem
        browser.get(f"{live_server_with_data.url}{reverse('turmas:listar_turmas')}")
        assert "Turma de Geografia 2023" in browser.page_source