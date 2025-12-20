"""
Script Selenium para testar a máscara de horário no formulário de turmas.
Captura logs do console JavaScript e testa o comportamento da máscara.

AMBIENTES:
- Desenvolvimento: python test_mascara_horario.py
- Produção: python test_mascara_horario.py --prod
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Determinar ambiente
AMBIENTE = "PRODUÇÃO" if "--prod" in sys.argv else "DESENVOLVIMENTO"
URL_BASE = "http://localhost" if "--prod" in sys.argv else "http://localhost:8000"
USERNAME = "admin" if "--prod" in sys.argv else "desenv"
PASSWORD = "admin123" if "--prod" in sys.argv else "desenv123"

# Configurar Chrome com logging habilitado
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

# Iniciar navegador
driver = webdriver.Chrome(options=options)

try:
    print("=" * 80)
    print(f"TESTE DA MÁSCARA DE HORÁRIO - AMBIENTE: {AMBIENTE}")
    print("=" * 80)
    
    # 1. Acessar a página
    url = f"{URL_BASE}/turmas/criar/"
    print(f"\n1. Acessando: {url}")
    driver.get(url)
    time.sleep(1)
    
    # 2. Verificar se precisa fazer login (checar se o campo horário existe)
    print("\n2. Verificando se precisa login...")
    time.sleep(1)
    
    # Tentar encontrar o campo horário OU campo de login
    try:
        driver.find_element(By.NAME, "horario")
        print("   ✅ Já está logado!")
    except:
        print("   Campo horário não encontrado, tentando fazer login...")
        try:
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            
            print(f"   Preenchendo credenciais: {USERNAME} / {PASSWORD}")
            username_field.send_keys(USERNAME)
            password_field.send_keys(PASSWORD)
            password_field.send_keys(Keys.RETURN)
            
            time.sleep(2)
            
            # Acessar novamente após login
            print(f"   Acessando novamente: {url}")
            driver.get(url)
            time.sleep(2)
        except Exception as e:
            print(f"   ⚠️ Não encontrou campos de login: {e}")
    
    # 3. Aguardar a página carregar completamente
    print("\n3. Aguardando página carregar...")
    wait = WebDriverWait(driver, 10)
    
    # 4. Capturar logs ANTES de interagir com o campo
    print("\n4. LOGS DO CONSOLE (carregamento inicial):")
    print("-" * 80)
    logs = driver.get_log('browser')
    for log in logs:
        if 'HORÁRIO' in log['message'] or 'horário' in log['message'] or 'Campo horário' in log['message']:
            print(f"   [{log['level']}] {log['message']}")
    
    # 5. Encontrar o campo horário
    print("\n5. Localizando campo horário...")
    try:
        horario_field = wait.until(
            EC.presence_of_element_located((By.NAME, "horario"))
        )
        print(f"   ✅ Campo encontrado!")
        print(f"   - ID: {horario_field.get_attribute('id')}")
        print(f"   - Valor inicial: '{horario_field.get_attribute('value')}'")
        print(f"   - Placeholder: '{horario_field.get_attribute('placeholder')}'")
    except TimeoutException:
        print("   ❌ Campo horário NÃO encontrado!")
        raise
    
    # 6. Clicar no campo (focus)
    print("\n6. Clicando no campo (focus)...")
    horario_field.click()
    time.sleep(0.5)
    
    # Capturar logs após focus
    print("\n   LOGS DO CONSOLE (após focus):")
    print("   " + "-" * 76)
    logs = driver.get_log('browser')
    for log in logs:
        print(f"   [{log['level']}] {log['message']}")
    
    # Verificar valor após focus
    valor_apos_focus = horario_field.get_attribute('value')
    print(f"\n   Valor após focus: '{valor_apos_focus}'")
    
    # 7. Digitar dígitos
    print("\n7. Digitando '1'...")
    horario_field.send_keys('1')
    time.sleep(0.5)
    
    # Capturar logs após digitar '1'
    print("\n   LOGS DO CONSOLE (após digitar '1'):")
    print("   " + "-" * 76)
    logs = driver.get_log('browser')
    for log in logs:
        print(f"   [{log['level']}] {log['message']}")
    
    valor_apos_1 = horario_field.get_attribute('value')
    print(f"\n   Valor após '1': '{valor_apos_1}'")
    print(f"   Esperado: '1_:__ às __:__'")
    print(f"   Match: {'✅' if '1' in valor_apos_1 and ':' in valor_apos_1 else '❌'}")
    
    # 8. Digitar mais dígitos
    print("\n8. Digitando '3'...")
    horario_field.send_keys('3')
    time.sleep(0.5)
    
    logs = driver.get_log('browser')
    if logs:
        print("\n   LOGS DO CONSOLE (após digitar '3'):")
        print("   " + "-" * 76)
        for log in logs:
            print(f"   [{log['level']}] {log['message']}")
    
    valor_apos_13 = horario_field.get_attribute('value')
    print(f"\n   Valor após '13': '{valor_apos_13}'")
    print(f"   Esperado: '13:__ às __:__'")
    print(f"   Match: {'✅' if '13:' in valor_apos_13 else '❌'}")
    
    # 9. Continuar digitando para completar horário
    print("\n9. Digitando '2' e '2'...")
    horario_field.send_keys('22')
    time.sleep(0.5)
    
    valor_apos_1322 = horario_field.get_attribute('value')
    print(f"\n   Valor após '1322': '{valor_apos_1322}'")
    print(f"   Esperado: '13:22 às __:__'")
    print(f"   Match: {'✅' if '13:22' in valor_apos_1322 else '❌'}")
    
    # 10. Verificar todos os event listeners registrados
    print("\n10. Verificando event listeners no campo...")
    listeners_script = """
    const input = document.querySelector('input[name="horario"]');
    if (!input) return 'Campo não encontrado';
    
    // Tentar obter listeners (não funciona em todos os navegadores)
    return {
        value: input.value,
        readOnly: input.readOnly,
        disabled: input.disabled,
        type: input.type,
        maxLength: input.maxLength
    };
    """
    info = driver.execute_script(listeners_script)
    print(f"   Info do campo: {info}")
    
    # 11. Capturar TODOS os logs finais
    print("\n11. TODOS OS LOGS DO CONSOLE (final):")
    print("-" * 80)
    logs = driver.get_log('browser')
    if logs:
        for log in logs:
            print(f"   [{log['level']}] {log['message']}")
    else:
        print("   (nenhum log adicional)")
    
    # 12. Tirar screenshot
    screenshot_path = "e:/projetos/omaum/test_mascara_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"\n12. Screenshot salvo em: {screenshot_path}")
    
    # Aguardar para visualização manual
    print("\n" + "=" * 80)
    print("Teste concluído! Aguardando 10 segundos para você visualizar...")
    print("=" * 80)
    time.sleep(10)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    
    # Tirar screenshot do erro
    try:
        driver.save_screenshot("e:/projetos/omaum/test_mascara_erro.png")
        print("Screenshot do erro salvo em: test_mascara_erro.png")
    except:
        pass
    
finally:
    print("\nFechando navegador...")
    driver.quit()
