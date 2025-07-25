
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from datetime import date
import json
import time

# Imports condicionais para Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

from alunos.services import criar_aluno
from turmas.models import Turma
from atividades.models import Atividade
from presencas.models import PresencaAcademica


class JavaScriptTestCase(TestCase):
    """Testes de funcionalidades JavaScript sem browser real."""

    def setUp(self):
        self.user = User.objects.create_user(username="js_user", password="test123")

        self.turma = Turma.objects.create(
            codigo_turma="JS001", nome="Turma JavaScript Test"
        )

        self.atividade = Atividade.objects.create(
            nome="Atividade JS", tipo="AULA", ativa=True
        )

        # Criar alguns alunos
        self.alunos = []
        for i in range(5):
            aluno_data = {
                "cpf": f"123456789{i:02d}",
                "nome": f"Aluno JS {i + 1}",
                "data_nascimento": "1990-01-01",
                "hora_nascimento": "14:30",
                "email": f"alunojs{i + 1}@test.com",
                "sexo": "M",
                "nacionalidade": "Brasileira",
                "naturalidade": "São Paulo",
                "rua": f"Rua JS {i + 1}",
                "numero_imovel": str(i + 1),
                "cidade": "São Paulo",
                "estado": "SP",
                "bairro": "Centro",
                "cep": "01234567",
                "nome_primeiro_contato": f"Contato {i + 1}",
                "celular_primeiro_contato": f"11999999{i:03d}",
                "tipo_relacionamento_primeiro_contato": "Mãe",
                "nome_segundo_contato": f"Pai {i + 1}",
                "celular_segundo_contato": f"11888888{i:03d}",
                "tipo_relacionamento_segundo_contato": "Pai",
                "tipo_sanguineo": "A",
                "fator_rh": "+",
            }
            aluno = criar_aluno(aluno_data)
            self.alunos.append(aluno)

        self.client.login(username="js_user", password="test123")

    def test_html_tem_elementos_javascript(self):
        """Testa se HTML contém elementos necessários para JavaScript."""
        url = reverse("presencas:registro_rapido")
        response = self.client.get(url, {"turma": self.turma.id})

        # Verificar elementos essenciais para JavaScript
        self.assertContains(response, "data-aluno-id")
        self.assertContains(response, 'class="presenca-checkbox"')
        self.assertContains(response, 'class="justificativa-field"')

        # Scripts JavaScript devem estar presentes
        self.assertContains(response, "<script")
        self.assertContains(response, "presencas.js")

    def test_api_endpoints_para_ajax(self):
        """Testa se endpoints de API respondem corretamente para AJAX."""
        # API de alunos da turma
        url = reverse("presencas:api_alunos_turma")
        response = self.client.get(
            url, {"turma_id": self.turma.id}, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn("alunos", data)
        self.assertEqual(len(data["alunos"]), 5)

        # Cada aluno deve ter campos necessários para JavaScript
        for aluno_data in data["alunos"]:
            self.assertIn("id", aluno_data)
            self.assertIn("nome", aluno_data)
            self.assertIn("cpf", aluno_data)

    def test_api_salvar_presenca_ajax(self):
        """Testa API de salvamento via AJAX."""
        url = reverse("presencas:api_salvar_presenca")

        data = {
            "aluno_id": self.alunos[0].id,
            "turma_id": self.turma.id,
            "atividade_id": self.atividade.id,
            "data": date.today().strftime("%Y-%m-%d"),
            "presente": True,
        }

        response = self.client.post(
            url,
            json.dumps(data),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result.get("success", False))

        # Verificar se presença foi salva
        presenca = PresencaAcademica.objects.filter(
            aluno=self.alunos[0], turma=self.turma, data=date.today()
        ).first()
        self.assertIsNotNone(presenca)

    def test_estrutura_html_grade_editavel(self):
        """Testa estrutura HTML para grade editável tipo Excel."""
        url = reverse("presencas:grade_presencas")
        response = self.client.get(
            url,
            {
                "turma": self.turma.id,
                "mes": date.today().month,
                "ano": date.today().year,
            },
        )

        self.assertEqual(response.status_code, 200)

        # Verificar estrutura de tabela editável
        self.assertContains(response, 'table class="grade-presencas"')
        self.assertContains(response, 'td class="editable-cell"')
        self.assertContains(response, 'data-field="presente"')
        self.assertContains(response, 'data-field="justificativa"')

        # Atributos para navegação por teclado
        self.assertContains(response, "tabindex=")
        self.assertContains(response, "data-row=")
        self.assertContains(response, "data-col=")


# Testes que requerem Selenium (executados apenas se disponível)
if SELENIUM_AVAILABLE:
    # ... definição de SeleniumTestCase ...

    # ... definição de SeleniumTestCase ...

    # ... definição de SeleniumTestCase ...

    # ... definição de SeleniumTestCase ...

    # Outras classes de teste Selenium...

    class BadgeConvocadoModalTest(SeleniumTestCase):
        """Testa se o badge 'Convocado' aparece no modal para atividade convocada."""
        def setUp(self):
            if not self.driver:
                self.skipTest("Selenium driver não disponível")
            # Cria usuário e faz login
            self.user = User.objects.create_user(username="lcsilv3", password="iG356900")
            self.turma = Turma.objects.create(codigo_turma="SEL002", nome="Turma Badge Test")
            self.atividade = Atividade.objects.create(nome="Atividade Convocada", tipo="AULA", ativa=True, convocada=True)
            self.aluno = criar_aluno({
                "cpf": "99999999999",
                "nome": "Aluno Badge",
                "data_nascimento": "1990-01-01",
                "hora_nascimento": "14:30",
                "email": "badge@test.com",
                "sexo": "M",
                "nacionalidade": "Brasileira",
                "naturalidade": "São Paulo",
                "rua": "Rua Badge",
                "numero_imovel": "1",
                "cidade": "São Paulo",
                "estado": "SP",
                "bairro": "Centro",
                "cep": "01234567",
                "nome_primeiro_contato": "Contato Badge",
                "celular_primeiro_contato": "11999999999",
                "tipo_relacionamento_primeiro_contato": "Mãe",
                "nome_segundo_contato": "Pai Badge",
                "celular_segundo_contato": "11888888888",
                "tipo_relacionamento_segundo_contato": "Pai",
                "tipo_sanguineo": "A",
                "fator_rh": "+",
            })

        def test_badge_convocado_modal(self):
            # Login
            self.driver.get(f"{self.live_server_url}/admin/login/")
            username_input = self.driver.find_element(By.NAME, "username")
            password_input = self.driver.find_element(By.NAME, "password")
            username_input.send_keys("lcsilv3")
            password_input.send_keys("iG356900")
            password_input.send_keys(Keys.RETURN)
            WebDriverWait(self.driver, 10).until(EC.url_changes(f"{self.live_server_url}/admin/login/"))

            # Acessa página de registro de presença
            url = f"{self.live_server_url}" + reverse("presencas:registro_rapido")
            self.driver.get(f"{url}?turma={self.turma.id}")

            # Espera o calendário carregar e seleciona o input da atividade convocada
            input_selector = f"input[data-atividade='{self.atividade.id}']"
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_selector)))
            input_elem = self.driver.find_element(By.CSS_SELECTOR, input_selector)
            input_elem.click()

            # Seleciona o primeiro dia disponível no calendário
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "flatpickr-day")))
            day_elem = self.driver.find_element(By.CLASS_NAME, "flatpickr-day")
            day_elem.click()

            # Clica novamente para abrir o modal
            day_elem.click()

            # Espera o modal abrir e verifica o badge
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "presencaModal")))
            modal_title = self.driver.find_element(By.ID, "modalTitle")
            self.assertIn("Convocado", modal_title.get_attribute("innerHTML"))

    class SeleniumTestCase(StaticLiveServerTestCase):
        """Classe base para testes com Selenium."""

        @classmethod
        def setUpClass(cls):
            super().setUpClass()

            # Configurar Chrome em modo headless
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")

            try:
                cls.driver = webdriver.Chrome(options=chrome_options)
                cls.driver.implicitly_wait(10)
            except Exception as e:
                # Se Chrome não estiver disponível, pular testes
                cls.driver = None
                print(f"Chrome driver não disponível: {e}")

        @classmethod
        def tearDownClass(cls):
            if cls.driver:
                cls.driver.quit()
            super().tearDownClass()

        def setUp(self):
            if not self.driver:
                self.skipTest("Selenium driver não disponível")

            # Setup de dados
            self.user = User.objects.create_user(
                username="selenium_user", password="test123"
            )

            self.turma = Turma.objects.create(
                codigo_turma="SEL001", nome="Turma Selenium Test"
            )

            self.atividade = Atividade.objects.create(
                nome="Atividade Selenium", tipo="AULA", ativa=True
            )

            # Criar alunos
            self.alunos = []
            for i in range(3):
                aluno_data = {
                    "cpf": f"987654321{i:02d}",
                    "nome": f"Aluno Selenium {i + 1}",
                    "data_nascimento": "1990-01-01",
                    "hora_nascimento": "14:30",
                    "email": f"selenium{i + 1}@test.com",
                    "sexo": "M",
                    "nacionalidade": "Brasileira",
                    "naturalidade": "São Paulo",
                    "rua": f"Rua Selenium {i + 1}",
                    "numero_imovel": str(i + 1),
                    "cidade": "São Paulo",
                    "estado": "SP",
                    "bairro": "Centro",
                    "cep": "01234567",
                    "nome_primeiro_contato": f"Contato {i + 1}",
                    "celular_primeiro_contato": f"11777777{i:03d}",
                    "tipo_relacionamento_primeiro_contato": "Mãe",
                    "nome_segundo_contato": f"Pai {i + 1}",
                    "celular_segundo_contato": f"11666666{i:03d}",
                    "tipo_relacionamento_segundo_contato": "Pai",
                    "tipo_sanguineo": "A",
                    "fator_rh": "+",
                }
                aluno = criar_aluno(aluno_data)
                self.alunos.append(aluno)

        def login_selenium(self):
            """Realiza login via Selenium."""
            self.driver.get(f"{self.live_server_url}/admin/login/")

            username_input = self.driver.find_element(By.NAME, "username")
            password_input = self.driver.find_element(By.NAME, "password")

            username_input.send_keys("selenium_user")
            password_input.send_keys("test123")

            password_input.send_keys(Keys.RETURN)

            # Aguardar redirecionamento
            WebDriverWait(self.driver, 10).until(
                EC.url_changes(f"{self.live_server_url}/admin/login/")
            )

    class InteracaoMouseTecladoTest(SeleniumTestCase):
        """Testes de interações com mouse e teclado."""

        def test_clique_checkbox_presenca(self):
            """Testa clique em checkbox de presença."""
            self.login_selenium()

            # Navegar para página de registro
            url = f"{self.live_server_url}{reverse('presencas:registro_rapido')}"
            self.driver.get(f"{url}?turma={self.turma.id}")

            # Aguardar carregamento
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "presenca-checkbox"))
            )

            # Encontrar checkbox do primeiro aluno
            checkbox = self.driver.find_element(
                By.CSS_SELECTOR, f"input[name='aluno_{self.alunos[0].id}_presente']"
            )

            # Estado inicial (deve estar marcado por padrão)
            self.assertTrue(checkbox.is_selected())

            # Desmarcar
            checkbox.click()
            self.assertFalse(checkbox.is_selected())

            # Marcar novamente
            checkbox.click()
            self.assertTrue(checkbox.is_selected())

        def test_edicao_inline_justificativa(self):
            """Testa edição inline de justificativa."""
            self.login_selenium()

            # Criar presença para editar
            PresencaAcademica.objects.create(
                aluno=self.alunos[0],
                turma=self.turma,
                atividade=self.atividade,
                data=date.today(),
                presente=False,
                justificativa="Justificativa inicial",
            )

            # Navegar para grade editável
            url = f"{self.live_server_url}{reverse('presencas:grade_presencas')}"
            self.driver.get(f"{url}?turma={self.turma.id}")

            # Aguardar carregamento
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "editable-cell"))
            )

            # Encontrar célula de justificativa
            justificativa_cell = self.driver.find_element(
                By.CSS_SELECTOR,
                f"td[data-aluno-id='{self.alunos[0].id}'][data-field='justificativa']",
            )

            # Duplo clique para editar
            self.driver.execute_script("arguments[0].dblclick();", justificativa_cell)

            # Aguardar campo de input aparecer
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "input"))
            )

            # Editar texto
            input_field = justificativa_cell.find_element(By.TAG_NAME, "input")
            input_field.clear()
            input_field.send_keys("Nova justificativa editada")
            input_field.send_keys(Keys.RETURN)

            # Aguardar salvamento
            time.sleep(1)

            # Verificar se texto foi atualizado
            self.assertIn("Nova justificativa editada", justificativa_cell.text)

        def test_navegacao_setas_teclado(self):
            """Testa navegação com setas do teclado na grade."""
            self.login_selenium()

            url = f"{self.live_server_url}{reverse('presencas:grade_presencas')}"
            self.driver.get(f"{url}?turma={self.turma.id}")

            # Aguardar carregamento
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "editable-cell"))
            )

            # Focar na primeira célula
            primeira_celula = self.driver.find_element(
                By.CSS_SELECTOR, "td.editable-cell[data-row='0'][data-col='0']"
            )
            primeira_celula.click()

            # Navegar para a direita
            primeira_celula.send_keys(Keys.ARROW_RIGHT)

            # Verificar se foco mudou
            elemento_ativo = self.driver.switch_to.active_element
            self.assertEqual(elemento_ativo.get_attribute("data-col"), "1")

            # Navegar para baixo
            elemento_ativo.send_keys(Keys.ARROW_DOWN)

            # Verificar se foco mudou
            elemento_ativo = self.driver.switch_to.active_element
            self.assertEqual(elemento_ativo.get_attribute("data-row"), "1")

    class FuncionalidadeAjaxTest(SeleniumTestCase):
        """Testes de funcionalidades AJAX em tempo real."""

        def test_busca_alunos_tempo_real(self):
            """Testa busca de alunos em tempo real."""
            self.login_selenium()

            url = f"{self.live_server_url}{reverse('presencas:registro_rapido')}"
            self.driver.get(url)

            # Aguardar carregamento
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "id_turma"))
            )

            # Selecionar turma
            turma_select = self.driver.find_element(By.ID, "id_turma")
            for option in turma_select.find_elements(By.TAG_NAME, "option"):
                if option.get_attribute("value") == str(self.turma.id):
                    option.click()
                    break

            # Aguardar carregamento AJAX dos alunos
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "aluno-row"))
            )

            # Verificar se alunos foram carregados
            aluno_rows = self.driver.find_elements(By.CLASS_NAME, "aluno-row")
            self.assertEqual(len(aluno_rows), 3)  # 3 alunos criados

            # Verificar se nomes dos alunos estão presentes
            for aluno in self.alunos:
                self.assertIn(aluno.nome, self.driver.page_source)

        def test_salvamento_automatico(self):
            """Testa salvamento automático de alterações."""
            self.login_selenium()

            url = f"{self.live_server_url}{reverse('presencas:grade_presencas')}"
            self.driver.get(f"{url}?turma={self.turma.id}")

            # Aguardar carregamento
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "presenca-checkbox"))
            )

            # Alterar status de presença
            checkbox = self.driver.find_element(
                By.CSS_SELECTOR, f"input[data-aluno-id='{self.alunos[0].id}']"
            )
            checkbox.click()

            # Aguardar indicação de salvamento
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "salvando"))
            )

            # Aguardar confirmação de salvamento
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "salvo"))
            )

            # Verificar se foi salvo no banco
            time.sleep(1)  # Aguardar processamento
            presenca = PresencaAcademica.objects.filter(
                aluno=self.alunos[0], turma=self.turma, data=date.today()
            ).first()

            self.assertIsNotNone(presenca)

        def test_feedback_visual_acoes(self):
            """Testa feedback visual para ações do usuário."""
            self.login_selenium()

            url = f"{self.live_server_url}{reverse('presencas:registro_rapido')}"
            self.driver.get(f"{url}?turma={self.turma.id}")

            # Aguardar carregamento
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn-salvar"))
            )

            # Clicar no botão salvar
            btn_salvar = self.driver.find_element(By.CLASS_NAME, "btn-salvar")
            btn_salvar.click()

            # Verificar loading spinner
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "loading-spinner"))
            )

            # Aguardar sucesso
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
            )

            # Verificar mensagem de sucesso
            success_message = self.driver.find_element(By.CLASS_NAME, "alert-success")
            self.assertIn("sucesso", success_message.text.lower())


else:
    # Classes vazias quando Selenium não está disponível
    class SeleniumTestCase(TestCase):
        def setUp(self):
            self.skipTest("Selenium não está disponível")

    class InteracaoMouseTecladoTest(SeleniumTestCase):
        pass

    class FuncionalidadeAjaxTest(SeleniumTestCase):
        pass


class ResponsividadeTest(TestCase):
    """Testes de responsividade sem browser real."""

    def setUp(self):
        self.user = User.objects.create_user(username="resp_user", password="test123")
        self.client.login(username="resp_user", password="test123")

    def test_meta_viewport_presente(self):
        """Testa se meta viewport está presente para mobile."""
        url = reverse("presencas:index")
        response = self.client.get(url)

        self.assertContains(response, 'name="viewport"')
        self.assertContains(response, "width=device-width")

    def test_classes_responsivas(self):
        """Testa se classes CSS responsivas estão presentes."""
        url = reverse("presencas:registro_rapido")
        response = self.client.get(url)

        # Classes Bootstrap ou CSS customizado responsivo
        responsive_classes = [
            "col-sm-",
            "col-md-",
            "col-lg-",
            "hidden-xs",
            "hidden-sm",
            "table-responsive",
            "btn-block",
        ]

        for css_class in responsive_classes:
            self.assertContains(response, css_class)

    def test_javascript_mobile_friendly(self):
        """Testa se JavaScript inclui tratamento para mobile."""
        url = reverse("presencas:grade_presencas")
        response = self.client.get(url)

        # Verificar se há tratamento para touch events
        mobile_js_patterns = [
            "touchstart",
            "touchend",
            "ontouchstart",
            "navigator.userAgent",
        ]

        # Pelo menos um padrão mobile deve estar presente
        has_mobile_support = any(
            pattern in response.content.decode() for pattern in mobile_js_patterns
        )

        self.assertTrue(has_mobile_support or "mobile.js" in response.content.decode())


class AccessibilidadeTest(TestCase):
    """Testes básicos de acessibilidade."""

    def setUp(self):
        self.user = User.objects.create_user(username="access_user", password="test123")
        self.client.login(username="access_user", password="test123")

    def test_labels_formularios(self):
        """Testa se formulários têm labels apropriados."""
        url = reverse("presencas:registro_rapido")
        response = self.client.get(url)

        # Verificar labels
        self.assertContains(response, "<label for=")
        self.assertContains(response, "aria-label=")

    def test_estrutura_semantica(self):
        """Testa estrutura semântica do HTML."""
        url = reverse("presencas:index")
        response = self.client.get(url)

        # Elementos semânticos
        semantic_elements = ["<main", "<section", "<article", "<nav", "<header"]

        for element in semantic_elements:
            self.assertContains(response, element)

    def test_contraste_cores(self):
        """Testa se CSS inclui classes para alto contraste."""
        url = reverse("presencas:consolidado")
        response = self.client.get(url)

        # Verificar se há classes de contraste
        contrast_classes = [
            "high-contrast",
            "text-primary",
            "text-danger",
            "bg-warning",
        ]

        for css_class in contrast_classes:
            self.assertContains(response, css_class)

    def test_navegacao_teclado(self):
        """Testa se elementos são navegáveis por teclado."""
        url = reverse("presencas:grade_presencas")
        response = self.client.get(url)

        # Verificar tabindex e foco
        self.assertContains(response, "tabindex=")
        self.assertContains(response, ":focus")
        self.assertContains(response, "outline:")
