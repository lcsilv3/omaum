################################################################################
# Script de Transferência Automática para Produção
# De: LUISHP (desenvolvimento) -> Para: DESKTOP-OAE3R5M (produção)
# Autor: Sistema OMAUM
# Data: 2025-11-22
################################################################################

param(
    [string]$ServidorIP = "192.168.15.4",
    [string]$ServidorUser = "admin",
    [string]$ArquivoEspecifico = ""
)

$ErrorActionPreference = "Stop"

# Configurações
$LocalRoot = "c:\projetos\omaum"
$LocalExportDir = "$LocalRoot\scripts\deploy\exports"
$RemoteRoot = "c:\projetos\omaum"
$RemoteExportDir = "$RemoteRoot\scripts\deploy\exports"

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

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  TRANSFERENCIA AUTOMATICA PARA PRODUCAO" -ForegroundColor Cyan
Write-Host "  De: LUISHP -> Para: DESKTOP-OAE3R5M" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está na máquina de desenvolvimento
if ($env:COMPUTERNAME -eq "DESKTOP-OAE3R5M") {
    Write-Err "Este script deve ser executado na maquina de DESENVOLVIMENTO!"
    Write-Err "Voce ja esta no servidor de producao."
    exit 1
}

Write-Info "Maquina atual: $env:COMPUTERNAME"
Write-Info "Destino: $ServidorIP (DESKTOP-OAE3R5M)"
Write-Host ""

# Encontrar arquivo de exportação mais recente
if ($ArquivoEspecifico) {
    $exportFile = Get-Item $ArquivoEspecifico
} else {
    $exportFile = Get-ChildItem -Path $LocalExportDir -Filter "dev_data_*.json" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
}

if (!$exportFile) {
    Write-Err "Nenhum arquivo de exportacao encontrado!"
    Write-Info "Execute primeiro: python scripts\deploy\01_export_dev_data.py"
    exit 1
}

$fileSize = [math]::Round($exportFile.Length / 1KB, 2)
Write-Info "Arquivo a transferir:"
Write-Host "  Nome: $($exportFile.Name)" -ForegroundColor White
Write-Host "  Tamanho: $fileSize KB" -ForegroundColor White
Write-Host "  Data: $($exportFile.LastWriteTime)" -ForegroundColor White
Write-Host ""

# Método 1: Compartilhamento de rede (UNC)
function Transfer-ViaNetworkShare {
    Write-Info "Metodo 1: Tentando via compartilhamento de rede..."
    
    $uncPath = "\\$ServidorIP\c$\projetos\omaum\scripts\deploy\exports"
    
    Write-Info "Testando acesso a: $uncPath"
    
    if (Test-Path $uncPath -ErrorAction SilentlyContinue) {
        Write-Success "Acesso de rede disponivel!"
        
        try {
            Copy-Item $exportFile.FullName -Destination $uncPath -Force
            Write-Success "Arquivo transferido via rede!"
            return $true
        } catch {
            Write-Warn "Erro ao copiar: $($_.Exception.Message)"
            return $false
        }
    } else {
        Write-Warn "Compartilhamento administrativo nao acessivel"
        Write-Info "Certifique-se que:"
        Write-Host "  1. Usuario tem permissoes de administrador" -ForegroundColor White
        Write-Host "  2. Compartilhamento administrativo (C$) esta habilitado" -ForegroundColor White
        Write-Host "  3. Firewall permite acesso SMB" -ForegroundColor White
        return $false
    }
}

# Método 2: PowerShell Remoting (WinRM)
function Transfer-ViaPSRemoting {
    Write-Info "Metodo 2: Tentando via PowerShell Remoting (WinRM)..."
    
    try {
        # Testar conexão WinRM
        $session = New-PSSession -ComputerName $ServidorIP -ErrorAction Stop
        
        Write-Success "Sessao remota estabelecida!"
        
        # Copiar arquivo
        Copy-Item $exportFile.FullName -Destination $RemoteExportDir -ToSession $session -Force
        
        # Fechar sessão
        Remove-PSSession $session
        
        Write-Success "Arquivo transferido via PSRemoting!"
        return $true
        
    } catch {
        Write-Warn "WinRM nao disponivel: $($_.Exception.Message)"
        Write-Info "Para habilitar WinRM no servidor:"
        Write-Host "  Enable-PSRemoting -Force" -ForegroundColor White
        return $false
    }
}

# Método 3: PsExec (Sysinternals)
function Transfer-ViaPsExec {
    Write-Info "Metodo 3: Tentando via PsExec..."
    
    $psexecPath = "C:\Tools\PSTools\PsExec.exe"
    
    if (!(Test-Path $psexecPath)) {
        Write-Warn "PsExec nao encontrado em: $psexecPath"
        Write-Info "Baixe em: https://docs.microsoft.com/sysinternals/downloads/psexec"
        return $false
    }
    
    try {
        # Primeiro copiar via rede
        if (Transfer-ViaNetworkShare) {
            Write-Success "Arquivo transferido via PsExec+Rede!"
            return $true
        }
        return $false
    } catch {
        Write-Warn "Erro ao usar PsExec: $($_.Exception.Message)"
        return $false
    }
}

# Método 4: Instruções manuais
function Show-ManualInstructions {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Yellow
    Write-Host "  TRANSFERENCIA MANUAL NECESSARIA" -ForegroundColor Yellow
    Write-Host "================================================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Warn "Metodos automaticos nao funcionaram. Use uma destas opcoes:"
    Write-Host ""
    
    Write-Host "OPCAO 1 - Compartilhamento de Rede:" -ForegroundColor Cyan
    Write-Host "  1. Habilite compartilhamento administrativo no servidor:" -ForegroundColor White
    Write-Host "     - Execute como admin: reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f" -ForegroundColor Gray
    Write-Host "  2. Execute este script novamente" -ForegroundColor White
    Write-Host ""
    
    Write-Host "OPCAO 2 - Remote Desktop (RDP):" -ForegroundColor Cyan
    Write-Host "  1. Abra Remote Desktop: mstsc /v:$ServidorIP" -ForegroundColor White
    Write-Host "  2. Na sessao RDP, abra File Explorer" -ForegroundColor White
    Write-Host "  3. Cole este caminho na barra de endereco:" -ForegroundColor White
    Write-Host "     \\LUISHP\c$\projetos\omaum\scripts\deploy\exports\" -ForegroundColor Gray
    Write-Host "  4. Copie o arquivo: $($exportFile.Name)" -ForegroundColor White
    Write-Host "  5. Cole em: $RemoteExportDir" -ForegroundColor White
    Write-Host ""
    
    Write-Host "OPCAO 3 - Pendrive/Midia Removivel:" -ForegroundColor Cyan
    Write-Host "  1. Copie o arquivo para pendrive:" -ForegroundColor White
    Write-Host "     Copy-Item `"$($exportFile.FullName)`" E:\" -ForegroundColor Gray
    Write-Host "  2. Conecte o pendrive no servidor" -ForegroundColor White
    Write-Host "  3. Copie de E:\ para: $RemoteExportDir" -ForegroundColor White
    Write-Host ""
    
    Write-Host "OPCAO 4 - Email/OneDrive/Dropbox:" -ForegroundColor Cyan
    Write-Host "  1. Envie o arquivo para si mesmo ou use nuvem" -ForegroundColor White
    Write-Host "  2. Baixe no servidor em: $RemoteExportDir" -ForegroundColor White
    Write-Host ""
    
    Write-Host "================================================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Info "Arquivo a transferir:"
    Write-Host "  Origem: $($exportFile.FullName)" -ForegroundColor White
    Write-Host "  Destino: $RemoteExportDir\$($exportFile.Name)" -ForegroundColor White
}

# Executar métodos de transferência
Write-Host "Tentando transferencia automatica..." -ForegroundColor Cyan
Write-Host ""

$transferred = $false

# Tentar cada método
if (Transfer-ViaNetworkShare) {
    $transferred = $true
} elseif (Transfer-ViaPSRemoting) {
    $transferred = $true
} elseif (Transfer-ViaPsExec) {
    $transferred = $true
}

if ($transferred) {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Green
    Write-Success "TRANSFERENCIA CONCLUIDA COM SUCESSO!"
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Info "Proximo passo:"
    Write-Host "  1. Conecte ao servidor (RDP ou fisicamente)" -ForegroundColor White
    Write-Host "  2. Abra PowerShell em: c:\projetos\omaum" -ForegroundColor White
    Write-Host "  3. Execute: .\scripts\deploy\02_deploy_atualizar_producao.ps1" -ForegroundColor White
    Write-Host ""
    Write-Info "Comando RDP:"
    Write-Host "  mstsc /v:$ServidorIP" -ForegroundColor Cyan
    Write-Host ""
} else {
    Show-ManualInstructions
}
