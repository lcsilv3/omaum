# Deploy em Produção – Quickstart

Este guia cobre o fluxo de deploy com Docker Compose usando o profile `production`.

## Pré-requisitos
- Docker + Docker Compose v2
- Variáveis preenchidas em `docker/.env.production`
- Arquivos `docker/docker-compose.yml` e `docker/docker-compose.prod.override.yml`

## Comandos principais (VS Code Tasks)
- "Prod: Deploy (up + migrate + collectstatic)"
  - Executa `scripts/deploy_prod.ps1`:
    - `docker compose --profile production ... up -d`
    - `python manage.py check --deploy`
    - `python manage.py migrate --noinput`
    - `python manage.py collectstatic --noinput --clear`
- "Prod: Reiniciar omaum-web"
  - Executa `scripts/restart_prod.ps1`

## Uso via terminal (alternativa)
```powershell
# Deploy completo
pwsh -File scripts/deploy_prod.ps1

# Opções
pwsh -File scripts/deploy_prod.ps1 -Pull -Build -Recreate
pwsh -File scripts/deploy_prod.ps1 -SkipMigrate -SkipCollectstatic

# Reinício rápido
pwsh -File scripts/restart_prod.ps1
```

## Checklist pós-deploy
- Acessar aplicação e validar login/fluxos críticos
- Conferir `docker compose ps` no host
- Ver últimas linhas de log: `docker compose logs --tail=100 omaum-web`
- Instruir front-end sobre invalidação de cache se houver CDN

## Observações
- Em produção, alterações devem passar por este fluxo (sem watchers).
- Para CI/CD, crie um pipeline que faça build da imagem, publique no registry e rode `deploy_prod.ps1` no servidor (via SSH/runner).
