################################################################################
# Script de Atualização Rápida - OMAUM (Sem Downtime)
# Para atualizações menores de código sem parar o sistema
# Autor: Sistema OMAUM
# Data: 2025-11-22
################################################################################

$ErrorActionPreference = "Stop"

$ProjectRoot = "c:\projetos\omaum"
$BackupDir = "$ProjectRoot\backups"
$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'

function Write-Info { 
    param($Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan 
}

function Write-Success { 
    param($Message)
    Write-Host "[OK] $Message" -ForegroundColor Green 
}

function Write-Warn { 
    param($Message)
    Write-Host "[AVISO] $Message" -ForegroundColor Yellow 
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  ATUALIZACAO RAPIDA - OMAUM (SEM DOWNTIME)" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Mudar para pasta do projeto
Set-Location $ProjectRoot

# 1. Backup rápido
Write-Info "1/4 - Fazendo backup rapido do banco..."
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}
docker exec omaum-db-prod pg_dump -U postgres omaum | Out-File -FilePath "$BackupDir\backup_$Timestamp.sql" -Encoding UTF8
Write-Success "Backup criado"

# 2. Reconstruir apenas o container web
Write-Info "2/4 - Reconstruindo container web..."
docker-compose up -d --build --no-deps web
Write-Success "Container web reconstruido"

# 3. Aguardar inicialização
Write-Info "3/4 - Aguardando inicializacao..."
Start-Sleep -Seconds 5

# 4. Verificar funcionamento
Write-Info "4/4 - Verificando funcionamento..."
docker-compose logs --tail=20 web

try {
    $response = Invoke-WebRequest -Uri "http://192.168.15.4" -UseBasicParsing -TimeoutSec 10
    Write-Success "Aplicacao respondendo: HTTP $($response.StatusCode)"
} catch {
    Write-Warn "Falha ao acessar aplicacao: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Success "ATUALIZACAO RAPIDA CONCLUIDA!"
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Info "Backup: $BackupDir\backup_$Timestamp.sql"
Write-Host ""
