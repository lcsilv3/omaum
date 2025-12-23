param(
    [ValidateSet('dev','prod')]
    [string]$Environment,
    [ValidateSet('up','restart','down','status','logs','collectstatic','migrate','open')]
    [string]$Action
)

$ErrorActionPreference = 'Stop'

function Write-Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Write-Warn($m){ Write-Host "[AVISO] $m" -ForegroundColor Yellow }
function Write-Err($m){ Write-Host "[ERRO] $m" -ForegroundColor Red }

$repoRoot = (Get-Item -LiteralPath $PSScriptRoot).Parent.Parent.FullName
$dockerDir = Join-Path $repoRoot 'docker'
$envConfigs = @{
    dev = @{
        ComposeArgs = @('-p','omaum-dev','--env-file','..\.env.dev','-f','docker-compose.yml')
        ProfileArgs = @()
        Url         = 'http://localhost:8001'
        Browser     = 'Dev'
    }
    prod = @{
        ComposeArgs = @('-p','omaum-prod','--env-file','..\.env.production','-f','docker-compose.yml','-f','docker-compose.prod.override.yml')
        ProfileArgs = @('--profile','production')
        Url         = 'http://localhost:8000'
        Browser     = 'Prod'
    }
}

function Ensure-WSL {
    try { & wsl.exe -l -q *> $null; Write-Info 'WSL ok'; return $true } catch { Write-Warn 'WSL não respondeu; verifique instalação'; return $false }
}

function Ensure-Docker {
    try { & docker info *> $null; Write-Info 'Docker pronto'; return $true } catch {}
    $desktop = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
    if (Test-Path $desktop) { Write-Info 'Abrindo Docker Desktop...'; Start-Process -FilePath $desktop | Out-Null } else { Write-Warn 'Docker Desktop não encontrado em C:\Program Files\Docker\Docker\Docker Desktop.exe'; return $false }
    Write-Info 'Aguardando Docker...'
    for($i=0;$i -lt 20;$i++){ Start-Sleep -Seconds 3; try { & docker info *> $null; Write-Info 'Docker iniciado'; return $true } catch {} }
    Write-Err 'Docker não respondeu a tempo'; return $false
}

function Prompt-Environment {
    Write-Host ''
    Write-Host 'Selecione o ambiente:'
    Write-Host '  1 - Desenvolvimento'
    Write-Host '  2 - Produção'
    while($true){ $a = Read-Host 'Opção (1/2)' ; switch($a){ '1' {return 'dev'} '2' {return 'prod'} default { Write-Warn 'Escolha 1 ou 2' } } }
}

function Prompt-Action {
    Write-Host ''
    Write-Host 'Ação:'
    Write-Host '  1 - Subir (up)'
    Write-Host '  2 - Reiniciar (down/up)'
    Write-Host '  3 - Parar (down)'
    Write-Host '  4 - Status'
    Write-Host '  5 - Logs (web)'
    Write-Host '  6 - Collectstatic'
    Write-Host '  7 - Migrate'
    Write-Host '  8 - Abrir no navegador'
    while($true){ $a = Read-Host 'Opção (1-8)' ; switch($a){
        '1' {return 'up'} '2' {return 'restart'} '3' {return 'down'} '4' {return 'status'} '5' {return 'logs'} '6' {return 'collectstatic'} '7' {return 'migrate'} '8' {return 'open'} default { Write-Warn 'Escolha 1-8' }
    }}
}

function Compose($envKey){
    $cfg = $envConfigs[$envKey]
    $args = @('compose') + $cfg.ProfileArgs + $cfg.ComposeArgs
    return $args
}

function Run-Compose($envKey, $extra){
    $args = Compose $envKey
    $args += $extra
    & docker @args
    return $LASTEXITCODE
}

try {
    if (-not $Environment) { $Environment = Prompt-Environment }
    if (-not $envConfigs.ContainsKey($Environment)) { throw "Ambiente inválido: $Environment" }
    if (-not $Action) { $Action = Prompt-Action }

    if (-not (Test-Path $dockerDir)) { throw "Pasta docker não encontrada em $dockerDir" }
    Push-Location $dockerDir
    Ensure-WSL | Out-Null
    if (-not (Ensure-Docker)) { throw 'Docker indisponível' }

    switch ($Action) {
        'up'        { if (Run-Compose $Environment @('up','-d') -ne 0) { throw 'Falha ao subir' } ; Write-Info 'Abrindo no navegador...'; Start-Process $envConfigs[$Environment].Url }
        'restart'   { if (Run-Compose $Environment @('down') -ne 0) { throw 'Falha no down' }; if (Run-Compose $Environment @('up','-d') -ne 0) { throw 'Falha ao subir' } ; Write-Info 'Abrindo no navegador...'; Start-Process $envConfigs[$Environment].Url }
        'down'      { if (Run-Compose $Environment @('down') -ne 0) { throw 'Falha ao parar' } }
        'status'    { Run-Compose $Environment @('ps') | Out-Null }
        'logs'      { Run-Compose $Environment @('logs','-f','omaum-web') | Out-Null }
        'collectstatic' { if (Run-Compose $Environment @('exec','-T','omaum-web','python','manage.py','collectstatic','--noinput','--clear') -ne 0) { throw 'Falha no collectstatic' } }
        'migrate'   { if (Run-Compose $Environment @('exec','-T','omaum-web','python','manage.py','migrate','--noinput') -ne 0) { throw 'Falha no migrate' } }
        'open'      { Start-Process $envConfigs[$Environment].Url }
    }

    if ($Action -in @('up','restart')) { Write-Info "Pronto: $($envConfigs[$Environment].Url)" }
    if ($Action -in @('status','logs')) { Write-Info 'Status/Logs exibidos acima.' }
}
catch {
    Write-Err $_
    exit 1
}
finally {
    Pop-Location -ErrorAction SilentlyContinue
}
