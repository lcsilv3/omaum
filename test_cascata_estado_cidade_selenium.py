#!/usr/bin/env python
"""
Teste Selenium para validar cascateamento Estado → Cidade → Bairro
no formulário de alunos.
"""
import os
import sys
import time
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omaum.settings.development")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from django.contrib.auth import get_user_model

User = get_user_model()

# Configurações
BASE_URL = "http://localhost:8000"
TIMEOUT = 10

def setup_driver():
    """Configura o driver do Chrome."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Remova para ver o navegador
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    return driver

def login(driver, username="desenv", password="desenv"):
    """Faz login no sistema."""
    print(f"\n🔑 Fazendo login como '{username}'...")
    driver.get(f"{BASE_URL}/entrar/")
    
    # Aguarda o formulário de login
    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    
    # Preenche e submete
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Aguarda redirecionamento
    WebDriverWait(driver, TIMEOUT).until(
        EC.url_changes(f"{BASE_URL}/entrar/")
    )
    print(f"✅ Login realizado com sucesso!")

def test_estado_cidade_cascata(driver):
    """Testa o cascateamento Estado → Cidade → Bairro."""
    
    print("\n" + "="*60)
    print("🧪 TESTANDO CASCATEAMENTO ESTADO → CIDADE → BAIRRO")
    print("="*60)
    
    # 1. Acessa a página de criar aluno
    print("\n📄 Acessando /alunos/criar/...")
    driver.get(f"{BASE_URL}/alunos/criar/")
    
    # Aguarda o formulário carregar
    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "id_nome"))
    )
    print("✅ Formulário carregado")
    
    # 2. Aguarda Select2 inicializar
    print("\n⏳ Aguardando Select2 inicializar...")
    time.sleep(2)  # Select2 precisa de tempo para inicializar
    
    # 3. Localiza o container Select2 do estado
    print("\n🔍 Localizando campo Estado...")
    try:
        estado_select2 = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.select2-container[aria-labelledby='select2-id_estado_ref-container']"))
        )
        print("✅ Campo Estado encontrado")
    except TimeoutException:
        print("❌ Campo Estado não encontrado!")
        print("Elementos Select2 disponíveis:")
        select2_elements = driver.find_elements(By.CSS_SELECTOR, "span.select2-container")
        for elem in select2_elements:
            print(f"  - {elem.get_attribute('aria-labelledby')}")
        return False
    
    # 4. Clica no Select2 do estado para abrir
    print("\n🖱️  Clicando no campo Estado...")
    estado_select2.click()
    time.sleep(1)
    
    # 5. Aguarda o dropdown do Select2 abrir
    print("⏳ Aguardando dropdown abrir...")
    try:
        search_input = WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input.select2-search__field"))
        )
        print("✅ Dropdown aberto")
    except TimeoutException:
        print("❌ Dropdown não abriu!")
        return False
    
    # 6. Digita para buscar "AL" (Alagoas)
    print("\n⌨️  Digitando 'AL' para buscar Alagoas...")
    search_input.send_keys("AL")
    time.sleep(1)
    
    # 7. Aguarda resultados e seleciona Alagoas
    print("⏳ Aguardando resultados...")
    try:
        resultado = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.select2-results__option"))
        )
        texto_resultado = resultado.text
        print(f"✅ Resultado encontrado: '{texto_resultado}'")
        resultado.click()
        time.sleep(1)
        print("✅ Estado 'AL' selecionado")
    except TimeoutException:
        print("❌ Nenhum resultado encontrado para 'AL'!")
        return False
    
    # 8. Agora testa se o campo Cidade está habilitado
    print("\n🔍 Verificando campo Cidade...")
    try:
        cidade_select2 = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.select2-container[aria-labelledby='select2-id_cidade_ref-container']"))
        )
        print("✅ Campo Cidade encontrado")
    except TimeoutException:
        print("❌ Campo Cidade não encontrado!")
        return False
    
    # 9. Clica no Select2 da cidade
    print("\n🖱️  Clicando no campo Cidade...")
    cidade_select2.click()
    time.sleep(1)
    
    # 10. Aguarda o dropdown da cidade abrir
    print("⏳ Aguardando dropdown Cidade abrir...")
    try:
        cidade_search_input = WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input.select2-search__field"))
        )
        print("✅ Dropdown Cidade aberto")
    except TimeoutException:
        print("❌ Dropdown Cidade não abriu!")
        return False
    
    # 11. Digita para buscar cidade "Maceió"
    print("\n⌨️  Digitando 'Mac' para buscar Maceió...")
    cidade_search_input.send_keys("Mac")
    time.sleep(2)  # Aguarda AJAX carregar resultados
    
    # 12. Verifica se há resultados de cidades
    print("⏳ Aguardando resultados de cidades...")
    try:
        # Aguarda os resultados aparecerem
        resultado_cidade = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.select2-results__option"))
        )
        
        # Verifica se não é mensagem de "No results"
        texto = resultado_cidade.text
        if "No results" in texto or "Nenhum resultado" in texto:
            print(f"❌ FALHA: Nenhuma cidade encontrada!")
            print(f"   Mensagem: '{texto}'")
            return False
        
        print(f"✅ SUCESSO: Cidades encontradas! Primeiro resultado: '{texto}'")
        
        # Clica na primeira cidade
        resultado_cidade.click()
        time.sleep(1)
        print(f"✅ Cidade selecionada: '{texto}'")
        
        return True
        
    except TimeoutException:
        print("❌ FALHA: Timeout aguardando resultados de cidades!")
        
        # Captura screenshot para debug
        screenshot_path = "test_cascata_erro.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot salva em: {screenshot_path}")
        
        # Mostra o HTML do dropdown
        try:
            dropdown = driver.find_element(By.CSS_SELECTOR, ".select2-results")
            print(f"\n📄 HTML do dropdown:\n{dropdown.get_attribute('outerHTML')}")
        except:
            print("⚠️  Não foi possível capturar HTML do dropdown")
        
        return False

def main():
    """Função principal."""
    driver = None
    try:
        # Setup
        driver = setup_driver()
        
        # Login
        login(driver)
        
        # Testa cascateamento
        sucesso = test_estado_cidade_cascata(driver)
        
        # Resultado final
        print("\n" + "="*60)
        if sucesso:
            print("✅ TESTE PASSOU: Cascateamento funcionando corretamente!")
        else:
            print("❌ TESTE FALHOU: Problema no cascateamento Estado → Cidade")
        print("="*60)
        
        return 0 if sucesso else 1
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        
        # Captura screenshot
        if driver:
            try:
                screenshot_path = "test_cascata_exception.png"
                driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot salva em: {screenshot_path}")
            except:
                pass
        
        return 1
        
    finally:
        if driver:
            driver.quit()
            print("\n🔒 Navegador fechado")

if __name__ == "__main__":
    exit(main())
