# Reinício rápido do container de produção (omaum-prod)
$ErrorActionPreference = 'Stop'
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$DockerDir = Join-Path $RepoRoot "docker"
Push-Location $DockerDir
try {
  docker compose --profile production -p omaum-prod --env-file ..\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml restart omaum-web | Out-Host
} finally { Pop-Location }
