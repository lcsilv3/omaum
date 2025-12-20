# ✅ Execução Simultânea dos Ambientes Dev e Prod

## 📋 Resumo

Os ambientes de **desenvolvimento** e **produção** estão configurados para rodar **simultaneamente** sem conflitos.

## 🔌 Mapeamento de Portas

| Serviço        | Desenvolvimento      | Produção            |
|----------------|----------------------|---------------------|
| **Web**        | 8001 (localhost)     | 8000 (localhost)    |
| **Nginx**      | ❌ Não habilitado    | 80 (localhost)      |
| **PostgreSQL** | 5432 (localhost)     | 5433 (localhost)    |
| **Redis**      | 6379 (localhost)     | 6380 (localhost)    |
| **Database**   | `omaum_dev`          | `omaum_prod`        |
| **Volumes**    | `E:/docker/omaum/dev/` | `D:/docker/omaum/prod/` |

## 🚀 Comandos para Execução Simultânea

### 1️⃣ Iniciar Desenvolvimento

```powershell
cd E:\projetos\omaum\docker
docker compose -p omaum-dev `
  --env-file ..\.env.dev `
  -f docker-compose.yml `
  -f docker-compose.dev.override.yml `
  up -d
```

**Acesso:** http://localhost:8001  
**Badge:** 🟡 Amarelo "Ambiente de Desenvolvimento"

---

### 2️⃣ Iniciar Produção

```powershell
cd E:\projetos\omaum\docker
docker compose --profile production -p omaum-prod `
  --env-file ..\.env.production `
  -f docker-compose.yml `
  -f docker-compose.prod.override.yml `
  up -d
```

**Acesso:** 
- Direto: http://localhost:8000
- Nginx: http://localhost:80

**Badge:** 🔴 Vermelho "Ambiente de Produção"

---

### 3️⃣ Parar Todos os Ambientes

```powershell
cd E:\projetos\omaum\docker

# Parar desenvolvimento
docker compose -p omaum-dev `
  --env-file ..\.env.dev `
  -f docker-compose.yml `
  -f docker-compose.dev.override.yml `
  down

# Parar produção
docker compose --profile production -p omaum-prod `
  --env-file ..\.env.production `
  -f docker-compose.yml `
  -f docker-compose.prod.override.yml `
  down
```

Ou use o script: `../scripts/docker/parar_docker.bat`

---

## ⚙️ Scripts Auxiliares

### `../scripts/docker/iniciar_dev_docker.bat`
Inicia apenas o ambiente de **desenvolvimento** (porta 8001).

### `../scripts/docker/iniciar_prod_docker.bat`
Inicia apenas o ambiente de **produção** (porta 8000 + Nginx na 80).

### `../scripts/docker/parar_docker.bat`
Para **AMBOS** os ambientes (dev e prod).

### `../scripts/docker/atualizar_docker.bat`
Para, reconstrói imagens e reinicia **desenvolvimento**.

---

## 🔍 Verificar Status

```powershell
# Listar containers em execução
docker ps

# Containers esperados quando AMBOS estão rodando:
# - omaum-dev-omaum-web-1 (porta 8001)
# - omaum-dev-omaum-db-1 (porta 5432)
# - omaum-dev-omaum-redis-1 (porta 6379)
# - omaum-prod-omaum-web-1 (porta 8000)
# - omaum-prod-omaum-db-1 (porta 5433)
# - omaum-prod-omaum-redis-1 (porta 6380)
# - omaum-prod-omaum-nginx-1 (porta 80) [apenas se --profile production]
```

---

## 🧪 Casos de Uso

### Cenário 1: Desenvolvimento Ativo
- **Use:** Apenas `omaum-dev`
- **Quando:** Editando código, testando mudanças
- **Hot Reload:** ✅ Sim (código montado via volume)

### Cenário 2: Testes de Integração
- **Use:** `omaum-dev` + `omaum-prod`
- **Quando:** Validar comportamento antes de deploy
- **Hot Reload:** ✅ Dev sim, ❌ Prod não

### Cenário 3: Demonstração/Homologação
- **Use:** Apenas `omaum-prod`
- **Quando:** Apresentar para stakeholders
- **Performance:** Otimizada (Gunicorn + Nginx)

---

## 🔐 Segurança

### Desenvolvimento
- `DEBUG=True`
- Portas DB/Redis expostas (acesso externo)
- Código montado como volume

### Produção
- `DEBUG=False`
- Portas DB/Redis apenas para monitoramento (não obrigatório)
- Código copiado na imagem (não editável)
- Gunicorn com 3 workers
- Nginx como proxy reverso

---

## ⚠️ Considerações de Recursos

Executar ambos simultaneamente requer:

| Recurso       | Desenvolvimento | Produção | Total  |
|---------------|-----------------|----------|--------|
| **RAM**       | ~1 GB           | ~2 GB    | ~3 GB  |
| **CPU**       | 1-2 cores       | 2-3 cores| 3-5 cores |
| **Disco**     | Volumes E:/     | Volumes D:/ | 2 locais |

**Recomendação:** 8 GB RAM e 4+ cores de CPU para execução confortável.

---

## 🐛 Troubleshooting

### Porta já em uso
```
Error: port is already allocated
```

**Solução:**
1. Verifique se outro serviço usa a porta:
   ```powershell
   netstat -ano | findstr :8000
   netstat -ano | findstr :8001
   ```
2. Pare o serviço conflitante ou altere a porta no override correspondente

### Containers não iniciam
```powershell
# Ver logs completos
docker compose -p omaum-dev logs
docker compose -p omaum-prod logs

# Ver logs de um serviço específico
docker compose -p omaum-dev logs omaum-web
```

### Banco de dados não conecta
- Verifique se o `DATABASE_URL` no `.env.*` está correto
- Confirme que o banco existe: `docker exec omaum-dev-omaum-db-1 psql -U omaum_user -l`

### Mudanças no código não refletem (Produção)
Prod **NÃO** tem hot reload! Você precisa:
1. Parar o container
2. Reconstruir a imagem: `docker compose -p omaum-prod build`
3. Reiniciar: `docker compose -p omaum-prod up -d`

---

## 📚 Referências

- [DOCKER_SEPARACAO_AMBIENTES.md](DOCKER_SEPARACAO_AMBIENTES.md) - Detalhes técnicos da separação
- [README.md](../README.md) - Documentação geral do projeto
- [Docker Compose CLI](https://docs.docker.com/compose/reference/) - Referência oficial

---

**Atualizado:** 2025-01-23  
**Versão:** 1.0
