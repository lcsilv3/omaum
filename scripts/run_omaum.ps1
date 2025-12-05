param(
    [ValidateSet('dev', 'prod')]
    [string]$Environment,
    [string]$AppUrl
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Get-Item -LiteralPath $PSScriptRoot).Parent.FullName
$envConfigs = @{
    dev = @{
        ComposeFile    = Join-Path $repoRoot 'docker\docker-compose.yml'
        EnvFile        = $null
        Services       = @('omaum-web')
        ContainerNames = @('omaum-web', 'omaum-db', 'omaum-redis')
        ProjectName    = 'omaum-dev'
        BrowserUrl     = 'http://localhost:8000/'
    }
    prod = @{
        ComposeFile    = Join-Path $repoRoot 'docker\docker-compose.prod.yml'
        EnvFile        = Join-Path $repoRoot 'docker\.env.production'
        Services       = @('omaum-web', 'omaum-nginx')
        ContainerNames = @(
            'omaum-web-prod',
            'omaum-nginx-prod',
            'omaum-celery-prod',
            'omaum-celery-beat-prod',
            'omaum-db-prod',
            'omaum-redis-prod'
        )
        ProjectName    = 'docker'
        BrowserUrl     = 'http://omaum.local/'
    }
}

function Prompt-Environment {
    Write-Host ''
    Write-Host 'Selecione o ambiente:'
    Write-Host '  1 - Desenvolvimento'
    Write-Host '  2 - Producao'
    while ($true) {
        $answer = Read-Host 'Opcao (1/2)'
        switch ($answer) {
            '1' { return 'dev' }
            '2' { return 'prod' }
            default { Write-Warn 'Opcao inválida. Informe 1 ou 2.' }
        }
    }
}

if ([string]::IsNullOrWhiteSpace($Environment)) {
    $Environment = Prompt-Environment
}

if (-not $envConfigs.ContainsKey($Environment)) {
    throw "Ambiente desconhecido: $Environment"
}

$script:SelectedConfig = $envConfigs[$Environment]
if ([string]::IsNullOrWhiteSpace($AppUrl)) {
    $AppUrl = $script:SelectedConfig.BrowserUrl
}
$script:TargetAppUrl = $AppUrl
$script:Services = $script:SelectedConfig.Services
$script:ContainerNames = $script:SelectedConfig.ContainerNames

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
    $args = @('compose', '-f', $script:SelectedConfig.ComposeFile)
    if ($script:SelectedConfig.EnvFile) {
        $args += @('--env-file', $script:SelectedConfig.EnvFile)
    }
    if ($script:SelectedConfig.ProjectName) {
        $args += @('-p', $script:SelectedConfig.ProjectName)
    }
    return $args
}

function Get-RunningContainers {
    $running = @()
    try {
        $rawNames = & docker ps --format '{{.Names}}'
        if ($LASTEXITCODE -eq 0 -and $null -ne $rawNames) {
            if ($rawNames -is [string]) {
                $rawNames = @($rawNames)
            }
            $rawNames = $rawNames | ForEach-Object { $_.Trim() } | Where-Object { $_ }
            foreach ($name in $script:ContainerNames) {
                if ($rawNames -contains $name) {
                    $running += $name
                }
            }
            return $running
        }
        Write-Warn 'Não foi possível obter containers via docker ps. Usando fallback.'
    } catch {
        Write-Warn 'Falha ao consultar docker ps. Usando fallback por inspeção.'
    }

    foreach ($name in $script:ContainerNames) {
        try {
            $status = & docker inspect --format '{{.State.Status}}' $name 2>$null
            if ($LASTEXITCODE -eq 0 -and $status -eq 'running') {
                $running += $name
            }
        } catch {
            continue
        }
    }
    return $running
}

function Ensure-Services {
    $running = Get-RunningContainers
    if ($running.Count -eq $script:ContainerNames.Count) {
        Write-Info 'Serviços já estão ativos.'
        return $true
    }
    if ($running.Count -gt 0) {
        Write-Info ("Containers já ativos: {0}" -f ($running -join ', '))
    }
    Write-Info 'Inicializando serviços docker... (aguarde, o processo pode levar alguns instantes)'
    Write-Progress -Activity 'docker compose up' -Status 'Processando...' -PercentComplete 20
    $args = Get-ComposeArgs
    $args += @('up', '-d') + $script:Services
    & docker @args
    Write-Progress -Activity 'docker compose up' -Completed
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
        Start-Process $script:TargetAppUrl
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
        Start-Process -FilePath $browserPath -ArgumentList $script:TargetAppUrl
    } else {
        Write-Warn "${label} não foi encontrado. Abrindo no navegador padrão."
        Start-Process $script:TargetAppUrl
    }
}

function Ensure-WSL {
    Write-Info 'Verificando WSL (requerido para o backend do Docker em Windows)...'
    try {
        & wsl.exe -l -q *> $null
        Write-Info 'WSL respondeu corretamente.'
        return $true
    } catch {
        Write-Warn 'WSL não respondeu. Tentando inicializar...'
        try {
            & wsl.exe --status *> $null
            Start-Sleep -Seconds 2
            & wsl.exe -l -q *> $null
            Write-Info 'WSL foi iniciado com sucesso.'
            return $true
        } catch {
            Write-Warn 'Não foi possível confirmar o WSL. Verifique se ele está instalado e habilitado.'
            return $false
        }
    }
}

try {
    if (-not (Test-Path $script:SelectedConfig.ComposeFile)) {
        throw "Arquivo docker-compose não encontrado em $($script:SelectedConfig.ComposeFile)"
    }
    Ensure-WSL | Out-Null
    Write-Info "Ambiente selecionado: $Environment"
    if (-not (Wait-DockerReady)) {
        throw 'Docker indisponível. Encerrando.'
    }
    if (-not (Ensure-Services)) {
        throw 'Serviços não puderam ser inicializados.'
    }
    $choice = Select-Browser
    Open-App $choice
    Write-Info "Ambiente pronto ($Environment). Boa utilização!"
} catch {
    Write-ErrorMessage $_
    Read-Host 'Pressione Enter para sair'
}
