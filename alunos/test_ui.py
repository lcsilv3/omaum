from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from alunos.models import Aluno, Pais, Estado, Cidade, Bairro
from datetime import date

class AlunoUITest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()
        try:
            cls.admin_user = User.objects.get(username="testadmin")
        except User.DoesNotExist:
            cls.admin_user = User.objects.create_superuser(
                username="testadmin", password="password123", email="admin@test.com"
            )
        # Criar dados de localização
        pais, _ = Pais.objects.get_or_create(
            nome="Brasil", defaults={"nacionalidade": "Brasileira"}
        )
        estado, _ = Estado.objects.get_or_create(
            nome="Rio de Janeiro", defaults={"codigo": "RJ"}
        )
        cidade, _ = Cidade.objects.get_or_create(
            nome="Rio de Janeiro", defaults={"estado": estado}
        )
        bairro, _ = Bairro.objects.get_or_create(
            nome="Copacabana", defaults={"cidade": cidade}
        )

        cls.aluno, _ = Aluno.objects.get_or_create(
            cpf="11122233344",
            defaults={
                "nome": "Maria Test",
                "data_nascimento": date(2000, 1, 1),
                "email": "maria@test.com",
                "sexo": "F",
                "situacao": "ATIVO",
                "pais_nacionalidade": pais,
                "cidade_naturalidade": cidade,
                "cidade_ref": cidade,
                "bairro_ref": bairro,
            },
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        """Configura o ambiente de teste, criando um superusuário e um aluno."""
        # O setup do navegador e dos dados agora é feito no setUpClass
        pass

    def tearDown(self):
        """Finaliza o teste fechando o navegador."""
        # O tearDown do navegador agora é feito no tearDownClass
        pass

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
