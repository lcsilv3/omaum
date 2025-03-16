from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from alunos.models import Aluno
from datetime import date, time

class AlunoUITest(LiveServerTestCase):
    def setUp(self):
        service = Service('chromedriver.exe')
        self.browser = webdriver.Chrome(service=service)
        
        # Create a test student
        self.aluno = Aluno.objects.create(
            cpf='12345678901',
            nome='Maria Test',
            data_nascimento=date(1995, 5, 15),
            hora_nascimento=time(14, 30),
            email='maria@test.com',
            sexo='F',
            nacionalidade='Brasileira',
            naturalidade='São Paulo',
            rua='Rua Test',
            numero_imovel='123',
            cidade='São Paulo',
            estado='SP',
            bairro='Centro',
            cep='01234567',
            nome_primeiro_contato='João Test',
            celular_primeiro_contato='11999999999',
            tipo_relacionamento_primeiro_contato='Pai',
            nome_segundo_contato='Ana Test',
            celular_segundo_contato='11988888888',
            tipo_relacionamento_segundo_contato='Mãe',
            tipo_sanguineo='A',
            fator_rh='+'
        )

    def tearDown(self):
        self.browser.quit()

    def test_listar_alunos(self):
        # Access the student listing page
        self.browser.get(f'{self.live_server_url}/alunos/')
        
        # Check page title
        self.assertIn('Lista de Alunos', self.browser.title)
        
        # Check header
        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(header.text, 'Lista de Alunos')
        
        # Check if test student is listed
        student_element = self.browser.find_element(By.CLASS_NAME, 'aluno-nome')
        self.assertEqual(student_element.text, 'Maria Test')
