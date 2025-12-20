#!/usr/bin/env python
"""
Script para testar filtros dinâmicos de atividades usando Selenium
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

# Iniciar navegador
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1920, 1080)

try:
    print("🔍 Teste de Filtros Dinâmicos - Atividades\n")
    
    # 1. Acessar página de login
    print("1️⃣ Acessando login...")
    driver.get("http://localhost:8001/entrar/")
    time.sleep(2)
    
    # 2. Fazer login
    print("2️⃣ Fazendo login como 'desenv'...")
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")
    username.send_keys("desenv")
    password.send_keys("desenv")
    
    submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit.click()
    time.sleep(2)
    
    # 3. Acessar página de atividades
    print("3️⃣ Acessando /atividades/...")
    driver.get("http://localhost:8001/atividades/")
    time.sleep(2)
    
    # 4. Verificar se o script carregou
    print("4️⃣ Verificando console logs...")
    logs = driver.get_log('browser')
    print("\n📋 Console Logs (inicial):")
    for entry in logs:
        print(f"   {entry['level']}: {entry['message']}")
    
    # 5. Digitar no campo de busca
    print("\n5️⃣ Digitando 'aula' no campo de busca...")
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id_q"))
    )
    search_input.clear()
    search_input.send_keys("aula")
    
    # 6. Aguardar debounce (500ms) + requisição
    print("6️⃣ Aguardando debounce e requisição AJAX...")
    time.sleep(2)
    
    # 7. Capturar logs novamente
    logs = driver.get_log('browser')
    print("\n📋 Console Logs (após busca):")
    for entry in logs:
        print(f"   {entry['level']}: {entry['message']}")
    
    # 8. Verificar se spinner apareceu
    try:
        spinner = driver.find_element(By.ID, "atividades-spinner")
        print(f"\n🔄 Spinner encontrado - Display: {spinner.value_of_css_property('display')}")
    except:
        print("\n⚠️  Spinner não encontrado")
    
    # 9. Verificar tabela
    try:
        tabela = driver.find_element(By.ID, "tabela-atividades-container")
        print(f"\n📊 Tabela encontrada - Display: {tabela.value_of_css_property('display')}")
        print(f"   Conteúdo (primeiros 200 chars): {tabela.text[:200]}")
    except:
        print("\n⚠️  Tabela não encontrada")
    
    # 10. Capturar screenshot
    print("\n📸 Salvando screenshot...")
    driver.save_screenshot("/tmp/atividades_test.png")
    print("   Screenshot salvo em /tmp/atividades_test.png")
    
    print("\n✅ Teste concluído!")
    
except Exception as e:
    print(f"\n❌ Erro durante teste: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    driver.quit()
    print("\n🔚 Navegador fechado")
