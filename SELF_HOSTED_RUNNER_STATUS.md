# 🚀 CI/CD Produção – Status Atual

## ✅ O que está pronto

### 1. **Build Pipeline** (build-push-prod.yml)
```
main push → Build Docker image → Push para GHCR
```
- ✅ Dispara automático em push para main
- ✅ Cria tags: latest, branch-name, sha, semver
- ✅ Notificação Slack (se configurado)
- **Status**: Testado e funcionando

### 2. **Deploy Pipeline** (deploy-prod-ssh.yml)
```
Dispara manual → Self-hosted runner → Deploy local
```
- ✅ Convertido de SSH para self-hosted runner
- ✅ Executa localmente (sem SSH overhead)
- ✅ Parâmetros: pull, recreate, skip_migrate, skip_collectstatic
- ✅ Valida status e mostra logs
- **Status**: Pronto para testar após runner registrado

### 3. **Deploy Scripts**
- ✅ `scripts/deploy_prod.ps1` – Orquestração completa (docker up, migrate, collectstatic)
- ✅ `scripts/restart_prod.ps1` – Reinício rápido
- ✅ `scripts/watch_dev_ops.ps1` – Auto-restart em mudanças .py e static files
- **Status**: Prontos para uso

### 4. **Documentação**
- ✅ `docs/ci-cd-producao.md` – Setup completo com self-hosted runner
- ✅ `docs/self-hosted-runner-quickstart.md` – Guia de 2 minutos
- ✅ `docs/deploy_producao_quickstart.md` – Referência de flags
- **Status**: Documentação completa

---

## 📋 Próximos passos (user action required)

### 1. **Registrar Self-Hosted Runner** (👈 VOCÊ PRECISA FAZER)

**Na máquina de produção** (mesmo IP/máquina da dev):

#### Windows PowerShell (Admin):
```powershell
mkdir C:\actions-runner
cd C:\actions-runner

# Copie e execute os comandos EXATOS do GitHub UI:
# Settings → Actions → Runners → New self-hosted runner → Windows x64
```

#### Linux:
```bash
mkdir -p ~/actions-runner && cd ~/actions-runner

# Copie e execute os comandos EXATOS do GitHub UI:
# Settings → Actions → Runners → New self-hosted runner → Linux x64
```

**Verificação:**
- GitHub repo → Settings → Actions → Runners
- Deve aparecer "Idle" (verde)

### 2. **Testar Deploy Manual**

Quando runner estiver pronto:

```
GitHub Actions → Deploy em Produção (Self-hosted)
  ↓
Run workflow → deixe defaults
  ↓
Veja logs em tempo real
  ↓
Verifique containers: docker compose ps
```

### 3. **Opcional: Slack Webhook**

Se quiser notificações no Slack:
1. Crie webhook: https://api.slack.com/messaging/webhooks
2. Settings → Secrets and variables → Actions
3. Adicione `SLACK_WEBHOOK_URL`

---

## 🔍 Estrutura do fluxo final

```
┌──────────────────────────────────────────────────────────────┐
│                    PUSH em MAIN                              │
└────────────┬─────────────────────────────────────────────────┘
             │
             ├──→ build-push-prod.yml (ubuntu-latest)
             │    ✅ Build image
             │    ✅ Push GHCR
             │    ✅ Slack notification
             │
             └──→ [Espera trigger manual]
                  
┌──────────────────────────────────────────────────────────────┐
│          DISPATCH DEPLOY (manual no GitHub UI)               │
└────────────┬─────────────────────────────────────────────────┘
             │
             └──→ deploy-prod-ssh.yml (self-hosted runner)
                  ✅ Docker pull
                  ✅ Docker up
                  ✅ Django migrate
                  ✅ collectstatic
                  ✅ Verify & logs
                  ✅ Slack notification
                  
                  [Produção atualizada ✅]
```

---

## 📝 Arquivos modificados nesta sessão

- ✅ `.github/workflows/deploy-prod-ssh.yml` – Convertido de SSH para self-hosted
- ✅ `docs/ci-cd-producao.md` – Atualizado para self-hosted runner
- ✅ `docs/self-hosted-runner-quickstart.md` – Criado (guia de 2 minutos)

---

## 🎯 Checklist para próxima deploy

- [ ] Self-hosted runner registrado
- [ ] Runner "Idle" (verde) no GitHub
- [ ] Slack webhook configurado (opcional)
- [ ] Testar deploy manual via GitHub Actions
- [ ] Verificar containers e logs
- [ ] Documention lida e entendida

---

## 💡 Dicas importantes

**Antes de fazer deploy:**
1. Ensure código está em `main` e buildado (build-push-prod.yml rodou)
2. Self-hosted runner está online (Settings → Runners → "Idle")
3. Variáveis `.env.production` estão corretas

**Durante deploy:**
1. Veja logs em Actions → [Deploy workflow] → [job]
2. Se falhar, logs mostram exatamente aonde
3. Pode ser retentado (clicar "Re-run")

**Após deploy:**
1. Acesse produção: http://[seu-ip-prod]:8000 (ou port configurado)
2. Verifique: docker compose ps, docker compose logs
3. Se tudo ok, commit de sucesso pode ir para changelog

---

## 📞 Suporte rápido

| Dúvida | Resposta |
|--------|----------|
| Aonde registro o runner? | GitHub repo → Settings → Actions → Runners → New self-hosted runner |
| Qual IP registrar? | O IP da máquina de produção (mesmo da dev, endereço diferente) |
| Precisa de SSH agora? | **Não!** Self-hosted runner executa localmente |
| Como testar? | Actions → Deploy em Produção (Self-hosted) → Run workflow |
| Pode falhar seguro? | Sim, logs mostram tudo. Pode corrigir e retentary |

---

**Próximo passo:** Registre o self-hosted runner e avise quando estiver pronto! 🚀
