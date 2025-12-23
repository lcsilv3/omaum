# 🌐 Portas de Acesso - OMAUM

> **Data:** 23 de dezembro de 2025  
> **Versão:** 1.0

## 📋 Resumo Executivo

Este documento define **como acessar corretamente** os ambientes de desenvolvimento e produção do projeto OMAUM, especialmente quanto às portas e servidores web.

---

## 🚀 Ambientes e Portas

### ✅ **DESENVOLVIMENTO** (omaum-dev)

**Como subir:**
```powershell
cd E:\projetos\omaum\docker
docker compose -p omaum-dev -f docker-compose.yml -f docker-compose.dev.override.yml up -d
```

**Acesso correto:**
- **URL Principal:** `http://localhost:8001/`
- **Arquivos estáticos:** `http://localhost:8001/static/`
- **Admin:** `http://localhost:8001/admin/`

**Configuração:**
- `DEBUG=True`
- Django serve arquivos estáticos diretamente (via `django.contrib.staticfiles`)
- Não precisa de NGINX
- **Porta 8001** exposta diretamente do Django/runserver

---

### ✅ **PRODUÇÃO** (omaum-prod)

**Como subir:**
```powershell
cd E:\projetos\omaum\docker
docker compose --profile production -p omaum-prod --env-file ..\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml up -d
```

**Acesso correto:**
- **URL Principal:** `http://localhost/` ← **SEM PORTA!**
- **Arquivos estáticos:** `http://localhost/static/`
- **Admin:** `http://localhost/admin/`

**Configuração:**
- `DEBUG=False`
- **NGINX** (porta 80) serve arquivos estáticos de `/var/www/static/`
- Gunicorn (porta 8000 interna) serve apenas o Django
- **NUNCA acesse diretamente `localhost:8000` em produção!**

---

## 🚨 PROBLEMA COMUM: Acessar porta errada em produção

### ❌ **ERRADO** (não funciona):

```
http://localhost:8000/turmas/32/
```

**Sintomas:**
- Logo não aparece (apenas texto "Log")
- CSS/JavaScript podem não carregar
- Imagens quebradas
- Erro 404 para `/static/img/logo.png`

**Motivo:**
- Django com `DEBUG=False` **NÃO SERVE** arquivos estáticos
- A porta 8000 é apenas para debugging do Django
- Arquivos estáticos devem ser servidos pelo NGINX

---

### ✅ **CORRETO** (funciona perfeitamente):

```
http://localhost/turmas/32/
```

**Resultado:**
- ✅ Logo aparece corretamente
- ✅ CSS aplicado
- ✅ JavaScript funciona
- ✅ Todas as imagens carregam
- ✅ Resposta 200 OK para `/static/img/logo.png`

---

## 🔍 Diagnóstico de Problemas

### Testar se arquivos estáticos estão sendo servidos:

**DEV (porta 8001):**
```powershell
curl -I http://localhost:8001/static/img/logo.png
# Esperado: HTTP/1.1 200 OK
```

**PROD (porta 80 via NGINX):**
```powershell
curl -I http://localhost/static/img/logo.png
# Esperado: HTTP/1.1 200 OK (Server: nginx)
```

**PROD porta 8000 direta (NÃO USAR):**
```powershell
curl -I http://localhost:8000/static/img/logo.png
# Resultado: HTTP/1.1 404 Not Found ← NORMAL! Django não serve estáticos com DEBUG=False
```

---

## 📊 Tabela Comparativa

| Aspecto | DEV (8001) | PROD (80) | PROD (8000) ❌ |
|---------|-----------|-----------|----------------|
| **URL** | `localhost:8001` | `localhost` | `localhost:8000` |
| **Servidor Web** | Django runserver | NGINX → Gunicorn | Gunicorn direto |
| **DEBUG** | `True` | `False` | `False` |
| **Serve estáticos?** | ✅ Sim | ✅ Sim (NGINX) | ❌ Não |
| **Logo funciona?** | ✅ Sim | ✅ Sim | ❌ Não (404) |
| **Usar em produção?** | Não | **SIM** | **NÃO** |

---

## 🛠️ Arquitetura de Produção

```
┌─────────────────────────────────────────────────────────┐
│  Navegador: http://localhost/                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
            ┌────────────────┐
            │  NGINX (80)    │ ← ACESSO CORRETO ✅
            └────────┬───────┘
                     │
         ┌───────────┴──────────┐
         │                      │
         ↓                      ↓
┌────────────────┐    ┌─────────────────────┐
│  Arquivos      │    │  Django/Gunicorn    │
│  Estáticos     │    │  (8000 interno)     │
│  /var/www/     │    │                     │
│  static/       │    │  Views, DB, Logic   │
└────────────────┘    └─────────────────────┘
```

---

## 🔧 Collectstatic em Produção

**Por que é necessário?**

Quando `DEBUG=False`, Django não serve arquivos estáticos. O comando `collectstatic` copia todos os arquivos estáticos para um único diretório (`/app/staticfiles/`) que o NGINX pode servir.

**Quando executar:**

1. **Automático:** O `entrypoint.sh` executa `collectstatic` na inicialização do container
2. **Manual (se necessário):**
   ```powershell
   docker compose -p omaum-prod exec -T omaum-web python manage.py collectstatic --noinput --clear
   ```

**Verificar se foi executado:**
```powershell
docker compose -p omaum-prod exec -T omaum-web ls -lh /app/staticfiles/img/logo.png
# Esperado: arquivo de 18K com timestamp recente
```

---

## 📝 Checklist de Deploy

Antes de considerar um deploy bem-sucedido:

- [ ] Container `omaum-web` está rodando
- [ ] Container `omaum-nginx` está rodando
- [ ] Collectstatic executado (verificar logs)
- [ ] Teste: `curl -I http://localhost/static/img/logo.png` retorna 200 OK
- [ ] Acesso via navegador em `http://localhost/` (sem porta!)
- [ ] Logo aparece na navbar e footer
- [ ] CSS está aplicado corretamente

---

## 🤖 Para Agentes de IA

> **REGRA CRÍTICA:** Ao mencionar URL de acesso em produção, SEMPRE use:
> - ✅ `http://localhost/` (NGINX na porta 80)
> - ❌ NUNCA `http://localhost:8000/` (Django direto)
>
> **Exceção:** Apenas para debugging de problemas do Django (não de arquivos estáticos).

---

## 📞 Suporte

Problemas com acesso? Verifique:

1. Containers rodando: `docker compose -p omaum-prod ps`
2. Logs do NGINX: `docker logs omaum-prod-omaum-nginx-1`
3. Logs do Django: `docker logs omaum-prod-omaum-web-1`
4. Arquivo existe: `docker exec omaum-prod-omaum-web-1 ls -lh /app/staticfiles/img/logo.png`

**Contato:** suporte@omaum.edu.br
