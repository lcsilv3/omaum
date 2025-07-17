@echo off
REM Script de automação de testes para Windows
REM Executa o sistema completo de testes automatizados

echo 🤖 SISTEMA DE TESTES AUTOMATIZADOS - OMAUM
echo ==========================================

REM Verificar se Python está disponível
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado! Instale Python 3.9+ e tente novamente.
    pause
    exit /b 1
)

REM Definir diretório do projeto
set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

echo 📍 Diretório do projeto: %PROJECT_DIR%

REM Verificar argumentos
if "%1"=="--help" (
    echo.
    echo Uso: run_tests.bat [opções]
    echo.
    echo Opções:
    echo   --setup-only      Apenas configurar ambiente
    echo   --tests-only      Apenas executar testes
    echo   --coverage-only   Apenas análise de cobertura
    echo   --parallel        Executar testes em paralelo
    echo   --smoke           Executar apenas testes de fumaça
    echo   --help            Mostrar esta ajuda
    echo.
    pause
    exit /b 0
)

REM Executar automação baseada no argumento
if "%1"=="--setup-only" (
    echo 🔧 Configurando apenas o ambiente...
    python automate_tests.py --setup-only
    goto end
)

if "%1"=="--tests-only" (
    echo 🧪 Executando apenas os testes...
    python automate_tests.py --tests-only
    goto end
)

if "%1"=="--coverage-only" (
    echo 📊 Executando apenas análise de cobertura...
    python automate_tests.py --coverage-only
    goto end
)

if "%1"=="--parallel" (
    echo ⚡ Executando testes em paralelo...
    if exist "tests\run_parallel_tests.py" (
        python tests\run_parallel_tests.py
    ) else (
        echo ❌ Script de testes paralelos não encontrado!
        exit /b 1
    )
    goto end
)

if "%1"=="--smoke" (
    echo 🚨 Executando testes de fumaça...
    if exist "tests\run_parallel_tests.py" (
        python tests\run_parallel_tests.py --smoke
    ) else (
        echo ❌ Script de testes paralelos não encontrado!
        exit /b 1
    )
    goto end
)

REM Executar automação completa por padrão
echo 🚀 Executando automação completa...
python automate_tests.py

:end
if %errorlevel% equ 0 (
    echo.
    echo ✅ Automação concluída com sucesso!
    echo.
    echo 📋 Relatórios gerados:
    if exist "test_automation_report.json" echo   - test_automation_report.json
    if exist "relatorio_testes.json" echo   - relatorio_testes.json
    if exist "relatorio_testes.txt" echo   - relatorio_testes.txt
    if exist "coverage.json" echo   - coverage.json
    if exist "htmlcov\index.html" echo   - htmlcov\index.html
    echo.
    echo 🌐 Para ver o relatório de cobertura, abra: htmlcov\index.html
) else (
    echo.
    echo ❌ Automação falhou! Verifique os logs acima.
)

echo.
echo Pressione qualquer tecla para sair...
pause >nul
