# CI/CD para Produção – Setup e Uso

Este guia cobre o fluxo completo de CI/CD com GitHub Actions para build, push e deploy em produção.

## Workflows

### 1. build-push-prod.yml
**Dispara:** Push em `main` (mudanças em arquivos Python, Docker, requirements) ou manualmente.

O que faz:
- Build da imagem Docker usando buildx + cache GHA.
- Push para GitHub Container Registry (GHCR).
- Notificação no Slack (opcional).

Variáveis de saída:
- URL da imagem: `ghcr.io/<repo>/omaum:latest` e tags por branch/sha.

### 2. deploy-prod-ssh.yml
**Dispara:** Manualmente via GitHub Actions (recomendado) com opções interativas.

O que faz:
- **Self-hosted runner**: Executa localmente na máquina de produção (mesmo servidor da dev com IP diferente).
- Executa `scripts/deploy_prod.ps1` com parâmetros (pull, recreate, skip migrate/collectstatic).
- Valida status dos containers e mostra logs.
- Notificação no Slack com sucesso/falha.

Parâmetros interativos:
- `skip_migrate`: Pular migrations (padrão: false)
- `skip_collectstatic`: Pular collectstatic (padrão: false)
- `pull`: Executar docker pull antes de up (padrão: true)
- `recreate`: Forçar recriação de containers (padrão: false)

## Configuração necessária

### Secrets do repositório (Settings → Secrets and variables → Actions)

Obrigatórios para build:
- `GITHUB_TOKEN` (automático no GitHub Actions)

Opcional:
- `SLACK_WEBHOOK_URL`: Webhook do Slack para notificações

**NOTA:** Deploy com self-hosted runner NÃO precisa de secrets SSH, pois executa localmente.

### Setup no servidor de produção

#### 1. Clone/pull do repositório:
```bash
mkdir -p /app/omaum
cd /app/omaum
git clone https://github.com/<owner>/<repo>.git .
```

#### 2. Prepare variáveis de produção:
```bash
cp docker/.env.production.example docker/.env.production
# Edite docker/.env.production com dados reais
```

#### 3. Ensure Docker + Docker Compose:
```bash
docker --version && docker compose version
```

#### 4. **NOVO: Registre o GitHub self-hosted runner**

Na máquina de produção (Windows PowerShell ou Linux bash):

**Windows (PowerShell):**
```powershell
# 1. Vá para GitHub repo → Settings → Actions → Runners → New self-hosted runner
# 2. Escolha Windows x64
# 3. Copie e execute os comandos no PowerShell:

mkdir C:\actions-runner
cd C:\actions-runner

# Download (ajuste versão conforme GitHub indica)
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.320.0/actions-runner-win-x64-2.320.0.zip -OutFile runner.zip
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD\runner.zip", "$PWD")

# Configure
.\config.cmd --url https://github.com/<owner>/<repo> --token <GITHUB_TOKEN_RUNNER>

# Rode como serviço Windows (recomendado)
.\nssm install GitHubRunner "C:\actions-runner\run.cmd"
.\nssm start GitHubRunner
```

**Linux (bash):**
```bash
# 1. Vá para GitHub repo → Settings → Actions → Runners → New self-hosted runner
# 2. Escolha Linux x64
# 3. Copie e execute os comandos:

mkdir -p ~/actions-runner
cd ~/actions-runner

# Download (ajuste versão)
curl -o actions-runner-linux-x64-2.320.0.tar.gz \
  -L https://github.com/actions/runner/releases/download/v2.320.0/actions-runner-linux-x64-2.320.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.320.0.tar.gz

# Configure
./config.sh --url https://github.com/<owner>/<repo> --token <GITHUB_TOKEN_RUNNER>

# Rode em background (ou use systemd)
nohup ./run.sh &
```

**Verificação:**
- GitHub repo → Settings → Actions → Runners → Deve aparecer como "Idle" (online)

#### 5. Configure PowerShell (se em Linux):
```bash
sudo apt-get install -y powershell
# ou use seu package manager
```

## Como usar

### Opção 1: Deploy automático (após build bem-sucedido)
1. Faça push em `main`.
2. GitHub Actions roda build-push-prod.yml automaticamente.
3. Quando o build termina, dispare deploy-prod-ssh.yml manualmente:
   - Actions → **Deploy em Produção (Self-hosted)** → Run workflow
   - Escolha opções (pull, skip_migrate, etc.)
   - Workflow executa **localmente no runner** registrado

### Opção 2: Deploy manual (sem build)
- Actions → **Deploy em Produção (Self-hosted)** → Run workflow
- Pulará o build e rodará apenas o script de deploy no runner local.

### Monitoramento
- Veja logs do workflow em Actions → [workflow name] → [run]
- Slack notificará sucesso/falha (se configurado)
- Acesse o servidor para validar: `docker compose ps` e `docker compose logs`

## Troubleshooting

### Runner não aparece em "Idle"
- Verifique se o runner está rodando (Windows: Services → GitHubRunner, Linux: `ps aux | grep run.sh`)
- Cheque permissões de Docker (user com `sudo` ou adicionado ao grupo `docker`)
- Veja logs do runner em `./_diag/` no diretório do runner

### Deploy falha com "command not found"
- Verifique se PowerShell está instalado: `pwsh -v`
- Em Linux, instale: `sudo apt-get install -y powershell`
- Ou use `shell: bash` no workflow se preferir

### Docker permission denied
```bash
# Adicione seu user ao grupo docker
sudo usermod -aG docker $USER
# Aplique novo grupo sem reiniciar (Linux)
newgrp docker
```

### Variáveis de ambiente não carregadas
- Verifique `.env.production` existe e está correto
- Runner precisa estar na raiz do repositório ou com caminho absoluto
- Use `docker compose -f docker/docker-compose.yml --profile production` se usando override

## Troubleshooting

### "SSH key is not in a valid format"
- Certifique-se que a chave privada está em formato PEM (começa com `-----BEGIN RSA PRIVATE KEY-----`)
- Se estiver em OpenSSH format, converta:
  ```bash
  ssh-keygen -p -f id_rsa -m pem -P "" -N ""
  ```
- Cole o conteúdo completo da chave (incluindo linhas de início/fim) como secret

### "Permission denied (publickey)"
- Verifique se a chave pública está em `~/.ssh/authorized_keys` do usuário SSH
- Confirme que o usuário tem permissão para `/app/omaum` e `docker`

### "docker: command not found"
- Instale Docker no servidor
- Ou ajuste o script para usar `$PATH` completo

### Logs não aparecem
- Certifique-se que `PROD_APP_PATH` está correto
- SSH manualmente e rode `cd <path> && docker compose --profile production -p omaum-prod logs`

## Próximos passos

1. Teste a chave SSH e acesso:
   ```bash
   ssh -i <private_key> <PROD_USER>@<PROD_HOST> "docker --version"
   ```

2. Configure Slack webhook (opcional):
   - Crie um app em https://api.slack.com/apps
   - Gere incoming webhook URL
   - Salve como secret `SLACK_WEBHOOK_URL`

3. Execute um deploy teste manualmente:
   - Actions → Deploy em Produção (SSH) → Run workflow
   - Monitore logs
   - Valide no servidor: `docker compose ps`
