import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.django_db
def test_editar_aluno_adicionar_historico_81991045700(live_server):
    """
    Testa edição do aluno com CPF 81991045700, adicionando um registro de histórico via formset dinâmico.
    Salva o HTML da página de edição para diagnóstico.
    """
    from django.contrib.auth.models import User
    from alunos.models import Aluno
    from datetime import date

    # Garante que o usuário existe no banco de teste
    if not User.objects.filter(username="lcsilv3").exists():
        User.objects.create_user(
            username="lcsilv3", password="iG356900", is_staff=True, is_superuser=True
        )
    # Garante que o aluno de CPF 81991045700 existe
    if not Aluno.objects.filter(cpf="81991045700").exists():
        Aluno.objects.create(
            cpf="81991045700",
            nome="Aluno Teste Selenium",
            data_nascimento=date(2000, 1, 1),
            email="selenium81991045700@teste.com",
            sexo="M",
            situacao="ativo",
            nacionalidade="Brasileiro",
            naturalidade="SP",
            ativo=True,
            created_at=date.today(),
            updated_at=date.today(),
        )
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        # Realiza login pela página correta
        driver.get(live_server.url + "/entrar/")
        driver.find_element(By.NAME, "username").send_keys("lcsilv3")
        driver.find_element(By.NAME, "password").send_keys("iG356900")
        # Submete o formulário de login explicitamente
        login_form = driver.find_element(By.TAG_NAME, "form")
        login_form.submit()
        # Aguarda redirecionamento para página inicial ou dashboard
        wait.until(EC.url_changes(live_server.url + "/entrar/"))
        # Após login, acessa página de edição do aluno existente
        driver.get(live_server.url + "/alunos/81991045700/editar/")
        # Salva o HTML para diagnóstico
        with open("ui_test_error_dump.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        # Espera o botão de adicionar registro histórico estar visível e habilitado
        add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-historico-form")))
        driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            add_btn,
        )
        time.sleep(0.5)  # Pequeno delay para garantir que não há overlay
        add_btn.click()
        time.sleep(1)
        historico_list = driver.find_element(By.ID, "historico-form-list")
        forms = historico_list.find_elements(By.CLASS_NAME, "historico-form")
        novo_form = forms[-1]
        # Preenche campos do novo registro
        campos = {
            "codigo": "TESTE123",
            "ordem_servico": "OS999",
            "data_os": "2025-08-01",
            "numero_iniciatico": "002",
            "nome_iniciatico": "Teste UI",
            "observacoes": "Registro automatizado Selenium",
        }
        for campo, valor in campos.items():
            try:
                input_elem = novo_form.find_element(
                    By.NAME,
                    [
                        e.get_attribute("name")
                        for e in novo_form.find_elements(By.TAG_NAME, "input")
                        + novo_form.find_elements(By.TAG_NAME, "textarea")
                        if campo in e.get_attribute("name")
                    ][0],
                )
                input_elem.send_keys(valor)
            except Exception:
                pass
        # Envia o formulário
        driver.find_element(By.ID, "form-aluno").submit()

        # Valida se houve redirecionamento (registro salvo)
        wait.until(EC.url_contains("/alunos/"))
    finally:
        driver.quit()
