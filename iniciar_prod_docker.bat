@echo off
REM ============================================================================
REM OMAUM - Iniciar Ambiente de PRODUÇÃO
REM ============================================================================
REM ATENÇÃO: Este script inicia o ambiente de PRODUÇÃO com:
REM - Banco de dados: omaum_prod
REM - Porta: 8000 (direto) e 80 (Nginx)
REM - DEBUG: False
REM - Código: Copiado na imagem (não montado)
REM ============================================================================

setlocal EnableDelayedExpansion

echo ========================================
echo   OMAUM - AMBIENTE DE PRODUCAO
echo ========================================
echo.

REM Garante execução a partir da pasta do script
pushd "%~dp0" >nul

REM Verificar se desenvolvimento está rodando (INFORMATIVO apenas)
echo [1/5] Verificando conflitos...
docker ps --filter "name=omaum-dev-" --format "{{.Names}}" 2>nul | findstr "omaum-dev-" >nul
if %ERRORLEVEL% EQU 0 (
    echo    [INFO] Ambiente de DESENVOLVIMENTO esta rodando simultaneamente
    echo    [OK] Producao pode rodar junto - portas nao conflitam!
) else (
    echo    [OK] Nenhum outro ambiente detectado
)
echo.

REM Verificar arquivos necessários
echo [2/5] Verificando arquivos...
if not exist ".env.production" (
    echo    [ERRO] Arquivo .env.production nao encontrado!
    pause
    exit /b 1
)
if not exist "docker\docker-compose.yml" (
    echo    [ERRO] Arquivo docker-compose.yml nao encontrado!
    pause
    exit /b 1
)
if not exist "docker\docker-compose.prod.override.yml" (
    echo    [ERRO] Arquivo docker-compose.prod.override.yml nao encontrado!
    pause
    exit /b 1
)
echo    [OK] Arquivos encontrados
echo.

REM Verificar volumes
echo [3/5] Verificando volumes...
if not exist "D:\docker\omaum\prod\" (
    echo    [INFO] Criando diretorio D:\docker\omaum\prod\...
    mkdir "D:\docker\omaum\prod\" 2>nul
    mkdir "D:\docker\omaum\prod\db" 2>nul
    mkdir "D:\docker\omaum\prod\static" 2>nul
    mkdir "D:\docker\omaum\prod\staticfiles" 2>nul
    mkdir "D:\docker\omaum\prod\media" 2>nul
    mkdir "D:\docker\omaum\prod\logs" 2>nul
    mkdir "D:\docker\omaum\prod\redis" 2>nul
)
echo    [OK] Volumes prontos
echo.

REM Iniciar Docker
echo [4/5] Iniciando containers de PRODUCAO...
cd docker
docker compose --profile production -p omaum-prod --env-file ..\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml up -d

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo    [ERRO] Falha ao iniciar containers!
    echo    Verifique os logs:
    echo    docker compose -p omaum-prod logs
    pause
    exit /b 1
)
echo    [OK] Containers iniciados
echo.

REM Aguardar healthcheck
echo [5/5] Aguardando containers ficarem saudaveis...
timeout /t 5 /nobreak >nul

docker ps --filter "name=omaum-prod-" --format "{{.Names}}: {{.Status}}"
echo.

echo ========================================
echo   PRODUCAO INICIADA COM SUCESSO!
echo ========================================
echo.
echo Acesso:
echo   - Web (Nginx):  http://localhost
echo   - Web (Direto): http://localhost:8000
echo.
echo Portas Expostas:
echo   - PostgreSQL: localhost:5433
echo   - Redis: localhost:6380
echo.
echo [OK] Pode rodar junto com omaum-dev (porta 8001)!
echo.
echo Para parar:
echo   docker compose -p omaum-prod down
echo.

pause
exit /b 0
