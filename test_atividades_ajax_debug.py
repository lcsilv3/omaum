"""
Script de debug para testar AJAX de atividades e capturar logs.
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configurar Chrome em modo headless
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    print("🔵 Acessando página de login...")
    driver.get("http://localhost:8001/accounts/login/")
    
    print("🔵 Fazendo login...")
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = driver.find_element(By.NAME, "password")
    
    username_field.send_keys("desenv")
    password_field.send_keys("desenv123")
    
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    print("🔵 Aguardando redirect após login...")
    time.sleep(2)
    
    print("🔵 Acessando página de atividades...")
    driver.get("http://localhost:8001/atividades/")
    
    print("🔵 Aguardando campo de busca carregar...")
    search_field = wait.until(EC.presence_of_element_located((By.ID, "id_q")))
    
    print("🔵 Digitando 'aula' no campo de busca para disparar AJAX...")
    search_field.clear()
    search_field.send_keys("aula")
    
    print("🔵 Aguardando 3 segundos para AJAX completar...")
    time.sleep(3)
    
    # Capturar logs do console do navegador
    print("\n📋 LOGS DO CONSOLE DO NAVEGADOR:")
    for log in driver.get_log('browser'):
        print(f"  {log['level']}: {log['message']}")
    
    print("\n✅ Teste concluído! Verifique os logs do container agora.")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    driver.quit()
