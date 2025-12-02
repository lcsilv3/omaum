# 🐳 Guia Completo - Docker com Desenvolvimento e Produção

## ✅ SIM! O Projeto JÁ TEM os Dois Ambientes Docker

O OMAUM possui **3 configurações Docker** diferentes:

---

## 📁 Arquivos de Configuração

```
docker/
├── docker-compose.yml           → 🔵 DESENVOLVIMENTO (base)
├── docker-compose.override.yml  → 🔵 DESENVOLVIMENTO (sobrescreve)
└── docker-compose.prod.yml      → 🔴 PRODUÇÃO
```

> **Importante:** jamais reutilize o `docker-compose.yml` puro em produção.
> Ele monta o código via volume, expõe portas de banco/Redis e mantém
> `DEBUG=True`. Em produção sempre utilize o `docker-compose.prod.yml`
> (isolado ou combinado com o base via `docker compose -f ...`). Dessa força
> evitamos que variáveis, portas ou dados de desenvolvimento vazem para o
> ambiente crítico.

---

## 🔵 AMBIENTE DE DESENVOLVIMENTO

### Características:
- ✅ **Debug habilitado** (Django Debug Toolbar)
- ✅ **Hot reload** - Código atualiza automaticamente
- ✅ **Volumes montados** - Edita arquivos no Windows, reflete no container
- ✅ **Portas expostas** - Acesso direto ao DB e Redis
- ✅ **Banco de dados**: `omaum_dev`
- ✅ **Settings**: `omaum.settings.development`

### Portas:
- **8000** → Django
- **5432** → PostgreSQL
- **6379** → Redis

### Containers:
```
omaum-web       → Servidor Django (development mode)
omaum-db        → PostgreSQL 15 (omaum_dev)
omaum-redis     → Redis 7
```

### Como usar:

```powershell
# Ir para pasta docker
cd docker

# Iniciar ambiente de DESENVOLVIMENTO
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down

# Acessar
# http://localhost:8000
```

### Diferencial do DEV:
- ✅ Código é **montado como volume** (`- ../:/app`)
- ✅ Qualquer alteração no código reflete imediatamente
- ✅ Não precisa reconstruir imagem a cada mudança
- ✅ Debug Toolbar ativo
- ✅ Erros detalhados

---

## 🔴 AMBIENTE DE PRODUÇÃO

### Características:
- 🔒 **Debug desabilitado**
- 🔒 **Segurança reforçada**
- 🔒 **Volumes persistentes** - Dados não são perdidos
- 🔒 **Nginx como proxy reverso**
- 🔒 **Celery para tarefas assíncronas**
- 🔒 **Banco de dados**: `omaum_prod`
- 🔒 **Settings**: `omaum.settings.production`
- 🔒 **Variáveis em .env.production**

### Portas:
- **80** → HTTP (Nginx)
- **443** → HTTPS (Nginx)

### Containers:
```
omaum-nginx-prod      → Nginx (proxy reverso)
omaum-web-prod        → Gunicorn + Django
omaum-db-prod         → PostgreSQL 15 (omaum_prod)
omaum-redis-prod      → Redis 7 (com senha)
omaum-celery-prod     → Celery worker
omaum-celery-beat-prod → Celery beat (tarefas agendadas)
```

### Como usar:

```powershell
# Ir para pasta docker
cd docker

# Iniciar ambiente de PRODUÇÃO
docker-compose -f docker-compose.prod.yml up -d

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Parar
docker-compose -f docker-compose.prod.yml down

# Acessar
# http://192.168.15.4
# http://omaum.local
```

### Diferencial do PROD:
- 🔒 Código é **copiado na build** (não montado)
- 🔒 Para atualizar código, precisa **rebuild**
- 🔒 Gunicorn (mais rápido e estável)
- 🔒 Nginx na frente (cache, compressão, SSL)
- 🔒 Senhas fortes em `.env.production`
- 🔒 Celery para processamento em background

---

## 📊 COMPARAÇÃO LADO A LADO

| Característica | 🔵 Desenvolvimento | 🔴 Produção |
|----------------|-------------------|-------------|
| **Arquivo** | `docker-compose.yml` | `docker-compose.prod.yml` |
| **Settings** | `omaum.settings.development` | `omaum.settings.production` |
| **Debug** | ✅ Ativo | ❌ Desabilitado |
| **Servidor Web** | Django runserver | Gunicorn |
| **Proxy** | ❌ Sem proxy | ✅ Nginx |
| **Código** | Volume montado | Copiado na build |
| **Hot Reload** | ✅ Sim | ❌ Não |
| **Banco de dados** | `omaum_dev` | `omaum_prod` |
| **Redis senha** | ❌ Sem senha | ✅ Com senha |
| **Celery** | ❌ Opcional | ✅ Obrigatório |
| **SSL/HTTPS** | ❌ Não | ✅ Configurável |
| **Portas expostas** | ✅ Todas (DB, Redis) | ❌ Apenas 80/443 |
| **Performance** | Desenvolvimento | Otimizado |
| **Logs** | Detalhados | Produção |

---

## 🚀 WORKFLOWS RECOMENDADOS

### Fluxo de Desenvolvimento:

```powershell
# 1. Iniciar ambiente de desenvolvimento
cd docker
docker-compose up -d

# 2. Desenvolver normalmente
# Edita arquivos no Windows
# Mudanças refletem automaticamente no container

# 3. Testar
# http://localhost:8000

# 4. Commit
git add .
git commit -m "feat: nova funcionalidade"
git push

# 5. Parar quando terminar
docker-compose down
```

### Fluxo de Deploy para Produção:

```powershell
# 1. Parar produção (se estiver rodando)
cd docker
docker-compose -f docker-compose.prod.yml down

# 2. Atualizar código
cd ..
git pull origin master

# 3. Reconstruir e iniciar
cd docker
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# 4. Aplicar migrações
docker exec omaum-web-prod python manage.py migrate

# 5. Coletar estáticos
docker exec omaum-web-prod python manage.py collectstatic --noinput

# 6. Verificar
docker ps
curl http://192.168.15.4
```

---

## 🛠️ COMANDOS ÚTEIS

### Desenvolvimento:

```powershell
# Iniciar
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f web

# Executar comando Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Shell do container
docker-compose exec web bash

# Reiniciar apenas web
docker-compose restart web

# Ver status
docker-compose ps

# Parar tudo
docker-compose down

# Parar e remover volumes (CUIDADO!)
docker-compose down -v
```

### Produção:

```powershell
# Iniciar
docker-compose -f docker-compose.prod.yml up -d

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f web

# Executar comando Django
docker exec omaum-web-prod python manage.py migrate

# Shell do container
docker exec -it omaum-web-prod bash

# Reiniciar web
docker restart omaum-web-prod

# Ver status
docker ps

# Parar tudo
docker-compose -f docker-compose.prod.yml down
```

---

## 🔄 ATUALIZANDO CÓDIGO EM CADA AMBIENTE

### 🔵 Desenvolvimento (Automático):
```powershell
# Basta editar os arquivos!
# Hot reload ativo, não precisa rebuild
```

### 🔴 Produção (Manual):
```powershell
# Use o script criado:
.\atualizar_docker.bat

# OU manualmente:
cd docker
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
docker exec omaum-web-prod python manage.py migrate
docker exec omaum-web-prod python manage.py collectstatic --noinput
```

#### Como garantir que a build usa o hash correto de `main`

1. Obtenha o hash atual: `git rev-parse --short HEAD`
2. Monte uma tag para as imagens: `set TAG=afbfcc8` (exemplo)
3. Execute o build com tag explícita:
   ```powershell
   docker compose -f docker-compose.prod.yml build --build-arg GIT_SHA=%TAG% --no-cache
   docker tag omaum-web-prod:latest omaum-web-prod:%TAG%
   ```
4. (Opcional) Publique em um registry: `docker push omaum-web-prod:%TAG%`
5. Registre no log de deploy qual tag/commit foi aplicada e use `TAG` na hora de dar `up -d` (`IMAGE=omaum-web-prod:%TAG%`).

### Ritual obrigatório pós-merge em `main`

Repita este checklist **sempre** que um merge cair no `main`:

1. `git pull origin main` no ambiente alvo (dev ou prod).
2. `docker compose -f <arquivo>.yml build` ou `pull` para atualizar imagens.
3. `docker compose -f <arquivo>.yml up -d` para recriar serviços.
4. `docker compose -f <arquivo>.yml exec <web> python manage.py migrate --noinput`.
5. Rodar smoke tests (`scripts/run_smoke_tests.py`, `pytest` ou requisições básicas).
6. Registrar o hash aplicado no log/planilha de deploy.

#### Dependências extras para smoke tests

Os contêineres `omaum-web` (dev e prod) são construídos apenas com as dependências mínimas de produção. Para executar `scripts/run_smoke_tests.py` dentro do Docker é preciso instalar rapidamente os pacotes de teste:**pytest**, **pytest-django**, **pytest-cov** e **requests**. O processo pode ser feito logo após o `up -d`:

```powershell
docker compose -f docker/docker-compose.yml exec omaum-web pip install pytest pytest-django pytest-cov requests
```

Essas instalações ficam disponíveis apenas até o próximo `build`. Caso queira torná-las permanentes, adicione-as ao `requirements-dev.txt` e ajuste a imagem conforme necessário.

---

## 📋 CHECKLIST ANTES DE SUBIR PARA PRODUÇÃO

- [ ] Código testado em desenvolvimento
- [ ] Testes automatizados passando
- [ ] Migrações criadas e testadas
- [ ] `.env.production` atualizado
- [ ] SECRET_KEY forte e aleatória
- [ ] DEBUG=False no `.env.production`
- [ ] ALLOWED_HOSTS configurado corretamente
- [ ] Senhas de banco e Redis alteradas
- [ ] Backup do banco de produção feito
- [ ] Código commitado e pushado
- [ ] Rebuild da imagem feito
- [ ] Migrações aplicadas
- [ ] Estáticos coletados
- [ ] Site acessível e funcional

---

## 🎯 SITUAÇÃO ATUAL DO SEU PROJETO

### Status Agora:

```
🔵 DESENVOLVIMENTO (Docker):
   Status: ⚠️ NÃO RODANDO
   Como iniciar: docker-compose up -d
   URL: http://localhost:8000

🔴 PRODUÇÃO (Docker):
   Status: ✅ RODANDO (22h)
   Código: ❌ DESATUALIZADO (sem commit 475e4b84)
   URL: http://192.168.15.4
   Ação: Executar .\atualizar_docker.bat

💻 DESENVOLVIMENTO (Local/Windows):
   Status: ❌ QUEBRADO (Python não instalado)
   Ação: Instalar Python 3.12+
```

---

## 🎬 PRÓXIMOS PASSOS RECOMENDADOS

### 1. Atualizar Produção (Urgente):
```powershell
.\atualizar_docker.bat
```
Isso aplicará o commit 475e4b84 (grau_atual readonly)

### 2. Testar Desenvolvimento Docker:
```powershell
cd docker
docker-compose up -d
# Acessar http://localhost:8000
```

### 3. (Opcional) Configurar Desenvolvimento Local:
```powershell
# Instalar Python 3.12+
# Executar: .\setup_ambiente.bat
```

---

## 💡 RECOMENDAÇÃO

**Use Docker para tudo!**

- ✅ **Desenvolvimento**: `docker-compose up -d`
- ✅ **Produção**: `docker-compose -f docker-compose.prod.yml up -d`
- ✅ Não precisa instalar Python no Windows
- ✅ Ambientes isolados e reproduzíveis
- ✅ Mesma versão de Python em DEV e PROD (3.11)

**Deixe o ambiente local apenas para:**
- Testes rápidos sem Docker
- IDEs que precisam do interpretador local
- Scripts auxiliares

---

**Última atualização:** 29/11/2025
