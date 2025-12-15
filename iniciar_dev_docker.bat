@echo off
REM Manter janela aberta mesmo apos finalizar
setlocal EnableDelayedExpansion
REM Script para iniciar ambiente de DESENVOLVIMENTO Docker
REM Autor: GitHub Copilot
REM Atualizado em: 10/12/2025

echo ========================================
echo   OMAUM - AMBIENTE DOCKER
echo ========================================
echo.

REM Evita fechamento abrupto quando chamado via atalho (.lnk)
set "_was_called_via_double_click=1"
if defined PROMPT set "_was_called_via_double_click="

REM Garante execucao a partir da pasta do script
pushd "%~dp0" >nul

REM Configuracoes auxiliares
set "DOCKER_DESKTOP_EXE=C:\Program Files\Docker\Docker\Docker Desktop.exe"
set "DOCKER_RETRY=20"
set "ENV_SELECTED=dev"
set "COMPOSE_FILES="
set "ENV_FILE="
set "PROJECT_NAME=omaum-dev"
set "PROFILE_OPT="

REM 0. Garantir WSL e Docker Desktop em modo WSL2 (similar ao atalho .lnk)
echo 0. Verificando WSL...
wsl -l -v >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo    [INFO] Inicializando WSL...
    wsl -e /bin/true >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo    [ERRO] WSL nao respondeu. Abra o Docker Desktop manualmente ou configure o WSL.
        pause
        exit /b 1
    )
)
echo    [OK] WSL disponivel
echo.

echo 1. Verificando Docker Desktop...
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    if exist "%DOCKER_DESKTOP_EXE%" (
        echo    [INFO] Iniciando Docker Desktop...
        start "" "%DOCKER_DESKTOP_EXE%"
    ) else (
        echo    [ERRO] Docker Desktop nao encontrado em:
        echo          %DOCKER_DESKTOP_EXE%
        echo          Ajuste o caminho no script e tente novamente.
        pause
        exit /b 1
    )

    set "_docker_try=0"
:_wait_docker
    timeout /t 3 /nobreak >nul
    docker info >nul 2>&1
    if !ERRORLEVEL! EQU 0 goto _docker_ok
    set /a _docker_try+=1
    if !_docker_try! GEQ !DOCKER_RETRY! (
        echo    [ERRO] Docker Desktop nao ficou pronto a tempo. Abra manualmente e repita.
        pause
        exit /b 1
    )
    goto _wait_docker
)
:_docker_ok
echo    [OK] Docker pronto
echo.

REM Move para pasta docker relativa ao repo
if not exist "docker" (
    echo [ERRO] Nao encontrei a pasta 'docker' em %cd%.
    echo        Rode este atalho a partir da raiz do projeto.
    popd >nul
    if defined _was_called_via_double_click pause
    exit /b 1
)
cd docker

REM Escolha de ambiente (Dev/Prod local)
echo Ambiente alvo?
set /p ENV_SELECTED="[1=Desenvolvimento, 2=Producao] (padrao=1): "
REM Normaliza entrada
set "ENV_SELECTED=!ENV_SELECTED: =!"
set "ENV_SELECTED=!ENV_SELECTED:"=!"
set "_env_lower=!ENV_SELECTED!"
for %%A in (!ENV_SELECTED!) do set "_env_lower=%%A"
set "_env_lower=!_env_lower:~0,50!"
for %%A in (!ENV_SELECTED!) do set "_env_lower=!_env_lower!"
set "_env_lower=!_env_lower:PRODUCAO=producao!"
set "_env_lower=!_env_lower:Producao=producao!"
set "_env_lower=!_env_lower:producao=producao!"
set "_env_lower=!_env_lower:P=producao!"
set "_env_lower=!_env_lower:p=producao!"
if "!_env_lower!"=="" set "_env_lower=1"
if "!_env_lower!"=="2" set "_env_lower=producao"
if not "!_env_lower:2=!"=="!_env_lower!" set "_env_lower=producao"

if /I "!_env_lower!"=="producao" (
    set "ENV_SELECTED=prod"
) else (
    set "ENV_SELECTED=dev"
)
echo    [INFO] Ambiente escolhido: %ENV_SELECTED%
echo.

if "%ENV_SELECTED%"=="prod" (
    set "PROJECT_NAME=omaum-prod"
    set "ENV_FILE=..\.env.production"
    set "PROFILE_OPT=--profile production"
    if not exist "%ENV_FILE%" (
        if exist "..\.env" (
            set "ENV_FILE=..\.env"
            echo    [INFO] .env.production nao encontrado. Usando .env.
        ) else (
            echo    [ERRO] Nao encontrei .env.production nem .env na raiz do projeto.
            popd >nul
            if defined _was_called_via_double_click pause
            exit /b 1
        )
    )
    if exist "docker-compose.prod.override.yml" (
        set "COMPOSE_FILES=-f docker-compose.yml -f docker-compose.prod.override.yml"
    ) else (
        set "COMPOSE_FILES=-f docker-compose.yml"
    )
) else (
    set "PROJECT_NAME=omaum-dev"
    set "ENV_FILE=..\.env.dev"
    set "PROFILE_OPT="
    if not exist "%ENV_FILE%" (
        if exist "..\.env" (
            set "ENV_FILE=..\.env"
            echo    [INFO] Arquivo .env.dev nao encontrado. Usando .env.
        ) else (
            echo    [ERRO] Nao encontrei .env.dev nem .env na raiz do projeto.
            popd >nul
            if defined _was_called_via_double_click pause
            exit /b 1
        )
    )
    if exist "docker-compose.dev.override.yml" (
        set "COMPOSE_FILES=-f docker-compose.yml -f docker-compose.dev.override.yml"
    ) else (
        set "COMPOSE_FILES=-f docker-compose.yml"
    )
)

set "COMPOSE_ARGS=-p %PROJECT_NAME% --env-file %ENV_FILE% %COMPOSE_FILES%"
set "STARTED_NEW=0"
set "APP_URL=http://localhost:8000"
if "%ENV_SELECTED%"=="prod" (
    set "APP_URL=http://localhost"
)
set "MIGRATE_LOG=%TEMP%\omaum_migrate.log"

echo 2. Verificando ambiente (%ENV_SELECTED%)...
set "DEV_RUNNING="
set "_PS_TMP=%TEMP%\omaum_ps.tmp"
docker compose %PROFILE_OPT% %COMPOSE_ARGS% ps -q 1>"%_PS_TMP%" 2>nul
if errorlevel 1 (
    echo    [ERRO] Falha ao listar containers. Comando usado:
    echo           docker compose %PROFILE_OPT% %COMPOSE_ARGS% ps -q
    del "%_PS_TMP%" 2>nul
    pause
    exit /b 1
)
if exist "%_PS_TMP%" for %%F in ("%_PS_TMP%") do if %%~zF GTR 0 set "DEV_RUNNING=1"
del "%_PS_TMP%" 2>nul

if defined DEV_RUNNING goto :ENV_RUNNING
goto :ENV_START

:ENV_RUNNING
echo    [OK] Containers ja estao rodando.
set "RESTART_CHOICE="
set /p RESTART_CHOICE="Deseja reiniciar (down/up)? [S/N] (padrao=N): "
if /I "%RESTART_CHOICE%"=="S" goto :RESTART_CONTAINERS
goto :KEEP_RUNNING

:RESTART_CONTAINERS
echo    Reiniciando containers...
docker compose %PROFILE_OPT% %COMPOSE_ARGS% down
if errorlevel 1 (
    echo    [ERRO] Falha ao derrubar containers
    pause
    exit /b 1
)
docker compose %PROFILE_OPT% %COMPOSE_ARGS% up -d
if errorlevel 1 (
    echo    [ERRO] Falha ao iniciar containers
    pause
    exit /b 1
)
set "STARTED_NEW=1"
echo    [OK] Containers reiniciados
echo.
goto :AFTER_ENV

:KEEP_RUNNING
echo    Mantendo containers atuais.
if "%ENV_SELECTED%"=="prod" (
    set "NGINX_PRESENT="
    set "_PS_TMP=%TEMP%\omaum_ps_services.tmp"
    docker compose %PROFILE_OPT% %COMPOSE_ARGS% ps --services 1>"%_PS_TMP%" 2>nul
    if not errorlevel 1 (
        findstr /I "omaum-nginx" "%_PS_TMP%" >nul && set "NGINX_PRESENT=1"
    )
    del "%_PS_TMP%" 2>nul
    if not defined NGINX_PRESENT (
        echo    [INFO] nginx (profile production) nao estava rodando; iniciando...
        docker compose %PROFILE_OPT% %COMPOSE_ARGS% up -d omaum-nginx
        if errorlevel 1 (
            echo    [ERRO] Falha ao iniciar nginx
            pause
            exit /b 1
        )
    )
)
echo.
goto :AFTER_ENV

:ENV_START
echo    [OK] Nenhum container em execucao; iniciando...
docker compose %PROFILE_OPT% %COMPOSE_ARGS% up -d
if errorlevel 1 (
    echo    [ERRO] Falha ao iniciar containers
    pause
    exit /b 1
)
set "STARTED_NEW=1"
echo    [OK] Containers iniciados
goto :AFTER_ENV

:AFTER_ENV

echo 3. Aguardando servicos ficarem prontos (20s)...
timeout /t 20 /nobreak > nul
echo.

set "MIGRATE_DEFAULT=N"
if "%STARTED_NEW%"=="1" set "MIGRATE_DEFAULT=S"
set "MIGRATE_CHOICE="
set /p MIGRATE_CHOICE="Aplicar migracoes agora? [S/N] (padrao=%MIGRATE_DEFAULT%): "
if "%MIGRATE_CHOICE%"=="" set "MIGRATE_CHOICE=%MIGRATE_DEFAULT%"
if /I "%MIGRATE_CHOICE%"=="S" (
    echo 4. Verificando migracoes pendentes...
    del "%MIGRATE_LOG%" 2>nul
    docker compose %PROFILE_OPT% %COMPOSE_ARGS% exec -T omaum-web python manage.py migrate --check --noinput 1>"%MIGRATE_LOG%" 2>&1
    if errorlevel 1 (
        echo    [INFO] Migracoes pendentes detectadas. Aplicando...
        docker compose %PROFILE_OPT% %COMPOSE_ARGS% exec -T omaum-web python manage.py migrate --noinput 1>"%MIGRATE_LOG%" 2>&1
        if errorlevel 1 (
            echo    [ERRO] Falha ao aplicar migracoes. Detalhes:
            type "%MIGRATE_LOG%"
            pause
            exit /b 1
        )
        echo    [OK] Migracoes aplicadas
        del "%MIGRATE_LOG%" 2>nul
        echo.
    ) else (
        echo    [OK] Nenhuma migracao pendente; nada a aplicar.
        del "%MIGRATE_LOG%" 2>nul
        echo.
    )
) else (
    echo 4. Migracoes ignoradas a pedido do usuario.
    echo.
)

echo 5. Verificando status (%ENV_SELECTED%)...
docker compose %PROFILE_OPT% %COMPOSE_ARGS% ps
echo.

echo 6. Abrir no navegador...
set "BROWSER_CHOICE="
set /p BROWSER_CHOICE="Escolha navegador [1=Edge, 2=Chrome, 3=Firefox] (padrao=Edge): "
if "%BROWSER_CHOICE%"=="2" (
    start "" chrome "%APP_URL%"
    goto abrir_fim
)
if "%BROWSER_CHOICE%"=="3" (
    start "" firefox "%APP_URL%"
    goto abrir_fim
)
start "" msedge "%APP_URL%"
:abrir_fim
echo    [OK] Navegador acionado (fallback Edge se nao escolhido).
echo.

echo ========================================
echo   AMBIENTE PRONTO (%ENV_SELECTED%)
echo ========================================
echo.
echo O ambiente selecionado esta rodando em:
echo   %APP_URL%
echo.
echo Caracteristicas:
echo   - Debug ATIVO
echo   - Hot Reload ATIVO (codigo atualiza automaticamente)
echo   - PostgreSQL: localhost:5432 (usuario: omaum_user, senha: omaum_password)
echo   - Redis: localhost:6379
echo.
echo Comandos uteis:
echo   Ver logs:        docker-compose logs -f
echo   Parar:           docker-compose down
echo   Reiniciar:       docker-compose restart
echo   Shell:           docker-compose exec web bash
echo   Django shell:    docker-compose exec web python manage.py shell
echo.
popd >nul
pause

