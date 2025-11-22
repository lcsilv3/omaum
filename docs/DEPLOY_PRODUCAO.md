# OMAUM - Deploy (Implantação) para Produção

## 📋 Sumário

1. [Visão Geral](#visão-geral)
2. [Arquitetura de Produção](#arquitetura-de-produção)
3. [Pré-requisitos](#pré-requisitos)
4. [Configuração Inicial](#configuração-inicial)
5. [Processo de Deploy](#processo-de-deploy)
6. [Monitoramento e Logs](#monitoramento-e-logs)
7. [Rollback e Recuperação](#rollback-e-recuperação)
8. [Troubleshooting](#troubleshooting)
9. [Manutenção](#manutenção)
10. [Checklist de Deploy](#checklist-de-deploy)

---

## 🎯 Visão Geral

Este documento descreve o processo completo de implantação do sistema OMAUM em ambiente de produção, utilizando Docker Compose com estratégia de **zero-downtime** (sem interrupção do serviço).

### Características do Deploy

- ✅ **Zero-downtime**: Rolling restart sem interrupção
- ✅ **Backup automático**: Cópia de segurança antes de cada deploy
- ✅ **Validação automática**: Testes após implantação
- ✅ **Rollback facilitado**: Recuperação rápida em caso de problemas
- ✅ **Logs detalhados**: Rastreabilidade completa de cada etapa

### Tecnologias Utilizadas

- **Django 5.2.5**: Framework web Python
- **PostgreSQL 15**: Banco de dados relacional
- **Redis 7**: Cache e fila de tarefas
- **Celery**: Processamento assíncrono
- **Nginx**: Servidor web e proxy reverso
- **Gunicorn**: Servidor de aplicação WSGI
- **Docker Compose**: Orquestração de containers

---

## 🏗️ Arquitetura de Produção

### Diagrama de Serviços

```
┌─────────────────────────────────────────────────┐
│                   Internet                       │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Nginx (Porta 80)    │  ◄── Proxy reverso + arquivos estáticos
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Gunicorn (Porta 8000)│  ◄── Servidor de aplicação Django
         │    (omaum-web)        │
         └───────┬───────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌──────────┐
│ PostgreSQL│ │ Redis  │ │  Celery  │
│  (Porta   │ │ (Porta │ │ Workers  │
│   5432)   │ │  6379) │ │          │
└────────┘  └────────┘  └──────────┘
                              │
                              ▼
                        ┌──────────┐
                        │  Celery  │
                        │   Beat   │
                        └──────────┘
```

### Serviços Docker

| Serviço | Container | Porta | Descrição |
|---------|-----------|-------|-----------|
| **Nginx** | omaum-nginx | 80, 443 | Proxy reverso e servidor de arquivos estáticos |
| **Django** | omaum-web | 8000 | Aplicação web principal |
| **PostgreSQL** | omaum-db | 5432 | Banco de dados relacional |
| **Redis** | omaum-redis | 6379 | Cache e broker de mensagens |
| **Celery Worker** | omaum-celery | - | Processamento de tarefas assíncronas |
| **Celery Beat** | omaum-celery-beat | - | Agendamento de tarefas periódicas |

---

## ✅ Pré-requisitos

### Servidor de Produção

- **Sistema Operacional**: Linux (Ubuntu 20.04+ ou similar)
- **CPU**: Mínimo 2 cores (recomendado 4+)
- **RAM**: Mínimo 4GB (recomendado 8GB+)
- **Disco**: Mínimo 20GB livres (SSD recomendado)
- **Docker**: Versão 20.10+
- **Docker Compose**: Versão 2.0+

### Domínio e DNS

- Domínio registrado (ex: `omaum.edu.br`)
- Registro DNS tipo A apontando para IP do servidor
- Certificado SSL (Let's Encrypt recomendado)

### Acessos Necessários

- Acesso SSH ao servidor de produção
- Credenciais de banco de dados PostgreSQL
- Credenciais de email (SMTP)
- Chaves de API externas (se aplicável)

### Ambiente Local

- Python 3.11+
- Git configurado
- Acesso ao repositório do projeto

---

## ⚙️ Configuração Inicial

### 1. Preparar Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalação
docker --version
docker-compose --version
```

### 2. Clonar Repositório

```bash
# Criar diretório do projeto
sudo mkdir -p /var/www/omaum
sudo chown $USER:$USER /var/www/omaum

# Clonar código
cd /var/www/omaum
git clone https://github.com/seu-usuario/omaum.git .
git checkout main
```

### 3. Configurar Variáveis de Ambiente

Crie o arquivo `docker/.env.production`:

```bash
cd /var/www/omaum/docker
cp .env.production.example .env.production
nano .env.production
```

**Configurações essenciais:**

```env
# ============================================
# DJANGO
# ============================================
SECRET_KEY=sua_chave_secreta_aqui_minimo_50_caracteres_aleatorios
DEBUG=False
ALLOWED_HOSTS=omaum.edu.br,www.omaum.edu.br,localhost

# ============================================
# BANCO DE DADOS
# ============================================
POSTGRES_DB=omaum_prod
POSTGRES_USER=omaum_user
POSTGRES_PASSWORD=senha_super_segura_123!@#$%
DATABASE_URL=postgresql://omaum_user:senha_super_segura_123!@#$%@omaum-db:5432/omaum_prod

# ============================================
# REDIS
# ============================================
REDIS_PASSWORD=redis_senha_segura_456!@#$%
REDIS_URL=redis://:redis_senha_segura_456!@#$%@omaum-redis:6379/0

# ============================================
# EMAIL
# ============================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=sistema@omaum.edu.br
EMAIL_HOST_PASSWORD=sua_senha_de_app_do_gmail
DEFAULT_FROM_EMAIL=OMAUM <sistema@omaum.edu.br>

# ============================================
# SEGURANÇA
# ============================================
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True

# ============================================
# CELERY
# ============================================
CELERY_BROKER_URL=redis://:redis_senha_segura_456!@#$%@omaum-redis:6379/1
CELERY_RESULT_BACKEND=redis://:redis_senha_segura_456!@#$%@omaum-redis:6379/1

# ============================================
# LOGS
# ============================================
LOG_LEVEL=INFO
```

> **⚠️ IMPORTANTE:** Gere valores aleatórios fortes para `SECRET_KEY`, `POSTGRES_PASSWORD` e `REDIS_PASSWORD`!

### 4. Gerar SECRET_KEY

```bash
# Gerar SECRET_KEY aleatória
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 5. Configurar Nginx (SSL)

```bash
# Instalar Certbot para Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado SSL
sudo certbot --nginx -d omaum.edu.br -d www.omaum.edu.br
```

---

## 🚀 Processo de Deploy

### Deploy Completo (Primeira Vez)

#### **Etapa 1: Exportar Dados de Desenvolvimento**

No ambiente de **desenvolvimento** (Windows/Local):

```powershell
# Ativar ambiente virtual
cd C:\projetos\omaum
.venv\Scripts\Activate.ps1

# Executar exportação
python scripts/deploy/01_export_dev_data.py
```

**Saída esperada:**

```
============================================================
EXPORTAÇÃO DE DADOS - DESENVOLVIMENTO → PRODUÇÃO
============================================================

✓ auth.User                    →   15 registros
✓ auth.Group                   →    3 registros
✓ cursos.Curso                 →   12 registros
✓ alunos.Aluno                 →  150 registros
✓ turmas.Turma                 →   31 registros
✓ matriculas.Matricula         →  200 registros
✓ atividades.Atividade         →   45 registros
✓ presencas.RegistroPresenca   →  500 registros
✓ frequencias.Frequencia       →  150 registros
✓ notas.Nota                   →  100 registros
✓ pagamentos.Pagamento         →   80 registros

------------------------------------------------------------
Serializando dados...
✓ Dados exportados com sucesso!

============================================================
RESUMO DA EXPORTAÇÃO
============================================================
Arquivo: scripts/deploy/exports/dev_data_20251122_143022.json
Tamanho: 1548.23 KB
Total de modelos: 11
Total de registros: 1286
============================================================

✅ Exportação concluída!
📁 Arquivo: scripts/deploy/exports/dev_data_20251122_143022.json
```

#### **Etapa 2: Transferir Arquivos para Produção**

```bash
# Copiar arquivo de exportação para servidor
scp scripts/deploy/exports/dev_data_*.json usuario@servidor:/var/www/omaum/scripts/deploy/exports/

# Ou usar rsync
rsync -avz --progress scripts/deploy/exports/ usuario@servidor:/var/www/omaum/scripts/deploy/exports/
```

#### **Etapa 3: Deploy em Produção**

No servidor de **produção** (Linux):

```bash
# Conectar via SSH
ssh usuario@servidor

# Navegar para diretório do projeto
cd /var/www/omaum

# Executar script de deploy
chmod +x scripts/deploy/02_deploy_to_production.sh
./scripts/deploy/02_deploy_to_production.sh
```

**Fluxo de execução:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DEPLOY ZERO-DOWNTIME - OMAUM PRODUÇÃO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Iniciar deploy para produção? (y/N): y

[INFO] Verificando pré-requisitos...
[✓] Pré-requisitos verificados

[INFO] Criando backup do banco de dados de produção...
[✓] Backup criado: backups/20251122_143530/db_backup.sql (2.4 MB)

[INFO] Construindo novas imagens Docker...
[✓] Imagens construídas com sucesso

[INFO] Importando dados de desenvolvimento...
[INFO] Usando arquivo: scripts/deploy/exports/dev_data_20251122_143022.json
[⚠] Limpando banco de dados atual...
[INFO] Importando dados...
[✓] Dados importados com sucesso

[INFO] Aplicando migrações do banco de dados...
[✓] Migrações aplicadas

[INFO] Coletando arquivos estáticos...
[✓] Arquivos estáticos coletados

[INFO] Iniciando rolling restart dos serviços...
[INFO] Reiniciando omaum-celery-beat...
[✓] omaum-celery-beat reiniciado
[INFO] Reiniciando omaum-celery...
[✓] omaum-celery reiniciado
[INFO] Reiniciando omaum-web...
[✓] omaum-web reiniciado
[✓] Rolling restart concluído

[INFO] Verificando saúde dos serviços...
[✓] Verificação de saúde concluída

[INFO] Executando smoke tests...
[✓] Health check: OK
[INFO] Turmas no banco: 31
[✓] Dados verificados: OK
[✓] Smoke tests concluídos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[✓] DEPLOY CONCLUÍDO COM SUCESSO!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[INFO] Backup salvo em: backups/20251122_143530
```

### Deploy de Atualização (Sem Dados)

Para deploys subsequentes apenas com atualizações de código:

```bash
# Atualizar código
cd /var/www/omaum
git pull origin main

# Build e restart
cd docker
docker-compose -f docker-compose.prod.yml build --pull
docker-compose -f docker-compose.prod.yml up -d --no-deps omaum-web

# Aplicar migrações
docker-compose -f docker-compose.prod.yml exec omaum-web python manage.py migrate

# Coletar estáticos
docker-compose -f docker-compose.prod.yml exec omaum-web python manage.py collectstatic --no-input
```

---

## 📊 Monitoramento e Logs

### Visualizar Logs

```bash
# Logs de todos os serviços
docker-compose -f docker/docker-compose.prod.yml logs -f

# Logs de um serviço específico
docker-compose -f docker/docker-compose.prod.yml logs -f omaum-web

# Últimas 100 linhas
docker-compose -f docker/docker-compose.prod.yml logs --tail=100 omaum-web

# Logs do Nginx
docker-compose -f docker/docker-compose.prod.yml logs -f omaum-nginx

# Logs do Celery
docker-compose -f docker/docker-compose.prod.yml logs -f omaum-celery
```

### Status dos Containers

```bash
# Verificar status de todos os containers
docker-compose -f docker/docker-compose.prod.yml ps

# Verificar consumo de recursos
docker stats

# Health check manual
curl http://localhost/health/
```

### Monitoramento de Banco de Dados

```bash
# Conectar ao PostgreSQL
docker-compose -f docker/docker-compose.prod.yml exec omaum-db psql -U omaum_user -d omaum_prod

# Consultas úteis
\dt                          # Listar tabelas
SELECT COUNT(*) FROM turmas_turma;
SELECT COUNT(*) FROM alunos_aluno;
\q                           # Sair
```

---

## 🔄 Rollback e Recuperação

### Rollback de Banco de Dados

```bash
# Listar backups disponíveis
ls -lh backups/

# Restaurar backup específico
cd /var/www/omaum
docker-compose -f docker/docker-compose.prod.yml exec -T omaum-db \
  psql -U omaum_user -d omaum_prod < backups/20251122_143530/db_backup.sql

# Reiniciar serviços
docker-compose -f docker/docker-compose.prod.yml restart
```

### Rollback de Código

```bash
# Verificar commits recentes
git log --oneline -10

# Voltar para commit específico
git reset --hard <commit-hash>

# Rebuild e restart
cd docker
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

### Backup Manual Emergencial

```bash
# Criar backup completo
mkdir -p /backup/emergency_$(date +%Y%m%d_%H%M%S)

# Backup do banco
docker-compose -f docker/docker-compose.prod.yml exec -T omaum-db \
  pg_dump -U omaum_user -d omaum_prod > /backup/emergency_$(date +%Y%m%d_%H%M%S)/db.sql

# Backup de arquivos de mídia
tar -czf /backup/emergency_$(date +%Y%m%d_%H%M%S)/media.tar.gz media/
```

---

## 🔧 Troubleshooting

### Problema: Containers não iniciam

**Sintomas:**
```
Error: Cannot start service omaum-web: driver failed programming external connectivity
```

**Solução:**
```bash
# Verificar portas em uso
sudo netstat -tulpn | grep -E ':(80|443|5432|6379)'

# Parar containers conflitantes
docker stop $(docker ps -aq)

# Reiniciar Docker
sudo systemctl restart docker

# Tentar novamente
docker-compose -f docker/docker-compose.prod.yml up -d
```

### Problema: Erro de conexão com banco de dados

**Sintomas:**
```
django.db.utils.OperationalError: could not connect to server
```

**Solução:**
```bash
# Verificar se PostgreSQL está rodando
docker-compose -f docker/docker-compose.prod.yml ps omaum-db

# Verificar logs do banco
docker-compose -f docker/docker-compose.prod.yml logs omaum-db

# Verificar variáveis de ambiente
docker-compose -f docker/docker-compose.prod.yml exec omaum-web env | grep DATABASE

# Testar conexão manual
docker-compose -f docker/docker-compose.prod.yml exec omaum-db \
  psql -U omaum_user -d omaum_prod -c "SELECT 1;"
```

### Problema: Arquivos estáticos não carregam

**Sintomas:**
- CSS/JS não carregam (erro 404)
- Páginas sem formatação

**Solução:**
```bash
# Recoletar arquivos estáticos
docker-compose -f docker/docker-compose.prod.yml exec omaum-web \
  python manage.py collectstatic --no-input --clear

# Verificar permissões
docker-compose -f docker/docker-compose.prod.yml exec omaum-web \
  ls -la /app/staticfiles/

# Reiniciar Nginx
docker-compose -f docker/docker-compose.prod.yml restart omaum-nginx
```

### Problema: Erro 502 Bad Gateway

**Sintomas:**
- Nginx retorna erro 502
- Aplicação inacessível

**Solução:**
```bash
# Verificar se Gunicorn está rodando
docker-compose -f docker/docker-compose.prod.yml exec omaum-web \
  ps aux | grep gunicorn

# Verificar logs do Nginx
docker-compose -f docker/docker-compose.prod.yml logs omaum-nginx

# Verificar configuração do Nginx
docker-compose -f docker/docker-compose.prod.yml exec omaum-nginx \
  nginx -t

# Reiniciar serviços
docker-compose -f docker/docker-compose.prod.yml restart omaum-web omaum-nginx
```

### Problema: Tarefas do Celery não executam

**Sintomas:**
- Tarefas agendadas não rodam
- Filas acumulam

**Solução:**
```bash
# Verificar se Celery está rodando
docker-compose -f docker/docker-compose.prod.yml ps omaum-celery

# Verificar conexão com Redis
docker-compose -f docker/docker-compose.prod.yml exec omaum-redis \
  redis-cli -a ${REDIS_PASSWORD} ping

# Verificar logs do Celery
docker-compose -f docker/docker-compose.prod.yml logs -f omaum-celery

# Reiniciar workers
docker-compose -f docker/docker-compose.prod.yml restart omaum-celery omaum-celery-beat
```

---

## 🛠️ Manutenção

### Manutenção Preventiva Semanal

```bash
# 1. Verificar espaço em disco
df -h

# 2. Limpar containers parados
docker container prune -f

# 3. Limpar imagens não utilizadas
docker image prune -a -f

# 4. Limpar volumes órfãos
docker volume prune -f

# 5. Backup do banco
cd /var/www/omaum
./scripts/backup_weekly.sh

# 6. Verificar logs grandes
du -sh logs/
```

### Atualização de Dependências

```bash
# Atualizar imagens base
cd docker
docker-compose -f docker-compose.prod.yml pull

# Rebuild com novas dependências
docker-compose -f docker-compose.prod.yml build --pull --no-cache

# Restart com zero-downtime
./scripts/deploy/02_deploy_to_production.sh
```

### Rotação de Logs

Adicionar em `/etc/logrotate.d/omaum`:

```
/var/www/omaum/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        docker-compose -f /var/www/omaum/docker/docker-compose.prod.yml exec omaum-web \
          kill -USR1 $(cat /tmp/gunicorn.pid)
    endscript
}
```

---

## ✅ Checklist de Deploy

### Antes do Deploy

- [ ] Código commitado e pushed para repositório
- [ ] Branch `main` atualizada
- [ ] Testes locais passando
- [ ] Migrações criadas e testadas
- [ ] Arquivo `.env.production` atualizado
- [ ] Backup manual adicional realizado
- [ ] Stakeholders notificados sobre deploy
- [ ] Janela de manutenção agendada (se necessário)
- [ ] Certificado SSL válido e não expirado

### Durante o Deploy

- [ ] Backup automático criado com sucesso
- [ ] Imagens Docker construídas sem erros
- [ ] Dados importados corretamente
- [ ] Migrações aplicadas sem falhas
- [ ] Arquivos estáticos coletados
- [ ] Rolling restart executado
- [ ] Health checks passando
- [ ] Smoke tests executados com sucesso

### Após o Deploy

- [ ] Aplicação acessível via navegador
- [ ] Login funcionando corretamente
- [ ] Páginas principais carregando
- [ ] CSS/JS aplicados corretamente
- [ ] Dados visíveis (turmas, alunos, etc.)
- [ ] Relatórios gerando PDFs
- [ ] Emails sendo enviados
- [ ] Tarefas do Celery executando
- [ ] Logs sem erros críticos
- [ ] Monitoramento ativo
- [ ] Documentação de deploy atualizada

---

## 📞 Suporte e Contatos

### Em Caso de Emergência

1. **Verificar logs**: `docker-compose logs -f`
2. **Consultar backups**: `ls -lh backups/`
3. **Executar rollback**: Seguir seção [Rollback e Recuperação](#rollback-e-recuperação)
4. **Contatar equipe técnica**: suporte@omaum.edu.br

### Documentação Adicional

- **README.md**: Visão geral do projeto
- **AGENT.md**: Instruções para agentes de IA
- **scripts/deploy/README.md**: Detalhes dos scripts de deploy
- **docs/**: Documentação técnica completa

### Recursos Úteis

- [Documentação Django](https://docs.djangoproject.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

## 📝 Histórico de Versões

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0.0 | 22/11/2025 | Sistema OMAUM | Versão inicial do documento de deploy |

---

**Última atualização:** 22 de novembro de 2025  
**Mantido por:** Equipe OMAUM  
**Contato:** suporte@omaum.edu.br
