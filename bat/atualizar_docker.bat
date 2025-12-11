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

pushd docker

echo 1. Parando containers (%TARGET_ENV%)...
docker compose %COMPOSE_ARGS% down
if errorlevel 1 goto :error
echo    [OK] Containers parados
echo.

echo 2. Reconstruindo imagens (%TARGET_ENV%)...
docker compose %COMPOSE_ARGS% build --no-cache
if errorlevel 1 goto :error
echo    [OK] Imagens reconstruidas
echo.

echo 3. Iniciando containers (%TARGET_ENV%)...
docker compose %COMPOSE_ARGS% up -d
if errorlevel 1 goto :error
echo    [OK] Containers iniciados
echo.

echo 4. Aguardando servicos ficarem prontos (30s)...
timeout /t 30 /nobreak > nul
echo.

echo 5. Aplicando migracoes...
docker compose %COMPOSE_ARGS% exec -T %WEB_SERVICE% python manage.py migrate --noinput
if errorlevel 1 goto :error
echo    [OK] Migracoes aplicadas
echo.

echo 6. Coletando arquivos estaticos...
docker compose %COMPOSE_ARGS% exec -T %WEB_SERVICE% python manage.py collectstatic --noinput
if errorlevel 1 goto :error
echo    [OK] Estaticos coletados
echo.

echo 7. Verificando status...
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo 8. Verificando versao do Django...
docker compose %COMPOSE_ARGS% exec -T %WEB_SERVICE% python -c "import django; print('Django:', django.get_version())"
if errorlevel 1 goto :error
echo.

echo 9. Abrir no navegador...
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

popd

echo ========================================
echo   ATUALIZACAO CONCLUIDA COM SUCESSO!
echo ========================================
echo.
echo O sistema esta acessivel em: %APP_URL%
echo Consulte os logs com:
echo   docker logs %WEB_CONTAINER%
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
