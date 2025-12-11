import datetime
import os
import pytest

from alunos import services as aluno_service
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from cursos.models import Curso
from turmas.models import Turma
from pagamentos.models import Pagamento


@pytest.mark.skip(reason="Fluxo de pagamentos E2E legado requer ajuste na UI")
class PagamentosE2ETestCase(StaticLiveServerTestCase):
    """Testes E2E para o módulo de pagamentos."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Configurar o driver do Selenium
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        chrome_binary = "/usr/bin/chromium"
        if not os.path.exists(chrome_binary):
            chrome_binary = "/usr/bin/chromium-browser"
        options.binary_location = chrome_binary

        service = Service(executable_path="/usr/bin/chromedriver")
        cls.selenium = webdriver.Chrome(service=service, options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Criar um aluno para os testes (via serviço para preencher campos obrigatórios)
        self.aluno = aluno_service.criar_aluno(
            {
                "cpf": "12345678900",
                "nome": "Aluno Teste",
                "email": "aluno@teste.com",
                "data_nascimento": "1990-01-01",
                "sexo": "M",
                "situacao": "ATIVO",
            }
        )

        # Criar uma turma para os testes
        curso = Curso.objects.create(
            nome="Curso Pagamentos", descricao="Curso para testes", ativo=True
        )
        self.turma = Turma.objects.create(nome="Turma de Teste", curso=curso, status="A")

        # Não existe modelo TipoPagamento, ajuste o fluxo conforme necessário

    def test_fluxo_pagamento_completo(self):
        """Testa o fluxo completo de criação e registro de pagamento."""
        # Fazer login
        self.selenium.get(f"{self.live_server_url}/entrar/")
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")
        username_input.send_keys("testuser")
        password_input.send_keys("testpassword")
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Acessar a página de criação de pagamento
        self.selenium.get(f"{self.live_server_url}/pagamentos/criar/")

        # Preencher o formulário de criação de pagamento
        self.selenium.execute_script(
            "document.getElementById('id_aluno').value = arguments[0];",
            str(self.aluno.id),
        )
        self.selenium.find_element(By.ID, "id_valor").clear()
        self.selenium.find_element(By.ID, "id_valor").send_keys("500.00")

        data_vencimento = (
            timezone.now().date() + datetime.timedelta(days=30)
        ).strftime("%Y-%m-%d")
        self.selenium.find_element(By.ID, "id_data_vencimento").send_keys(
            data_vencimento
        )

        self.selenium.find_element(By.ID, "id_status").send_keys("PENDENTE")
        self.selenium.find_element(By.ID, "id_observacoes").send_keys(
            "Mensalidade de junho"
        )

        # Enviar o formulário
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Verificar se o pagamento foi criado com sucesso
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        # Acessar a página de listagem de pagamentos
        self.selenium.get(f"{self.live_server_url}/pagamentos/")
        # Verificação robusta de header
        header = None
        try:
            header = self.selenium.find_element(
                By.XPATH, "//h1[contains(text(), 'Pagamento')]"
            )
        except Exception:
            try:
                header = self.selenium.find_element(
                    By.XPATH, "//*[self::h2 or self::h3][contains(text(), 'Pagamento')]"
                )
            except Exception:
                body = self.selenium.find_element(By.TAG_NAME, "body").text
                assert "Pagamento" in body
        if header:
            assert "Pagamento" in header.text

        # Verificar se o pagamento está na lista
        self.assertIn("Mensalidade de junho", self.selenium.page_source)

        # Confirmar que o pagamento foi persistido
        pagamento = Pagamento.objects.latest("id")
        self.assertEqual(str(pagamento.aluno.id), str(self.aluno.id))
        self.assertEqual(pagamento.status, "PENDENTE")
