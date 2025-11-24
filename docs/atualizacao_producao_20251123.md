# Atualizacao de Producao - 23/11/2025

Este documento registra a sincronizacao completa do ambiente de producao com o ambiente de desenvolvimento do OMAUM utilizando o fluxo automatizado.

## Objetivo

- Replicar em producao todas as mudancas aplicadas no ambiente de desenvolvimento.
- Garantir execucao consistente dos passos: backup, importacao de dados, migracoes, coleta de estaticos, rebuild de containers e smoke tests.

## Script Utilizado

- `scripts/deploy/02_deploy_atualizar_producao.ps1`: fluxo oficial de deploy.
- `scripts/deploy/03_deploy_atualizar_producao_auto.ps1`: novo wrapper que responde automaticamente "sim" para todos os prompts, usando a mensagem de commit definida pelo operador.

### Execucao

```powershell
powershell -ExecutionPolicy Bypass -File scripts/deploy/03_deploy_atualizar_producao_auto.ps1 `
    -ProjectRoot "c:\projetos\omaum" `
    -CommitMessage "SYNC DEV -> PROD"
```

## Passos Automatizados

1. **Verificacao de pre-requisitos**: confirma Docker em execucao e containers `*-prod` ativos.
2. **Backup**: gera dump do banco `omaum_prod` e compacta em `backups/backup_<timestamp>.sql.zip`.
3. **Controle de versao**:
   - Caso existam alteracoes nao commitadas, cria commit com a mensagem informada.
   - Executa `git pull origin main` para alinhar com o remoto.
4. **Importacao dos dados de desenvolvimento**:
   - Seleciona o arquivo `dev_data_*.json` mais recente em `scripts/deploy/exports`.
   - Limpa o banco e carrega o dump via `loaddata` (sincronizando turmas, cursos etc.).
5. **Migracoes**: roda `makemigrations` e `migrate` via `docker-compose run --rm web`.
6. **Coleta de estaticos**: executa `collectstatic --clear` dentro do container web.
7. **Containers**: `docker-compose build --pull` seguido de `docker-compose up -d`.
8. **Healthcheck**: exibe `docker-compose ps`, logs recentes e testa acesso HTTP em `http://192.168.15.4`.
9. **Smoke tests**: conta registros de `Turma` e `Curso` para validar importacao.

## Observacoes

- O wrapper grava logs completos em arquivos temporarios e os exibe ao final.
- Em caso de erro o codigo de saida do script principal e propagado.
- O banco foi limpo e populado com o dataset `dev_data_20251123_212455.json`, garantindo equivalencia com o ambiente de desenvolvimento na data desta atualizacao.

Para futuras sincronizacoes, basta repetir o comando acima com a nova mensagem de commit e garantir que o arquivo `dev_data_*` mais recente esteja em `scripts/deploy/exports/`.
