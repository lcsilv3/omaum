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
from notas.models import Nota
from matriculas.models import Matricula


class NotasE2ETestCase(StaticLiveServerTestCase):
    """Testes E2E para o módulo de notas."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Configurar o driver do Selenium
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.selenium = webdriver.Chrome(options=options)
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

        # Criar uma turma para os testes
        self.turma = Turma.objects.create(
            nome="Turma de Teste",
            codigo="TT-001",
            data_inicio=timezone.now().date(),
            status="A",
        )

        # Criar uma atividade para os testes
        self.atividade = Atividade.objects.create(
            nome="Atividade de Teste",
            descricao="Descrição da atividade",
            data_inicio=timezone.now(),
            responsavel="Professor Teste",
            tipo_atividade="aula",
            status="agendada",
        )
        self.atividade.turmas.add(self.turma)

        # Criar alunos para os testes
        self.aluno1 = Aluno.objects.create(
            cpf="12345678900",
            nome="Aluno Teste 1",
            email="aluno1@teste.com",
            data_nascimento="1990-01-01",
        )

        self.aluno2 = Aluno.objects.create(
            cpf="98765432100",
            nome="Aluno Teste 2",
            email="aluno2@teste.com",
            data_nascimento="1992-05-15",
        )

        # Matricular alunos na turma
        Matricula.objects.create(
            aluno=self.aluno1,
            turma=self.turma,
            data_matricula=timezone.now().date(),
            status="A",
        )

        Matricula.objects.create(
            aluno=self.aluno2,
            turma=self.turma,
            data_matricula=timezone.now().date(),
            status="A",
        )

    def test_fluxo_lancamento_notas(self):
        """Testa o fluxo completo de lançamento de notas."""
        # Fazer login
        self.selenium.get(f"{self.live_server_url}/accounts/login/")
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")
        username_input.send_keys("testuser")
        password_input.send_keys("testpassword")
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Acessar a página de criação de avaliação
        self.selenium.get(f"{self.live_server_url}/notas/avaliacoes/criar/")

        # Preencher o formulário de criação de avaliação
        self.selenium.find_element(By.ID, "id_nome").send_keys("Prova Final")
        self.selenium.find_element(By.ID, "id_descricao").send_keys(
            "Avaliação final do curso"
        )
        self.selenium.find_element(By.ID, "id_data").send_keys(
            timezone.now().date().strftime("%Y-%m-%d")
        )
        self.selenium.find_element(By.ID, "id_peso").send_keys("2.0")
        self.selenium.find_element(By.ID, "id_turma").send_keys(self.turma.id)
        self.selenium.find_element(By.ID, "id_atividade").send_keys(self.atividade.id)

        # Enviar o formulário
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Verificar se a avaliação foi criada com sucesso
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        # Acessar a página de listagem de avaliações
        self.selenium.get(f"{self.live_server_url}/notas/avaliacoes/")

        # Verificar se a avaliação está na lista
        self.assertIn("Prova Final", self.selenium.page_source)

        # Clicar no botão de lançar notas
        self.selenium.find_element(By.LINK_TEXT, "Lançar Notas").click()

        # Preencher as notas dos alunos
        self.selenium.find_element(By.NAME, "form-0-valor").send_keys("8.5")
        self.selenium.find_element(By.NAME, "form-0-observacao").send_keys(
            "Bom desempenho"
        )
        self.selenium.find_element(By.NAME, "form-1-valor").send_keys("7.0")
        self.selenium.find_element(By.NAME, "form-1-observacao").send_keys(
            "Desempenho regular"
        )

        # Enviar o formulário
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Verificar se as notas foram lançadas com sucesso
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        # Verificar se as notas foram salvas no banco de dados
        avaliacao = Avaliacao.objects.get(nome="Prova Final")
        nota1 = Nota.objects.get(avaliacao=avaliacao, aluno=self.aluno1)
        nota2 = Nota.objects.get(avaliacao=avaliacao, aluno=self.aluno2)

        self.assertEqual(nota1.valor, 8.5)
        self.assertEqual(nota1.observacao, "Bom desempenho")
        self.assertEqual(nota2.valor, 7.0)
        self.assertEqual(nota2.observacao, "Desempenho regular")
