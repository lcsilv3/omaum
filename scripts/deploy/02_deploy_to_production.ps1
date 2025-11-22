################################################################################
# Script de Deploy Zero-Downtime para Produção (PowerShell)
# Autor: Sistema OMAUM
# Data: 2025-11-22
################################################################################

$ErrorActionPreference = "Stop"

# Configurações
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Get-Item $ScriptDir).Parent.Parent.FullName
$DockerDir = Join-Path $ProjectRoot "docker"
$BackupDir = Join-Path $ProjectRoot "backups\$(Get-Date -Format 'yyyyMMdd_HHmmss')"
$ComposeFile = Join-Path $DockerDir "docker-compose.prod.yml"
$EnvFile = Join-Path $DockerDir ".env.production"

# Funções auxiliares
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

function Write-Err { 
    param($Message)
    Write-Host "[ERRO] $Message" -ForegroundColor Red 
}

# Verificar pré-requisitos
function Test-Prerequisites {
    Write-Info "Verificando pre-requisitos..."
    
    if (!(Test-Path $ComposeFile)) {
        Write-Err "Arquivo docker-compose.prod.yml nao encontrado!"
        exit 1
    }
    
    if (!(Test-Path $EnvFile)) {
        Write-Err "Arquivo .env.production nao encontrado!"
        exit 1
    }
    
    if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Err "Docker nao esta instalado!"
        exit 1
    }
    
    if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
        Write-Err "Docker Compose nao esta instalado!"
        exit 1
    }
    
    Write-Success "Pre-requisitos verificados"
}

# Criar backup do banco
function Backup-Database {
    Write-Info "Criando backup do banco de dados de producao..."
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    
    $backupFile = Join-Path $BackupDir "db_backup.sql"
    
    Push-Location $DockerDir
    docker-compose -f docker-compose.prod.yml --env-file .env.production exec -T omaum-db `
        pg_dump -U $env:POSTGRES_USER -d $env:POSTGRES_DB | Out-File -FilePath $backupFile -Encoding UTF8
    Pop-Location
    
    if (Test-Path $backupFile) {
        $sizeKB = [math]::Round((Get-Item $backupFile).Length / 1KB, 2)
        Write-Success "Backup criado: $backupFile ($sizeKB KB)"
    } else {
        Write-Err "Falha ao criar backup!"
        exit 1
    }
}

# Build de imagens
function Build-Images {
    Write-Info "Construindo novas imagens Docker..."
    
    Push-Location $DockerDir
    docker-compose -f docker-compose.prod.yml --env-file .env.production build --pull
    Pop-Location
    
    Write-Success "Imagens construidas com sucesso"
}

# Importar dados
function Import-DevData {
    Write-Info "Importando dados de desenvolvimento..."
    
    # Encontrar arquivo de export mais recente
    $exportDir = Join-Path $ScriptDir "exports"
    $exportFile = Get-ChildItem -Path $exportDir -Filter "dev_data_*.json" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
    
    if (!$exportFile) {
        Write-Err "Nenhum arquivo de exportacao encontrado!"
        Write-Err "Execute primeiro: python scripts/deploy/01_export_dev_data.py"
        exit 1
    }
    
    Write-Info "Usando arquivo: $($exportFile.FullName)"
    
    # Copiar para container
    docker cp $exportFile.FullName omaum-web-prod:/tmp/dev_data.json
    
    # Limpar banco
    Write-Warn "Limpando banco de dados atual..."
    Push-Location $DockerDir
    docker-compose -f docker-compose.prod.yml --env-file .env.production exec -T omaum-web `
        python manage.py flush --no-input
    
    # Importar dados
    Write-Info "Importando dados..."
    docker-compose -f docker-compose.prod.yml --env-file .env.production exec -T omaum-web `
        python manage.py loaddata /tmp/dev_data.json
    Pop-Location
    
    Write-Success "Dados importados com sucesso"
}

# Aplicar migrações
function Apply-Migrations {
    Write-Info "Aplicando migracoes do banco de dados..."
    
    Push-Location $DockerDir
    docker-compose -f docker-compose.prod.yml --env-file .env.production exec -T omaum-web `
        python manage.py migrate --no-input
    Pop-Location
    
    Write-Success "Migracoes aplicadas"
}

# Coletar estáticos
function Collect-Static {
    Write-Info "Coletando arquivos estaticos..."
    
    Push-Location $DockerDir
    docker-compose -f docker-compose.prod.yml --env-file .env.production exec -T omaum-web `
        python manage.py collectstatic --no-input --clear
    Pop-Location
    
    Write-Success "Arquivos estaticos coletados"
}

# Rolling restart
function Start-RollingRestart {
    Write-Info "Iniciando rolling restart dos servicos..."
    
    Push-Location $DockerDir
    
    $services = @("omaum-celery-beat", "omaum-celery", "omaum-web")
    
    foreach ($service in $services) {
        Write-Info "Reiniciando $service..."
        
        # Escalar para 2 instâncias
        $scaleCmd = "docker-compose -f docker-compose.prod.yml --env-file .env.production up -d --no-deps --scale $service=2 $service"
        Invoke-Expression $scaleCmd
        Start-Sleep -Seconds 10
        
        # Voltar para 1 instância
        $scaleCmd = "docker-compose -f docker-compose.prod.yml --env-file .env.production up -d --no-deps --scale $service=1 $service"
        Invoke-Expression $scaleCmd
        
        Write-Success "$service reiniciado"
    }
    
    # Recarregar nginx
    docker-compose -f docker-compose.prod.yml --env-file .env.production exec omaum-nginx nginx -s reload
    
    Pop-Location
    
    Write-Success "Rolling restart concluido"
}

# Health check
function Test-Health {
    Write-Info "Verificando saude dos servicos..."
    
    Start-Sleep -Seconds 5
    
    Push-Location $DockerDir
    docker-compose -f docker-compose.prod.yml --env-file .env.production ps
    
    Write-Info "Ultimas linhas dos logs:"
    docker-compose -f docker-compose.prod.yml --env-file .env.production logs --tail=20 omaum-web
    Pop-Location
    
    Write-Success "Verificacao de saude concluida"
}

# Smoke tests
function Invoke-SmokeTests {
    Write-Info "Executando smoke tests..."
    
    # Health check HTTP
    try {
        $response = Invoke-WebRequest -Uri "http://localhost/health/" -UseBasicParsing -TimeoutSec 10
        Write-Success "Health check: OK"
    } catch {
        Write-Err "Health check: FALHOU"
        return
    }
    
    # Verificar dados
    Push-Location $DockerDir
    $shellCmd = 'from turmas.models import Turma; print(Turma.objects.count())'
    $turmasCount = docker-compose -f docker-compose.prod.yml --env-file .env.production exec -T omaum-web python manage.py shell -c $shellCmd
    Pop-Location
    
    Write-Info "Turmas no banco: $turmasCount"
    
    if ([int]$turmasCount -gt 0) {
        Write-Success "Dados verificados: OK"
    } else {
        Write-Warn "Nenhuma turma encontrada no banco"
    }
    
    Write-Success "Smoke tests concluidos"
}

# Função principal
function Main {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "  DEPLOY ZERO-DOWNTIME - OMAUM PRODUCAO" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Confirmação
    $confirm = Read-Host "Iniciar deploy para producao? (y/N)"
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
        Write-Warn "Deploy cancelado pelo usuario"
        exit 0
    }
    
    # Executar etapas
    try {
        Test-Prerequisites
        Backup-Database
        Build-Images
        Import-DevData
        Apply-Migrations
        Collect-Static
        Start-RollingRestart
        Test-Health
        Invoke-SmokeTests
        
        Write-Host ""
        Write-Host "================================================================" -ForegroundColor Green
        Write-Success "DEPLOY CONCLUIDO COM SUCESSO!"
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host ""
        Write-Info "Backup salvo em: $BackupDir"
        Write-Host ""
    } catch {
        Write-Err "Erro durante deploy: $($_.Exception.Message)"
        Write-Host $_.ScriptStackTrace -ForegroundColor Red
        exit 1
    }
}

# Executar
Main
