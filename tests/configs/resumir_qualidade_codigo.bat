:: Script para Windows - Retomar melhoria da qualidade do código
:: Baseado no checkpoint salvo

@echo off
setlocal enabledelayedexpansion

echo.
echo ===============================================
echo  RETOMANDO MELHORIA DA QUALIDADE DO CODIGO
echo ===============================================
echo.

:: Verificar se estamos no diretório correto
if not exist "manage.py" (
    echo ❌ Erro: Arquivo manage.py nao encontrado!
    echo Execute este script no diretorio raiz do projeto Django.
    pause
    exit /b 1
)

:: Verificar se checkpoint existe
if not exist "CHECKPOINT_QUALIDADE_CODIGO.md" (
    echo ❌ Erro: Arquivo CHECKPOINT_QUALIDADE_CODIGO.md nao encontrado!
    echo Execute a tarefa de melhoria primeiro.
    pause
    exit /b 1
)

:: Mostrar status atual
echo 📊 Status atual:
echo.
echo 🔍 Verificando Django...
python manage.py check
if %errorlevel% neq 0 (
    echo ❌ Django nao esta funcionando!
    pause
    exit /b 1
)
echo ✅ Django OK

echo.
echo 🔍 Estatisticas do ruff:
C:\projetos\omaum\.venv\Scripts\python.exe -m ruff check --statistics .

echo.
echo ===============================================
echo  OPCOES DISPONIVEIS:
echo ===============================================
echo.
echo [1] Aplicar correcoes automaticas seguras
echo [2] Aplicar correcoes automaticas + nao seguras
echo [3] Apenas mostrar relatorio detalhado
echo [4] Verificar arquivos especificos
echo [5] Sair
echo.

set /p choice="Escolha uma opcao (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🔧 Aplicando correcoes automaticas seguras...
    C:\projetos\omaum\.venv\Scripts\python.exe -m ruff check --fix .
    
    echo.
    echo 🔍 Verificando Django apos correcoes...
    python manage.py check
    if %errorlevel% neq 0 (
        echo ❌ Django quebrou apos correcoes!
        pause
        exit /b 1
    )
    
    echo.
    echo 📊 Estatisticas apos correcoes:
    C:\projetos\omaum\.venv\Scripts\python.exe -m ruff check --statistics .
    echo.
    echo ✅ Correcoes aplicadas com sucesso!
    
) else if "%choice%"=="2" (
    echo.
    echo 🔧 Aplicando correcoes automaticas + nao seguras...
    C:\projetos\omaum\.venv\Scripts\python.exe -m ruff check --fix --unsafe-fixes .
    
    echo.
    echo 🔍 Verificando Django apos correcoes...
    python manage.py check
    if %errorlevel% neq 0 (
        echo ❌ Django quebrou apos correcoes!
        pause
        exit /b 1
    )
    
    echo.
    echo 📊 Estatisticas apos correcoes:
    C:\projetos\omaum\.venv\Scripts\python.exe -m ruff check --statistics .
    echo.
    echo ✅ Correcoes aplicadas com sucesso!
    
) else if "%choice%"=="3" (
    echo.
    echo 📋 Relatorio detalhado por categoria:
    echo.
    echo 🔍 F401 - Imports nao utilizados:
    C:\projetos\omaum\.venv\Scripts\python.exe -m ruff check --select F401 . | head -10
    echo.
    echo 🔍 E402 - Imports nao no topo:
    C:\projetos\omaum\.venv\Scripts\python.exe -m ruff check --select E402 . | head -10
    echo.
    echo 🔍 F405 - Star imports:
    C:\projetos\omaum\.venv\Scripts\python.exe -m ruff check --select F405 . | head -10
    echo.
    echo 🔍 F403 - Star imports undefined:
    C:\projetos\omaum\.venv\Scripts\python.exe -m ruff check --select F403 . | head -10
    echo.
    echo 🔍 F811 - Redefinicoes:
    C:\projetos\omaum\.venv\Scripts\python.exe -m ruff check --select F811 . | head -10
    
) else if "%choice%"=="4" (
    echo.
    set /p filepath="Digite o caminho do arquivo (ex: alunos/views/__init__.py): "
    echo.
    echo 🔍 Verificando arquivo: !filepath!
    C:\projetos\omaum\.venv\Scripts\python.exe -m ruff check "!filepath!"
    
) else if "%choice%"=="5" (
    echo.
    echo 👋 Ate logo!
    exit /b 0
    
) else (
    echo.
    echo ❌ Opcao invalida!
    pause
    exit /b 1
)

echo.
echo ===============================================
echo  PROXIMOS PASSOS RECOMENDADOS:
echo ===============================================
echo.
echo 1. Revisar arquivos modificados
echo 2. Executar testes: python manage.py test
echo 3. Verificar funcionalidade: python manage.py runserver
echo 4. Continuar com correcoes manuais se necessario
echo.
echo 💡 Para detalhes completos, consulte: CHECKPOINT_QUALIDADE_CODIGO.md
echo.

pause
