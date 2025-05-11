from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from alunos.models import Aluno
from turmas.models import Turma
from pagamentos.models import Pagamento, TipoPagamento
import datetime
import time

class PagamentosE2ETestCase(StaticLiveServerTestCase):
    """Testes E2E para o módulo de pagamentos."""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Configurar o driver do Selenium
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.selenium = webdriver.Chrome(options=options)
        cls.selenium.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def setUp(self):
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Criar um aluno para os testes
        self.aluno = Aluno.objects.create(
            cpf="12345678900",
            nome="Aluno Teste",
            email="aluno@teste.com",
            data_nascimento="1990-01-01"
        )
        
        # Criar uma turma para os testes
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A"
        )
        
        # Criar tipo de pagamento para os testes
        self.tipo_pagamento = TipoPagamento.objects.create(
            nome="Mensalidade",
            descricao="Pagamento mensal do curso",
            valor_padrao=500.00
        )
    
    def test_fluxo_pagamento_completo(self):
        """Testa o fluxo completo de criação e registro de pagamento."""
        # Fazer login
        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        username_input.send_keys('testuser')
        password_input.send_keys('testpassword')
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # Acessar a página de criação de pagamento
        self.selenium.get(f'{self.live_server_url}/pagamentos/criar/')
        
        # Preencher o formulário de criação de pagamento
        Select(self.selenium.find_element(By.ID, 'id_aluno')).select_by_value(self.aluno.cpf)
        Select(self.selenium.find_element(By.ID, 'id_turma')).select_by_value(str(self.turma.id))
        Select(self.selenium.find_element(By.ID, 'id_tipo_pagamento')).select_by_value(str(self.tipo_pagamento.id))
        self.selenium.find_element(By.ID, 'id_valor').clear()
        self.selenium.find_element(By.ID, 'id_valor').send_keys('500.00')
        
        data_vencimento = (timezone.now().date() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        self.selenium.find_element(By.ID, 'id_data_vencimento').send_keys(data_vencimento)
        
        Select(self.selenium.find_element(By.ID, 'id_status')).select_by_value('pendente')
        self.selenium.find_element(By.ID, 'id_observacao').send_keys('Mensalidade de junho')
        
        # Enviar o formulário
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # Verificar se o pagamento foi criado com sucesso
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        
        # Acessar a página de listagem de pagamentos
        self.selenium.get(f'{self.live_server_url}/pagamentos/')
        
        # Verificar se o pagamento está na lista
        self.assertIn('Mensalidade de junho', self.selenium.page_source)
        
        # Clicar no botão de registrar pagamento
        self.selenium.find_element(By.LINK_TEXT, 'Registrar Pagamento').click()
        
        # Preencher o formulário de registro de pagamento
        data_pagamento = timezone.now().date().strftime('%Y-%m-%d')
        self.selenium.find_element(By.ID, 'id_data_pagamento').send_keys(data_pagamento)
        
        Select(self.selenium.find_element(By.ID, 'id_forma_pagamento')).select_by_value('pix')
        self.selenium.find_element(By.ID, 'id_observacao').send_keys('Pagamento via PIX')
        
        # Enviar o formulário
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # Verificar se o pagamento foi registrado com sucesso
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        
        # Verificar se o pagamento foi atualizado no banco de dados
        pagamento = Pagamento.objects.get(observacao='Pagamento via PIX')
        self.assertEqual(pagamento.status, 'pago')
        self.assertEqual(pagamento.forma_pagamento, 'pix')