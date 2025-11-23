param(
    [string]$AppUrl = "http://omaum.local/"
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Get-Item -LiteralPath $PSScriptRoot).Parent.FullName
$composeFile = Join-Path $repoRoot 'docker\docker-compose.prod.yml'
$envFile = Join-Path $repoRoot 'docker\.env.production'
$services = @('omaum-web', 'omaum-nginx')

function Write-Info($message) {
    Write-Host "[INFO] $message" -ForegroundColor Cyan
}

function Write-Warn($message) {
    Write-Host "[AVISO] $message" -ForegroundColor Yellow
}

function Write-ErrorMessage($message) {
    Write-Host "[ERRO] $message" -ForegroundColor Red
}

function Test-DockerRunning {
    try {
        & docker info *> $null
        return $true
    } catch {
        return $false
    }
}

function Start-Docker {
    Write-Info 'Tentando iniciar o Docker...'
    $service = Get-Service -Name 'com.docker.service' -ErrorAction SilentlyContinue
    if ($null -ne $service -and $service.Status -ne 'Running') {
        try {
            Start-Service -InputObject $service -ErrorAction Stop
            return $true
        } catch {
            Write-Warn 'Falha ao iniciar o serviço com.docker.service via Start-Service.'
        }
    }
    $desktopExe = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
    if (Test-Path $desktopExe) {
        try {
            Start-Process -FilePath $desktopExe -ErrorAction Stop
            return $true
        } catch {
            Write-Warn 'Não foi possível abrir o Docker Desktop automaticamente.'
        }
    }
    Write-Warn 'Abra o Docker Desktop manualmente e execute este script novamente.'
    return $false
}

function Wait-DockerReady {
    if (Test-DockerRunning) {
        Write-Info 'Docker já está em execução.'
        return $true
    }
    if (-not (Start-Docker)) {
        return $false
    }
    Write-Info 'Aguardando resposta do Docker...'
    for ($i = 0; $i -lt 10; $i++) {
        if (Test-DockerRunning) {
            Write-Info 'Docker iniciado com sucesso.'
            return $true
        }
        Start-Sleep -Seconds 3
    }
    Write-Warn 'O Docker não respondeu a tempo. Verifique o Docker Desktop.'
    return $false
}

function Get-ComposeArgs {
    $args = @('compose', '-f', $composeFile)
    if (Test-Path $envFile) {
        $args += @('--env-file', $envFile)
    }
    return $args
}

function Get-RunningServices {
    $args = Get-ComposeArgs
    $args += @('ps', '--services', '--filter', 'status=running')
    $cmdOutput = & docker @args 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Warn 'Não foi possível verificar o status dos serviços.'
        return @()
    }
    if ($null -eq $cmdOutput) {
        return @()
    }
    return ($cmdOutput | Where-Object { $_ -ne '' })
}

function Ensure-Services {
    $running = Get-RunningServices
    if ($running.Count -gt 0) {
        $missing = @($services | Where-Object { $running -notcontains $_ })
        if ($missing.Count -eq 0) {
            Write-Info 'Serviços já estão ativos.'
            return $true
        }
    }
    Write-Info 'Inicializando serviços docker...'
    $args = Get-ComposeArgs
    $args += @('up', '-d') + $services
    & docker @args
    if ($LASTEXITCODE -ne 0) {
        Write-ErrorMessage 'Falha ao subir os serviços do OMAUM.'
        return $false
    }
    Write-Info 'Serviços iniciados com sucesso.'
    return $true
}

function Select-Browser {
    Write-Host ''
    Write-Host 'Selecione o navegador:'
    Write-Host '  1 - Mozilla Firefox'
    Write-Host '  2 - Google Chrome'
    Write-Host '  3 - Microsoft Edge'
    Write-Host '  Enter - Navegador padrão'
    Read-Host 'Opção'
}

function Open-App($choice) {
    $map = @{
        '1' = @('firefox.exe', 'Mozilla Firefox', @('C:\Program Files\Mozilla Firefox\firefox.exe', 'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'));
        '2' = @('chrome.exe', 'Google Chrome', @('C:\Program Files\Google\Chrome\Application\chrome.exe', 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'));
        '3' = @('msedge.exe', 'Microsoft Edge', @('C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', 'C:\Program Files\Microsoft\Edge\Application\msedge.exe'))
    }
    if (-not $map.ContainsKey($choice) -or [string]::IsNullOrWhiteSpace($choice)) {
        Write-Info 'Abrindo no navegador padrão.'
        Start-Process $AppUrl
        return
    }
    $entry = $map[$choice]
    $candidate = $entry[0]
    $label = $entry[1]
    $fallbacks = $entry[2]
    $commandInfo = Get-Command $candidate -ErrorAction SilentlyContinue
    $browserPath = $null
    if ($commandInfo) {
        $browserPath = $commandInfo.Source
    }
    if (-not $browserPath) {
        foreach ($path in $fallbacks) {
            if (Test-Path $path) {
                $browserPath = $path
                break
            }
        }
    }
    if ($null -ne $browserPath) {
        Write-Info "Abrindo no $label."
        Start-Process -FilePath $browserPath -ArgumentList $AppUrl
    } else {
        Write-Warn "${label} não foi encontrado. Abrindo no navegador padrão."
        Start-Process $AppUrl
    }
}

try {
    if (-not (Test-Path $composeFile)) {
        throw "Arquivo docker-compose não encontrado em $composeFile"
    }
    if (-not (Wait-DockerReady)) {
        throw 'Docker indisponível. Encerrando.'
    }
    if (-not (Ensure-Services)) {
        throw 'Serviços não puderam ser inicializados.'
    }
    $choice = Select-Browser
    Open-App $choice
    Write-Info 'Ambiente pronto. Boa utilização!'
} catch {
    Write-ErrorMessage $_
    Read-Host 'Pressione Enter para sair'
}
