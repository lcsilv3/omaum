# Plano e execução: padronização de stacks e swap de banco

Data: 2025-12-10
Responsável: Copilot (GPT-5.1-Codex-Max)

## Objetivos
- Fixar um único project name para desenvolvimento (`omaum-dev`) e evitar novos prefixos/volumes.
- Trazer o conteúdo do stack antigo (volume `omaum-dev_omaum_db_data`) para o stack atual.
- Fazer backup do que estava em uso antes do swap.
- Limpar volumes obsoletos.

## Decisões
- Project name padrão: `omaum-dev` (definido em `.env` na raiz e reforçado via variável de ambiente).
- Estratégia de banco: swap completo para o volume antigo `omaum-dev_omaum_db_data` (que contém o aluno e tabelas de localização).
- Media: usar o volume `omaum-dev_omaum_media` (já tinha `alunos/fotos`); o volume `docker_omaum_media` estava vazio.
- Static/staticfiles: regeneráveis, não migrados.
- Logs antigos: backup tar antes de remover volume.
- Volumes `omaum-prod_*`: mantidos (não confirmada a utilidade); sujeitos a limpeza futura se confirmado que não são usados.

## Passos executados
1) Padronização do project name
   - `.env` atualizado com `COMPOSE_PROJECT_NAME=omaum-dev`.
   - Uso explícito de env na CLI para garantir o prefixo: 
     - Down antigo: `$env:COMPOSE_PROJECT_NAME="docker"; docker compose -f docker/docker-compose.yml down`.
     - Up com padrão: `$env:COMPOSE_PROJECT_NAME="omaum-dev"; docker compose -f docker/docker-compose.yml up -d`.

2) Backups
   - Dump do banco atual (prefixo antigo `docker_...`): `backups/backup_db_current_before_swap_20251210.sql`.
   - Dump do banco antigo (volume alvo): `backups/backup_db_old_volume_20251210.sql`.
   - Tar do volume de logs antigo: `backups/volume_docker_omaum_logs_20251210.tar.gz`.

3) Swap do banco
   - Derrubado stack antigo (`docker`), subido stack com `omaum-dev` usando volume `omaum-dev_omaum_db_data`.
   - Validação: `SELECT id, cpf, nome, ativo FROM alunos_aluno WHERE cpf='81991045700';` retornou o aluno id=55 ativo=falso. Tabelas de localização já estavam carregadas (27 estados, 5.571 cidades).

4) Media/static/logs
   - `docker_omaum_media` estava vazio; `omaum-dev_omaum_media` mantido (possui `alunos/fotos`).
   - Static/staticfiles: não migrados (gerados na build). 
   - Logs antigos preservados via tar antes da limpeza; logs atuais em `omaum-dev_omaum_logs`.

5) Limpeza de volumes
   - Removidos (prefixo antigo): `docker_omaum_db_data`, `_dev`, `_prod`, `docker_omaum_logs`, `_dev`, `_prod`, `docker_omaum_media`, `_dev`, `_prod`, `docker_omaum_redis_data`, `_dev`, `_prod`, `docker_omaum_static`, `_dev`, `_prod`, `docker_omaum_staticfiles`, `_dev`, `_prod`, e `omaum-db_data`.
   - Removidos (prod, após backup tar): `omaum-prod_omaum_db_data`, `omaum-prod_omaum_db_data_prod`, `omaum-prod_omaum_logs`, `omaum-prod_omaum_logs_prod`, `omaum-prod_omaum_media`, `omaum-prod_omaum_media_prod`, `omaum-prod_omaum_redis_data`, `omaum-prod_omaum_redis_data_prod`, `omaum-prod_omaum_static`, `omaum-prod_omaum_static_prod`, `omaum-prod_omaum_staticfiles_prod`. Backups gerados em `backups/*_20251210.tar.gz`.
   - Restantes (dev): `omaum-dev_omaum_db_data`, `omaum-dev_omaum_media`, `omaum-dev_omaum_static`, `omaum-dev_omaum_staticfiles`, `omaum-dev_omaum_logs`, `omaum-dev_omaum_redis_data`.

## Como operar daqui em diante

- Guia detalhado dev/prod-local com discos separados: `docs/ambientes_dev_prod.md`.
- Alvos de conveniência no `Makefile` (aplicam project name e overrides):
   - Dev: `make up-dev`, `make down-dev`, `make logs-dev`, `make ps-dev` (usa `COMPOSE_PROJECT_NAME=omaum-dev`, override em `docker/docker-compose.dev.override.yml`, binds em `E:`).
   - Prod-local: `make up-prod-local`, `make down-prod-local`, `make logs-prod-local`, `make ps-prod-local` (usa `COMPOSE_PROJECT_NAME=omaum-prod`, override em `docker/docker-compose.prod.override.yml`, binds em `D:` e portas 5433/8001/6380).
- Rodar sempre a partir da raiz do repositório com o `.env` presente. Para garantir o prefixo manualmente, use:
   - `PS> $env:COMPOSE_PROJECT_NAME="omaum-dev"; docker compose -f docker/docker-compose.yml up -d`
   - Para derrubar: `PS> $env:COMPOSE_PROJECT_NAME="omaum-dev"; docker compose -f docker/docker-compose.yml down`
- Se preferir não setar env manualmente, mantenha o `.env` e rode do mesmo diretório do `docker-compose.yml` com `docker compose ...` — mas, na prática, definir a env na chamada evitou quedas para o prefixo `docker`.

   ### Estrutura em disco (criada)

   - Dev (binds em `E:/docker/omaum/dev/...`): `db`, `media`, `static`, `staticfiles`, `logs`, `redis`.
   - Prod-local (binds em `D:/docker/omaum/prod/...`): `db`, `media`, `static`, `staticfiles`, `logs`, `redis`.
   - Compose principal sem `container_name`; URLs internas usam `omaum-db`/`omaum-redis` para coexistir por project name.

   ### Estado atual

   - Stack dev ativo com override e binds (subido via `docker compose -p omaum-dev --env-file .env.dev -f docker/docker-compose.yml -f docker/docker-compose.dev.override.yml up -d`).
   - Banco restaurado do backup `backups/backup_db_old_volume_20251210.sql` para o bind `E:/docker/omaum/dev/db` (consulta CPF 81991045700 retorna id=55).
   - Media copiada do volume antigo `omaum-dev_omaum_media` para `E:/docker/omaum/dev/media`.
   - Stack prod-local ativo com binds em `D:/docker/omaum/prod/...` (subido via `docker compose -p omaum-prod --env-file .env.prod -f docker/docker-compose.yml -f docker/docker-compose.prod.override.yml up -d`).
   - Portas expostas apenas no override dev (5432/8000/6379). O compose base não publica portas; prod-local não expõe portas externas por padrão.

## Pendências / observações
- Volumes `omaum-prod_*` não foram removidos por falta de confirmação de uso.
- Se desejar, posso gerar dumps/tars desses volumes antes de descartá-los.
- Recomenda-se rodar smoke/pytest após mudanças (não executado aqui).
