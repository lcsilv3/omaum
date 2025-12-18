"""
Script Selenium para testar o campo Ordem de Serviço no formulário de alunos.
Captura logs do console JavaScript e testa o comportamento do campo.

AMBIENTES:
- Desenvolvimento: python test_aluno_ordem_servico.py
- Produção: python test_aluno_ordem_servico.py --prod
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
    print(f"TESTE DO CAMPO ORDEM DE SERVIÇO - AMBIENTE: {AMBIENTE}")
    print("=" * 80)
    
    # 1. Acessar a página de criar aluno
    url = f"{URL_BASE}/alunos/criar/"
    print(f"\n1. Acessando: {url}")
    driver.get(url)
    time.sleep(1)
    
    # 2. Verificar se precisa fazer login
    print("\n2. Verificando se precisa login...")
    time.sleep(1)
    
    try:
        # Verificar se já está na página do formulário (procurar por algum campo específico)
        driver.find_element(By.ID, "id_nome")
        print("   ✅ Já está logado!")
    except:
        print("   Tentando fazer login...")
        try:
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            
            print(f"   Preenchendo credenciais: {USERNAME} / {PASSWORD}")
            username_field.send_keys(USERNAME)
            password_field.send_keys(PASSWORD)
            password_field.send_keys(Keys.RETURN)
            
            time.sleep(2)
            print(f"   Acessando novamente: {url}")
            driver.get(url)
            time.sleep(2)
        except Exception as e:
            print(f"   ❌ Erro ao fazer login: {e}")
            driver.save_screenshot("test_aluno_erro_login.png")
            raise
    
    print("\n3. Aguardando página carregar...")
    time.sleep(2)
    
    # 4. Capturar logs do console (carregamento inicial)
    print("\n4. LOGS DO CONSOLE (carregamento inicial):")
    print("-" * 80)
    logs = driver.get_log('browser')
    for log in logs:
        if log['level'] in ['INFO', 'WARNING', 'SEVERE']:
            print(f"   [{log['level']}] {log['source']} {log['message']}")
    if not logs:
        print("   (nenhum log)")
    
    # 5. Expandir card "Dados Iniciáticos"
    print("\n5. Expandindo card 'Dados Iniciáticos'...")
    try:
        # Usar JavaScript para expandir o collapse
        driver.execute_script("""
            var collapse = document.getElementById('dados-iniciaticos');
            if (collapse) {
                var bsCollapse = new bootstrap.Collapse(collapse, {toggle: true});
            }
        """)
        time.sleep(1)
        print("   ✅ Card expandido via JavaScript!")
    except Exception as e:
        print(f"   ⚠️ Erro ao expandir card: {e}")
    
    # 6. Adicionar um registro de histórico (via JavaScript)
    print("\n6. Adicionando novo registro de histórico...")
    try:
        driver.execute_script("""
            var addButton = document.getElementById('add-historico-form');
            if (addButton) {
                addButton.scrollIntoView({behavior: 'smooth', block: 'center'});
                addButton.click();
            }
        """)
        time.sleep(1)
        print("   ✅ Novo registro adicionado via JavaScript!")
    except Exception as e:
        print(f"   ⚠️ Erro ao adicionar registro: {e}")
    
    # 7. Localizar campo Ordem de Serviço
    print("\n7. Localizando campo Ordem de Serviço...")
    try:
        # Procurar por campos de ordem de serviço que NÃO sejam templates
        ordem_fields = driver.find_elements(By.CSS_SELECTOR, 'input[name*="ordem_servico"]:not([name*="__prefix__"])')
        if ordem_fields:
            ordem_field = ordem_fields[-1]  # Pegar o último (recém-adicionado)
            print(f"   ✅ Campo encontrado!")
            print(f"   - ID: {ordem_field.get_attribute('id')}")
            print(f"   - Name: {ordem_field.get_attribute('name')}")
            print(f"   - Valor inicial: '{ordem_field.get_attribute('value')}'")
            print(f"   - MaxLength: {ordem_field.get_attribute('maxlength')}")
        else:
            print("   ❌ Campo não encontrado!")
            driver.save_screenshot("test_aluno_campo_nao_encontrado.png")
            raise Exception("Campo ordem_servico não encontrado")
    except Exception as e:
        print(f"   ❌ Erro ao localizar campo: {e}")
        driver.save_screenshot("test_aluno_erro.png")
        raise
    
    # 8. Clicar no campo (focus) usando JavaScript
    print("\n8. Clicando no campo (focus)...")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ordem_field)
    time.sleep(0.5)
    driver.execute_script("arguments[0].focus();", ordem_field)
    time.sleep(0.5)
    
    # Capturar logs após focus
    print("\n   LOGS DO CONSOLE (após focus):")
    print("   " + "-" * 76)
    logs = driver.get_log('browser')
    for log in logs:
        if log['level'] in ['INFO', 'WARNING', 'SEVERE']:
            print(f"   [{log['level']}] {log['message']}")
    if not logs:
        print("   (nenhum log)")
    
    print(f"   Valor após focus: '{ordem_field.get_attribute('value')}'")
    
    # 9. Digitar sequência de teste via JavaScript
    print("\n9. Digitando '12345' (via JavaScript)...")
    driver.execute_script("""
        arguments[0].value = '12345';
        arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
        arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
    """, ordem_field)
    time.sleep(0.5)
    
    # Capturar logs após digitar
    print("\n   LOGS DO CONSOLE (após digitar):")
    print("   " + "-" * 76)
    logs = driver.get_log('browser')
    for log in logs:
        if log['level'] in ['INFO', 'WARNING', 'SEVERE']:
            print(f"   [{log['level']}] {log['message']}")
    if not logs:
        print("   (nenhum log)")
    
    valor_final = ordem_field.get_attribute('value')
    print(f"   Valor após '12345': '{valor_final}'")
    print(f"   Esperado: '12345'")
    print(f"   Match: {'✅' if valor_final == '12345' else '❌'}")
    
    # 10. Verificar propriedades do campo
    print("\n10. Verificando propriedades do campo...")
    info = {
        'disabled': ordem_field.get_attribute('disabled'),
        'readonly': ordem_field.get_attribute('readonly'),
        'type': ordem_field.get_attribute('type'),
        'value': ordem_field.get_attribute('value'),
        'maxlength': ordem_field.get_attribute('maxlength')
    }
    print(f"   Info do campo: {info}")
    
    # 11. Todos os logs do console (final)
    print("\n11. TODOS OS LOGS DO CONSOLE (final):")
    print("-" * 80)
    logs = driver.get_log('browser')
    if logs:
        for log in logs:
            print(f"   [{log['level']}] {log['message']}")
    else:
        print("   (nenhum log adicional)")
    
    # 12. Screenshot final
    screenshot_path = "e:/projetos/omaum/test_aluno_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"\n12. Screenshot salvo em: {screenshot_path}")
    
    print("\n" + "=" * 80)
    print("Teste concluído! Aguardando 10 segundos para você visualizar...")
    print("=" * 80)
    time.sleep(10)

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    
    screenshot_path = "test_aluno_erro.png"
    driver.save_screenshot(screenshot_path)
    print(f"\nScreenshot do erro salvo em: {screenshot_path}")

finally:
    print("\nFechando navegador...")
    driver.quit()
