@echo off
setlocal enabledelayedexpansion
REM Script para atualizar o ambiente Docker do OMAUM
REM Autor: GitHub Copilot
REM Atualizado em: 10/12/2025

echo ========================================
echo   ATUALIZACAO DOCKER - OMAUM
echo ========================================
echo.
echo Selecione o ambiente-alvo:
echo   [D] Desenvolvimento
echo   [P] Producao
choice /C DP /M "Escolha uma opcao"
if errorlevel 2 (
    set TARGET_ENV=PRODUCAO
    set COMPOSE_ARGS=-p omaum-prod --env-file ..\.env.prod -f docker-compose.yml -f docker-compose.prod.override.yml
    set WEB_SERVICE=omaum-web
    set APP_URL=http://omaum.local
) else (
    set TARGET_ENV=DESENVOLVIMENTO
    set COMPOSE_ARGS=-p omaum-dev --env-file ..\.env.dev -f docker-compose.yml -f docker-compose.dev.override.yml
    set WEB_SERVICE=omaum-web
    set APP_URL=http://localhost:8000
)

echo Ambiente selecionado: %TARGET_ENV%
echo.

pushd "%~dp0..\docker"

set "STARTED_NEW=0"
set "BUILD_FLAG="

echo 1. Verificando ambiente (%TARGET_ENV%)...
set "ENV_RUNNING="
for /f "delims=" %%i in ('docker compose %COMPOSE_ARGS% ps -q 2^>nul') do set "ENV_RUNNING=1"
if defined ENV_RUNNING (
    echo    [OK] Containers em execucao.
    set "RECREATE_CHOICE="
    set /p RECREATE_CHOICE="Deseja parar e recriar (down/up)? [S/N] (padrao=N): "
    if /I "!RECREATE_CHOICE!"=="S" (
        echo    Parando containers...
        docker compose %COMPOSE_ARGS% down
        if errorlevel 1 goto :error
        set "RECREATE_BUILD_CHOICE="
        set /p RECREATE_BUILD_CHOICE="Reconstruir imagens (--no-cache)? [S/N] (padrao=N): "
        if /I "!RECREATE_BUILD_CHOICE!"=="S" (
            set "BUILD_FLAG=--build --no-cache"
        )
        echo    Subindo containers...
        docker compose %COMPOSE_ARGS% up -d %BUILD_FLAG%
        if errorlevel 1 goto :error
        set "STARTED_NEW=1"
        echo    [OK] Containers recriados
    ) else (
        echo    Mantendo containers atuais.
    )
) else (
    echo    [OK] Containers nao estao rodando; iniciando...
    set "RECREATE_BUILD_CHOICE="
    set /p RECREATE_BUILD_CHOICE="Reconstruir imagens (--no-cache)? [S/N] (padrao=N): "
    if /I "!RECREATE_BUILD_CHOICE!"=="S" (
        set "BUILD_FLAG=--build --no-cache"
    )
    echo    Subindo containers...
    docker compose %COMPOSE_ARGS% up -d %BUILD_FLAG%
    if errorlevel 1 goto :error
    set "STARTED_NEW=1"
    echo    [OK] Containers iniciados
)
echo.

echo 2. Aguardando servicos ficarem prontos (30s)...
timeout /t 30 /nobreak > nul
echo.

set "MIGRATE_DEFAULT=N"
if "%STARTED_NEW%"=="1" set "MIGRATE_DEFAULT=S"
set "MIGRATE_CHOICE="
set /p MIGRATE_CHOICE="Aplicar migracoes agora? [S/N] (padrao=%MIGRATE_DEFAULT%): "
if "!MIGRATE_CHOICE!"=="" set "MIGRATE_CHOICE=!MIGRATE_DEFAULT!"
if /I "!MIGRATE_CHOICE!"=="S" (
    echo 3. Aplicando migracoes...
    docker compose %COMPOSE_ARGS% exec -T %WEB_SERVICE% python manage.py migrate --noinput
    if errorlevel 1 goto :error
    echo    [OK] Migracoes aplicadas
    echo.
) else (
    echo 3. Migracoes ignoradas a pedido do usuario.
    echo.
)

set "COLLECT_DEFAULT=N"
if "%STARTED_NEW%"=="1" set "COLLECT_DEFAULT=S"
set "COLLECT_CHOICE="
set /p COLLECT_CHOICE="Coletar estaticos agora? [S/N] (padrao=%COLLECT_DEFAULT%): "
if "!COLLECT_CHOICE!"=="" set "COLLECT_CHOICE=!COLLECT_DEFAULT!"
if /I "!COLLECT_CHOICE!"=="S" (
    echo 4. Coletando arquivos estaticos...
    docker compose %COMPOSE_ARGS% exec -T %WEB_SERVICE% python manage.py collectstatic --noinput
    if errorlevel 1 goto :error
    echo    [OK] Estaticos coletados
    echo.
) else (
    echo 4. Coleta de estaticos ignorada a pedido do usuario.
    echo.
)

echo 5. Verificando status...
docker compose %COMPOSE_ARGS% ps
echo.

echo 6. Verificando versao do Django...
docker compose %COMPOSE_ARGS% exec -T %WEB_SERVICE% python -c "import django; print('Django:', django.get_version())"
if errorlevel 1 goto :error
echo.

echo 7. Abrir no navegador...
set "BROWSER_CHOICE="
set /p BROWSER_CHOICE="Escolha navegador [1=Edge, 2=Chrome, 3=Firefox] (padrao=Edge): "
if "!BROWSER_CHOICE!"=="2" (
    start "" chrome "%APP_URL%"
    goto abrir_fim
)
if "!BROWSER_CHOICE!"=="3" (
    start "" firefox "%APP_URL%"
    goto abrir_fim
)
start "" msedge "%APP_URL%"
:abrir_fim
echo    [OK] Navegador acionado (fallback Edge se nao escolhido).
echo.

popd

echo ========================================
echo   ATUALIZACAO CONCLUIDA COM SUCESSO!
echo ========================================
echo.
echo O sistema esta acessivel em: %APP_URL%
echo Consulte os logs com:
echo   docker compose %COMPOSE_ARGS% logs %WEB_SERVICE%
echo.
goto :fim

:error
echo.
echo ========================================
echo   ERRO DURANTE A ATUALIZACAO!
echo ========================================
echo Verifique as mensagens acima para detalhes.

popd >nul 2>&1

:fim
pause
