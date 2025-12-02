@echo off
REM Script para atualizar o ambiente Docker de producao
REM Autor: GitHub Copilot
REM Data: 29/11/2025

echo ========================================
echo   ATUALIZACAO DOCKER - OMAUM PRODUCAO
echo ========================================
echo.

cd docker

echo 1. Parando containers...
docker-compose --env-file .env.production -f docker-compose.prod.yml down
echo    [OK] Containers parados
echo.

echo 2. Reconstruindo imagens...
docker-compose --env-file .env.production -f docker-compose.prod.yml build --no-cache
echo    [OK] Imagens reconstruidas
echo.

echo 3. Iniciando containers...
docker-compose --env-file .env.production -f docker-compose.prod.yml up -d
echo    [OK] Containers iniciados
echo.

echo 4. Aguardando servicos ficarem prontos (30s)...
timeout /t 30 /nobreak > nul
echo.

echo 5. Aplicando migracoes...
docker exec omaum-web-prod python manage.py migrate --noinput
echo    [OK] Migracoes aplicadas
echo.

echo 6. Coletando arquivos estaticos...
docker exec omaum-web-prod python manage.py collectstatic --noinput
echo    [OK] Estaticos coletados
echo.

echo 7. Verificando status...
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo 8. Verificando Django...
docker exec omaum-web-prod python -c "import django; print('Django:', django.get_version())"
echo.

echo ========================================
echo   ATUALIZACAO CONCLUIDA COM SUCESSO!
echo ========================================
echo.
echo O sistema esta acessivel em:
echo   http://192.168.15.4
echo   http://omaum.local
echo.
echo Para verificar logs:
echo   docker logs omaum-web-prod
echo.

pause
