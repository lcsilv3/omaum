from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from alunos.models import Aluno
from datetime import date

class AlunoUITest(LiveServerTestCase):
    def setUp(self):
        """Configura o ambiente de teste, criando um superusuário e um aluno."""
        self.browser = webdriver.Chrome()
        self.admin_user = User.objects.create_superuser(
            username="testadmin", password="password123", email="admin@test.com"
        )
        self.aluno = Aluno.objects.create(
            cpf="11122233344",
            nome="Maria Test",
            data_nascimento=date(2000, 1, 1),
            email="maria@test.com",
            sexo="F",
            situacao="ATIVO",
        )

    def tearDown(self):
        """Finaliza o teste fechando o navegador."""
        self.browser.quit()

    def _login(self):
        """Realiza o login no sistema."""
        self.browser.get(f"{self.live_server_url}/accounts/login/")
        try:
            self.browser.find_element(By.NAME, "username").send_keys("testadmin")
            self.browser.find_element(By.NAME, "password").send_keys("password123")
            self.browser.find_element(By.XPATH, "//button[@type='submit']").click()
        except Exception as e:
            # Salva o HTML da página para depuração em caso de falha no login
            with open("saida_login_debug.html", "w", encoding="utf-8") as f:
                f.write(self.browser.page_source)
            # Levanta uma exceção clara informando sobre a falha
            raise AssertionError(
                f"Não foi possível realizar o login. Erro: {e}. "
                "Veja saida_login_debug.html para depuração."
            )

    def test_listar_alunos(self):
        """
        Testa o fluxo completo de login e verificação da listagem de alunos.
        """
        self._login()

        # Acessa a página de listagem de alunos
        self.browser.get(f"{self.live_server_url}/alunos/")

        # Verifica se o título da página está correto
        self.assertIn("Alunos", self.browser.title)

        # Verifica se o nome do aluno de teste está presente na página
        try:
            student_element = self.browser.find_element(By.XPATH, f"//*[contains(text(), '{self.aluno.nome}')]")
            self.assertEqual(student_element.text, self.aluno.nome)
        except Exception as e:
            # Salva o HTML da página para depuração se o aluno não for encontrado
            with open("saida_lista_alunos_debug.html", "w", encoding="utf-8") as f:
                f.write(self.browser.page_source)
            raise AssertionError(
                f"Não foi possível encontrar o aluno '{self.aluno.nome}' na lista. Erro: {e}. "
                "Veja saida_lista_alunos_debug.html para depuração."
            )
