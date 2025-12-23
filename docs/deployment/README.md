# 🚀 Documentação de Deploy - OMAUM

Este diretório contém documentação relacionada ao deploy e configuração de ambientes do projeto OMAUM.

## 📑 Índice de Documentos

### [PORTAS_ACESSO.md](PORTAS_ACESSO.md) 🌐
**Portas de Acesso Corretas - Desenvolvimento vs Produção**

Documento essencial que define:
- ✅ Como acessar corretamente DEV (`localhost:8001`) e PROD (`localhost`)
- ❌ Por que NÃO acessar `localhost:8000` em produção
- 🔍 Como Django com `DEBUG=False` funciona com arquivos estáticos
- 📊 Tabela comparativa de ambientes
- 🛠️ Arquitetura NGINX + Gunicorn
- 📝 Checklist de deploy

**Quando consultar:**
- Antes de fazer deploy em produção
- Quando logo/CSS/JS não carregam em produção
- Para entender diferenças entre ambientes
- Ao configurar novos ambientes

---

## 🎯 Quick Reference

### Desenvolvimento
```powershell
cd E:\projetos\omaum\docker
docker compose -p omaum-dev -f docker-compose.yml -f docker-compose.dev.override.yml up -d
```
**Acesso:** http://localhost:8001/

### Produção
```powershell
cd E:\projetos\omaum\docker
docker compose --profile production -p omaum-prod --env-file ..\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml up -d
```
**Acesso:** http://localhost/ (porta 80 via NGINX)

---

## 📞 Suporte

Problemas com deploy? Consulte:
1. [PORTAS_ACESSO.md](PORTAS_ACESSO.md) - Problemas com acesso/estáticos
2. Logs: `docker logs omaum-prod-omaum-web-1`
3. Status: `docker compose -p omaum-prod ps`

**Contato:** suporte@omaum.edu.br
