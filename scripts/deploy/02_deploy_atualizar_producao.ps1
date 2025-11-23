################################################################################
# Script de Atualização de Produção - OMAUM (Windows)
# EXECUTAR NO SERVIDOR DE PRODUCAO: DESKTOP-OAE3R5M (192.168.15.4)
# Containers: omaum-*-prod
# Autor: Sistema OMAUM
# Data: 2025-11-22
################################################################################

param(
    [switch]$SemBackup,
    [switch]$SemDados,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# IMPORTANTE: Este script deve ser executado no SERVIDOR DE PRODUCAO
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host "VERIFICANDO AMBIENTE DE EXECUCAO..." -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host "Maquina Atual: $env:COMPUTERNAME" -ForegroundColor White
Write-Host "Usuario: $env:USERNAME" -ForegroundColor White
Write-Host ""

if ($env:COMPUTERNAME -ne "DESKTOP-OAE3R5M") {
    Write-Host "AVISO: Este script deve ser executado no servidor de producao!" -ForegroundColor Red
    Write-Host "Servidor esperado: DESKTOP-OAE3R5M" -ForegroundColor Red
    Write-Host "Servidor atual: $env:COMPUTERNAME" -ForegroundColor Red
    Write-Host ""
    $continue = Read-Host "Deseja continuar mesmo assim? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        Write-Host "Execucao cancelada" -ForegroundColor Yellow
        exit 0
    }
}

# Configurações
$ProjectRoot = "c:\projetos\omaum"
$BackupDir = "$ProjectRoot\backups"
$ExportDir = "$ProjectRoot\scripts\deploy\exports"
$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'

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

function Write-Step {
    param($Number, $Total, $Message)
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "  PASSO $Number/$Total - $Message" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
}

# 1. Verificar pré-requisitos
function Test-Prerequisites {
    Write-Step 1 8 "VERIFICANDO PRE-REQUISITOS"
    
    # Verificar se está na pasta correta
    if ((Get-Location).Path -ne $ProjectRoot) {
        Write-Info "Mudando para pasta do projeto: $ProjectRoot"
        Set-Location $ProjectRoot
    }
    
    # Verificar se Docker está rodando
    try {
        $null = docker ps 2>&1
        Write-Success "Docker esta rodando"
    } catch {
        Write-Err "Docker nao esta rodando ou nao esta instalado!"
        exit 1
    }
    
    # Verificar containers de produção
    $containers = docker ps --format "{{.Names}}" | Where-Object { $_ -like "omaum-*-prod" -or $_ -like "omaum-*" }
    
    if ($containers.Count -eq 0) {
        Write-Err "Nenhum container do OMAUM encontrado!"
        Write-Info "Execute primeiro: docker-compose up -d"
        exit 1
    }
    
    # Verificar se tem containers com sufixo -prod
    $prodContainers = $containers | Where-Object { $_ -like "*-prod" }
    if ($prodContainers.Count -eq 0) {
        Write-Warn "Containers encontrados NAO tem sufixo -prod"
        Write-Warn "Isso pode indicar que nao esta no ambiente de producao"
    }
    
    Write-Success "Containers encontrados: $($containers.Count)"
    $containers | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
    
    Write-Success "Pre-requisitos verificados"
}

# 2. Backup do banco de dados
function Backup-Database {
    if ($SemBackup) {
        Write-Warn "Pulando backup (parametro -SemBackup utilizado)"
        return
    }
    
    Write-Step 2 8 "BACKUP DO BANCO DE DADOS"
    
    # Criar pasta de backups
    if (!(Test-Path $BackupDir)) {
        New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    }
    
    $backupFile = "$BackupDir\backup_$Timestamp.sql"
    
    Write-Info "Criando backup do PostgreSQL..."
    Write-Info "Arquivo: $backupFile"
    
    try {
        # Tentar com sufixo -prod primeiro, senão sem sufixo
        $dbContainer = docker ps --format "{{.Names}}" | Where-Object { $_ -eq "omaum-db-prod" }
        if (!$dbContainer) {
            $dbContainer = "omaum-db"
            Write-Warn "Usando container sem sufixo -prod: $dbContainer"
        }
        
        docker exec $dbContainer pg_dump -U postgres omaum | Out-File -FilePath $backupFile -Encoding UTF8
        
        if (Test-Path $backupFile) {
            $sizeKB = [math]::Round((Get-Item $backupFile).Length / 1KB, 2)
            Write-Success "Backup criado com sucesso: $sizeKB KB"
            
            # Comprimir backup
            Write-Info "Comprimindo backup..."
            Compress-Archive -Path $backupFile -DestinationPath "$backupFile.zip" -Force
            Remove-Item $backupFile
            Write-Success "Backup comprimido: $backupFile.zip"
        } else {
            Write-Err "Falha ao criar backup!"
            exit 1
        }
    } catch {
        Write-Err "Erro ao criar backup: $($_.Exception.Message)"
        exit 1
    }
}

# 3. Atualizar código (Git)
function Update-Code {
    Write-Step 3 8 "ATUALIZANDO CODIGO"
    
    # Verificar se é repositório Git
    if (Test-Path "$ProjectRoot\.git") {
        Write-Info "Verificando status do Git..."
        
        $status = git status --porcelain
        if ($status) {
            Write-Warn "Existem alteracoes nao commitadas:"
            git status --short
            Write-Host ""
            
            $commit = Read-Host "Deseja fazer commit das alteracoes? (y/N)"
            if ($commit -eq 'y' -or $commit -eq 'Y') {
                $message = Read-Host "Mensagem do commit"
                git add .
                git commit -m $message
                Write-Success "Commit realizado"
            }
        } else {
            Write-Success "Nenhuma alteracao pendente"
        }
        
        # Pull (se houver remote)
        $hasRemote = git remote | Where-Object { $_ -eq 'origin' }
        if ($hasRemote) {
            $pull = Read-Host "Deseja fazer pull do repositorio remoto? (y/N)"
            if ($pull -eq 'y' -or $pull -eq 'Y') {
                Write-Info "Executando git pull..."
                git pull origin main
                Write-Success "Codigo atualizado do repositorio"
            }
        }
    } else {
        Write-Info "Nao e um repositorio Git (pulando atualizacao)"
    }
}

# 4. Importar dados de desenvolvimento (se solicitado)
function Import-DevData {
    if ($SemDados) {
        Write-Info "Pulando importacao de dados (parametro -SemDados utilizado)"
        return
    }
    
    Write-Step 4 8 "IMPORTANDO DADOS DE DESENVOLVIMENTO"
    
    # Encontrar arquivo de exportação mais recente
    $exportFiles = Get-ChildItem -Path $ExportDir -Filter "dev_data_*.json" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending
    
    if ($exportFiles.Count -eq 0) {
        Write-Warn "Nenhum arquivo de exportacao encontrado em $ExportDir"
        $import = Read-Host "Deseja importar dados de desenvolvimento? (y/N)"
        if ($import -ne 'y' -and $import -ne 'Y') {
            Write-Info "Pulando importacao de dados"
            return
        }
        
        Write-Info "Execute primeiro: python scripts\deploy\01_export_dev_data.py"
        exit 1
    }
    
    $exportFile = $exportFiles[0]
    Write-Info "Arquivo encontrado: $($exportFile.Name)"
    Write-Info "Data: $($exportFile.LastWriteTime)"
    Write-Info "Tamanho: $([math]::Round($exportFile.Length / 1KB, 2)) KB"
    Write-Host ""
    
    $confirm = Read-Host "Deseja importar estes dados? ISSO IRA LIMPAR O BANCO ATUAL! (y/N)"
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
        Write-Warn "Importacao cancelada pelo usuario"
        return
    }
    
    Write-Warn "ATENCAO: Limpando banco de dados atual..."
    docker-compose run --rm web python manage.py flush --no-input
    
    Write-Info "Copiando arquivo para container..."
    docker cp $exportFile.FullName omaum-web-prod:/tmp/dev_data.json
    
    Write-Info "Importando dados..."
    docker exec omaum-web-prod python manage.py loaddata /tmp/dev_data.json
    
    Write-Success "Dados importados com sucesso!"
}

# 5. Aplicar migrações
function Apply-Migrations {
    Write-Step 5 8 "APLICANDO MIGRACOES"
    
    Write-Info "Criando migracoes (se houver alteracoes nos models)..."
    docker-compose run --rm web python manage.py makemigrations
    
    Write-Info "Aplicando migracoes..."
    docker-compose run --rm web python manage.py migrate --no-input
    
    Write-Success "Migracoes aplicadas"
}

# 6. Coletar arquivos estáticos
function Collect-Static {
    Write-Step 6 8 "COLETANDO ARQUIVOS ESTATICOS"
    
    Write-Info "Coletando CSS, JS, imagens..."
    docker-compose run --rm web python manage.py collectstatic --no-input --clear
    
    Write-Success "Arquivos estaticos coletados"
}

# 7. Reconstruir e reiniciar containers
function Rebuild-Containers {
    Write-Step 7 8 "RECONSTRUINDO E REINICIANDO CONTAINERS"
    
    Write-Info "Reconstruindo imagens Docker..."
    docker-compose build --pull
    
    Write-Info "Reiniciando containers..."
    docker-compose up -d
    
    Write-Success "Containers reiniciados"
    
    # Aguardar healthcheck
    Write-Info "Aguardando inicializacao dos servicos..."
    Start-Sleep -Seconds 10
}

# 8. Verificar saúde
function Test-Health {
    Write-Step 8 8 "VERIFICANDO SAUDE DOS SERVICOS"
    
    Write-Info "Status dos containers:"
    docker-compose ps
    
    Write-Host ""
    Write-Info "Ultimas linhas dos logs:"
    docker-compose logs --tail=20 web
    
    # Testar acesso HTTP
    Write-Host ""
    Write-Info "Testando acesso HTTP..."
    try {
        $response = Invoke-WebRequest -Uri "http://192.168.15.4" -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
        Write-Success "Aplicacao acessivel: HTTP $($response.StatusCode)"
    } catch {
        Write-Warn "Falha ao acessar aplicacao: $($_.Exception.Message)"
    }
    
    Write-Success "Verificacao de saude concluida"
}

# 9. Smoke tests
function Invoke-SmokeTests {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "  TESTES DE VALIDACAO" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    
    Write-Info "Verificando dados no banco..."
    $shellCmd = 'from turmas.models import Turma; from cursos.models import Curso; print(f\"Turmas: {Turma.objects.count()}, Cursos: {Curso.objects.count()}\")'
    $result = docker exec omaum-web-prod python manage.py shell -c $shellCmd
    Write-Host "  $result" -ForegroundColor White
    
    Write-Success "Testes concluidos"
}

# Função principal
function Main {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "  ATUALIZACAO DE PRODUCAO - OMAUM" -ForegroundColor Cyan
    Write-Host "  Servidor: DESKTOP-OAE3R5M (192.168.15.4)" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Confirmar início
    Write-Host "Este script ira:" -ForegroundColor Yellow
    Write-Host "  1. Fazer backup do banco de dados" -ForegroundColor White
    if (!$SemDados) {
        Write-Host "  2. Importar dados de desenvolvimento (OPCIONAL)" -ForegroundColor White
    }
    Write-Host "  3. Aplicar migracoes do banco" -ForegroundColor White
    Write-Host "  4. Coletar arquivos estaticos" -ForegroundColor White
    Write-Host "  5. Reconstruir e reiniciar containers" -ForegroundColor White
    Write-Host "  6. Validar funcionamento" -ForegroundColor White
    Write-Host ""
    
    $confirm = Read-Host "Deseja continuar? (y/N)"
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
        Write-Warn "Atualizacao cancelada pelo usuario"
        exit 0
    }
    
    # Executar etapas
    try {
        $startTime = Get-Date
        
        Test-Prerequisites
        Backup-Database
        Update-Code
        
        if (!$SemDados) {
            Import-DevData
        }
        
        Apply-Migrations
        Collect-Static
        Rebuild-Containers
        Test-Health
        Invoke-SmokeTests
        
        $duration = (Get-Date) - $startTime
        
        Write-Host ""
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host "  ATUALIZACAO CONCLUIDA COM SUCESSO!" -ForegroundColor Green
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host ""
        Write-Success "Tempo total: $($duration.Minutes)m $($duration.Seconds)s"
        Write-Info "Backup salvo em: $BackupDir\backup_$Timestamp.sql.zip"
        Write-Host ""
        Write-Info "Acessos:"
        Write-Host "  - Web: http://192.168.15.4" -ForegroundColor White
        Write-Host "  - Admin: http://192.168.15.4/admin" -ForegroundColor White
        Write-Host ""
        
    } catch {
        Write-Host ""
        Write-Host "================================================================" -ForegroundColor Red
        Write-Err "ERRO DURANTE ATUALIZACAO!"
        Write-Host "================================================================" -ForegroundColor Red
        Write-Host ""
        Write-Err "Mensagem: $($_.Exception.Message)"
        Write-Host $_.ScriptStackTrace -ForegroundColor Red
        Write-Host ""
        Write-Warn "Para restaurar o backup:"
        Write-Host "  Expand-Archive $BackupDir\backup_$Timestamp.sql.zip -DestinationPath $BackupDir\temp" -ForegroundColor White
        Write-Host "  Get-Content $BackupDir\temp\backup_$Timestamp.sql | docker exec -i omaum-db-prod psql -U postgres omaum" -ForegroundColor White
        Write-Host ""
        exit 1
    }
}

# Executar
Main
