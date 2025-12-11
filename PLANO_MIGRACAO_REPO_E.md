# PLANO DE MIGRACAO DO REPOSITORIO PARA E:\projetos\omaum

Data de criacao: 2025-12-10T00:00:00Z

## Objetivo

Mover o workspace do repositorio de `C:\projetos\omaum` para `E:\projetos\omaum`, mantendo os stacks `dev` (binds em E:) e `prod-local` (binds em D:) funcionais e sincronizados.

## Estado atual (resumo)

- Repo copiado para `E:\projetos\omaum` (destino principal); copia original permanece em `C:\projetos\omaum` como fallback temporario.
- Stacks: `dev` exposto (5432/8000/6379) usando binds em `E:\docker\omaum\dev`; `prod-local` interno usando binds em `D:\docker\omaum\prod`.
- Overrides e envs: `docker/docker-compose.yml` + `docker/docker-compose.dev.override.yml` + `docker/docker-compose.prod.override.yml`; envs `.env.dev` e `.env.prod` na raiz.

## Inventario de referencias ao caminho atual

**Alvos prioritarios para atualizar/parametrizar:**

- Documentacao: `README.md`, `docs/GUIA_INSTALACAO.md`, `docs/atualizacao_producao_20251123.md`.
- Scripts de deploy: `scripts/deploy/01_export_dev_data.ps1`, `scripts/deploy/02_deploy_atualizar_producao.ps1`, `scripts/deploy/03_deploy_atualizar_producao_auto.ps1`.
- Scripts auxiliares: `scripts/importar_codigos_planilha.py` (xlsx), `scripts/legacy/collect_atividade_ritualistica_code.py` (project_root), `scripts/testes_manuais/test_fixes.py` (js_file), `migrar_backup_antigo.py` (DEFAULT_OUTPUT_PATH).
- Bat utilitario: `tests/configs/resumir_qualidade_codigo.bat`.
- Comentarios de cabecalho em alguns arquivos (ex.: `turmas/services.py`, `presencas/services/analytics.py`) – podem ser ajustados ou removidos.

**Baixa prioridade (gerados/logs; pode apenas documentar/limpar se desejar):**

- Arquivos de cobertura em `htmlcov/` e logs em `scripts/deploy/logs/`.
- Arquivo de resultado `tests/resultado_testes.txt`.

## Plano executivo (atualizar conforme executar)

1. Congelar ambiente antes de mover
   - Parar watchers no VS Code.
   - Derrubar stacks:
      - `docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.override.yml --env-file .env.dev down`
      - `docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.override.yml --env-file .env.prod down`
   - Confirmar que nao ha contenedores com project name `omaum-dev` ou `omaum-prod` rodando (`docker ps`).

1. Backup rapido (opcional mas recomendado)
   - Criar zip de `C:\projetos\omaum` ou snapshot com `robocopy` para pasta temporaria (ex.: `E:\tmp\omaum_backup`).

1. Copiar/mover repo para E:\projetos
   - Garantir que Docker Desktop tem E: compartilhado.
   - Criar destino `E:\projetos` se nao existir.
   - Copiar preservando ACLs e timestamps (exemplo PowerShell):

```powershell
robocopy C:\projetos\omaum E:\projetos\omaum /MIR /XJ /XD .venv /R:1 /W:1
```

   - Opcional: manter `.venv` em C: ou recriar em E: apos a copia.

1. Atualizar referencias fixas (usar caminhos relativos sempre que possivel)
   - Rodar varredura para confirmar pendencias (a partir do novo path):

```powershell
Set-Location -Path "E:\projetos\omaum"
Get-ChildItem -Recurse -File |
   Where-Object { $_.FullName -notmatch "htmlcov" -and $_.FullName -notmatch "scripts\\deploy\\logs" } |
   Select-String -Pattern "C\\\\projetos\\\\omaum|c:/projetos/omaum"
```

   - Ajustar arquivos prioritarios listados acima para apontar para `E:\projetos\omaum` ou, preferencialmente, usar caminhos relativos (`$PSScriptRoot`, `Path(__file__).parent`, `$(pwd)`).
   - Revisar docs para instruir uso de `E:\projetos\omaum` como novo caminho padrao.

1. Validar stacks no novo local
   - Reabrir VS Code a partir de `E:\projetos\omaum`.
   - Subir dev: `docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.override.yml --env-file .env.dev up -d`; checar `docker compose ps` (postgres 5432, web 8000, redis 6379).
   - Subir prod-local (se necessario): `docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.override.yml --env-file .env.prod up -d`; checar que nenhum port-forward foi aberto.
   - Sanity check:
      - `docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.override.yml --env-file .env.dev exec omaum-web python manage.py check`
      - `docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.override.yml --env-file .env.dev exec omaum-db psql -U omaum -d omaum -c "select 1;"`

1. Limpeza e comunicacao
   - Atualizar este plano com o que foi concluido/ajustado.
   - Se tudo ok, remover/sincronizar a copia antiga em `C:\projetos\omaum`.
   - Comunicar novo caminho nos docs/README para evitar confusoes futuras.

## Log de execucao (preencha durante a execucao)

- [x] 2025-12-10: Derrubados stacks dev e prod-local via docker compose (envs na raiz).
- [x] 2025-12-10: Copia inicial realizada para `E:\projetos\omaum` com `robocopy /MIR /XD .venv`.
- [x] 2025-12-10: Stacks dev/prod-local iniciados em `E:\projetos\omaum`; `manage.py check` OK; `psql -U omaum_user -d omaum_dev -c "select 1;"` OK.
- [ ] 2025-12-10: Remoção/redirect de `C:\projetos\omaum` -> `E:\projetos\omaum` pendente (Move-Item falhou por caminho em uso; comando sugerido após fechar VS Code: `Move-Item C:\projetos\omaum C:\projetos\omaum_old; cmd /c mklink /J C:\projetos\omaum E:\projetos\omaum`).
- [ ] Data/Passo/Observacao:

