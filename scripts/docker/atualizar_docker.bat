@echo off
setlocal enabledelayedexpansion
REM Script para atualizar o ambiente Docker do OMAUM
REM Autor: GitHub Copilot
REM Atualizado em: 04/12/2025

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
	set COMPOSE_FILE=docker-compose.prod.yml
	set ENV_FILE=.env.production
	set PROJECT_NAME=omaum-prod
	set WEB_CONTAINER=omaum-web-prod
	set APP_URL=http://omaum.local
) else (
	set TARGET_ENV=DESENVOLVIMENTO
	set COMPOSE_FILE=docker-compose.yml
	set ENV_FILE=
	set PROJECT_NAME=omaum-dev
	set WEB_CONTAINER=omaum-web
	set APP_URL=http://localhost:8000
)

set ENV_ARGS=
if defined ENV_FILE set ENV_ARGS=--env-file %ENV_FILE%

echo Ambiente selecionado: %TARGET_ENV%
echo.

pushd docker

echo 1. Parando containers (%TARGET_ENV%)...
docker-compose %ENV_ARGS% -p %PROJECT_NAME% -f %COMPOSE_FILE% down
if errorlevel 1 goto :error
echo    [OK] Containers parados
echo.

echo 2. Reconstruindo imagens (%TARGET_ENV%)...
docker-compose %ENV_ARGS% -p %PROJECT_NAME% -f %COMPOSE_FILE% build --no-cache
if errorlevel 1 goto :error
echo    [OK] Imagens reconstruidas
echo.

echo 3. Iniciando containers (%TARGET_ENV%)...
docker-compose %ENV_ARGS% -p %PROJECT_NAME% -f %COMPOSE_FILE% up -d
if errorlevel 1 goto :error
echo    [OK] Containers iniciados
echo.

echo 4. Aguardando servicos ficarem prontos (30s)...
timeout /t 30 /nobreak > nul
echo.

echo 5. Aplicando migracoes...
docker exec %WEB_CONTAINER% python manage.py migrate --noinput
if errorlevel 1 goto :error
echo    [OK] Migracoes aplicadas
echo.

echo 6. Coletando arquivos estaticos...
docker exec %WEB_CONTAINER% python manage.py collectstatic --noinput
if errorlevel 1 goto :error
echo    [OK] Estaticos coletados
echo.

echo 7. Verificando status...
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo 8. Verificando versao do Django...
docker exec %WEB_CONTAINER% python -c "import django; print('Django:', django.get_version())"
if errorlevel 1 goto :error
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
