from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class AlunoUITest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def tearDown(self):
        self.browser.quit()

    def test_listar_alunos(self):
        self.browser.get(self.live_server_url + reverse('listar_alunos'))
        self.assertIn('Lista de Alunos', self.browser.title)

    def test_criar_aluno(self):
        self.browser.get(self.live_server_url + reverse('criar_aluno'))
        self.assertIn('Criar Aluno', self.browser.title)
        
        # Fill form and submit
        self.browser.find_element(By.NAME, 'nome').send_keys('João Test')
        self.browser.find_element(By.NAME, 'cpf').send_keys('98765432100')
        # Add other form fields...
        
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # Verify success        self.assertIn('Aluno criado com sucesso', self.browser.page_source)        self.assertIn('Lista de Alunos', self.browser.title)