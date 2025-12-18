"""
Teste simplificado para verificar máscara de Ordem de Serviço
Simula digitação real tecla por tecla
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)

try:
    # Login
    driver.get("http://localhost:8000/alunos/criar/")
    time.sleep(1)
    
    try:
        driver.find_element(By.ID, "id_nome")
    except:
        user = driver.find_element(By.NAME, "username")
        pwd = driver.find_element(By.NAME, "password")
        user.send_keys("desenv")
        pwd.send_keys("desenv123")
        pwd.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get("http://localhost:8000/alunos/criar/")
        time.sleep(2)
    
    # Expandir card e adicionar registro
    driver.execute_script("""
        var collapse = document.getElementById('dados-iniciaticos');
        if (collapse) new bootstrap.Collapse(collapse, {toggle: true});
    """)
    time.sleep(1)
    
    driver.execute_script("""
        var btn = document.getElementById('add-historico-form');
        if (btn) btn.click();
    """)
    time.sleep(1)
    
    # Localizar campo
    campo = driver.find_elements(By.CSS_SELECTOR, 'input[name*="ordem_servico"]:not([name*="__prefix__"])')[-1]
    
    print("Campo encontrado:", campo.get_attribute('id'))
    print("Valor inicial:", repr(campo.get_attribute('value')))
    
    # Verificar logs do console
    print("\n📋 LOGS DO CONSOLE APÓS ADICIONAR CAMPO:")
    logs = driver.get_log('browser')
    for log in logs:
        if 'máscara' in log['message'].lower() or 'ordem' in log['message'].lower():
            print(f"  [{log['level']}] {log['message']}")
    
    # Dar foco
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo)
    driver.execute_script("arguments[0].focus();", campo)
    time.sleep(0.5)
    
    print("\nValor após focus:", repr(campo.get_attribute('value')))
    
    # Verificar logs após focus
    print("\n📋 LOGS DO CONSOLE APÓS FOCUS:")
    logs = driver.get_log('browser')
    for log in logs:
        print(f"  [{log['level']}] {log['message']}")
    
    # Digitar tecla por tecla
    digitos = ['1', '2', '3', '4', '5', '6', '7', '8']
    for i, digito in enumerate(digitos, 1):
        driver.execute_script(f"""
            var campo = arguments[0];
            var evt = new KeyboardEvent('keydown', {{
                key: '{digito}',
                code: 'Digit{digito}',
                keyCode: {ord(digito)},
                which: {ord(digito)},
                bubbles: true,
                cancelable: true
            }});
            campo.dispatchEvent(evt);
        """, campo)
        time.sleep(0.1)
        valor = campo.get_attribute('value')
        print(f"Após digitar '{digito}' ({i} dígitos): '{valor}'")
    
    print("\n✅ Valor final:", repr(campo.get_attribute('value')))
    print("✅ Esperado: '1234/5678'")
    
    time.sleep(5)

except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    driver.save_screenshot("test_aluno_erro_digitacao.png")

finally:
    driver.quit()
