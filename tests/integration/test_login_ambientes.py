"""
Teste Selenium para validar login nos ambientes de desenvolvimento e produção.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def setup_driver():
    """Configura o Chrome WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver


def test_login(driver, url, username, password, ambiente):
    """
    Testa login em um ambiente específico.
    
    Args:
        driver: WebDriver do Selenium
        url: URL do ambiente
        username: Nome de usuário
        password: Senha
        ambiente: Nome do ambiente (para logs)
    """
    print(f"\n{'='*60}")
    print(f"🔍 Testando ambiente: {ambiente}")
    print(f"   URL: {url}")
    print(f"   Usuário: {username}")
    print(f"{'='*60}")
    
    try:
        # Acessa a página de login
        print(f"📍 Acessando {url}...")
        driver.get(url)
        time.sleep(2)
        
        # Tira screenshot da página inicial
        screenshot_inicial = f"test_login_{ambiente.lower().replace(' ', '_')}_inicial.png"
        driver.save_screenshot(screenshot_inicial)
        print(f"📸 Screenshot salvo: {screenshot_inicial}")
        
        # Verifica se está na página de login
        if "/accounts/login/" not in driver.current_url and "login" not in driver.page_source.lower():
            print(f"⚠️  Redirecionando para página de login...")
            driver.get(f"{url}/accounts/login/")
            time.sleep(2)
        
        # Localiza os campos de login
        print(f"🔎 Localizando campos de login...")
        
        # Tenta múltiplos seletores para username
        username_field = None
        username_selectors = [
            "id_username",
            "username",
            "id_username_home",
            "login"
        ]
        
        for selector in username_selectors:
            try:
                username_field = driver.find_element(By.ID, selector)
                print(f"✅ Campo username encontrado: #{selector}")
                break
            except NoSuchElementException:
                continue
        
        if not username_field:
            try:
                username_field = driver.find_element(By.NAME, "username")
                print(f"✅ Campo username encontrado por name")
            except NoSuchElementException:
                print(f"❌ Campo username não encontrado!")
                raise
        
        # Tenta múltiplos seletores para password
        password_field = None
        password_selectors = [
            "id_password",
            "password",
            "id_password_home"
        ]
        
        for selector in password_selectors:
            try:
                password_field = driver.find_element(By.ID, selector)
                print(f"✅ Campo password encontrado: #{selector}")
                break
            except NoSuchElementException:
                continue
        
        if not password_field:
            try:
                password_field = driver.find_element(By.NAME, "password")
                print(f"✅ Campo password encontrado por name")
            except NoSuchElementException:
                print(f"❌ Campo password não encontrado!")
                raise
        
        # Preenche os campos
        print(f"⌨️  Preenchendo credenciais...")
        username_field.clear()
        username_field.send_keys(username)
        time.sleep(0.5)
        
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(0.5)
        
        # Localiza e clica no botão de submit
        print(f"🖱️  Clicando no botão de login...")
        submit_button = None
        
        try:
            # Tenta encontrar botão por texto
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(., 'Entrar')]")
        except NoSuchElementException:
            try:
                # Tenta encontrar qualquer botão submit
                submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            except NoSuchElementException:
                # Tenta encontrar input submit
                submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        
        submit_button.click()
        
        # Aguarda redirecionamento
        print(f"⏳ Aguardando redirecionamento...")
        time.sleep(3)
        
        # Tira screenshot após login
        screenshot_pos = f"test_login_{ambiente.lower().replace(' ', '_')}_pos_login.png"
        driver.save_screenshot(screenshot_pos)
        print(f"📸 Screenshot salvo: {screenshot_pos}")
        
        # Verifica se o login foi bem-sucedido
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        # Critérios de sucesso
        success_indicators = [
            "/accounts/login/" not in current_url,
            "sgi - omaum" in page_source or "bem-vindo" in page_source,
            "sair" in page_source or "logout" in page_source,
            "ambiente de" in page_source
        ]
        
        is_success = sum(success_indicators) >= 2
        
        if is_success:
            print(f"✅ LOGIN BEM-SUCEDIDO!")
            print(f"   URL atual: {current_url}")
            
            # Tenta capturar o nome do usuário logado
            try:
                user_element = driver.find_element(By.XPATH, "//*[contains(@class, 'nav-link') and contains(text(), '{username}')]".replace("{username}", username))
                print(f"   Usuário logado: {user_element.text}")
            except:
                pass
            
            return True
        else:
            print(f"❌ LOGIN FALHOU!")
            print(f"   URL atual: {current_url}")
            
            # Verifica se há mensagens de erro
            try:
                error_messages = driver.find_elements(By.XPATH, "//*[contains(@class, 'alert') or contains(@class, 'error')]")
                if error_messages:
                    print(f"   Mensagens de erro:")
                    for msg in error_messages:
                        print(f"      - {msg.text}")
            except:
                pass
            
            return False
            
    except Exception as e:
        print(f"❌ ERRO durante o teste: {str(e)}")
        screenshot_erro = f"test_login_{ambiente.lower().replace(' ', '_')}_erro.png"
        driver.save_screenshot(screenshot_erro)
        print(f"📸 Screenshot de erro salvo: {screenshot_erro}")
        return False


def main():
    """Função principal que executa os testes."""
    print("\n" + "="*60)
    print("🚀 TESTE DE LOGIN - AMBIENTES OMAUM")
    print("="*60)
    
    # Configuração dos ambientes
    ambientes = [
        {
            "nome": "Desenvolvimento",
            "url": "http://localhost:8001",  # Dev usa porta 8001
            "username": "desenv",
            "password": "desenv123"
        },
        {
            "nome": "Produção",
            "url": "http://localhost",  # Prod usa porta 80 via Nginx
            "username": "admin",
            "password": "admin123"
        }
    ]
    
    resultados = []
    driver = None
    
    try:
        # Cria o driver
        print("\n🔧 Configurando Chrome WebDriver...")
        driver = setup_driver()
        print("✅ WebDriver configurado com sucesso!")
        
        # Testa cada ambiente
        for amb in ambientes:
            resultado = test_login(
                driver,
                amb["url"],
                amb["username"],
                amb["password"],
                amb["nome"]
            )
            resultados.append({
                "ambiente": amb["nome"],
                "sucesso": resultado
            })
            
            # Aguarda entre testes
            time.sleep(2)
        
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {str(e)}")
        
    finally:
        # Fecha o navegador
        if driver:
            print("\n🔒 Fechando navegador...")
            driver.quit()
    
    # Exibe resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    for resultado in resultados:
        status = "✅ SUCESSO" if resultado["sucesso"] else "❌ FALHA"
        print(f"{resultado['ambiente']:20s} : {status}")
    
    print("="*60 + "\n")
    
    # Retorna código de saída
    todos_sucesso = all(r["sucesso"] for r in resultados)
    return 0 if todos_sucesso else 1


if __name__ == "__main__":
    exit(main())
