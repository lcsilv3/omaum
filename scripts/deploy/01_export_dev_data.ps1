################################################################################
# Script de Exportação de Dados de Desenvolvimento - OMAUM
# EXECUTAR NA MÁQUINA DE DESENVOLVIMENTO
# Exporta dados do container Docker de dev para fixture JSON
# Autor: Sistema OMAUM
# Data: 2025-11-24
################################################################################

$ErrorActionPreference = "Stop"

# Configurações
$ProjectRoot = "c:\projetos\omaum"
$ExportDir = "$ProjectRoot\scripts\deploy\exports"
$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$ExportFile = "$ExportDir\dev_data_$Timestamp.json"
$DockerContainerName = "omaum-web"

# Cores
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

# Banner
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  EXPORTACAO DE DADOS DE DESENVOLVIMENTO - OMAUM" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está na pasta correta
if ((Get-Location).Path -ne $ProjectRoot) {
    Write-Info "Mudando para pasta do projeto: $ProjectRoot"
    Set-Location $ProjectRoot
}

# Criar diretório de exports se não existir
if (-not (Test-Path $ExportDir)) {
    Write-Info "Criando diretório de exports..."
    New-Item -ItemType Directory -Path $ExportDir -Force | Out-Null
}

# Verificar se Docker está rodando
Write-Info "Verificando Docker..."
try {
    docker ps | Out-Null
    Write-Success "Docker esta rodando"
} catch {
    Write-Err "Docker nao esta rodando ou nao esta acessivel"
    exit 1
}

# Verificar se container de desenvolvimento existe e está rodando
Write-Info "Verificando container de desenvolvimento..."
$containerStatus = docker ps --filter "name=$DockerContainerName" --format "{{.Names}}"
if (-not $containerStatus) {
    Write-Err "Container '$DockerContainerName' nao esta rodando!"
    Write-Info "Execute primeiro: docker compose up -d"
    exit 1
}
Write-Success "Container '$DockerContainerName' encontrado"

# Verificar contagem de dados
Write-Host ""
Write-Info "Verificando dados disponiveis no banco de desenvolvimento..."
$checkCmd = "from cursos.models import Curso; from turmas.models import Turma; from alunos.models import Aluno; print(f'Cursos: {Curso.objects.count()}, Turmas: {Turma.objects.count()}, Alunos: {Aluno.objects.count()}')"
$dataCount = docker exec $DockerContainerName python manage.py shell -c $checkCmd 2>&1 | Select-String -Pattern "Cursos:|Turmas:|Alunos:"

if ($dataCount) {
    Write-Host "  $dataCount" -ForegroundColor White
} else {
    Write-Warn "Nao foi possivel verificar contagem de dados"
}

Write-Host ""
$confirm = Read-Host "Deseja exportar os dados? (y/N)"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Warn "Exportacao cancelada pelo usuario"
    exit 0
}

# Exportar dados
Write-Host ""
Write-Info "Exportando dados do container '$DockerContainerName'..."
Write-Info "Arquivo de destino: $ExportFile"
Write-Host ""

$dumpCmd = @"
docker exec $DockerContainerName python manage.py dumpdata --indent=2 -e contenttypes -e auth.Permission -e sessions -e admin.logentry 2>&1
"@

try {
    # Executar dumpdata e capturar apenas o JSON (ignorar warnings)
    $output = Invoke-Expression $dumpCmd
    
    # Filtrar apenas linhas JSON (começam com [ ou { ou são parte do array)
    $jsonLines = $output | Where-Object { 
        $_ -match '^\s*[\[\{]' -or 
        $_ -match '^\s*[\]\}]' -or 
        $_ -match '^\s*"model":' -or
        $_ -match '^\s*"pk":' -or
        $_ -match '^\s*"fields":' -or
        $_ -match '^\s*\},?\s*$'
    }
    
    # Salvar sem BOM UTF-8
    $jsonContent = $jsonLines -join "`n"
    [System.IO.File]::WriteAllText($ExportFile, $jsonContent, (New-Object System.Text.UTF8Encoding $false))
    
    # Verificar se arquivo foi criado
    if (Test-Path $ExportFile) {
        $fileInfo = Get-Item $ExportFile
        $sizeKB = [math]::Round($fileInfo.Length / 1KB, 2)
        
        Write-Success "Dados exportados com sucesso!"
        Write-Host ""
        Write-Host "  Arquivo: $($fileInfo.Name)" -ForegroundColor White
        Write-Host "  Tamanho: $sizeKB KB" -ForegroundColor White
        Write-Host "  Caminho: $($fileInfo.FullName)" -ForegroundColor White
        Write-Host ""
        
        # Validar JSON básico
        if ($sizeKB -lt 1) {
            Write-Warn "Arquivo muito pequeno ($sizeKB KB) - pode estar vazio ou incompleto"
        } else {
            Write-Success "Arquivo parece valido"
        }
        
        # Instruções de próximos passos
        Write-Host ""
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host "  PROXIMOS PASSOS" -ForegroundColor Green
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "1. Copie o arquivo para a maquina de PRODUCAO:" -ForegroundColor Yellow
        Write-Host "   $ExportFile" -ForegroundColor White
        Write-Host ""
        Write-Host "2. Coloque no mesmo caminho na maquina de producao:" -ForegroundColor Yellow
        Write-Host "   c:\projetos\omaum\scripts\deploy\exports\" -ForegroundColor White
        Write-Host ""
        Write-Host "3. Execute o deploy na maquina de producao:" -ForegroundColor Yellow
        Write-Host "   .\scripts\deploy\02_deploy_atualizar_producao.ps1" -ForegroundColor White
        Write-Host ""
        Write-Host "   OU importe manualmente:" -ForegroundColor Yellow
        Write-Host "   docker cp scripts\deploy\exports\$($fileInfo.Name) omaum-web-prod:/tmp/dev_data.json" -ForegroundColor White
        Write-Host "   docker exec omaum-web-prod python manage.py loaddata /tmp/dev_data.json" -ForegroundColor White
        Write-Host ""
        
    } else {
        Write-Err "Arquivo nao foi criado!"
        exit 1
    }
    
} catch {
    Write-Err "Erro ao exportar dados: $($_.Exception.Message)"
    exit 1
}

Write-Success "Exportacao concluida!"
Write-Host ""
