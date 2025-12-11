@echo off
REM Script para iniciar ambiente de DESENVOLVIMENTO Docker
REM Autor: GitHub Copilot
REM Atualizado em: 10/12/2025

echo ========================================
echo   AMBIENTE DE DESENVOLVIMENTO - OMAUM
echo ========================================
echo.

cd docker

echo 1. Verificando Docker...
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo    [ERRO] Docker nao esta instalado ou nao esta em execucao
    echo.
    echo    Por favor, inicie o Docker Desktop e tente novamente.
    pause
    exit /b 1
)
echo    [OK] Docker disponivel
echo.

set "COMPOSE_ARGS=-p omaum-dev --env-file ..\.env.dev -f docker-compose.yml -f docker-compose.dev.override.yml"

echo 2. Verificando ambiente de desenvolvimento...
set "DEV_RUNNING="
for /f "delims=" %%i in ('docker compose %COMPOSE_ARGS% ps -q 2^>nul') do set "DEV_RUNNING=1"
if defined DEV_RUNNING (
    echo    [OK] Containers ja estao rodando; nao vou parar.
) else (
    echo    [OK] Nenhum container em execucao; pronto para subir.
)
echo.

echo 3. Iniciando ambiente de DESENVOLVIMENTO (binds em E:)...
docker compose %COMPOSE_ARGS% up -d
if %ERRORLEVEL% NEQ 0 (
    echo    [ERRO] Falha ao iniciar containers
    pause
    exit /b 1
)
echo    [OK] Containers iniciados
echo.

echo 4. Aguardando servicos ficarem prontos (20s)...
timeout /t 20 /nobreak > nul
echo.

echo 5. Aplicando migracoes...
docker compose -p omaum-dev --env-file ..\.env.dev -f docker-compose.yml -f docker-compose.dev.override.yml exec -T omaum-web python manage.py migrate --noinput
echo    [OK] Migracoes aplicadas
echo.

echo 6. Verificando status...
docker compose -p omaum-dev --env-file ..\.env.dev -f docker-compose.yml -f docker-compose.dev.override.yml ps
echo.

set "APP_URL=http://localhost:8000"

echo 7. Abrir no navegador...
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
echo   AMBIENTE PRONTO!
echo ========================================
echo.
echo O ambiente de DESENVOLVIMENTO esta rodando em:
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

pause
