# Guia de operação local: dev e prod isolados

Data: 2025-12-10
Responsável: Copilot (GPT-5.1-Codex-Max)

## Objetivos

- Permitir rodar dev e prod-local na mesma máquina sem colisão.
- Fixar prefixos (`COMPOSE_PROJECT_NAME`): `omaum-dev` e `omaum-prod`.
- Separar discos: dev em `E:`; prod-local em `D:`.
- Evitar comandos fora da raiz e evitar project names divergentes.

## Pré-requisitos

- Docker Desktop com compartilhamento de discos `D:` e `E:` habilitado.
- Pastas criadas:
  - `E:/docker/omaum/dev/db`, `E:/docker/omaum/dev/media`, `E:/docker/omaum/dev/static`, `E:/docker/omaum/dev/staticfiles`, `E:/docker/omaum/dev/logs`, `E:/docker/omaum/dev/redis`.
  - `D:/docker/omaum/prod/db`, `D:/docker/omaum/prod/media`, `D:/docker/omaum/prod/static`, `D:/docker/omaum/prod/staticfiles`, `D:/docker/omaum/prod/logs`, `D:/docker/omaum/prod/redis`.
- Arquivos de ambiente (exemplos):
  - `.env.dev` (pode reutilizar `.env` atual) com `COMPOSE_PROJECT_NAME=omaum-dev` e variáveis de dev.
  - `.env.prod` com `COMPOSE_PROJECT_NAME=omaum-prod` e variáveis do stack prod-local.

## Comandos recomendados (Makefile)

- Dev: `make up-dev` / `make down-dev` / `make logs-dev` / `make ps-dev`.
- Prod-local: `make up-prod-local` / `make down-prod-local` / `make logs-prod-local` / `make ps-prod-local`.
- Os alvos checam se `docker/docker-compose.yml` está presente (evita rodar fora da raiz) e aplicam `COMPOSE_PROJECT_NAME` apropriado.
- Atalhos Windows ajustados:
  - `iniciar_dev_docker.bat`: sobe dev com project `omaum-dev`, `.env.dev` e override dev (binds em E:).
  - `bat/atualizar_docker.bat`: reconstrói e sobe dev ou prod-local usando compose base + overrides + env adequados.

## Estrutura de overrides

- `docker/docker-compose.dev.override.yml`: binds para `E:` (db, media, static, staticfiles, logs, redis).
- `docker/docker-compose.prod.override.yml`: binds para `D:` (db, media, static, staticfiles, logs, redis) e portas distintas (sugerido: 5433/8001/6380) para coexistir com dev.

> Observação: o compose base ainda publica 5432/8000/6379. Se usar o override, remova as portas do arquivo base para o stack prod-local não tentar expor 5432/8000/6379 e evitar conflito. Alternativamente, mantenha apenas as portas no override.

## Sobre coexistência

- Para rodar dev e prod-local juntos, é necessário remover/neutralizar `container_name` fixo no `docker-compose.yml` principal e garantir mapeamentos de porta distintos (override prod-local já sugere portas diferentes). Enquanto `container_name` existir, suba apenas um stack por vez.
- `container_name` foi removido do compose principal e `DATABASE_URL`/`REDIS_URL` agora apontam para os nomes de serviço (`omaum-db`, `omaum-redis`), permitindo coexistência com project names distintos.

## Migração de dados para os binds

- Dev: restaurar dump para o Postgres apontando para `E:/docker/omaum/dev/db` (stack dev com override ativo). Media: copiar conteúdos para `E:/docker/omaum/dev/media`.
- Prod-local: restaurar dos tars em `backups/*_20251210.tar.gz` para as pastas em `D:` ou iniciar vazio, conforme necessidade.

## Boas práticas

- Sempre rodar `make` a partir da raiz do repositório.
- Usar os alvos `make` em vez de comandos diretos para evitar project name errado.
- Não compartilhar credenciais entre `.env.dev` e `.env.prod`; use arquivos separados.
- Mantê-los sob controle: dev = `omaum-dev`, prod-local = `omaum-prod`.
