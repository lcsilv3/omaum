# 🐳 Ambientes Docker - Desenvolvimento vs Produção

## ✅ EXECUÇÃO SIMULTÂNEA PERMITIDA

Este projeto possui **DOIS ambientes Docker completamente separados**:

1. 🟡 **Desenvolvimento** (`omaum-dev`)
2. 🔴 **Produção** (`omaum-prod`)

**✅ PODEM rodar simultaneamente** sem conflitos de portas!

---

## 📊 Comparação dos Ambientes

| Aspecto | 🟡 Desenvolvimento | 🔴 Produção |
|---------|-------------------|-------------|
| **Projeto Docker** | `omaum-dev` | `omaum-prod` |
| **Porta Web** | `8001:8000` | `8000:8000` |
| **Porta DB** | `5432:5432` | `5433:5432` ✅ |
| **Porta Redis** | `6379:6379` | `6380:6379` ✅ |
| **Banco de Dados** | `omaum_dev` | `omaum_prod` |
| **Settings Django** | `omaum.settings.development` | `omaum.settings.production` |
| **DEBUG** | `True` | `False` |
| **Código Fonte** | Montado via volume (`../:/app`) | Copiado na imagem (sem volume) |
| **Hot Reload** | ✅ Ativo | ❌ Desativado |
| **Servidor** | `runserver` | `gunicorn` (3 workers) |
| **Nginx** | ❌ Desativado | ✅ Proxy reverso (porta 80) |
| **Volumes Host** | `E:/docker/omaum/dev/` | `D:/docker/omaum/prod/` |
| **Fotos Externas** | ✅ Montado | ✅ Montado (read-only) |

---

## 🟡 DESENVOLVIMENTO

### Arquivos Utilizados:
```
docker-compose.yml                  (base)
docker-compose.dev.override.yml     (sobrescreve)
.env.dev                            (variáveis)
```

### Comando para Iniciar:
```powershell
cd docker
docker compose -p omaum-dev --env-file ../.env.dev -f docker-compose.yml -f docker-compose.dev.override.yml up -d
```

### Acesso:
- **Web:** http://localhost:8001
- **PostgreSQL:** localhost:5432 (omaum_dev)
- **Redis:** localhost:6379

### Características:
✅ Código montado como volume → Alterações refletem automaticamente  
✅ Debug Toolbar ativo  
✅ Portas de banco/Redis expostas para ferramentas externas (DBeaver, Redis Desktop)  
✅ Logs detalhados  

### Containers:
```
omaum-dev-omaum-web-1      → Django runserver (porta 8001)
omaum-dev-omaum-db-1       → PostgreSQL (omaum_dev)
omaum-dev-omaum-redis-1    → Redis
```

---

## 🔴 PRODUÇÃO

### Arquivos Utilizados:
```
docker-compose.yml                    (base)
docker-compose.prod.override.yml      (sobrescreve)
.env.production                       (variáveis)
```

### Comando para Iniciar:
```powershell
cd docker
docker compose --profile production -p omaum-prod --env-file ../.env.production -f docker-compose.yml -f docker-compose.prod.override.yml up -d
```

### Acesso:
- **Web (Nginx):** http://localhost (porta 80)
- **Web (Direto):** http://localhost:8000
- **PostgreSQL:** ❌ NÃO exposto (apenas interno)
- **Redis:** ❌ NÃO exposto (apenas interno)

### Características:
🔒 Código **COPIADO** na imagem Docker (não montado)  
🔒 DEBUG desabilitado  
🔒 Gunicorn com 3 workers  
🔒 Nginx como proxy reverso  
🔒 Banco/Redis isolados (apenas rede interna)  
🔒 Logs controlados  

### Containers:
```
omaum-prod-omaum-web-1      → Gunicorn (porta 8000)
omaum-prod-omaum-nginx-1    → Nginx (porta 80)
omaum-prod-omaum-db-1       → PostgreSQL (omaum_prod)
omaum-prod-omaum-redis-1    → Redis
omaum-prod-omaum-celery-1   → Celery worker (opcional)
```

---

## ✅ Execução Simultânea

### Portas configuradas para evitar conflitos:

| Serviço      | Desenvolvimento | Produção | Conflito? |
|--------------|-----------------|----------|-----------|
| Web          | 8001            | 8000     | ❌ Não    |
| Nginx        | N/A             | 80       | ❌ Não    |
| PostgreSQL   | 5432            | 5433     | ❌ Não    |
| Redis        | 6379            | 6380     | ❌ Não    |

### Iniciando ambos simultaneamente:

```powershell
# 1. Iniciar desenvolvimento
cd E:\projetos\omaum\docker
docker compose -p omaum-dev --env-file ..\.env.dev ^
  -f docker-compose.yml ^
  -f docker-compose.dev.override.yml up -d

# 2. Iniciar produção
docker compose --profile production -p omaum-prod ^
  --env-file ..\.env.production ^
  -f docker-compose.yml ^
  -f docker-compose.prod.override.yml up -d
```

### Acessando os ambientes:
- **Dev:** http://localhost:8001 (🟡 Badge amarelo)
- **Prod Web:** http://localhost:8000 (🔴 Badge vermelho)
- **Prod Nginx:** http://localhost:80 (🔴 Badge vermelho)

### Parando ambos:
```powershell
# Parar desenvolvimento
docker compose -p omaum-dev down

# Parar produção
docker compose -p omaum-prod down
```

### Segurança do isolamento:

✅ **Projetos isolados** via `-p omaum-dev` vs `-p omaum-prod`  
✅ **Bancos de dados diferentes** (`omaum_dev` vs `omaum_prod`)  
✅ **Volumes em drives diferentes** (E:/ vs D:/)  
✅ **Portas não conflitantes** (ver tabela acima)  
✅ **Networks Docker separadas** (bridge automáticas)

---

## 📋 Checklist de Verificação

### Antes de iniciar DESENVOLVIMENTO:
- [ ] Arquivo `.env.dev` existe e está correto
- [ ] Drive `E:/docker/omaum/dev/` existe
- [ ] Drive `D:/Documentos Ordem/Ordem/CIIniciados/fotos` existe
- [ ] Porta 8001 disponível: `netstat -ano | findstr :8001`

### Antes de iniciar PRODUÇÃO:
- [ ] Arquivo `.env.production` existe e está correto
- [ ] Drive `D:/docker/omaum/prod/` existe
- [ ] Porta 8000 disponível: `netstat -ano | findstr :8000`
- [ ] Porta 80 disponível: `netstat -ano | findstr :80`
- [ ] Drive `D:/Documentos Ordem/Ordem/CIIniciados/fotos` existe
- [ ] Segredos de produção (SECRET_KEY) estão configurados
- [ ] POSTGRES_PASSWORD está definido em `.env.production`

---

## 🛠️ Comandos Rápidos

### Desenvolvimento:
```powershell
# Iniciar
cd docker
docker compose -p omaum-dev --env-file ../.env.dev -f docker-compose.yml -f docker-compose.dev.override.yml up -d

# Ver logs
docker compose -p omaum-dev logs -f omaum-web

# Parar
docker compose -p omaum-dev down

# Rebuild (após mudanças no Dockerfile)
docker compose -p omaum-dev --env-file ../.env.dev -f docker-compose.yml -f docker-compose.dev.override.yml up -d --build
```

### Produção:
```powershell
# Iniciar
cd docker
docker compose --profile production -p omaum-prod --env-file ../.env.production -f docker-compose.yml -f docker-compose.prod.override.yml up -d

# Ver logs
docker compose -p omaum-prod logs -f omaum-web

# Parar
docker compose -p omaum-prod down

# Rebuild
docker compose --profile production -p omaum-prod --env-file ../.env.production -f docker-compose.yml -f docker-compose.prod.override.yml up -d --build
```

### Verificar qual está rodando:
```powershell
docker ps --filter "name=omaum-"
```

---

## 🚨 Solução de Problemas

### Erro: "port is already allocated"
**Causa:** Dois ambientes rodando simultaneamente ou outro serviço na porta.

**Solução:**
```powershell
# Ver containers rodando
docker ps

# Parar todos os containers do projeto
docker compose -p omaum-dev down
docker compose -p omaum-prod down

# Ver processos usando portas
netstat -ano | findstr :8000
netstat -ano | findstr :8001
netstat -ano | findstr :5432
```

### Erro: "database omaum_dev/omaum_prod does not exist"
**Causa:** Container do banco criado mas database não inicializado.

**Solução:**
```powershell
# Parar containers
docker compose -p omaum-dev down

# Remover volumes (CUIDADO: apaga dados!)
docker volume rm omaum-dev_omaum_db_data

# Recriar
docker compose -p omaum-dev up -d
```

### Mudanças no código não refletem (DESENVOLVIMENTO)
**Causa:** Volume não montado ou servidor não reiniciou.

**Verificar:**
```powershell
# Ver se volume está montado
docker inspect omaum-dev-omaum-web-1 | findstr Source

# Deve mostrar: E:\projetos\omaum
```

### Mudanças no código não refletem (PRODUÇÃO)
**Causa:** Código está na imagem, não em volume.

**Solução:**
```powershell
# Rebuild da imagem
docker compose -p omaum-prod --profile production -f docker-compose.yml -f docker-compose.prod.override.yml up -d --build
```

---

## 📝 Notas Importantes

1. **NUNCA** renomeie `docker-compose.dev.override.yml` para `docker-compose.override.yml`
   - Docker Compose lê `override.yml` automaticamente
   - Isso causaria conflito entre ambientes

2. **SEMPRE** use `-p omaum-dev` ou `-p omaum-prod`
   - Garante separação total dos containers

3. **SEMPRE** use `--env-file` correto:
   - Dev: `../.env.dev`
   - Prod: `../.env.production`

4. **Código fonte em produção:**
   - ❌ NÃO montar via volume (`../:/app`)
   - ✅ Copiar na imagem (via Dockerfile)
   - Isso garante que produção rode código "travado" e testado

5. **Bancos de dados separados:**
   - Dev: `omaum_dev` (pode resetar à vontade)
   - Prod: `omaum_prod` (NUNCA resetar sem backup!)

---

## 🎯 Resumo Executivo

| Ação | Comando |
|------|---------|
| **Iniciar Dev** | `docker compose -p omaum-dev --env-file ../.env.dev -f docker-compose.yml -f docker-compose.dev.override.yml up -d` |
| **Parar Dev** | `docker compose -p omaum-dev down` |
| **Iniciar Prod** | `docker compose --profile production -p omaum-prod --env-file ../.env.production -f docker-compose.yml -f docker-compose.prod.override.yml up -d` |
| **Parar Prod** | `docker compose -p omaum-prod down` |
| **Ver Logs** | `docker compose -p <projeto> logs -f` |
| **Status** | `docker ps --filter "name=omaum-"` |

---

**Última atualização:** 19/12/2025  
**Autor:** GitHub Copilot  
**Versão:** 2.0 (Corrigidos conflitos de portas e volumes)
