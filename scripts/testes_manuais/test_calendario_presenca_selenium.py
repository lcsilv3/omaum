import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


class TestCalendarioPresenca(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ajuste o caminho do driver conforme necessário
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        # Altere a URL para o endereço correto do seu ambiente local
        cls.url = "http://localhost:8000/presencas/registrar-presenca/dias-atividades/"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_calendario_abre_ao_clicar_input_e_icone(self):
        driver = self.driver
        # 1. Acessa a página de login
        driver.get("http://localhost:8000/entrar/")
        time.sleep(1)
        # 2. Preenche usuário e senha
        username_input = driver.find_element(By.ID, "id_username")
        password_input = driver.find_element(By.ID, "id_password")
        username_input.send_keys("lcsilv3")
        password_input.send_keys("iG356900")
        # 3. Submete o formulário
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)
        # 4. Agora acessa a página de registro de presença
        driver.get(self.url)
        time.sleep(2)
        # DEBUG: printa o HTML carregado para inspeção
        print("\n======= HTML carregado pelo Selenium =======\n")
        print(driver.page_source)
        print("\n======= FIM HTML carregado pelo Selenium =======\n")
        # Seleciona o primeiro input do calendário
        input_box = driver.find_element(By.CSS_SELECTOR, ".dias-datepicker")
        # Clica no input
        ActionChains(driver).move_to_element(input_box).click().perform()
        time.sleep(1)
        # Verifica se o calendário apareceu
        calendario = driver.find_element(By.CLASS_NAME, "flatpickr-calendar")
        self.assertTrue(
            calendario.is_displayed(), "Calendário não abriu ao clicar no input."
        )
        # Fecha o calendário
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(1)
        # Clica no ícone do calendário
        calendar_icon = input_box.find_element(
            By.XPATH, "../../span[contains(@class, 'calendar-icon')]"
        )
        ActionChains(driver).move_to_element(calendar_icon).click().perform()
        time.sleep(1)
        # Verifica se o calendário apareceu novamente
        calendario = driver.find_element(By.CLASS_NAME, "flatpickr-calendar")
        self.assertTrue(
            calendario.is_displayed(), "Calendário não abriu ao clicar no ícone."
        )


if __name__ == "__main__":
    unittest.main()
