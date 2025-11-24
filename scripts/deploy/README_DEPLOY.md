# Deploy Automático - OMAUM Produção

## 📋 Visão Geral

Sistema automatizado de deploy para ambiente de produção do OMAUM, executando em **DESKTOP-OAE3R5M (192.168.15.4)**.

## 🚀 Como Executar

### Opção 1: Deploy Interativo (Recomendado)
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\deploy\02_deploy_atualizar_producao.ps1
```

### Opção 2: Deploy Automatizado (apenas commit message)
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\deploy\03_deploy_atualizar_producao_auto.ps1
```

## 📝 O que o Deploy Faz

1. **Backup do Banco** (PostgreSQL)
   - Arquivo: `backups/backup_TIMESTAMP.sql.zip`
   - Usuário: `omaum_app`
   - Banco: `omaum_prod`

2. **Atualização de Código**
   - Commit automático de alterações pendentes
   - Pull do branch master
   - Mensagem via variável `OMAUM_DEPLOY_COMMIT_MESSAGE`

3. **Migrações Django**
   - `makemigrations` (detecção automática)
   - `migrate` (aplicação)

4. **Importação de Dados** (opcional, `-SemDados` para pular)
   - Usa fixture mais recente em `scripts/deploy/exports/`
   - Limpa banco antes de importar (`flush`)

5. **Arquivos Estáticos**
   - `collectstatic --clear`
   - Copia para volumes Docker

6. **Rebuild Containers**
   - Build com `--pull` (atualiza imagens base)
   - Reinicia com healthcheck

7. **Validação**
   - Testa conexão com containers
   - Verifica dados no banco
   - Smoke tests básicos

## 📊 Logs

Cada execução gera log timestamped:
```
scripts/deploy/logs/deploy_YYYYMMDD_HHMMSS.log
```

Formato:
```
[YYYY-MM-DD HH:mm:ss] [LEVEL] Mensagem
```

Níveis: `INFO`, `SUCCESS`, `WARNING`, `ERROR`, `STEP`, `DEBUG`

## 🐳 Containers

| Nome | Porta | Descrição |
|------|-------|-----------|
| omaum-nginx-prod | 80, 443 | Nginx reverse proxy |
| omaum-web-prod | 8000 | Django + Gunicorn |
| omaum-celery-prod | - | Celery worker |
| omaum-celery-beat-prod | - | Celery beat scheduler |
| omaum-db-prod | 5432 | PostgreSQL 15 |
| omaum-redis-prod | 6379 | Redis cache/broker |

## 🔧 Correções de Fixtures

### Problema: Campo `situacao` VARCHAR(1)
Fixtures antigos continham valores como "ATIVO" (5 chars) quando o modelo aceita apenas 1 char ("a", "d", "f", "e").

**Solução:**
```powershell
python scripts\deploy\fix_fixture_situacao.py caminho/fixture.json
```

O script:
- Converte "ATIVO" → "a", "DESLIGADO" → "d", etc.
- Remove BOM UTF-8 que causa erro de deserialização
- Cria backup do original como `*_original.json`

### Problema: BOM UTF-8
PowerShell's `ConvertTo-Json | Set-Content` adiciona BOM, causando:
```
JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig)
```

**Solução automática no script** `fix_fixture_situacao.py`:
```python
# Verifica e remove BOM UTF-8 (EF BB BF)
if content.startswith(b'\xef\xbb\xbf'):
    content = content[3:]
```

## 🔐 Acesso

- **Web:** http://192.168.15.4
- **Admin:** http://192.168.15.4/admin
  - Usuário: `admin`
  - Senha: `admin123`

## 📦 Estrutura de Arquivos

```
scripts/deploy/
├── 02_deploy_atualizar_producao.ps1    # Script principal
├── 03_deploy_atualizar_producao_auto.ps1  # Wrapper automático
├── fix_fixture_situacao.py             # Corretor de fixtures
├── exports/                            # Fixtures para importação
│   └── dev_data_TIMESTAMP.json
├── logs/                               # Logs de execução
│   └── deploy_TIMESTAMP.log
└── README_DEPLOY.md                    # Esta documentação

backups/
└── backup_TIMESTAMP.sql.zip            # Backups do PostgreSQL
```

## ⚙️ Parâmetros

### 02_deploy_atualizar_producao.ps1

```powershell
-SemBackup    # Pula etapa de backup (NÃO RECOMENDADO)
-SemDados     # Pula importação de dados de desenvolvimento
-Verbose      # Mostra comandos docker sendo executados
```

### Variáveis de Ambiente

```powershell
$env:OMAUM_DEPLOY_COMMIT_MESSAGE = "Sua mensagem"
```
Se definida, evita prompt interativo para mensagem de commit.

## 🐛 Troubleshooting

### Nginx crash loop
**Erro:** `resolving names at run time requires upstream in shared memory`

**Solução:** Arquivo `docker/nginx/default.conf` não deve usar `resolve` na diretiva `server`:
```nginx
upstream omaum_web {
    server omaum-web:8000;  # ✓ Correto (sem resolve)
}
```

Rebuild necessário:
```powershell
docker compose -f docker\docker-compose.prod.yml build omaum-nginx
docker compose -f docker\docker-compose.prod.yml up -d omaum-nginx
```

### Fixtures incompatíveis
**Erro:** `Turma has no field named 'data_inicio'`

**Causa:** Fixture antigo com estrutura de modelo desatualizada.

**Solução:** Gerar novo fixture:
```powershell
docker exec omaum-web-prod python manage.py dumpdata --indent=2 \
  -e contenttypes -e auth.Permission -e sessions -e admin.logentry \
  > scripts\deploy\exports\dev_data_novo.json
```

### Dados não importados
Verifique:
1. Arquivo fixture existe e não está corrompido
2. BOM UTF-8 foi removido
3. Estrutura de campos compatível com modelos atuais
4. Log mostra mensagem de sucesso ou erro específico

### Containers não iniciam
```powershell
docker compose -f docker\docker-compose.prod.yml logs --tail=50
docker ps -a --filter "name=omaum"
```

## 📚 Histórico de Deploys

Consulte os logs em `scripts/deploy/logs/` para histórico completo de execuções.

Exemplo de análise:
```powershell
Get-Content scripts\deploy\logs\deploy_20251124_131407.log | Select-String "ERROR|SUCCESS"
```

## 🔄 Rollback

Em caso de problemas:

1. **Restaurar banco:**
```powershell
Expand-Archive backups\backup_TIMESTAMP.sql.zip -DestinationPath temp
Get-Content temp\backup_TIMESTAMP.sql | docker exec -i omaum-db-prod psql -U omaum_app omaum_prod
```

2. **Reverter código:**
```bash
git reset --hard COMMIT_ANTERIOR
docker compose -f docker/docker-compose.prod.yml build
docker compose -f docker/docker-compose.prod.yml up -d
```

## 📞 Suporte

- Email: suporte@omaum.edu.br
- Documentação: `docs/`
- Logs: `scripts/deploy/logs/`

---

**Última atualização:** 24/11/2025
**Versão:** 1.0
