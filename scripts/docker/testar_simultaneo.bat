@echo off
REM =============================================================================
REM OMAUM - Teste de Execução Simultânea
REM =============================================================================
REM Este script verifica se ambos os ambientes podem rodar simultaneamente
REM sem conflitos de portas ou recursos.
REM =============================================================================

setlocal EnableDelayedExpansion

echo ========================================
echo   TESTE DE EXECUCAO SIMULTANEA
echo ========================================
echo.

pushd "%~dp0" >nul

REM 1. Verificar portas disponíveis
echo [1/6] Verificando portas necessarias...

set "PORTAS_LIVRES=1"

REM Porta 8000 (Prod Web)
netstat -ano | findstr ":8000" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [AVISO] Porta 8000 em uso
    set "PORTAS_LIVRES=0"
)

REM Porta 8001 (Dev Web)
netstat -ano | findstr ":8001" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [AVISO] Porta 8001 em uso
    set "PORTAS_LIVRES=0"
)

REM Porta 80 (Nginx)
netstat -ano | findstr ":80 " >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [AVISO] Porta 80 em uso
    set "PORTAS_LIVRES=0"
)

REM Porta 5432 (Dev DB)
netstat -ano | findstr ":5432" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [AVISO] Porta 5432 em uso
    set "PORTAS_LIVRES=0"
)

REM Porta 5433 (Prod DB)
netstat -ano | findstr ":5433" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [AVISO] Porta 5433 em uso
    set "PORTAS_LIVRES=0"
)

REM Porta 6379 (Dev Redis)
netstat -ano | findstr ":6379" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [AVISO] Porta 6379 em uso
    set "PORTAS_LIVRES=0"
)

REM Porta 6380 (Prod Redis)
netstat -ano | findstr ":6380" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [AVISO] Porta 6380 em uso
    set "PORTAS_LIVRES=0"
)

if "%PORTAS_LIVRES%"=="1" (
    echo    [OK] Todas as portas necessarias estao livres
) else (
    echo    [INFO] Algumas portas em uso - containers existentes?
)
echo.

REM 2. Verificar containers em execução
echo [2/6] Verificando containers em execucao...

docker ps --filter "name=omaum-dev-" --format "{{.Names}}" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    docker ps --filter "name=omaum-dev-" --format "   [DEV] {{.Names}}: {{.Status}}"
)

docker ps --filter "name=omaum-prod-" --format "{{.Names}}" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    docker ps --filter "name=omaum-prod-" --format "   [PROD] {{.Names}}: {{.Status}}"
)
echo.

REM 3. Verificar arquivos de configuração
echo [3/6] Verificando arquivos de configuracao...

set "CONFIG_OK=1"

if not exist ".env.dev" (
    echo    [ERRO] .env.dev nao encontrado!
    set "CONFIG_OK=0"
) else (
    echo    [OK] .env.dev existe
)

if not exist ".env.production" (
    echo    [ERRO] .env.production nao encontrado!
    set "CONFIG_OK=0"
) else (
    echo    [OK] .env.production existe
)

if not exist "docker\docker-compose.yml" (
    echo    [ERRO] docker-compose.yml nao encontrado!
    set "CONFIG_OK=0"
) else (
    echo    [OK] docker-compose.yml existe
)

if not exist "docker\docker-compose.dev.override.yml" (
    echo    [ERRO] docker-compose.dev.override.yml nao encontrado!
    set "CONFIG_OK=0"
) else (
    echo    [OK] docker-compose.dev.override.yml existe
)

if not exist "docker\docker-compose.prod.override.yml" (
    echo    [ERRO] docker-compose.prod.override.yml nao encontrado!
    set "CONFIG_OK=0"
) else (
    echo    [OK] docker-compose.prod.override.yml existe
)
echo.

REM 4. Verificar volumes
echo [4/6] Verificando volumes (diretorios host)...

if not exist "E:\docker\omaum\dev\" (
    echo    [INFO] E:\docker\omaum\dev\ nao existe (sera criado)
) else (
    echo    [OK] E:\docker\omaum\dev\ existe
)

if not exist "D:\docker\omaum\prod\" (
    echo    [INFO] D:\docker\omaum\prod\ nao existe (sera criado)
) else (
    echo    [OK] D:\docker\omaum\prod\ existe
)
echo.

REM 5. Verificar COMPOSE_PROJECT_NAME
echo [5/6] Verificando COMPOSE_PROJECT_NAME...

findstr /C:"COMPOSE_PROJECT_NAME=omaum-dev" .env.dev >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [OK] .env.dev: COMPOSE_PROJECT_NAME=omaum-dev
) else (
    echo    [AVISO] .env.dev pode estar sem COMPOSE_PROJECT_NAME
)

findstr /C:"COMPOSE_PROJECT_NAME=omaum-prod" .env.production >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo    [OK] .env.production: COMPOSE_PROJECT_NAME=omaum-prod
) else (
    echo    [AVISO] .env.production pode estar sem COMPOSE_PROJECT_NAME
)
echo.

REM 6. Resumo
echo [6/6] RESUMO DA VALIDACAO
echo ========================================
if "%CONFIG_OK%"=="1" (
    echo Status: [OK] Configuracao valida
) else (
    echo Status: [ERRO] Configuracao incompleta
)

if "%PORTAS_LIVRES%"=="1" (
    echo Portas: [OK] Todas disponiveis
) else (
    echo Portas: [INFO] Algumas em uso (verifique acima)
)
echo ========================================
echo.

REM Sugestões
echo PROXIMOS PASSOS:
echo.
echo Para iniciar DESENVOLVIMENTO:
echo    iniciar_dev_docker.bat
echo.
echo Para iniciar PRODUCAO:
echo    iniciar_prod_docker.bat
echo.
echo Para parar AMBOS:
echo    parar_docker.bat
echo.
echo Para ver detalhes:
echo    docker ps
echo.

popd >nul
pause
