# Gestão de Arquivos Estáticos no Docker

## Problema Identificado

O diretório `static/` no workspace não é copiado para o container porque:
1. O volume mount `- ../:/app` no docker-compose.yml sobrescreve o conteúdo copiado durante o build
2. Arquivos em `static/` (como `logo.png`) não ficam disponíveis para o `collectstatic`

## Solução Implementada

### 1. Dockerfile Modificado

```dockerfile
# Criar backup dos arquivos estáticos antes de serem sobrescritos pelo volume mount
RUN mkdir -p /app/media /app/logs && \
    if [ -d "/app/static" ] && [ "$(ls -A /app/static 2>/dev/null)" ]; then \
        echo "Criando backup de arquivos estáticos..." && \
        cp -r /app/static /app/.static_backup; \
    fi && \
    chmod +x /app/docker/entrypoint.sh
```

### 2. Entrypoint Modificado

```bash
# Garantir que arquivos estáticos base existam
if [ ! -f "/app/static/img/logo.png" ]; then
    echo "⚠️  Arquivos estáticos base não encontrados em /app/static/"
    mkdir -p /app/static/img
    
    if [ -d "/app/.static_backup" ]; then
        echo "Restaurando arquivos estáticos do backup..."
        cp -r /app/.static_backup/* /app/static/
    fi
fi
```

### 3. Requirements Corrigidos

Adicionado `requests==2.32.5` ao `requirements-production.txt` (necessário para ViaCEP API).

## Comandos para Deploy Completo

### Desenvolvimento (porta 8000)

```powershell
# 1. Build da imagem
cd E:\projetos\omaum\docker
docker compose -p omaum-dev --env-file E:\projetos\omaum\.env.dev -f docker-compose.yml build omaum-web

# 2. Restart dos containers
docker compose -p omaum-dev --env-file E:\projetos\omaum\.env.dev -f docker-compose.yml up -d

# 3. Verificar logs
docker compose -p omaum-dev --env-file E:\projetos\omaum\.env.dev -f docker-compose.yml logs -f omaum-web
```

### Produção (porta 80)

```powershell
# 1. Build da imagem
cd E:\projetos\omaum\docker
docker compose --profile production -p omaum-prod --env-file E:\projetos\omaum\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml build omaum-web

# 2. Restart dos containers
docker compose --profile production -p omaum-prod --env-file E:\projetos\omaum\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml up -d

# 3. Verificar logs
docker compose --profile production -p omaum-prod --env-file E:\projetos\omaum\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml logs -f omaum-web
```

## Workaround Manual (se necessário)

Se após o deploy o logo ainda não aparecer:

```powershell
# Copiar logo manualmente
docker cp "E:\projetos\omaum\static\img\logo.png" <container-name>:/app/staticfiles/img/logo.png

# Exemplo para dev:
docker cp "E:\projetos\omaum\static\img\logo.png" omaum-dev-omaum-web-1:/app/staticfiles/img/logo.png

# Exemplo para prod:
docker cp "E:\projetos\omaum\static\img\logo.png" omaum-prod-omaum-web-1:/app/staticfiles/img/logo.png
```

## Verificação

```powershell
# Verificar se arquivo existe no container
docker exec <container-name> ls -la /app/staticfiles/img/logo.png

# Verificar se backup foi criado
docker exec <container-name> ls -la /app/.static_backup/img/logo.png
```

## Notas Importantes

1. **Sempre rebuild após mudanças no Dockerfile**: `docker compose build --no-cache`
2. **Volumes sobrescrevem builds**: O mount `- ../:/app` substitui tudo em runtime
3. **Collectstatic é executado automaticamente**: No entrypoint.sh
4. **Hard refresh necessário**: Após mudanças, pressione `Ctrl+Shift+R` no navegador
