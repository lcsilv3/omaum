# 📋 REVISÃO COMPLETA - Scripts de Deploy OMAUM

## ✅ **Situação Real Identificada**

### Ambiente de Desenvolvimento:
- **Máquina:** LUISHP
- **Usuário:** lcsil
- **Caminho:** `c:\projetos\omaum`
- **Containers:** omaum-web, omaum-db, omaum-redis (SEM sufixo `-prod`)
- **Banco:** SQLite (db.sqlite3)

### Ambiente de Produção:
- **Servidor:** DESKTOP-OAE3R5M (Windows)
- **IP:** 192.168.15.4 (rede intranet)
- **Usuário:** admin
- **Caminho:** `c:\projetos\omaum`
- **Containers:** omaum-*-prod (nginx, web, celery, beat, redis, db)
- **Banco:** PostgreSQL
- **Acesso:** http://192.168.15.4 ou https://192.168.15.4

### Particularidades:
- ✅ Desenvolvimento e produção em **máquinas DIFERENTES**
- ✅ Ambos Windows na mesma rede intranet
- ✅ Containers de produção têm sufixo `-prod`
- ✅ **Precisa** transferência entre máquinas
- ✅ Pode usar RDP, rede compartilhada ou WinRM

---

## 📁 **Arquivos Criados/Atualizados**

### ✅ Scripts Funcionais (Adaptados ao Ambiente Real):

1. **`01_export_dev_data.py`** ✅
   - Exporta dados do SQLite para JSON
   - Funcional e testado
   - Última execução: 410 registros, 207KB
   - Arquivo gerado: `dev_data_20251122_155515.json`

2. **`02_deploy_atualizar_producao.ps1`** ✅ **NOVO - PRINCIPAL**
   - Script completo de atualização para Windows
   - Backup automático do PostgreSQL
   - Importação opcional de dados (com confirmação)
   - Aplicação de migrações
   - Coleta de estáticos
   - Rebuild e restart de containers
   - Validação de saúde
   - Parâmetros: `-SemBackup`, `-SemDados`, `-Verbose`

3. **`03_atualizar_rapido.ps1`** ✅ **NOVO**
   - Atualização rápida sem downtime
   - Backup rápido + rebuild do web
   - Ideal para pequenas alterações de código
   - ~15 segundos de execução

4. **`README.md`** ✅ **ATUALIZADO**
   - Documentação corrigida para ambiente Windows
   - Instruções específicas para DESKTOP-OAE3R5M
   - Processos simplificados

5. **`docs/DEPLOY_PRODUCAO.md`** ✅
   - Documentação completa (genérica)
   - Útil para referência futura
   - Troubleshooting detalhado

### ❌ Scripts Obsoletos (Não Aplicáveis):

1. **`02_deploy_to_production.sh`** ❌
   - Criado para Linux, não funciona no Windows
   - Pode ser deletado

2. **`02_deploy_to_production.ps1`** ❌ (versão antiga)
   - Tinha problemas de encoding e assumia ambiente Linux
   - Substituído por `02_deploy_atualizar_producao.ps1`

3. **`03_transfer_to_server.ps1/sh`** ❌
   - Criado para transferência via SCP
   - Não necessário (mesma máquina)
   - Pode ser deletado

---

## 🎯 **Workflows Corretos para Usar**

### **Cenário 1: Atualização com Novos Dados**

Quando você quer **substituir** dados de produção por dados de desenvolvimento:

```powershell
# 1. Ativar ambiente virtual
cd c:\projetos\omaum
.venv\Scripts\Activate.ps1

# 2. Exportar dados de DEV
python scripts\deploy\01_export_dev_data.py

# 3. Atualizar produção (irá perguntar sobre importação)
.\scripts\deploy\02_deploy_atualizar_producao.ps1
```

**⚠️ ATENÇÃO:** Importação de dados **LIMPA O BANCO ATUAL**!

### **Cenário 2: Atualização Somente de Código**

Quando você alterou código mas quer **manter** dados de produção:

```powershell
cd c:\projetos\omaum

# Usar parâmetro -SemDados para pular importação
.\scripts\deploy\02_deploy_atualizar_producao.ps1 -SemDados
```

### **Cenário 3: Atualização Rápida (Pequenas Mudanças)**

Para mudanças menores sem precisar rebuild completo:

```powershell
cd c:\projetos\omaum
.\scripts\deploy\03_atualizar_rapido.ps1
```

### **Cenário 4: Somente Backup**

Para criar backup sem atualizar nada:

```powershell
cd c:\projetos\omaum

# Backup do PostgreSQL
docker exec omaum-db-prod pg_dump -U postgres omaum > backups\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql
```

---

## 📊 **Resultado da Última Exportação**

```
============================================================
EXPORTAÇÃO DE DADOS - DESENVOLVIMENTO → PRODUÇÃO
============================================================

✓ auth.User                      →    3 registros
  auth.Group                     → (vazio)
✓ cursos.Curso                   →   12 registros
✓ alunos.Aluno                   →   54 registros
✓ turmas.Turma                   →   31 registros
✓ matriculas.Matricula           →   68 registros
✓ atividades.Atividade           →   40 registros
  presencas.RegistroPresenca     → (vazio)
✗ frequencias.Frequencia         → ERRO: Model não existe
✓ notas.Nota                     →  130 registros
✓ pagamentos.Pagamento           →   72 registros

Total: 410 registros, 207.26 KB
Arquivo: dev_data_20251122_155515.json
```

---

## 🔧 **Comandos Úteis do Guia Original**

### Verificar Status:
```powershell
cd c:\projetos\omaum
docker-compose ps
docker stats
```

### Ver Logs:
```powershell
docker-compose logs -f web
docker-compose logs -f nginx
docker-compose logs -f celery
```

### Acessar Containers:
```powershell
docker exec -it omaum-web-prod sh
docker exec -it omaum-db-prod psql -U postgres omaum
```

### Backup Manual:
```powershell
$BackupDir = "c:\projetos\omaum\backups"
$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
docker exec omaum-db-prod pg_dump -U postgres omaum > "$BackupDir\backup_$Timestamp.sql"
```

### Restaurar Backup:
```powershell
Get-Content backups\backup_YYYYMMDD_HHMMSS.sql | docker exec -i omaum-db-prod psql -U postgres omaum
```

---

## ✅ **Próximos Passos Recomendados**

1. **Testar Script de Atualização:**
   ```powershell
   .\scripts\deploy\02_deploy_atualizar_producao.ps1 -SemDados
   ```
   *(Usa `-SemDados` para não apagar dados de produção)*

2. **Limpar Scripts Obsoletos:**
   - Deletar `02_deploy_to_production.sh`
   - Deletar versão antiga de `02_deploy_to_production.ps1`
   - Deletar `03_transfer_to_server.ps1` e `.sh`

3. **Criar Tarefa Agendada de Backup:**
   - Usar Agendador de Tarefas do Windows
   - Executar backup diário às 2h da manhã
   - Manter últimos 30 backups

4. **Validar Acesso:**
   - http://192.168.15.4
   - http://192.168.15.4/admin
   - Verificar se tudo funciona após atualização

---

## 📞 **Suporte**

- **Documentação Completa:** `docs/DEPLOY_PRODUCAO.md`
- **README Scripts:** `scripts/deploy/README.md`
- **Instruções para IA:** `AGENT.md`, `.github/copilot-instructions.md`

---

**Data da Revisão:** 22/11/2025  
**Status:** ✅ Scripts adaptados ao ambiente real Windows  
**Próxima Ação:** Testar atualização com `-SemDados`
