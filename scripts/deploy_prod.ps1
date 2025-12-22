#requires -Version 7.0
<#!
Deploy de Produção - OMAUM (Windows/PowerShell)

Pré-requisitos no host de produção:
- Docker + Docker Compose V2
- Arquivos docker-compose.yml e docker-compose.prod.override.yml
- Arquivo de variáveis: ..\.env.production

O que este script faz (por padrão):
1) Sobe/atualiza os serviços com o profile production
2) Executa check --deploy
3) Executa migrate --noinput
4) Executa collectstatic --noinput --clear
5) Mostra status e últimas linhas de log

Parâmetros úteis:
- -SkipMigrate          => Não roda migrations
- -SkipCollectstatic    => Não roda collectstatic
- -Pull                 => Executa docker compose pull antes de subir
- -Recreate             => Força recriação de containers (up --force-recreate)
- -Build                => Força build de imagens (up --build)
!>

param(
  [switch]$SkipMigrate,
  [switch]$SkipCollectstatic,
  [switch]$Pull,
  [switch]$Recreate,
  [switch]$Build
)

$ErrorActionPreference = 'Stop'

$scriptPath = $PSCommandPath
# Caminhos absolutos (self-hosted runner Windows)
$RepoRoot   = 'E:\projetos\omaum'
$DockerDir  = 'E:\projetos\omaum\docker'

Write-Host "[deploy-prod] scriptPath=$scriptPath" -ForegroundColor Cyan
Write-Host "[deploy-prod] PSScriptRoot=$PSScriptRoot" -ForegroundColor Cyan
Write-Host "[deploy-prod] RepoRoot=$RepoRoot" -ForegroundColor Cyan
Write-Host "[deploy-prod] DockerDir=$DockerDir" -ForegroundColor Cyan

if (-not (Test-Path $DockerDir)) { Write-Error "Diretório docker não encontrado: $DockerDir"; exit 1 }

<#
  Detecta automaticamente o caminho do arquivo .env.production.
  Prioridades:
  1) Repo raiz:    $RepoRoot/.env.production
  2) Pasta docker: $DockerDir/.env.production
  3) Caminhos absolutos conhecidos (E:\projetos\omaum)
  Se não encontrado, prossegue sem --env-file e emite aviso.
#>

$envFileCandidates = @()
if ($RepoRoot)   { $envFileCandidates += (Join-Path $RepoRoot ".env.production") }
if ($DockerDir)  { $envFileCandidates += (Join-Path $DockerDir ".env.production") }
$envFileCandidates += @("E:\projetos\omaum\.env.production", "E:\projetos\omaum\docker\.env.production")

$envFilePath = $null
foreach ($candidate in $envFileCandidates) {
  if (Test-Path $candidate) { $envFilePath = (Resolve-Path $candidate).Path; break }
}

if ($envFilePath) {
  Write-Host "[deploy-prod] Usando env-file: $envFilePath" -ForegroundColor Cyan
  $envFileArg = @('--env-file', $envFilePath)
} else {
  Write-Warning '[deploy-prod] Arquivo .env.production não encontrado; prosseguindo sem --env-file (variáveis devem estar no ambiente).'
  $envFileArg = @()
}

$compose = @(
  'compose',
  '--profile','production',
  '-p','omaum-prod'
) + $envFileArg + @(
  '-f', 'E:\projetos\omaum\docker\docker-compose.prod.yml'
)

Write-Host "[deploy-prod] DockerDir (debug) = '$DockerDir'" -ForegroundColor Yellow
Write-Host "[deploy-prod] compose args (debug) = " -ForegroundColor Yellow
Write-Host ($compose -join ' ') -ForegroundColor Yellow

Push-Location 'E:\projetos\omaum\docker'
try {
  if ($Pull) {
    Write-Host '[deploy-prod] Executando docker compose pull (produção)...' -ForegroundColor Cyan
    docker @compose pull | Out-Host
  }

  $upArgs = @('up','-d')
  if ($Recreate) { $upArgs += '--force-recreate' }
  if ($Build)    { $upArgs += '--build' }

  Write-Host ('[deploy-prod] Subindo serviços: docker ' + ($compose + $upArgs -join ' ')) -ForegroundColor Cyan
  docker @compose @upArgs | Out-Host

  Write-Host '[deploy-prod] checando configurações de deploy (Django check --deploy)' -ForegroundColor Cyan
  docker @compose exec -T omaum-web python manage.py check --deploy | Out-Host

  if (-not $SkipMigrate) {
    Write-Host '[deploy-prod] Aplicando migrations (manage.py migrate --noinput)' -ForegroundColor Cyan
    docker @compose exec -T omaum-web python manage.py migrate --noinput | Out-Host
  } else { Write-Warning '[deploy-prod] Pulando migrations por parâmetro' }

  if (-not $SkipCollectstatic) {
    Write-Host '[deploy-prod] Coletando arquivos estáticos (manage.py collectstatic --noinput --clear)' -ForegroundColor Cyan
    docker @compose exec -T omaum-web python manage.py collectstatic --noinput --clear | Out-Host
    Write-Host '[deploy-prod] collectstatic concluído. Lembre-se de invalidar cache de CDN se houver.' -ForegroundColor Green
  } else { Write-Warning '[deploy-prod] Pulando collectstatic por parâmetro' }

  Write-Host '[deploy-prod] Status dos serviços:' -ForegroundColor Cyan
  docker @compose ps | Out-Host

  Write-Host '[deploy-prod] Últimas 50 linhas de log do omaum-web:' -ForegroundColor Cyan
  docker @compose logs --tail=50 omaum-web | Out-Host

  Write-Host '[deploy-prod] Deploy de produção finalizado.' -ForegroundColor Green
}
finally { Pop-Location }
