from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from alunos.models import Aluno
from turmas.models import Turma
from atividades.models import Atividade
from frequencias.models import Frequencia, RegistroFrequencia
from matriculas.models import Matricula
import time

class FrequenciasE2ETestCase(StaticLiveServerTestCase):
    """Testes E2E para o módulo de frequências."""
    
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
        
        # Criar uma turma para os testes
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A"
        )
        
        # Criar uma atividade para os testes
        self.atividade = Atividade.objects.create(
            nome="Atividade de Teste",
            descricao="Descrição da atividade",
            data_inicio=timezone.now(),
            responsavel="Professor Teste",
            tipo_atividade="aula",
            status="agendada"
        )
        self.atividade.turmas.add(self.turma)
        
        # Criar alunos para os testes
        self.aluno1 = Aluno.objects.create(
            cpf="12345678900",
            nome="Aluno Teste 1",
            email="aluno1@teste.com",
            data_nascimento="1990-01-01"
        )
        
        self.aluno2 = Aluno.objects.create(
            cpf="98765432100",
            nome="Aluno Teste 2",
            email="aluno2@teste.com",
            data_nascimento="1992-05-15"
        )
        
        # Matricular alunos na turma
        Matricula.objects.create(
            aluno=self.aluno1,
            turma=self.turma,
            data_matricula=timezone.now().date(),
            status="A"
        )
        
        Matricula.objects.create(
            aluno=self.aluno2,
            turma=self.turma,
            data_matricula=timezone.now().date(),
            status="A"
        )
    
    def test_fluxo_registro_frequencia(self):
        """Testa o fluxo completo de registro de frequência."""
        # Fazer login
        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        username_input.send_keys('testuser')
        password_input.send_keys('testpassword')
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # Acessar a página de criação de frequência
        self.selenium.get(f'{self.live_server_url}/frequencias/criar/')
        
        # Preencher o formulário de criação de frequência
        self.selenium.find_element(By.ID, 'id_atividade').send_keys(self.atividade.id)
        self.selenium.find_element(By.ID, 'id_data').send_keys(timezone.now().date().strftime('%Y-%m-%d'))
        self.selenium.find_element(By.ID, 'id_observacoes').send_keys('Teste de frequência via Selenium')
        
        # Enviar o formulário
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # Verificar se a frequência foi criada com sucesso
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        
        # Acessar a página de listagem de frequências
        self.selenium.get(f'{self.live_server_url}/frequencias/')
        
        # Verificar se a frequência está na lista
        self.assertIn('Teste de frequência via Selenium', self.selenium.page_source)
        
        # Clicar no botão de registrar frequência
        self.selenium.find_element(By.LINK_TEXT, 'Registrar Frequência').click()
        
        # Marcar o aluno 1 como presente
        self.selenium.find_element(By.NAME, 'form-0-presente').click()
        
        # Marcar o aluno 2 como ausente e adicionar justificativa
        self.selenium.find_element(By.NAME, 'form-1-justificativa').send_keys('Atestado médico')
        
        # Enviar o formulário
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # Verificar se a frequência foi registrada com sucesso
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        
        # Verificar se os registros foram salvos no banco de dados
        frequencia = Frequencia.objects.get(observacoes='Teste de frequência via Selenium')
        registro1 = RegistroFrequencia.objects.get(frequencia=frequencia, aluno=self.aluno1)
        registro2 = RegistroFrequencia.objects.get(frequencia=frequencia, aluno=self.aluno2)
        
        self.assertTrue(registro1.presente)
        self.assertEqual(registro1.justificativa, '')
        self.assertFalse(registro2.presente)
        self.assertEqual(registro2.justificativa, 'Atestado médico')