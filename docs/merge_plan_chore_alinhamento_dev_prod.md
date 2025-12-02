# Plano de merge – branch `chore/alinhamento-dev-prod`

## Objetivo

Consolidar no `main` apenas o que já foi validado e testado em desenvolvimento, garantindo que cada conjunto de mudanças seja revisado separadamente e que o deploy em Docker continue previsível.

## Commits no branch

1. `fcc2b51e` – *chore(alunos): ajusta migrations de codigos*
   - Remove a migration 0006 antiga e aponta 0007 para a nova cadeia `0006_codigo_ativo_tipocodigo_ativo_and_more`.
   - **Ação**: revisar com o time de dados para confirmar que a migration legacy pode ser removida com segurança. Se sim, abrir PR exclusiva de migrations.

2. `1c44fc34` – *feat(alunos): melhora seletor do preview de foto*
   - Adiciona `id="foto-preview-container"` e atualiza o JS do formulário para usar o ID (evita conflitos quando há múltiplos blocos com a mesma classe).
   - **Ação**: pode ser incluído na mesma PR das migrations ou em PR separada focada em UX/JS, rodando smoke test de formulários.

3. `71e4833a` – *chore(docker): reorganiza stack dev e script de inicializacao*
   - Renomeia serviços para `*-dev`, ajusta portas (DB 5433, Redis 6380, nginx 8080), adiciona variáveis padrão e duplica o script `iniciar_dev_docker.bat` para `bat/iniciar_dev_docker.bat`.
   - **Ação**: abrir PR dedicada de infraestrutura. Antes de mergear, validar impacto nas instruções (`DOCKER_AMBIENTES.md`) e alinhar se o compose dev continuará usando os nomes/portas antigos.

4. `773c2196` – *feat(turmas): adiciona campos data_inicio e data_fim*
   - Adiciona os campos às models, exigindo nova migration.
   - **Ação**: gerar migration correspondente (`python manage.py makemigrations turmas`), incluir na PR e alinhar com o time responsável pelas telas para ajustar formulários/listas.

5. `4d234cb1` – *chore(backups): versiona dumps e scripts auxiliares*
   - Adiciona dumps SQL/JSON/SQLite e scripts `limpar_backup.py`, `migrate_sqlite_to_postgres.py` etc.
   - **Ação**: combinar com o time se esses arquivos ficarão no repositório principal ou em storage separado (Git LFS / Azure Storage). Caso fiquem, mover para `backups/` com README descrevendo como usá-los e evitar que sejam atualizados sem revisão.

## Estratégia sugerida

1. Criar PRs menores e temáticas, na ordem: migrations → UX do formulário → novos campos de turma → infra Docker → backups.
2. Em cada PR, rodar `pytest` do app afetado e, para Docker, executar `docker compose up -d` nos dois arquivos para garantir compatibilidade.
3. Após cada merge em `main`, seguir o ritual documentado (pull, build/pull, up, migrate, smoke tests).

## Próximos passos

- Validar com o time se a migration 0006 pode ser removida definitivamente.
- Decidir se os dumps permanecerão versionados no Git.
- Assim que houver aprovação, abrir a primeira PR (migrations) a partir de `chore/alinhamento-dev-prod` rebaseado em `main`.
