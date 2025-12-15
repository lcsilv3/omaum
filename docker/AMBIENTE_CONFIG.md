# Configuração de Ambientes Docker - OMAUM

## ⚠️ IMPORTANTE: Prevenção de Conflitos

Este documento descreve como os ambientes são configurados para **evitar conflitos** entre desenvolvimento e produção.

## 🎯 Problema Identificado e Resolvido

**Problema:** Ambos os ambientes mostravam o badge "Ambiente de Produção" porque:
1. O arquivo `docker-compose.override.yml` era lido automaticamente pelo Docker Compose
2. Esse arquivo forçava `DJANGO_SETTINGS_MODULE=omaum.settings.production` para todos os ambientes
3. Ambos os containers tentavam usar a porta 8000, causando conflitos

**Solução Implementada:**
1. ✅ Renomeado `docker-compose.override.yml` → `docker-compose.override.yml.example`
2. ✅ Ambiente dev usa porta **8001** (externo)
3. ✅ Ambiente prod usa porta **80** (via Nginx) e **8000** (direto)
4. ✅ Cada ambiente tem seu próprio arquivo de override explícito

## 📋 Estrutura de Arquivos

```
docker/
├── docker-compose.yml                    # Base (desenvolvimento)
├── docker-compose.prod.override.yml      # Override de PRODUÇÃO (explícito)
├── docker-compose.override.yml.example   # Exemplo (NÃO É LIDO automaticamente)
├── .env.dev                              # Variáveis de desenvolvimento
└── .env.production                       # Variáveis de produção
```

## 🚀 Comandos para Cada Ambiente

### Desenvolvimento (Porta 8001)

```powershell
# Subir ambiente de desenvolvimento
cd E:\projetos\omaum\docker
docker compose -p omaum-dev --env-file E:\projetos\omaum\.env.dev -f docker-compose.yml up -d

# Acessar: http://localhost:8001
# Badge: 🟡 Amarelo "Ambiente de Desenvolvimento"
# Settings: omaum.settings.development
```

### Produção (Porta 80 via Nginx, 8000 direto)

```powershell
# Subir ambiente de produção
cd E:\projetos\omaum\docker
docker compose --profile production -p omaum-prod --env-file E:\projetos\omaum\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml up -d

# Acessar: http://localhost (Nginx)
# Acessar: http://localhost:8000 (direto, para debug)
# Badge: 🔴 Vermelho "Ambiente de Produção"
# Settings: omaum.settings.production
```

## 🔍 Validação de Ambiente

Execute o script de validação para confirmar que os badges estão corretos:

```powershell
cd E:\projetos\omaum
python test_login_ambientes.py
```

Ou use o script de verificação rápida:

```powershell
python scripts/verificar_ambiente.py
```

## 📊 Tabela de Configuração

| Ambiente        | Porta Externa | Badge               | DJANGO_SETTINGS_MODULE     | Arquivo Env          |
|----------------|---------------|---------------------|----------------------------|---------------------|
| Desenvolvimento | **8001**      | 🟡 bg-warning       | omaum.settings.development | .env.dev            |
| Produção       | **80, 8000**  | 🔴 bg-danger        | omaum.settings.production  | .env.production     |

## ⚠️ Regras de Ouro

### ❌ NÃO FAÇA ISSO:

1. **NÃO** crie ou renomeie `docker-compose.override.yml.example` de volta para `docker-compose.override.yml`
   - Docker Compose lê esse arquivo automaticamente e pode sobrescrever configurações

2. **NÃO** use a mesma porta para dev e prod
   - Dev deve sempre usar porta **8001**
   - Prod deve usar porta **80** (Nginx) ou **8000** (direto)

3. **NÃO** edite as variáveis `ENVIRONMENT_*` no código
   - Sempre use os arquivos `.env.dev` ou `.env.production`

### ✅ SEMPRE FAÇA ISSO:

1. **SEMPRE** especifique explicitamente o arquivo de override para produção:
   ```
   -f docker-compose.yml -f docker-compose.prod.override.yml
   ```

2. **SEMPRE** use o arquivo `.env` correto para cada ambiente:
   ```
   --env-file E:\projetos\omaum\.env.dev         # Dev
   --env-file E:\projetos\omaum\.env.production  # Prod
   ```

3. **SEMPRE** use projetos nomeados diferentes:
   ```
   -p omaum-dev   # Desenvolvimento
   -p omaum-prod  # Produção
   ```

4. **SEMPRE** valide o badge após subir um ambiente:
   ```powershell
   # Dev
   curl -s http://localhost:8001/ | Select-String "Ambiente de Desenvolvimento"
   
   # Prod
   curl -s http://localhost/ | Select-String "Ambiente de Produção"
   ```

## 🧪 Testes Automatizados

O arquivo `test_login_ambientes.py` executa testes Selenium que:
1. ✅ Fazem login em ambos os ambientes
2. ✅ Capturam screenshots dos badges
3. ✅ Validam que os badges são diferentes
4. ✅ Confirmam que as portas estão corretas

Execute regularmente após mudanças de configuração:
```powershell
python test_login_ambientes.py
```

## 🔧 Troubleshooting

### Problema: Badge errado aparece

**Diagnóstico:**
```powershell
# Verificar qual settings está sendo usado
docker exec <container> python -c "import os; print(os.environ['DJANGO_SETTINGS_MODULE'])"

# Verificar variáveis de ambiente
docker exec <container> env | grep ENVIRONMENT
```

**Solução:**
1. Verificar se `docker-compose.override.yml` existe (deve ser `.example`)
2. Confirmar que o comando correto está sendo usado
3. Recriar containers: `docker compose ... down && docker compose ... up -d`

### Problema: Porta já em uso

**Diagnóstico:**
```powershell
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

**Solução:**
1. Dev deve usar porta 8001
2. Prod pode usar portas 80 e 8000
3. Parar containers conflitantes antes de subir novos

## 📝 Checklist de Deploy

Antes de cada deploy, confirme:

- [ ] Arquivo `docker-compose.override.yml` **NÃO** existe (deve ser `.example`)
- [ ] Dev configurado para porta 8001 em `docker-compose.yml`
- [ ] Prod configurado para portas 80/8000 em `docker-compose.prod.override.yml`
- [ ] Variáveis `ENVIRONMENT_*` corretas em `.env.dev` e `.env.production`
- [ ] Teste Selenium executado com sucesso
- [ ] Badges validados visualmente ou via curl

## 🔐 Credenciais de Teste

**Desenvolvimento (porta 8001):**
- Usuário: `desenv`
- Senha: `desenv123`

**Produção (porta 80):**
- Usuário: `admin`
- Senha: `admin123`

## 📚 Referências

- [docker-compose.yml](docker-compose.yml) - Configuração base (dev)
- [docker-compose.prod.override.yml](docker-compose.prod.override.yml) - Override de produção
- [.env.dev](../.env.dev) - Variáveis de desenvolvimento
- [.env.production](../.env.production) - Variáveis de produção
- [test_login_ambientes.py](../test_login_ambientes.py) - Testes Selenium

---

**Última atualização:** 15 de dezembro de 2025  
**Criado por:** Correção do bug de badges idênticos nos ambientes
