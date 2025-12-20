# Self-Hosted Runner Setup – Guia Rápido

## Por que self-hosted runner?

✅ **Mesma máquina física**: Dev e Prod no mesmo hardware, sem SSH complexo  
✅ **Sem secrets SSH**: Sem chaves privadas no GitHub  
✅ **Mais rápido**: Sem latência de rede ou overhead de SSH  
✅ **Simples**: Runner executa diretamente os scripts PowerShell/Bash  

---

## Setup de 2 minutos

### Windows PowerShell (Administrador)

```powershell
# 1. Crie pasta para o runner
mkdir C:\actions-runner
cd C:\actions-runner

# 2. Vá para: GitHub repo → Settings → Actions → Runners → New self-hosted runner
# Escolha Windows x64, copie os comandos EXATOS. Exemplo (substitua TOKEN):

# Download
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.320.0/actions-runner-win-x64-2.320.0.zip -OutFile runner.zip
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD\runner.zip", "$PWD")

# 3. Configure (copie comando exato do GitHub UI, inclui token)
.\config.cmd --url https://github.com/<owner>/<repo> --token <GITHUB_TOKEN_AQUI>

# 4. Rode como serviço Windows (auto-inicia ao boot)
.\nssm install GitHubRunner "C:\actions-runner\run.cmd"
.\nssm start GitHubRunner

# ✅ Pronto! Runner ativo no GitHub
```

### Linux/Ubuntu (Terminal)

```bash
# 1. Crie pasta para o runner
mkdir -p ~/actions-runner && cd ~/actions-runner

# 2. Vá para: GitHub repo → Settings → Actions → Runners → New self-hosted runner
# Escolha Linux x64, copie os comandos EXATOS. Exemplo:

# Download (ajuste versão)
curl -o actions-runner-linux-x64-2.320.0.tar.gz \
  -L https://github.com/actions/runner/releases/download/v2.320.0/actions-runner-linux-x64-2.320.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.320.0.tar.gz

# 3. Configure (copie comando exato do GitHub UI)
./config.sh --url https://github.com/<owner>/<repo> --token <GITHUB_TOKEN_AQUI>

# 4. Rode como serviço systemd (auto-inicia ao boot)
sudo ./svc.sh install
sudo ./svc.sh start

# ✅ Pronto! Runner ativo no GitHub
```

---

## Verificação

**No GitHub:**
1. Vá para repo → Settings → Actions → Runners
2. Procure por seu runner (ex: `ubuntu-latest` ou `windows-latest`)
3. Status deve ser **"Idle"** (verde) – pronto para receber jobs

**Na máquina:**
```bash
# Windows (Services.msc)
# Procure por "GitHubRunner" e verifique status "Running"

# Linux
sudo systemctl status actions.runner*
# Deve mostrar "active (running)"
```

---

## Deploy agora funciona assim:

```
1. Push em main → build-push-prod.yml roda (GHCR)
    ↓
2. Dispare Actions → Deploy em Produção (Self-hosted)
    ↓
3. GitHub envia job para seu self-hosted runner (local)
    ↓
4. Runner executa scripts/deploy_prod.ps1 (local, não SSH)
    ↓
5. Docker compose up, migrate, collectstatic (local)
    ↓
6. ✅ Produção atualizada (mesma máquina, IP diferente)
```

---

## Troubleshooting rápido

| Problema | Solução |
|----------|---------|
| Runner não aparece offline | Cheque pasta `./_work` tem permissão de escrita |
| "Permission denied" no Docker | `sudo usermod -aG docker $USER` |
| Serviço não inicia (Windows) | Verifique PowerShell path em nssm (use `Get-Command pwsh -All`) |
| Job fica em fila | Runner offline ou token expirado, reconfigure: `./config.cmd --url ...` |

---

## Maintenance

**Atualizar runner:**
```bash
# Desligue o serviço
sudo systemctl stop actions.runner*  # Linux
# ou Services.msc → Stop GitHubRunner  # Windows

# Baixe versão nova, replace files
rm -rf ~/actions-runner/*
# ... repeat download steps ...

# Reinicie serviço
```

**Desinstalação:**
```bash
# Linux
cd ~/actions-runner
./svc.sh uninstall
./config.sh remove --token <GITHUB_TOKEN>

# Windows
.\nssm remove GitHubRunner confirm
cd .. && rm -r actions-runner
```

---

## Próximos passos

✅ Runner registrado → Próximo deploy manual via GitHub Actions  
✅ Workflow `deploy-prod-ssh.yml` → Executa localmente  
✅ Sem SSH, sem secrets complexos → Simples e seguro  

**Vá para:** Actions → Deploy em Produção (Self-hosted) → Run workflow
