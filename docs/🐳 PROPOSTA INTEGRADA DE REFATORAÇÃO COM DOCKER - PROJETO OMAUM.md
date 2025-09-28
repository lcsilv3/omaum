# 🐳 PROPOSTA INTEGRADA DE REFATORAÇÃO COM DOCKER - PROJETO OMAUM

**Data:** 28/09/2025  
**Versão:** 2.0 - Docker Edition  
**Objetivo:** Refatoração completa com containerização para produção corporativa

---

## 📋 RESUMO EXECUTIVO

Esta proposta apresenta um **plano de refatoração completo** do projeto OmAum utilizando **Docker** para containerização, garantindo portabilidade, escalabilidade e facilidade de deploy. Inclui o padrão corporativo de cabeçalhos/rodapés e modernização completa da arquitetura.

### **Benefícios da Containerização:**
- ✅ **Portabilidade**: Funciona em qualquer ambiente
- ✅ **Escalabilidade**: Fácil escalonamento horizontal
- ✅ **Isolamento**: Dependências isoladas
- ✅ **Deploy Simplificado**: Um comando para subir tudo
- ✅ **Desenvolvimento Padronizado**: Ambiente idêntico para todos

---

## 🏗️ ARQUITETURA DOCKER PROPOSTA

### **Containers da Solução:**
```yaml
omaum-stack:
  ├── omaum-web          # Django Application (Gunicorn)
  ├── omaum-nginx        # Reverse Proxy + Static Files
  ├── omaum-db           # PostgreSQL Database
  ├── omaum-redis        # Cache + Session Store
  ├── omaum-celery       # Background Tasks
  └── omaum-monitoring   # Prometheus + Grafana (opcional)
```

### **Volumes Persistentes:**
- `omaum_db_data`: Dados do PostgreSQL
- `omaum_media`: Uploads e arquivos gerados
- `omaum_static`: Arquivos estáticos
- `omaum_logs`: Logs da aplicação

---

## 📦 ESTRUTURA DE ARQUIVOS DOCKER

```
omaum/
├── docker/
│   ├── Dockerfile              # Imagem principal Django
│   ├── Dockerfile.nginx        # Imagem Nginx customizada
│   ├── docker-compose.yml      # Orquestração desenvolvimento
│   ├── docker-compose.prod.yml # Orquestração produção
│   ├── nginx/
│   │   ├── nginx.conf          # Configuração Nginx
│   │   └── default.conf        # Virtual host padrão
│   ├── scripts/
│   │   ├── entrypoint.sh       # Script de inicialização
│   │   ├── wait-for-it.sh      # Aguardar dependências
│   │   └── backup.sh           # Script de backup
│   └── env/
│       ├── .env.development    # Variáveis desenvolvimento
│       ├── .env.production     # Variáveis produção
│       └── .env.example        # Template de variáveis
├── requirements/
│   ├── base.txt               # Dependências base
│   ├── development.txt        # Dependências desenvolvimento
│   └── production.txt         # Dependências produção
└── ... (resto do projeto Django)
```

---

## 🐳 IMPLEMENTAÇÃO DOCKER - PASSO A PASSO

### **PASSO 1: Criar Dockerfile Principal**

```dockerfile
# docker/Dockerfile
FROM python:3.11-slim

# Metadados
LABEL maintainer="OmAum Development Team"
LABEL version="2.0"
LABEL description="OM-AUM Django Application"

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=omaum.settings.production

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    gettext \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN groupadd -r omaum && useradd -r -g omaum omaum

# Criar diretórios
WORKDIR /app
RUN mkdir -p /app/static /app/media /app/logs
RUN chown -R omaum:omaum /app

# Instalar dependências Python
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

# Copiar código da aplicação
COPY . /app/
RUN chown -R omaum:omaum /app

# Copiar scripts
COPY docker/scripts/entrypoint.sh /entrypoint.sh
COPY docker/scripts/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /entrypoint.sh /wait-for-it.sh

# Mudar para usuário não-root
USER omaum

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expor porta
EXPOSE 8000

# Comando de inicialização
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "omaum.wsgi:application"]
```

### **PASSO 2: Criar Dockerfile Nginx**

```dockerfile
# docker/Dockerfile.nginx
FROM nginx:alpine

# Copiar configurações
COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# Criar diretórios para arquivos estáticos
RUN mkdir -p /var/www/static /var/www/media

# Expor porta
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### **PASSO 3: Configurar Nginx**

```nginx
# docker/nginx/nginx.conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logs
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    
    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    # Incluir configurações dos sites
    include /etc/nginx/conf.d/*.conf;
}
```

```nginx
# docker/nginx/default.conf
upstream omaum_web {
    server omaum-web:8000;
}

server {
    listen 80;
    server_name localhost;
    client_max_body_size 100M;
    
    # Logs específicos
    access_log /var/log/nginx/omaum_access.log;
    error_log /var/log/nginx/omaum_error.log;
    
    # Arquivos estáticos
    location /static/ {
        alias /var/www/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Arquivos de media
    location /media/ {
        alias /var/www/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # Aplicação Django
    location / {
        proxy_pass http://omaum_web;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Health check
    location /health/ {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### **PASSO 4: Docker Compose para Desenvolvimento**

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  # Banco de dados
  omaum-db:
    image: postgres:15-alpine
    container_name: omaum-db
    environment:
      POSTGRES_DB: omaum_dev
      POSTGRES_USER: omaum_user
      POSTGRES_PASSWORD: omaum_password
    volumes:
      - omaum_db_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    ports:
      - "5432:5432"
    networks:
      - omaum-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U omaum_user -d omaum_dev"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis para cache e sessões
  omaum-redis:
    image: redis:7-alpine
    container_name: omaum-redis
    command: redis-server --appendonly yes
    volumes:
      - omaum_redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - omaum-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Aplicação Django
  omaum-web:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: omaum-web
    environment:
      - DJANGO_SETTINGS_MODULE=omaum.settings.development
      - DATABASE_URL=postgresql://omaum_user:omaum_password@omaum-db:5432/omaum_dev
      - REDIS_URL=redis://omaum-redis:6379/0
    volumes:
      - ../:/app
      - omaum_static:/app/static
      - omaum_media:/app/media
      - omaum_logs:/app/logs
    ports:
      - "8000:8000"
    depends_on:
      omaum-db:
        condition: service_healthy
      omaum-redis:
        condition: service_healthy
    networks:
      - omaum-network
    command: >
      sh -c "/wait-for-it.sh omaum-db:5432 --timeout=60 --strict -- 
             python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             python manage.py runserver 0.0.0.0:8000"

  # Nginx (apenas para produção)
  omaum-nginx:
    build:
      context: ..
      dockerfile: docker/Dockerfile.nginx
    container_name: omaum-nginx
    volumes:
      - omaum_static:/var/www/static:ro
      - omaum_media:/var/www/media:ro
    ports:
      - "80:80"
    depends_on:
      - omaum-web
    networks:
      - omaum-network
    profiles:
      - production

  # Celery Worker
  omaum-celery:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: omaum-celery
    environment:
      - DJANGO_SETTINGS_MODULE=omaum.settings.development
      - DATABASE_URL=postgresql://omaum_user:omaum_password@omaum-db:5432/omaum_dev
      - REDIS_URL=redis://omaum-redis:6379/0
    volumes:
      - ../:/app
      - omaum_media:/app/media
      - omaum_logs:/app/logs
    depends_on:
      omaum-db:
        condition: service_healthy
      omaum-redis:
        condition: service_healthy
    networks:
      - omaum-network
    command: celery -A omaum worker -l info
    profiles:
      - celery

volumes:
  omaum_db_data:
  omaum_redis_data:
  omaum_static:
  omaum_media:
  omaum_logs:

networks:
  omaum-network:
    driver: bridge
```

### **PASSO 5: Docker Compose para Produção**

```yaml
# docker/docker-compose.prod.yml
version: '3.8'

services:
  # Banco de dados
  omaum-db:
    image: postgres:15-alpine
    container_name: omaum-db-prod
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - omaum_db_data:/var/lib/postgresql/data
    networks:
      - omaum-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis
  omaum-redis:
    image: redis:7-alpine
    container_name: omaum-redis-prod
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - omaum_redis_data:/data
    networks:
      - omaum-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "--no-auth-warning", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Aplicação Django
  omaum-web:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: omaum-web-prod
    environment:
      - DJANGO_SETTINGS_MODULE=omaum.settings.production
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@omaum-db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@omaum-redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
    volumes:
      - omaum_static:/app/static
      - omaum_media:/app/media
      - omaum_logs:/app/logs
    depends_on:
      omaum-db:
        condition: service_healthy
      omaum-redis:
        condition: service_healthy
    networks:
      - omaum-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Nginx
  omaum-nginx:
    build:
      context: ..
      dockerfile: docker/Dockerfile.nginx
    container_name: omaum-nginx-prod
    volumes:
      - omaum_static:/var/www/static:ro
      - omaum_media:/var/www/media:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      omaum-web:
        condition: service_healthy
    networks:
      - omaum-network
    restart: unless-stopped

  # Celery Worker
  omaum-celery:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: omaum-celery-prod
    environment:
      - DJANGO_SETTINGS_MODULE=omaum.settings.production
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@omaum-db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@omaum-redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - omaum_media:/app/media
      - omaum_logs:/app/logs
    depends_on:
      omaum-db:
        condition: service_healthy
      omaum-redis:
        condition: service_healthy
    networks:
      - omaum-network
    restart: unless-stopped
    command: celery -A omaum worker -l info

  # Celery Beat (agendador)
  omaum-celery-beat:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: omaum-celery-beat-prod
    environment:
      - DJANGO_SETTINGS_MODULE=omaum.settings.production
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@omaum-db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://:${REDIS_PASSWORD}@omaum-redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - omaum_logs:/app/logs
    depends_on:
      omaum-db:
        condition: service_healthy
      omaum-redis:
        condition: service_healthy
    networks:
      - omaum-network
    restart: unless-stopped
    command: celery -A omaum beat -l info

volumes:
  omaum_db_data:
  omaum_redis_data:
  omaum_static:
  omaum_media:
  omaum_logs:

networks:
  omaum-network:
    driver: bridge
```

### **PASSO 6: Scripts de Inicialização**

```bash
#!/bin/bash
# docker/scripts/entrypoint.sh

set -e

# Aguardar banco de dados
echo "Aguardando banco de dados..."
/wait-for-it.sh ${DATABASE_HOST:-omaum-db}:${DATABASE_PORT:-5432} --timeout=60 --strict

# Executar migrações
echo "Executando migrações..."
python manage.py migrate --noinput

# Criar superusuário se não existir
echo "Verificando superusuário..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@omaum.org',
        password='admin123'
    )
    print('Superusuário criado: admin/admin123')
"

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Executar comando passado como argumento
exec "$@"
```

```bash
#!/bin/bash
# docker/scripts/wait-for-it.sh
# Script para aguardar serviços ficarem disponíveis
# (Usar o script oficial do wait-for-it)

WAITFORIT_cmdname=${0##*/}

echoerr() { if [[ $WAITFORIT_QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }

usage()
{
    cat << USAGE >&2
Usage:
    $WAITFORIT_cmdname host:port [-s] [-t timeout] [-- command args]
    -h HOST | --host=HOST       Host or IP under test
    -p PORT | --port=PORT       TCP port under test
                                Alternatively, you specify the host and port as host:port
    -s | --strict               Only execute subcommand if the test succeeds
    -q | --quiet                Don't output any status messages
    -t TIMEOUT | --timeout=TIMEOUT
                                Timeout in seconds, zero for no timeout
    -- COMMAND ARGS             Execute command with args after the test finishes
USAGE
    exit 1
}

wait_for()
{
    if [[ $WAITFORIT_TIMEOUT -gt 0 ]]; then
        echoerr "$WAITFORIT_cmdname: waiting $WAITFORIT_TIMEOUT seconds for $WAITFORIT_HOST:$WAITFORIT_PORT"
    else
        echoerr "$WAITFORIT_cmdname: waiting for $WAITFORIT_HOST:$WAITFORIT_PORT without a timeout"
    fi
    WAITFORIT_start_ts=$(date +%s)
    while :
    do
        if [[ $WAITFORIT_ISBUSY -eq 1 ]]; then
            nc -z $WAITFORIT_HOST $WAITFORIT_PORT
            WAITFORIT_result=$?
        else
            (echo > /dev/tcp/$WAITFORIT_HOST/$WAITFORIT_PORT) >/dev/null 2>&1
            WAITFORIT_result=$?
        fi
        if [[ $WAITFORIT_result -eq 0 ]]; then
            WAITFORIT_end_ts=$(date +%s)
            echoerr "$WAITFORIT_cmdname: $WAITFORIT_HOST:$WAITFORIT_PORT is available after $((WAITFORIT_end_ts - WAITFORIT_start_ts)) seconds"
            break
        fi
        sleep 1
    done
    return $WAITFORIT_result
}

wait_for_wrapper()
{
    # In order to support SIGINT during timeout: http://unix.stackexchange.com/a/57692
    if [[ $WAITFORIT_QUIET -eq 1 ]]; then
        timeout $WAITFORIT_BUSYTIMEFLAG $WAITFORIT_TIMEOUT $0 --quiet --child --host=$WAITFORIT_HOST --port=$WAITFORIT_PORT --timeout=$WAITFORIT_TIMEOUT &
    else
        timeout $WAITFORIT_BUSYTIMEFLAG $WAITFORIT_TIMEOUT $0 --child --host=$WAITFORIT_HOST --port=$WAITFORIT_PORT --timeout=$WAITFORIT_TIMEOUT &
    fi
    WAITFORIT_PID=$!
    trap "kill -INT -$WAITFORIT_PID" INT
    wait $WAITFORIT_PID
    WAITFORIT_RESULT=$?
    if [[ $WAITFORIT_RESULT -ne 0 ]]; then
        echoerr "$WAITFORIT_cmdname: timeout occurred after waiting $WAITFORIT_TIMEOUT seconds for $WAITFORIT_HOST:$WAITFORIT_PORT"
    fi
    return $WAITFORIT_RESULT
}

# process arguments
while [[ $# -gt 0 ]]
do
    case "$1" in
        *:* )
        WAITFORIT_hostport=(${1//:/ })
        WAITFORIT_HOST=${WAITFORIT_hostport[0]}
        WAITFORIT_PORT=${WAITFORIT_hostport[1]}
        shift 1
        ;;
        --child)
        WAITFORIT_CHILD=1
        shift 1
        ;;
        -q | --quiet)
        WAITFORIT_QUIET=1
        shift 1
        ;;
        -s | --strict)
        WAITFORIT_STRICT=1
        shift 1
        ;;
        -h)
        WAITFORIT_HOST="$2"
        if [[ $WAITFORIT_HOST == "" ]]; then break; fi
        shift 2
        ;;
        --host=*)
        WAITFORIT_HOST="${1#*=}"
        shift 1
        ;;
        -p)
        WAITFORIT_PORT="$2"
        if [[ $WAITFORIT_PORT == "" ]]; then break; fi
        shift 2
        ;;
        --port=*)
        WAITFORIT_PORT="${1#*=}"
        shift 1
        ;;
        -t)
        WAITFORIT_TIMEOUT="$2"
        if [[ $WAITFORIT_TIMEOUT == "" ]]; then break; fi
        shift 2
        ;;
        --timeout=*)
        WAITFORIT_TIMEOUT="${1#*=}"
        shift 1
        ;;
        --)
        shift
        WAITFORIT_CLI=("$@")
        break
        ;;
        --help)
        usage
        ;;
        *)
        echoerr "Unknown argument: $1"
        usage
        ;;
    esac
done

if [[ "$WAITFORIT_HOST" == "" || "$WAITFORIT_PORT" == "" ]]; then
    echoerr "Error: you need to provide a host and port to test."
    usage
fi

WAITFORIT_TIMEOUT=${WAITFORIT_TIMEOUT:-15}
WAITFORIT_STRICT=${WAITFORIT_STRICT:-0}
WAITFORIT_CHILD=${WAITFORIT_CHILD:-0}
WAITFORIT_QUIET=${WAITFORIT_QUIET:-0}

# Check to see if timeout is from busybox?
WAITFORIT_TIMEOUT_PATH=$(type -p timeout)
WAITFORIT_TIMEOUT_PATH=$(realpath $WAITFORIT_TIMEOUT_PATH 2>/dev/null || echo $WAITFORIT_TIMEOUT_PATH)

WAITFORIT_BUSYTIMEFLAG=""
if [[ $WAITFORIT_TIMEOUT_PATH =~ "busybox" ]]; then
    WAITFORIT_ISBUSY=1
    # Check if busybox timeout uses -t flag
    # (recent Alpine versions don't support -t anymore)
    if timeout &>/dev/stdout | grep -q -e '-t '; then
        WAITFORIT_BUSYTIMEFLAG="-t"
    fi
else
    WAITFORIT_ISBUSY=0
fi

if [[ $WAITFORIT_CHILD -gt 0 ]]; then
    wait_for
    WAITFORIT_RESULT=$?
    exit $WAITFORIT_RESULT
else
    if [[ $WAITFORIT_TIMEOUT -gt 0 ]]; then
        wait_for_wrapper
        WAITFORIT_RESULT=$?
    else
        wait_for
        WAITFORIT_RESULT=$?
    fi
fi

if [[ $WAITFORIT_CLI != "" ]]; then
    if [[ $WAITFORIT_RESULT -ne 0 && $WAITFORIT_STRICT -eq 1 ]]; then
        echoerr "$WAITFORIT_cmdname: strict mode, refusing to execute subprocess"
        exit $WAITFORIT_RESULT
    fi
    exec "${WAITFORIT_CLI[@]}"
else
    exit $WAITFORIT_RESULT
fi
```

### **PASSO 7: Configurações de Ambiente**

```bash
# docker/env/.env.development
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
POSTGRES_DB=omaum_dev
POSTGRES_USER=omaum_user
POSTGRES_PASSWORD=omaum_password
DATABASE_URL=postgresql://omaum_user:omaum_password@omaum-db:5432/omaum_dev

# Redis
REDIS_PASSWORD=redis_dev_password
REDIS_URL=redis://:redis_dev_password@omaum-redis:6379/0

# Email (desenvolvimento)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Logs
LOG_LEVEL=DEBUG
```

```bash
# docker/env/.env.production
DEBUG=False
SECRET_KEY=your-super-secret-production-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
POSTGRES_DB=omaum_prod
POSTGRES_USER=omaum_prod_user
POSTGRES_PASSWORD=super-secure-password-here
DATABASE_URL=postgresql://omaum_prod_user:super-secure-password-here@omaum-db:5432/omaum_prod

# Redis
REDIS_PASSWORD=super-secure-redis-password
REDIS_URL=redis://:super-secure-redis-password@omaum-redis:6379/0

# Email (produção)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Logs
LOG_LEVEL=INFO

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### **PASSO 8: Makefile para Automação**

```makefile
# Makefile
.PHONY: help build up down logs shell test backup restore

# Variáveis
COMPOSE_FILE = docker/docker-compose.yml
COMPOSE_FILE_PROD = docker/docker-compose.prod.yml
PROJECT_NAME = omaum

help: ## Mostra esta ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Desenvolvimento
build: ## Constrói as imagens Docker
	docker-compose -f $(COMPOSE_FILE) build

up: ## Sobe o ambiente de desenvolvimento
	docker-compose -f $(COMPOSE_FILE) up -d

down: ## Para o ambiente de desenvolvimento
	docker-compose -f $(COMPOSE_FILE) down

logs: ## Mostra os logs dos containers
	docker-compose -f $(COMPOSE_FILE) logs -f

shell: ## Acessa o shell do container Django
	docker-compose -f $(COMPOSE_FILE) exec omaum-web bash

test: ## Executa os testes
	docker-compose -f $(COMPOSE_FILE) exec omaum-web python manage.py test

migrate: ## Executa migrações
	docker-compose -f $(COMPOSE_FILE) exec omaum-web python manage.py migrate

makemigrations: ## Cria novas migrações
	docker-compose -f $(COMPOSE_FILE) exec omaum-web python manage.py makemigrations

collectstatic: ## Coleta arquivos estáticos
	docker-compose -f $(COMPOSE_FILE) exec omaum-web python manage.py collectstatic --noinput

# Produção
build-prod: ## Constrói imagens para produção
	docker-compose -f $(COMPOSE_FILE_PROD) build

up-prod: ## Sobe ambiente de produção
	docker-compose -f $(COMPOSE_FILE_PROD) up -d

down-prod: ## Para ambiente de produção
	docker-compose -f $(COMPOSE_FILE_PROD) down

logs-prod: ## Logs do ambiente de produção
	docker-compose -f $(COMPOSE_FILE_PROD) logs -f

# Backup e Restore
backup: ## Cria backup do banco de dados
	docker-compose -f $(COMPOSE_FILE) exec omaum-db pg_dump -U omaum_user omaum_dev > backup_$(shell date +%Y%m%d_%H%M%S).sql

backup-prod: ## Cria backup do banco de produção
	docker-compose -f $(COMPOSE_FILE_PROD) exec omaum-db pg_dump -U $(POSTGRES_USER) $(POSTGRES_DB) > backup_prod_$(shell date +%Y%m%d_%H%M%S).sql

restore: ## Restaura backup (uso: make restore FILE=backup.sql)
	docker-compose -f $(COMPOSE_FILE) exec -T omaum-db psql -U omaum_user omaum_dev < $(FILE)

# Limpeza
clean: ## Remove containers, volumes e imagens não utilizados
	docker system prune -f
	docker volume prune -f

clean-all: ## Remove TUDO (cuidado!)
	docker-compose -f $(COMPOSE_FILE) down -v --rmi all
	docker system prune -af

# Monitoramento
stats: ## Mostra estatísticas dos containers
	docker stats

ps: ## Lista containers em execução
	docker-compose -f $(COMPOSE_FILE) ps

# Desenvolvimento
install: ## Instalação inicial do projeto
	cp docker/env/.env.example docker/env/.env.development
	make build
	make up
	sleep 10
	make migrate
	make collectstatic
	@echo "Projeto instalado! Acesse http://localhost:8000"

reset: ## Reset completo do ambiente de desenvolvimento
	make down
	docker volume rm omaum_db_data omaum_redis_data || true
	make up
	sleep 10
	make migrate
	make collectstatic
```

---

## 🚀 GUIA DE IMPLEMENTAÇÃO PASSO A PASSO

### **FASE 1: Preparação do Ambiente (1 dia)**

#### **1.1 Instalar Dependências**
```bash
# No servidor/máquina de desenvolvimento
sudo apt update
sudo apt install docker.io docker-compose git make

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Verificar instalação
docker --version
docker-compose --version
```

#### **1.2 Clonar e Preparar Projeto**
```bash
# Clonar projeto
git clone <url-do-repositorio> omaum
cd omaum

# Criar estrutura Docker
mkdir -p docker/{nginx,scripts,env}
mkdir -p requirements

# Copiar arquivos criados nos passos anteriores
# (Dockerfile, docker-compose.yml, etc.)
```

#### **1.3 Configurar Variáveis de Ambiente**
```bash
# Copiar template de variáveis
cp docker/env/.env.example docker/env/.env.development

# Editar variáveis conforme necessário
nano docker/env/.env.development
```

### **FASE 2: Configuração Django para Docker (1 dia)**

#### **2.1 Criar Settings por Ambiente**
```python
# omaum/settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'core',
    'alunos',
    'turmas',
    'presencas',
    'atividades',
    'cursos',
    'relatorios_presenca',
    'corporativo',  # Novo app para padrões corporativos
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'celery',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'omaum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'omaum.wsgi.application'

# Database
import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    )
}

# Cache (Redis)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'assets',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery Configuration
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'class': 'logging.FileHandler',
            'filename': '/app/logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': os.environ.get('LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'omaum': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
```

```python
# omaum/settings/development.py
from .base import *

DEBUG = True

# Configurações específicas de desenvolvimento
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS para desenvolvimento
CORS_ALLOW_ALL_ORIGINS = True

# Debug Toolbar (opcional)
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']
```

```python
# omaum/settings/production.py
from .base import *

DEBUG = False

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# CORS settings
CORS_ALLOWED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS if host != 'localhost'
]
```

#### **2.2 Criar Requirements**
```txt
# requirements/base.txt
Django==4.2.7
psycopg2-binary==2.9.7
redis==4.6.0
django-redis==5.3.0
celery==5.3.4
dj-database-url==2.1.0
gunicorn==21.2.0
Pillow==10.0.1
openpyxl==3.1.2
reportlab==4.0.4
djangorestframework==3.14.0
django-cors-headers==4.3.1
python-decouple==3.8
```

```txt
# requirements/development.txt
-r base.txt
django-debug-toolbar==4.2.0
pytest-django==4.5.2
factory-boy==3.3.0
coverage==7.3.2
```

```txt
# requirements/production.txt
-r base.txt
sentry-sdk==1.38.0
```

### **FASE 3: Implementação do Padrão Corporativo (2 dias)**

#### **3.1 Criar App Corporativo**
```bash
# Dentro do container ou ambiente
python manage.py startapp corporativo
```

#### **3.2 Implementar Sistema de Cabeçalhos/Rodapés**
```python
# corporativo/models.py
from django.db import models

class ConfiguracaoCorporativa(models.Model):
    """Configurações corporativas do sistema."""
    
    nome_organizacao = models.CharField(
        max_length=200,
        default='OM-AUM (Ordem Mística de Aspiração Universal ao Mestrado)'
    )
    logo = models.ImageField(upload_to='corporativo/logos/', blank=True)
    endereco = models.TextField(blank=True)
    telefone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    site = models.URLField(blank=True)
    
    # Configurações de relatórios
    mostrar_data_hora_cabecalho = models.BooleanField(default=True)
    formato_data_hora = models.CharField(
        max_length=50,
        default='%d/%m/%Y - %H:%M'
    )
    mostrar_numeracao_pagina = models.BooleanField(default=True)
    texto_rodape_personalizado = models.CharField(
        max_length=200,
        blank=True,
        help_text='Texto adicional para o rodapé (opcional)'
    )
    
    class Meta:
        verbose_name = 'Configuração Corporativa'
        verbose_name_plural = 'Configurações Corporativas'
    
    def __str__(self):
        return self.nome_organizacao
    
    @classmethod
    def get_configuracao(cls):
        """Retorna a configuração ativa ou cria uma padrão."""
        config, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'nome_organizacao': 'OM-AUM (Ordem Mística de Aspiração Universal ao Mestrado)'
            }
        )
        return config
```

```python
# corporativo/templatetags/corporativo_tags.py
from django import template
from django.utils import timezone
from ..models import ConfiguracaoCorporativa

register = template.Library()

@register.inclusion_tag('corporativo/cabecalho_relatorio.html')
def cabecalho_relatorio(titulo_relatorio):
    """Renderiza cabeçalho padrão para relatórios."""
    config = ConfiguracaoCorporativa.get_configuracao()
    return {
        'config': config,
        'titulo_relatorio': titulo_relatorio,
        'data_hora_atual': timezone.now(),
    }

@register.inclusion_tag('corporativo/rodape_relatorio.html')
def rodape_relatorio(numero_pagina=None):
    """Renderiza rodapé padrão para relatórios."""
    config = ConfiguracaoCorporativa.get_configuracao()
    return {
        'config': config,
        'numero_pagina': numero_pagina,
    }

@register.simple_tag
def nome_organizacao():
    """Retorna o nome da organização."""
    config = ConfiguracaoCorporativa.get_configuracao()
    return config.nome_organizacao

@register.simple_tag
def data_hora_formatada():
    """Retorna data/hora atual formatada."""
    config = ConfiguracaoCorporativa.get_configuracao()
    return timezone.now().strftime(config.formato_data_hora)
```

#### **3.3 Templates Corporativos**
```html
<!-- corporativo/templates/corporativo/cabecalho_relatorio.html -->
<div class="cabecalho-corporativo">
    <div class="linha-principal">
        <div class="nome-organizacao">
            {{ config.nome_organizacao }}
        </div>
        {% if config.mostrar_data_hora_cabecalho %}
        <div class="data-hora">
            {{ data_hora_atual|date:config.formato_data_hora }}
        </div>
        {% endif %}
    </div>
    <div class="linha-titulo">
        <h2>{{ titulo_relatorio }}</h2>
    </div>
</div>
```

```html
<!-- corporativo/templates/corporativo/rodape_relatorio.html -->
<div class="rodape-corporativo">
    {% if config.mostrar_numeracao_pagina %}
    <div class="numeracao-pagina">
        Página {% if numero_pagina %}{{ numero_pagina }}{% else %}1{% endif %}
    </div>
    {% endif %}
    {% if config.texto_rodape_personalizado %}
    <div class="texto-personalizado">
        {{ config.texto_rodape_personalizado }}
    </div>
    {% endif %}
</div>
```

```html
<!-- corporativo/templates/corporativo/base_relatorio.html -->
{% load static %}
{% load corporativo_tags %}
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% nome_organizacao %}{% endblock %}</title>
    
    <!-- CSS Corporativo -->
    <link href="{% static 'corporativo/css/relatorios.css' %}" rel="stylesheet">
    <link href="{% static 'corporativo/css/print.css' %}" rel="stylesheet" media="print">
    
    {% block extra_css %}{% endblock %}
</head>
<body class="relatorio-corporativo">
    <!-- Cabeçalho -->
    {% cabecalho_relatorio titulo_relatorio %}
    
    <!-- Conteúdo do Relatório -->
    <main class="conteudo-relatorio">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Rodapé -->
    {% rodape_relatorio %}
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### **FASE 4: Execução e Testes (1 dia)**

#### **4.1 Primeira Execução**
```bash
# Instalar projeto completo
make install

# Verificar se tudo está funcionando
make ps
make logs

# Acessar aplicação
# http://localhost:8000
```

#### **4.2 Testes de Funcionalidade**
```bash
# Executar testes
make test

# Verificar cobertura
docker-compose exec omaum-web coverage run --source='.' manage.py test
docker-compose exec omaum-web coverage report

# Testar geração de relatórios
# Acessar interface web e gerar relatórios
```

#### **4.3 Backup e Restore**
```bash
# Criar backup
make backup

# Testar restore
make restore FILE=backup_20231228_143022.sql
```

### **FASE 5: Deploy em Produção (1 dia)**

#### **4.1 Preparar Servidor de Produção**
```bash
# No servidor de produção
sudo apt update
sudo apt install docker.io docker-compose git

# Configurar firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Configurar SSL (Let's Encrypt)
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com
```

#### **4.2 Deploy**
```bash
# Clonar projeto no servidor
git clone <url> /opt/omaum
cd /opt/omaum

# Configurar variáveis de produção
cp docker/env/.env.example docker/env/.env.production
nano docker/env/.env.production

# Fazer deploy
make build-prod
make up-prod

# Verificar status
make logs-prod
```

---

## 📊 CRONOGRAMA DETALHADO

| Fase | Atividade | Duração | Responsável |
|------|-----------|---------|-------------|
| 1 | Preparação do ambiente Docker | 1 dia | DevOps |
| 2 | Configuração Django para Docker | 1 dia | Backend |
| 3 | Implementação padrão corporativo | 2 dias | Full Stack |
| 4 | Testes e validação | 1 dia | QA/Dev |
| 5 | Deploy em produção | 1 dia | DevOps |

**Total: 6 dias úteis**

---

## 🎯 BENEFÍCIOS DA SOLUÇÃO DOCKER

### **Desenvolvimento:**
- ✅ Ambiente idêntico para todos os desenvolvedores
- ✅ Setup em minutos com `make install`
- ✅ Isolamento completo de dependências
- ✅ Fácil reset do ambiente

### **Produção:**
- ✅ Deploy consistente e confiável
- ✅ Escalabilidade horizontal simples
- ✅ Rollback rápido em caso de problemas
- ✅ Monitoramento integrado

### **Manutenção:**
- ✅ Backup automatizado
- ✅ Logs centralizados
- ✅ Updates sem downtime
- ✅ Configuração por variáveis de ambiente

---

**Esta proposta com Docker garante um projeto moderno, escalável e fácil de manter, com o padrão corporativo implementado em todos os relatórios conforme solicitado.**

