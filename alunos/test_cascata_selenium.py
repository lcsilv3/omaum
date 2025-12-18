"""
Teste Selenium para verificar cascade Estado → Cidade → Bairro
"""
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

User = get_user_model()


class TestCascataEstadoCidade(StaticLiveServerTestCase):
    """Testa o funcionamento do cascade Estado → Cidade → Bairro no formulário de aluno."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Configurar Chrome em modo headless
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        cls.selenium = webdriver.Chrome(options=options)
        cls.selenium.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def setUp(self):
        """Criar usuário e fazer login."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Fazer login
        self.selenium.get(f'{self.live_server_url}/entrar/')
        
        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        
        username_input.send_keys('testuser')
        password_input.send_keys('testpass123')
        
        self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        
        # Aguardar redirecionamento
        WebDriverWait(self.selenium, 10).until(
            EC.url_changes(f'{self.live_server_url}/entrar/')
        )
    
    def test_cascade_estado_cidade(self):
        """Testa se selecionar estado carrega as cidades correspondentes."""
        
        # Acessar página de criar aluno
        self.selenium.get(f'{self.live_server_url}/alunos/criar/')
        
        # Aguardar página carregar
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, 'id_estado_ref'))
        )
        
        # Verificar estado inicial do campo cidade (deve estar desabilitado)
        cidade_select = self.selenium.find_element(By.ID, 'id_cidade_ref')
        print(f"Cidade desabilitada inicialmente: {not cidade_select.is_enabled()}")
        
        # Selecionar estado AL (Alagoas)
        estado_select = Select(self.selenium.find_element(By.ID, 'id_estado_ref'))
        
        # Printar opções disponíveis
        print(f"Estados disponíveis: {len(estado_select.options)}")
        for option in estado_select.options[:5]:  # Primeiras 5 opções
            print(f"  - {option.text}")
        
        # Encontrar e selecionar AL
        al_found = False
        for option in estado_select.options:
            if 'AL' in option.text or 'Alagoas' in option.text:
                estado_select.select_by_visible_text(option.text)
                al_found = True
                print(f"Selecionado estado: {option.text}")
                break
        
        self.assertTrue(al_found, "Estado AL não encontrado nas opções")
        
        # Aguardar requisição AJAX carregar cidades
        time.sleep(2)
        
        # Verificar se campo cidade foi habilitado
        cidade_select = self.selenium.find_element(By.ID, 'id_cidade_ref')
        print(f"Cidade habilitada após selecionar estado: {cidade_select.is_enabled()}")
        
        # Verificar se há cidades carregadas
        cidade_select_obj = Select(cidade_select)
        print(f"Cidades carregadas: {len(cidade_select_obj.options)}")
        
        for option in cidade_select_obj.options[:5]:  # Primeiras 5 cidades
            print(f"  - {option.text}")
        
        # Verificar que há mais de 1 opção (mais que só "Selecione...")
        self.assertGreater(
            len(cidade_select_obj.options), 
            1, 
            "Nenhuma cidade foi carregada após selecionar o estado"
        )
        
        # Selecionar uma cidade
        if len(cidade_select_obj.options) > 1:
            cidade_select_obj.select_by_index(1)  # Seleciona a primeira cidade (não o placeholder)
            print(f"Cidade selecionada: {cidade_select_obj.options[1].text}")
            
            # Aguardar carregar bairros
            time.sleep(2)
            
            # Verificar se bairro foi habilitado
            bairro_select = self.selenium.find_element(By.ID, 'id_bairro_ref')
            print(f"Bairro habilitado após selecionar cidade: {bairro_select.is_enabled()}")
            
            bairro_select_obj = Select(bairro_select)
            print(f"Bairros carregados: {len(bairro_select_obj.options)}")
        
        print("✅ Teste concluído com sucesso!")
