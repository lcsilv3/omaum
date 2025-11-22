# 🚀 Scripts de Deploy e Atualização - OMAUM

Scripts para deploy e atualização do sistema OMAUM em produção.

## 📋 Informações do Ambiente

### **Máquina de Desenvolvimento:**
- **Nome:** LUISHP
- **Usuário:** lcsil
- **Caminho:** `c:\projetos\omaum`
- **Containers:** omaum-web, omaum-db, omaum-redis (sem sufixo `-prod`)
- **Banco:** SQLite (db.sqlite3)

### **Servidor de Produção:**
- **Nome:** DESKTOP-OAE3R5M
- **IP Intranet:** 192.168.15.4
- **Usuário:** admin
- **Caminho:** `c:\projetos\omaum`
- **Containers:** omaum-*-prod (nginx, web, celery, beat, redis, db)
- **Banco:** PostgreSQL
- **Acesso Web:** http://192.168.15.4 ou https://192.168.15.4

## 🎯 Pré-requisitos

### No Desenvolvimento (LUISHP):
- Python 3.11+ com ambiente virtual
- Acesso de rede ao servidor de produção

### Na Produção (DESKTOP-OAE3R5M):
- Docker e Docker Compose instalados
- PowerShell 5.1+
- Containers em execução

## 🔄 Processo Completo de Deploy

### **PASSO 1: Exportar Dados (Na Máquina de Desenvolvimento - LUISHP)**

```powershell
# Ativar ambiente virtual
cd c:\projetos\omaum
.venv\Scripts\Activate.ps1

# Exportar dados do SQLite
python scripts\deploy\01_export_dev_data.py
```

**Resultado:** Arquivo `scripts\deploy\exports\dev_data_YYYYMMDD_HHMMSS.json`

---

### **PASSO 2: Transferir Dados para Produção**

#### **Opção A: Transferência Automática** ⭐ *Recomendado*

```powershell
# Ainda na máquina de desenvolvimento (LUISHP)
.\scripts\deploy\04_transferir_para_producao.ps1
```

O script tentará automaticamente:
1. ✅ Compartilhamento de rede (\\192.168.15.4\c$)
2. ✅ PowerShell Remoting (WinRM)
3. ✅ PsExec (se instalado)
4. ❌ Se falhar: Mostra instruções manuais

#### **Opção B: Transferência Manual via RDP**

1. Abrir Remote Desktop:
   ```powershell
   mstsc /v:192.168.15.4
   ```

2. Na sessão RDP, acessar:
   ```
   \\LUISHP\c$\projetos\omaum\scripts\deploy\exports\
   ```

3. Copiar arquivo `dev_data_*.json` para:
   ```
   c:\projetos\omaum\scripts\deploy\exports\
   ```

#### **Opção C: Pendrive/Mídia Removível**

```powershell
# Copiar para pendrive (E:)
Copy-Item "scripts\deploy\exports\dev_data_*.json" E:\

# Depois, no servidor, copiar para:
# c:\projetos\omaum\scripts\deploy\exports\
```

---

### **PASSO 3: Executar Deploy (No Servidor de Produção - DESKTOP-OAE3R5M)**

Conecte ao servidor via RDP ou fisicamente:

```powershell
# No servidor de produção
cd c:\projetos\omaum

# Executar atualização completa
.\scripts\deploy\02_deploy_atualizar_producao.ps1
```

**O script irá:**
1. ✅ Verificar se está no servidor correto
2. ✅ Fazer backup automático do PostgreSQL
3. ✅ Verificar/atualizar código via Git
4. ✅ Perguntar se deseja importar dados (⚠️ LIMPA O BANCO!)
5. ✅ Aplicar migrações
6. ✅ Coletar arquivos estáticos
7. ✅ Reconstruir e reiniciar containers
8. ✅ Validar funcionamento

---

### **⚡ Atualização Rápida (Somente Código - Sem Dados)**

Se você só alterou código e quer manter dados de produção:

```powershell
# No servidor de produção
cd c:\projetos\omaum
.\scripts\deploy\03_atualizar_rapido.ps1
```

## 📊 Etapas do Deploy

O script executa automaticamente:

1. **✅ Verificação de Pré-requisitos**
   - Docker instalado e rodando
   - Arquivos de configuração presentes
   - Permissões adequadas

2. **🛡️ Backup do Banco de Produção**
   - Cria dump do PostgreSQL atual
   - Salva em `backups/YYYYMMDD_HHMMSS/`

3. **📦 Build de Imagens Docker**
   - Pull de imagens base atualizadas
   - Build das imagens customizadas

4. **📥 Importação de Dados**
   - Limpa banco de produção
   - Importa dados de desenvolvimento
   - Preserva estrutura de FK

5. **🔄 Aplicação de Migrações**
   - Executa `python manage.py migrate`
   - Atualiza schema do banco

6. **📁 Coleta de Arquivos Estáticos**
   - Executa `collectstatic --clear`
   - Atualiza arquivos CSS/JS/imagens

7. **🔄 Rolling Restart**
   - Reinicia serviços sem downtime
   - Escala temporariamente para 2 instâncias
   - Remove instâncias antigas após healthcheck

8. **✅ Testes de Validação**
   - Health checks HTTP
   - Verificação de dados no banco
   - Análise de logs

## 🔧 Configuração do Ambiente

### **Arquivo `.env.production`**

Crie em `docker/.env.production`:

```env
# Banco de Dados
POSTGRES_DB=omaum_prod
POSTGRES_USER=omaum_user
POSTGRES_PASSWORD=senha_super_segura_aqui_123!@#

# Redis
REDIS_PASSWORD=redis_senha_segura_aqui_456!@#

# Django
SECRET_KEY=chave_aleatoria_com_50_caracteres_ou_mais_aqui
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com,localhost

# Email (ajuste conforme seu provedor)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_app

# Outros
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

## 🛡️ Segurança

- ✅ **Backups automáticos** antes de cada deploy
- ✅ **Zero-downtime** com rolling restart
- ✅ **Validação automática** após deploy
- ✅ **Logs detalhados** de cada etapa
- ✅ **Rollback possível** via backups

## 📝 Troubleshooting

### **Erro: "Nenhum arquivo de exportação encontrado"**

```powershell
# Execute novamente a exportação
python scripts/deploy/01_export_dev_data.py
```

### **Erro: "Health check failed"**

```bash
# Verificar logs do container
docker logs omaum-web-prod --tail 50

# Verificar status dos serviços
docker-compose -f docker/docker-compose.prod.yml ps
```

### **Rollback para Backup Anterior**

```bash
# Restaurar banco a partir do backup
docker exec -i omaum-db-prod psql -U omaum_user -d omaum_prod < backups/YYYYMMDD_HHMMSS/db_backup.sql

# Reiniciar serviços
cd docker
docker-compose -f docker-compose.prod.yml restart
```

## 📊 Estrutura de Arquivos

```
scripts/deploy/
├── 01_export_dev_data.py          # Exportação de dados (dev)
├── 02_deploy_to_production.sh     # Deploy (Linux/Mac)
├── 02_deploy_to_production.ps1    # Deploy (Windows)
├── README.md                       # Esta documentação
└── exports/                        # Dados exportados
    ├── dev_data_YYYYMMDD_HHMMSS.json
    └── stats_YYYYMMDD_HHMMSS.json
```

## 🎯 Checklist Pré-Deploy

- [ ] Código commitado e pushed para repositório
- [ ] Testes locais executados com sucesso
- [ ] Migrações criadas e testadas
- [ ] Arquivo `.env.production` atualizado
- [ ] Backup manual adicional realizado (opcional)
- [ ] Stakeholders notificados sobre deploy
- [ ] Janela de manutenção agendada (se necessário)

## 🆘 Suporte

Em caso de problemas:
1. Verifique os logs: `docker logs omaum-web-prod`
2. Consulte backups em: `backups/`
3. Contate: suporte@omaum.edu.br

---

**Última atualização:** 22/11/2025
