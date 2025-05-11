import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse

@pytest.mark.django_db
class TestAtividadesE2E:
    """Testes de ponta a ponta para o fluxo de atividades."""
    
    def test_criar_atividade_academica(self, browser, live_server_with_data):
        """Testa a criação de uma atividade acadêmica."""
        # Fazer login
        browser.get(f"{live_server_with_data.url}/login/")
        browser.find_element(By.NAME, "username").send_keys("testuser")
        browser.find_element(By.NAME, "password").send_keys("testpassword")
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Acessar a página de criação de atividade acadêmica
        browser.get(f"{live_server_with_data.url}{reverse('atividades:criar_atividade_academica')}")
        
        # Verificar se a página carregou corretamente
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "id_nome"))
        )
        
        # Preencher o formulário
        browser.find_element(By.ID, "id_nome").send_keys("Aula de Matemática")
        browser.find_element(By.ID, "id_descricao").send_keys("Introdução à Álgebra")
        browser.find_element(By.ID, "id_data_inicio").send_keys("2023-12-01")
        browser.find_element(By.ID, "id_responsavel").send_keys("Prof. Oliveira")
        browser.find_element(By.ID, "id_local").send_keys("Sala 103")
        
        # Selecionar tipo de atividade
        Select(browser.find_element(By.ID, "id_tipo_atividade")).select_by_value("aula")
        
        # Selecionar status
        Select(browser.find_element(By.ID, "id_status")).select_by_value("agendada")
        
        # Selecionar turma (primeira opção)
        turmas_select = Select(browser.find_element(By.ID, "id_turmas"))
        turmas_select.select_by_index(0)
        
        # Enviar o formulário
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Verificar se a atividade foi criada com sucesso
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        
        # Verificar se a atividade aparece na listagem
        browser.get(f"{live_server_with_data.url}{reverse('atividades:listar_atividades_academicas')}")
        assert "Aula de Matemática" in browser.page_source
    
    def test_calendario_atividades(self, browser, live_server_with_data):
        """Testa a visualização do calendário de atividades."""
        # Fazer login
        browser.get(f"{live_server_with_data.url}/login/")
        browser.find_element(By.NAME, "username").send_keys("testuser")
        browser.find_element(By.NAME, "password").send_keys("testpassword")
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Acessar a página do calendário de atividades
        browser.get(f"{live_server_with_data.url}{reverse('atividades:calendario_atividades')}")
        
        # Verificar se a página carregou corretamente
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "calendar"))
        )
        
        # Verificar se o calendário foi renderizado
        assert "fc-view-harness" in browser.page_source
        
        # Verificar se há eventos no calendário (pode variar dependendo do mês atual)
        # Aguardar o carregamento dos eventos via AJAX
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-daygrid-day-events"))
        )        # Verificar se o calendário foi renderizado