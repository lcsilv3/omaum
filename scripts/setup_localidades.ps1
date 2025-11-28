# Script PowerShell para configurar sistema de localidades do OMAUM
# Baixa dados do IBGE e popula banco de dados

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SETUP DE LOCALIDADES - OMAUM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se estamos no diretório correto
if (-not (Test-Path "manage.py")) {
    Write-Host "ERRO: Execute este script da raiz do projeto OMAUM" -ForegroundColor Red
    exit 1
}

# Etapa 1: Baixar dados do IBGE
Write-Host "[1/4] Baixando dados de municípios do IBGE 2024..." -ForegroundColor Yellow
docker exec omaum-web-prod python scripts/baixar_ibge_dtb.py --ano 2024 --dest /app/docs/ibge_municipios.csv

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Falha ao baixar dados do IBGE" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dados do IBGE baixados com sucesso" -ForegroundColor Green
Write-Host ""

# Etapa 2: Verificar arquivo CSV
Write-Host "[2/4] Verificando arquivo CSV gerado..." -ForegroundColor Yellow
docker exec omaum-web-prod test -f /app/docs/ibge_municipios.csv

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Arquivo CSV não encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Arquivo CSV localizado" -ForegroundColor Green
Write-Host ""

# Etapa 3: Importar municípios (todos os estados)
Write-Host "[3/4] Importando municípios para o banco de dados..." -ForegroundColor Yellow
Write-Host "⏱️  Isso pode levar alguns minutos (5.570 municípios)..." -ForegroundColor Gray
docker exec omaum-web-prod python manage.py importar_municipios_ibge --csv /app/docs/ibge_municipios.csv

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Falha na importação de municípios" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Municípios importados com sucesso" -ForegroundColor Green
Write-Host ""

# Etapa 4: Verificar dados importados
Write-Host "[4/4] Verificando dados importados..." -ForegroundColor Yellow
docker exec omaum-web-prod python manage.py shell -c "from alunos.models import Pais, Estado, Cidade; print(f'Estados: {Estado.objects.count()}'); print(f'Cidades: {Cidade.objects.count()}')"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ✅ SETUP CONCLUÍDO COM SUCESSO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximo passo: Configurar filtro dinâmico no formulário" -ForegroundColor Yellow
