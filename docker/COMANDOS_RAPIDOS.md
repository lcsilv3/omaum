# 🚀 Guia Rápido - Comandos Docker OMAUM

## ✅ Comandos Validados (Use estes!)

### Desenvolvimento (Porta 8001)
```powershell
# Subir
cd E:\projetos\omaum\docker
docker compose -p omaum-dev --env-file E:\projetos\omaum\.env.dev -f docker-compose.yml up -d

# Derrubar
docker compose -p omaum-dev --env-file E:\projetos\omaum\.env.dev -f docker-compose.yml down

# Logs
docker compose -p omaum-dev --env-file E:\projetos\omaum\.env.dev -f docker-compose.yml logs -f omaum-web

# Rebuild
docker compose -p omaum-dev --env-file E:\projetos\omaum\.env.dev -f docker-compose.yml build omaum-web
docker compose -p omaum-dev --env-file E:\projetos\omaum\.env.dev -f docker-compose.yml up -d --force-recreate omaum-web
```

### Produção (Porta 80 via Nginx, 8000 direto)
```powershell
# Subir
cd E:\projetos\omaum\docker
docker compose --profile production -p omaum-prod --env-file E:\projetos\omaum\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml up -d

# Derrubar
docker compose --profile production -p omaum-prod --env-file E:\projetos\omaum\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml down

# Logs
docker compose --profile production -p omaum-prod --env-file E:\projetos\omaum\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml logs -f omaum-web

# Rebuild
docker compose --profile production -p omaum-prod --env-file E:\projetos\omaum\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml build omaum-web
docker compose --profile production -p omaum-prod --env-file E:\projetos\omaum\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml up -d --force-recreate omaum-web
```

## 🔍 Verificação

### Verificar Status
```powershell
# Ver todos os containers
docker ps

# Verificar portas
docker ps --format "table {{.Names}}\t{{.Ports}}"

# Verificar saúde
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Verificar Badges
```powershell
# Dev (deve mostrar "Ambiente de Desenvolvimento")
curl -s http://localhost:8001/ | Select-String "Ambiente de"

# Prod (deve mostrar "Ambiente de Produção")
curl -s http://localhost/ | Select-String "Ambiente de"
```

### Script Automático de Verificação
```powershell
# Executa todas as verificações
python scripts\verificar_ambiente.py
```

## 🧪 Testes

### Teste Selenium de Login
```powershell
# Testa login em ambos os ambientes
python test_login_ambientes.py
```

## ⚠️ Troubleshooting

### Porta já em uso
```powershell
# Parar todos os containers
docker compose -p omaum-dev down
docker compose --profile production -p omaum-prod down

# Subir novamente
# [usar comandos acima]
```

### Badge errado
```powershell
# 1. Verificar se docker-compose.override.yml NÃO existe
dir E:\projetos\omaum\docker\docker-compose.override.yml
# (deve dar erro "não encontrado")

# 2. Ver variável de ambiente do container
docker exec omaum-dev-omaum-web-1 env | Select-String "DJANGO_SETTINGS"
# Deve mostrar: omaum.settings.development

docker exec omaum-prod-omaum-web-1 env | Select-String "DJANGO_SETTINGS"
# Deve mostrar: omaum.settings.production

# 3. Recriar container
docker compose -p omaum-dev down
docker compose -p omaum-dev --env-file E:\projetos\omaum\.env.dev -f docker-compose.yml up -d
```

### Collectstatic (arquivos estáticos)
```powershell
# Dev
docker compose -p omaum-dev exec omaum-web python manage.py collectstatic --noinput --clear

# Prod
docker compose --profile production -p omaum-prod exec omaum-web python manage.py collectstatic --noinput --clear

# Logo manual (após rebuild)
docker cp "E:\projetos\omaum\static\img\logo.png" omaum-dev-omaum-web-1:/app/staticfiles/img/logo.png
docker cp "E:\projetos\omaum\static\img\logo.png" omaum-prod-omaum-web-1:/app/staticfiles/img/logo.png
```

## 📋 Checklist Antes de Deploy

- [ ] `docker-compose.override.yml` NÃO existe (deve ser `.example`)
- [ ] Executar `python scripts\verificar_ambiente.py` → Todas as verificações passam
- [ ] Executar `python test_login_ambientes.py` → Login funciona em ambos
- [ ] Dev acessível em `http://localhost:8001` com badge amarelo
- [ ] Prod acessível em `http://localhost` com badge vermelho
- [ ] Screenshots diferentes nos testes Selenium

## 🎯 URLs de Acesso

| Ambiente | URL | Badge | Credenciais |
|----------|-----|-------|-------------|
| Dev | http://localhost:8001 | 🟡 Amarelo | desenv / desenv123 |
| Prod (Nginx) | http://localhost | 🔴 Vermelho | admin / admin123 |
| Prod (Direto) | http://localhost:8000 | 🔴 Vermelho | admin / admin123 |

## 📚 Documentação Completa

- [AMBIENTE_CONFIG.md](AMBIENTE_CONFIG.md) - Documentação detalhada
- [README_STATIC_FILES.md](README_STATIC_FILES.md) - Gestão de arquivos estáticos
- [../docs/architecture/DOCKER_AMBIENTES.md](../docs/architecture/DOCKER_AMBIENTES.md) - Arquitetura de ambientes

---
**Última atualização:** 20 de dezembro de 2025
