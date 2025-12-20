#requires -Version 7.0
<#!
  Watcher de desenvolvimento para o projeto OMAUM (Windows/PowerShell)
  - Ao modificar arquivos .py => reinicia o container omaum-web
  - Ao modificar arquivos estáticos (static/**) => executa collectstatic no container de dev

  Observa o workspace atual e faz debounce dos eventos para evitar tempestade de reinícios.
!>

param(
  [int]$DebounceMs = 1500
)

$ErrorActionPreference = 'Stop'

function Write-Info($msg) { Write-Host ("[watch-dev] " + $msg) -ForegroundColor Cyan }
function Write-Warn($msg) { Write-Host ("[watch-dev] " + $msg) -ForegroundColor Yellow }
function Write-Ok($msg)   { Write-Host ("[watch-dev] " + $msg) -ForegroundColor Green }
function Write-Err($msg)  { Write-Host ("[watch-dev] " + $msg) -ForegroundColor Red }

# Caminhos base
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$DockerDir = Join-Path $RepoRoot "docker"

if (-not (Test-Path $DockerDir)) {
  Write-Err "Diretório docker não encontrado em $DockerDir"
  exit 1
}

# Comandos utilitários
function Restart-Container {
  Write-Warn "Reiniciando container omaum-web (mudança em Python)..."
  Push-Location $DockerDir
  try {
    docker compose -p omaum-dev restart omaum-web | Out-Host
    Write-Ok "Container reiniciado."
  } finally { Pop-Location }
}

function Run-Collectstatic {
  Write-Warn "Executando collectstatic (mudança em arquivos estáticos)..."
  Push-Location $DockerDir
  try {
    docker compose -p omaum-dev --env-file ..\.env.dev -f docker-compose.yml exec -T omaum-web python manage.py collectstatic --noinput --clear | Out-Host
    Write-Ok "collectstatic concluído. Faça Hard Refresh (Ctrl+Shift+R)."
  } finally { Pop-Location }
}

# Debounce timers
$pyTimer = $null
$staticTimer = $null

# Filtros
$pathPy      = (Join-Path $RepoRoot "**/*.py")
$pathStatic  = (Join-Path $RepoRoot "static/*");
$pathAppStat = (Join-Path $RepoRoot "*/static/*")

# Usar .NET FileSystemWatcher para alto desempenho
$watcher = [System.IO.FileSystemWatcher]::new($RepoRoot)
$watcher.IncludeSubdirectories = $true
$watcher.EnableRaisingEvents = $true
$watcher.NotifyFilter = [System.IO.NotifyFilters]'FileName, LastWrite, Size, DirectoryName'

Register-ObjectEvent -InputObject $watcher -EventName Changed -SourceIdentifier WatchChanged -Action {
  param($sender, $e)
  $full = $e.FullPath
  if ($full -match '\\.git' -or $full -match '\\htmlcov') { return }

  if ($full.EndsWith('.py')) {
    if ($pyTimer) { $pyTimer.Stop(); $pyTimer.Dispose() }
    $pyTimer = New-Object Timers.Timer $using:DebounceMs
    $pyTimer.AutoReset = $false
    $pyTimer.add_Elapsed({ Restart-Container })
    $pyTimer.Start()
  }
  elseif ($full -match '\\static\\' -and ($full -match '\\css\\|\\js\\|\\img\\|\\images\\|\\fonts\\')) {
    if ($staticTimer) { $staticTimer.Stop(); $staticTimer.Dispose() }
    $staticTimer = New-Object Timers.Timer $using:DebounceMs
    $staticTimer.AutoReset = $false
    $staticTimer.add_Elapsed({ Run-Collectstatic })
    $staticTimer.Start()
  }
}

Register-ObjectEvent -InputObject $watcher -EventName Created -SourceIdentifier WatchCreated -Action { $ExecutionContext.InvokeCommand.InvokeScript($event.MessageData) } -MessageData {
  param()
  # Reaproveitar a mesma lógica do Changed
}

Write-Info "Watcher iniciado em $RepoRoot"
Write-Info "- .py => restart container"
Write-Info "- static/** => collectstatic"

# Mantém processo vivo
while ($true) { Start-Sleep -Seconds 60 }
