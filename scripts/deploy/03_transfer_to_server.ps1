################################################################################
# Script de Transferência de Arquivos para Servidor de Produção
# Autor: Sistema OMAUM
# Data: 2025-11-22
################################################################################

param(
    [Parameter(Mandatory=$false)]
    [string]$ServerHost = "",
    
    [Parameter(Mandatory=$false)]
    [string]$ServerUser = "",
    
    [Parameter(Mandatory=$false)]
    [string]$ServerPath = "/var/www/omaum"
)

$ErrorActionPreference = "Stop"

# Configurações
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Get-Item $ScriptDir).Parent.Parent.FullName
$ExportDir = Join-Path $ScriptDir "exports"

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

# Verificar se SCP está disponível
function Test-ScpAvailable {
    try {
        $null = Get-Command scp -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Encontrar arquivo de exportação mais recente
function Get-LatestExport {
    $files = Get-ChildItem -Path $ExportDir -Filter "dev_data_*.json" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending
    
    if ($files.Count -eq 0) {
        Write-Err "Nenhum arquivo de exportacao encontrado!"
        Write-Err "Execute primeiro: python scripts/deploy/01_export_dev_data.py"
        exit 1
    }
    
    return $files[0]
}

# Transferir via SCP
function Transfer-ViaScp {
    param(
        [string]$File,
        [string]$Destination
    )
    
    Write-Info "Transferindo via SCP..."
    Write-Info "Arquivo: $($File.Name)"
    Write-Info "Destino: $Destination"
    
    $scpCommand = "scp `"$($File.FullName)`" `"${ServerUser}@${ServerHost}:${ServerPath}/scripts/deploy/exports/`""
    
    Write-Info "Executando: $scpCommand"
    
    try {
        Invoke-Expression $scpCommand
        Write-Success "Arquivo transferido com sucesso via SCP!"
        return $true
    } catch {
        Write-Err "Erro ao transferir via SCP: $($_.Exception.Message)"
        return $false
    }
}

# Transferir via PSCP (PuTTY)
function Transfer-ViaPscp {
    param(
        [string]$File,
        [string]$Destination
    )
    
    Write-Info "Transferindo via PSCP (PuTTY)..."
    
    # Verificar se PSCP está disponível
    $pscpPath = $null
    $possiblePaths = @(
        "C:\Program Files\PuTTY\pscp.exe",
        "C:\Program Files (x86)\PuTTY\pscp.exe",
        "${env:ProgramFiles}\PuTTY\pscp.exe",
        "${env:ProgramFiles(x86)}\PuTTY\pscp.exe"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $pscpPath = $path
            break
        }
    }
    
    if (!$pscpPath) {
        try {
            $pscpPath = (Get-Command pscp -ErrorAction Stop).Source
        } catch {
            Write-Warn "PSCP nao encontrado. Instalando via WinGet..."
            winget install -e --id PuTTY.PuTTY
            $pscpPath = "C:\Program Files\PuTTY\pscp.exe"
        }
    }
    
    if (!(Test-Path $pscpPath)) {
        Write-Err "PSCP nao esta disponivel!"
        return $false
    }
    
    $pscpCommand = "& `"$pscpPath`" -batch `"$($File.FullName)`" `"${ServerUser}@${ServerHost}:${ServerPath}/scripts/deploy/exports/`""
    
    Write-Info "Executando: $pscpCommand"
    
    try {
        Invoke-Expression $pscpCommand
        Write-Success "Arquivo transferido com sucesso via PSCP!"
        return $true
    } catch {
        Write-Err "Erro ao transferir via PSCP: $($_.Exception.Message)"
        return $false
    }
}

# Gerar comando manual
function Show-ManualInstructions {
    param($File)
    
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Yellow
    Write-Host "  TRANSFERENCIA MANUAL NECESSARIA" -ForegroundColor Yellow
    Write-Host "================================================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Warn "Nenhum metodo automatico disponivel."
    Write-Host ""
    Write-Info "Opcao 1 - Usar WinSCP (Recomendado):"
    Write-Host "  1. Baixe WinSCP: https://winscp.net/download/WinSCP-Setup.exe" -ForegroundColor White
    Write-Host "  2. Conecte ao servidor: ${ServerUser}@${ServerHost}" -ForegroundColor White
    Write-Host "  3. Navegue ate: ${ServerPath}/scripts/deploy/exports/" -ForegroundColor White
    Write-Host "  4. Arraste o arquivo: $($File.FullName)" -ForegroundColor White
    Write-Host ""
    Write-Info "Opcao 2 - Usar SCP via WSL:"
    Write-Host "  wsl scp `"$($File.FullName)`" ${ServerUser}@${ServerHost}:${ServerPath}/scripts/deploy/exports/" -ForegroundColor White
    Write-Host ""
    Write-Info "Opcao 3 - Usar FileZilla:"
    Write-Host "  1. Baixe FileZilla: https://filezilla-project.org/" -ForegroundColor White
    Write-Host "  2. Conecte via SFTP ao servidor" -ForegroundColor White
    Write-Host "  3. Transfira o arquivo para o caminho acima" -ForegroundColor White
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Yellow
}

# Função principal
function Main {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "  TRANSFERENCIA DE DADOS PARA PRODUCAO" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Encontrar arquivo mais recente
    $exportFile = Get-LatestExport
    $fileSize = [math]::Round($exportFile.Length / 1KB, 2)
    
    Write-Info "Arquivo encontrado:"
    Write-Host "  Nome: $($exportFile.Name)" -ForegroundColor White
    Write-Host "  Tamanho: $fileSize KB" -ForegroundColor White
    Write-Host "  Data: $($exportFile.LastWriteTime)" -ForegroundColor White
    Write-Host ""
    
    # Solicitar informações do servidor se não fornecidas
    if ([string]::IsNullOrEmpty($ServerHost)) {
        $ServerHost = Read-Host "Digite o IP ou hostname do servidor"
    }
    
    if ([string]::IsNullOrEmpty($ServerUser)) {
        $ServerUser = Read-Host "Digite o usuario SSH"
    }
    
    if ([string]::IsNullOrEmpty($ServerPath)) {
        $userPath = Read-Host "Digite o caminho no servidor [/var/www/omaum]"
        if (![string]::IsNullOrEmpty($userPath)) {
            $ServerPath = $userPath
        }
    }
    
    Write-Host ""
    Write-Info "Configuracao:"
    Write-Host "  Servidor: ${ServerUser}@${ServerHost}" -ForegroundColor White
    Write-Host "  Destino: ${ServerPath}/scripts/deploy/exports/" -ForegroundColor White
    Write-Host ""
    
    # Confirmar transferência
    $confirm = Read-Host "Iniciar transferencia? (y/N)"
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
        Write-Warn "Transferencia cancelada pelo usuario"
        exit 0
    }
    
    Write-Host ""
    
    # Tentar métodos de transferência
    $transferred = $false
    
    # Método 1: SCP (OpenSSH)
    if (Test-ScpAvailable) {
        Write-Info "Metodo: OpenSSH SCP"
        $transferred = Transfer-ViaScp -File $exportFile -Destination "${ServerUser}@${ServerHost}:${ServerPath}/scripts/deploy/exports/"
    }
    
    # Método 2: PSCP (PuTTY)
    if (!$transferred) {
        Write-Info "Metodo: PuTTY PSCP"
        $transferred = Transfer-ViaPscp -File $exportFile -Destination "${ServerUser}@${ServerHost}:${ServerPath}/scripts/deploy/exports/"
    }
    
    # Método 3: Instruções manuais
    if (!$transferred) {
        Show-ManualInstructions -File $exportFile
    } else {
        Write-Host ""
        Write-Host "================================================================" -ForegroundColor Green
        Write-Success "TRANSFERENCIA CONCLUIDA COM SUCESSO!"
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host ""
        Write-Info "Proximo passo no servidor:"
        Write-Host "  ssh ${ServerUser}@${ServerHost}" -ForegroundColor White
        Write-Host "  cd ${ServerPath}" -ForegroundColor White
        Write-Host "  ./scripts/deploy/02_deploy_to_production.sh" -ForegroundColor White
        Write-Host ""
    }
}

# Executar
try {
    Main
} catch {
    Write-Err "Erro durante transferencia: $($_.Exception.Message)"
    Write-Host $_.ScriptStackTrace -ForegroundColor Red
    exit 1
}
