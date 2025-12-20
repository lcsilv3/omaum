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

function Info($m){ Write-Host ("[deploy-prod] " + $m) -ForegroundColor Cyan }
function Ok($m){ Write-Host ("[deploy-prod] " + $m) -ForegroundColor Green }
function Warn($m){ Write-Host ("[deploy-prod] " + $m) -ForegroundColor Yellow }
function Err($m){ Write-Host ("[deploy-prod] " + $m) -ForegroundColor Red }

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$DockerDir = Join-Path $RepoRoot "docker"

if (-not (Test-Path $DockerDir)) { Err "Diretório docker não encontrado: $DockerDir"; exit 1 }

$compose = @(
  'compose',
  '--profile','production',
  '-p','omaum-prod',
  '--env-file','..\\.env.production',
  '-f','docker-compose.yml',
  '-f','docker-compose.prod.override.yml'
)

Push-Location $DockerDir
try {
  if ($Pull) {
    Info 'Executando docker compose pull (produção)...'
    docker @compose pull | Out-Host
  }

  $upArgs = @('up','-d')
  if ($Recreate) { $upArgs += '--force-recreate' }
  if ($Build)    { $upArgs += '--build' }

  Info ('Subindo serviços: docker ' + ($compose + $upArgs -join ' '))
  docker @compose @upArgs | Out-Host

  Info 'checando configurações de deploy (Django check --deploy)'
  docker @compose exec -T omaum-web python manage.py check --deploy | Out-Host

  if (-not $SkipMigrate) {
    Info 'Aplicando migrations (manage.py migrate --noinput)'
    docker @compose exec -T omaum-web python manage.py migrate --noinput | Out-Host
  } else { Warn 'Pulando migrations por parâmetro' }

  if (-not $SkipCollectstatic) {
    Info 'Coletando arquivos estáticos (manage.py collectstatic --noinput --clear)'
    docker @compose exec -T omaum-web python manage.py collectstatic --noinput --clear | Out-Host
    Ok 'collectstatic concluído. Lembre-se de invalidar cache de CDN se houver.'
  } else { Warn 'Pulando collectstatic por parâmetro' }

  Info 'Status dos serviços:'
  docker @compose ps | Out-Host

  Info 'Últimas 50 linhas de log do omaum-web:'
  docker @compose logs --tail=50 omaum-web | Out-Host

  Ok 'Deploy de produção finalizado.'
}
finally { Pop-Location }
