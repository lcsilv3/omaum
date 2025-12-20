@echo off
REM ============================================================================
REM OMAUM - Parar Todos os Ambientes Docker
REM ============================================================================
REM Este script para TODOS os containers do projeto OMAUM de forma segura
REM ============================================================================

setlocal EnableDelayedExpansion

echo ========================================
echo   OMAUM - PARAR AMBIENTES
echo ========================================
echo.

REM Verificar containers rodando
echo Verificando containers...
docker ps --filter "name=omaum-" --format "{{.Names}}" > temp_containers.txt

set "DEV_RUNNING=0"
set "PROD_RUNNING=0"

for /f "delims=" %%i in (temp_containers.txt) do (
    echo %%i | findstr "omaum-dev-" >nul && set "DEV_RUNNING=1"
    echo %%i | findstr "omaum-prod-" >nul && set "PROD_RUNNING=1"
)

del temp_containers.txt >nul 2>&1

if !DEV_RUNNING! EQU 0 if !PROD_RUNNING! EQU 0 (
    echo.
    echo [INFO] Nenhum container do OMAUM esta rodando.
    echo.
    pause
    exit /b 0
)

echo.
if !DEV_RUNNING! EQU 1 echo [!] Desenvolvimento (omaum-dev) esta rodando
if !PROD_RUNNING! EQU 1 echo [!] Producao (omaum-prod) esta rodando
echo.

REM Confirmar
set /p "CONFIRM=Deseja parar TODOS os ambientes? (S/N): "
if /i not "%CONFIRM%"=="S" (
    echo.
    echo Operacao cancelada.
    pause
    exit /b 0
)

echo.
echo Parando containers...
echo.

REM Parar desenvolvimento
if !DEV_RUNNING! EQU 1 (
    echo [1/2] Parando DESENVOLVIMENTO...
    cd docker
    docker compose -p omaum-dev down
    if %ERRORLEVEL% EQU 0 (
        echo    [OK] Desenvolvimento parado
    ) else (
        echo    [ERRO] Falha ao parar desenvolvimento
    )
    cd ..
    echo.
)

REM Parar produção
if !PROD_RUNNING! EQU 1 (
    echo [2/2] Parando PRODUCAO...
    cd docker
    docker compose -p omaum-prod down
    if %ERRORLEVEL% EQU 0 (
        echo    [OK] Producao parada
    ) else (
        echo    [ERRO] Falha ao parar producao
    )
    cd ..
    echo.
)

echo ========================================
echo   AMBIENTES PARADOS
echo ========================================
echo.
echo Verifique:
docker ps --filter "name=omaum-"
echo.

pause
exit /b 0
