# ✅ Adaptação para Self-Hosted Runner Completa!

## 📋 Resumo do que foi alterado

### 1. **Workflow de Deploy**
**Arquivo:** [.github/workflows/deploy-prod-ssh.yml](.github/workflows/deploy-prod-ssh.yml)

**Antes:** SSH remoto via `appleboy/ssh-action` (ultrapassado, requer secrets SSH)  
**Depois:** **Self-hosted runner** local (executa direto na máquina sem SSH)

#### Mudanças específicas:
```yaml
# ANTES
runs-on: ubuntu-latest
uses: appleboy/ssh-action@master
with:
  host: ${{ secrets.PROD_HOST }}
  ...

# DEPOIS
runs-on: [self-hosted]
shell: pwsh
run: |
  Invoke-Expression "pwsh -NoLogo -NoProfile -File scripts/deploy_prod.ps1"
```

✅ **Benefício:** Deploy local, sem SSH overhead, sem secrets complexas

---

### 2. **Documentação Atualizada**
**Arquivo:** [docs/ci-cd-producao.md](docs/ci-cd-producao.md)

- ✅ Removed SSH configuration sections
- ✅ Added self-hosted runner registration steps
- ✅ Removed PROD_HOST, PROD_USER, PROD_SSH_KEY secrets
- ✅ Added troubleshooting para self-hosted runner

---

### 3. **Novo Guia Rápido**
**Arquivo:** [docs/self-hosted-runner-quickstart.md](docs/self-hosted-runner-quickstart.md)

**Conteúdo:**
- Setup de 2 minutos (Windows + Linux)
- Verificação passo-a-passo
- Troubleshooting rápido
- Maintenance guide

---

### 4. **Status Document**
**Arquivo:** [SELF_HOSTED_RUNNER_STATUS.md](SELF_HOSTED_RUNNER_STATUS.md)

**Conteúdo:**
- ✅ O que está pronto (pipelines completos)
- 📋 Próximos passos (você precisa fazer)
- 🎯 Checklist para próxima deploy
- 💡 Dicas importantes

---

## 🚀 Fluxo Final (sem SSH)

```
┌─────────────────┐
│  PUSH EM MAIN   │
└────────┬────────┘
         │
         ├─→ [1] BUILD-PUSH (ubuntu-latest)
         │        • Build Docker image
         │        • Push GHCR ✅
         │
         └─→ [Espera trigger manual]
         
┌──────────────────────────┐
│ DISPATCH DEPLOY (GitHub) │
└────────┬─────────────────┘
         │
         └─→ [2] DEPLOY (self-hosted) ✅ NOVO
                  • Executa localmente
                  • Sem SSH, sem secrets
                  • docker compose up
                  • migrate + collectstatic
                  • Verify + logs
                  • Slack notification
```

---

## 🎯 Próximo Passo (Action Required)

### Registre o Self-Hosted Runner

**Vá para:** GitHub repo → Settings → Actions → Runners → "New self-hosted runner"

**Windows PowerShell (Admin):**
```powershell
mkdir C:\actions-runner
cd C:\actions-runner

# Copie os 3 comandos EXATOS do GitHub UI
# (que está na tela "New self-hosted runner")

# Instale como serviço (auto-inicia ao boot)
.\nssm install GitHubRunner "C:\actions-runner\run.cmd"
.\nssm start GitHubRunner
```

**Linux:**
```bash
mkdir -p ~/actions-runner && cd ~/actions-runner

# Copie os 4 comandos EXATOS do GitHub UI

# Instale como serviço systemd
sudo ./svc.sh install
sudo ./svc.sh start
```

**Verificação:**
```
GitHub repo → Settings → Actions → Runners
[Seu runner] Status: "Idle" ✅ (verde)
```

---

## 📊 Comparação: SSH vs Self-Hosted

| Aspecto | SSH (Antes) | Self-Hosted (Agora) |
|---------|-----------|------------------|
| **Execução** | Remote via SSH | Local direto |
| **Secrets** | PROD_HOST, PROD_USER, PROD_SSH_KEY | Nenhum (local) |
| **Latência** | Rede remota | Sem latência |
| **Complejidade** | Alta (chaves SSH) | Baixa (local) |
| **Máquina** | Qualquer servidor | Same machine |
| **Configuração** | Moderada | 2 minutos |

✅ **Você escolheu a melhor opção para seu caso!**

---

## 🧪 Como testar

1. **Self-hosted runner registrado?**
   ```
   GitHub repo → Settings → Actions → Runners → Status "Idle"
   ```

2. **Faça um commit/push em main** (ou dispare build manualmente)
   ```
   GitHub Actions → build-push-prod.yml → check sucesso
   ```

3. **Dispare deploy manualmente**
   ```
   GitHub Actions → Deploy em Produção (Self-hosted)
              ↓
   Run workflow → deixe defaults
              ↓
   Veja logs em tempo real ✅
   ```

4. **Verifique produção**
   ```bash
   # Na máquina de produção
   docker compose --profile production -p omaum-prod ps
   docker compose --profile production -p omaum-prod logs omaum-web
   ```

---

## 📝 Arquivos tocados nesta sessão

✅ `.github/workflows/deploy-prod-ssh.yml`
- Convertido de SSH para self-hosted runner
- Simplificado (sem SSH config)
- Mais legível (PowerShell direto)

✅ `docs/ci-cd-producao.md`
- Removido seções SSH
- Adicionado guia self-hosted runner
- Atualizado troubleshooting

✅ `docs/self-hosted-runner-quickstart.md` (NEW)
- Guia ultra-rápido
- 2 minutos setup
- Copy-paste friendly

✅ `SELF_HOSTED_RUNNER_STATUS.md` (NEW)
- Resumo executivo
- Checklist próxima deploy
- Dicas importantes

---

## 💡 Pontos-chave para lembrar

1. **Mesma máquina, endereço diferente** ✅
   - Dev: localhost:8001 ou IP-local:8001
   - Prod: IP-prod:8000 (mesma máquina física)

2. **Runner local = sem SSH**
   - Elimina complexidade de chaves
   - Mais rápido (sem latência de rede)
   - Deploy pode ser testado localmente

3. **Secrets Slack (opcional)**
   - Se quiser notificações, adicione `SLACK_WEBHOOK_URL`
   - Deploy continua funcionando sem (skip notification)

4. **Fluxo sempre manual**
   - Build: automático (push em main)
   - Deploy: manual (dispara workflow)
   - ✅ Mais seguro (você controla)

---

## ✨ Próximas ações sugeridas

1. **Registre runner** (você precisa fazer)
   - Windows ou Linux conforme sua setup
   - 2-3 minutos de trabalho

2. **Teste deploy** (vire trigger manual)
   - Actions → Deploy em Produção (Self-hosted)
   - Veja tudo rodar localmente

3. **Commit mudanças** (após validar)
   - Todos os arquivos .md + .yml estão prontos
   - Use mensagem: "ci(deploy): use self-hosted runner for local production"

4. **Documente no projeto** (informar time)
   - Link: [SELF_HOSTED_RUNNER_STATUS.md](SELF_HOSTED_RUNNER_STATUS.md)
   - Ou: [docs/self-hosted-runner-quickstart.md](docs/self-hosted-runner-quickstart.md)

---

**Aviso:** Quando estiver pronto com o runner registrado, avise! Fecho a sessão no próximo passo com sucesso confirmado. 🎉
