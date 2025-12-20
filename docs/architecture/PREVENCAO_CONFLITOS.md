# 🛡️ Sistema de Prevenção de Conflitos de Ambiente

## 📊 Status Atual

✅ **Problema RESOLVIDO e PREVENIDO**

```
┌─────────────────────────────────────────────────────────────────┐
│                  ANTES (Problema)                                │
├─────────────────────────────────────────────────────────────────┤
│ Dev:  localhost:8000  🔴 "Ambiente de Produção"    ❌ ERRADO   │
│ Prod: localhost:80    🔴 "Ambiente de Produção"    ✅ correto  │
│                                                                  │
│ Causa: docker-compose.override.yml lido automaticamente         │
│        forçava settings.production em AMBOS os ambientes        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  DEPOIS (Solução)                                │
├─────────────────────────────────────────────────────────────────┤
│ Dev:  localhost:8001  🟡 "Ambiente de Desenvolvimento" ✅ correto│
│ Prod: localhost:80    🔴 "Ambiente de Produção"        ✅ correto│
│                                                                  │
│ Solução: override.yml → .example, portas separadas, validação   │
└─────────────────────────────────────────────────────────────────┘
```

## 🔐 Múltiplas Camadas de Proteção

### 1️⃣ Nível de Arquivos
```
✅ docker-compose.override.yml → .example (não é lido)
✅ docker/.gitignore → ignora se alguém criar por engano
✅ Portas separadas: Dev=8001, Prod=80/8000
```

### 2️⃣ Nível de Documentação
```
✅ AMBIENTE_CONFIG.md → Guia completo com warnings
✅ COMANDOS_RAPIDOS.md → Referência rápida validada
✅ Comentários inline nos docker-compose.yml
```

### 3️⃣ Nível de Validação Automatizada
```
✅ scripts/verificar_ambiente.py → Verifica tudo automaticamente
✅ test_login_ambientes.py → Testes Selenium com screenshots
```

## 🎯 Como Usar a Proteção

### Validação Rápida (30 segundos)
```powershell
# Executa TODAS as verificações
python scripts\verificar_ambiente.py
```

**O que é verificado:**
- ✅ Arquivo override não existe
- ✅ Containers usando portas corretas
- ✅ Badges diferentes em cada ambiente
- ✅ DJANGO_SETTINGS_MODULE correto

### Teste Completo com Screenshots (2 minutos)
```powershell
# Faz login, captura screenshots, valida badges
python test_login_ambientes.py
```

**Saída:**
- 4 screenshots com badges visuais diferentes
- Validação de login funcional
- Confirmação de ambientes isolados

## 🚨 Sinais de Alerta

Se você ver qualquer um destes, **PARE E CORRIJA**:

❌ `docker-compose.override.yml` existe (sem .example)
❌ Ambos ambientes na porta 8000
❌ Badge vermelho aparece no dev
❌ Badge amarelo aparece no prod
❌ `verificar_ambiente.py` falha

## 🔧 Auto-Correção

Se algo der errado:

```powershell
# 1. Renomear arquivo problemático
cd E:\projetos\omaum\docker
Rename-Item docker-compose.override.yml docker-compose.override.yml.example

# 2. Recriar containers
docker compose -p omaum-dev down
docker compose --profile production -p omaum-prod down

# 3. Subir corretamente
# [usar comandos em COMANDOS_RAPIDOS.md]

# 4. Validar
python scripts\verificar_ambiente.py
```

## 📋 Checklist de Deploy

Antes de cada mudança de ambiente, execute:

```powershell
# 1. Verificação automática
python scripts\verificar_ambiente.py

# 2. Se TUDO passar:
✅ Ambiente seguro para uso!

# 3. Se ALGO falhar:
❌ Ler output do script
❌ Seguir "Ações recomendadas"
❌ Consultar docker/AMBIENTE_CONFIG.md
```

## 📚 Documentação Relacionada

| Arquivo | Propósito | Quando Usar |
|---------|-----------|-------------|
| [AMBIENTE_CONFIG.md](docker/AMBIENTE_CONFIG.md) | Guia completo detalhado | Problemas complexos |
| [COMANDOS_RAPIDOS.md](docker/COMANDOS_RAPIDOS.md) | Referência rápida | Uso diário |
| [verificar_ambiente.py](scripts/verificar_ambiente.py) | Validação automática | Antes de cada deploy |
| [test_login_ambientes.py](test_login_ambientes.py) | Testes E2E com Selenium | Validação visual |

## 🎓 Lições Aprendidas

### Problema Raiz
1. Docker Compose lê `docker-compose.override.yml` **automaticamente**
2. Esse arquivo estava forçando `settings.production` em todos os ambientes
3. Ambos containers tentavam usar porta 8000

### Solução Multi-Camada
1. **Prevenção:** Renomear → `.example`, ignorar no git
2. **Isolamento:** Portas diferentes (8001 vs 80/8000)
3. **Validação:** Scripts automatizados
4. **Documentação:** Guias com exemplos e warnings

### Por Que Funciona
- ✅ Arquivo `.example` não é lido automaticamente
- ✅ Git ignora se alguém criar por engano
- ✅ Portas diferentes = sem conflito
- ✅ Validação detecta problemas antes do deploy
- ✅ Documentação clara previne erros humanos

## 🔄 Manutenção Contínua

### Mensalmente
```powershell
# Validar que proteções estão ativas
python scripts\verificar_ambiente.py
```

### Após Mudanças de Configuração
```powershell
# 1. Testar ambos ambientes
python test_login_ambientes.py

# 2. Validar configuração
python scripts\verificar_ambiente.py

# 3. Atualizar documentação se necessário
```

### Ao Adicionar Novos Ambientes (staging, etc.)
1. Criar arquivo override específico (não usar .override.yml genérico)
2. Usar porta única
3. Adicionar validação em `verificar_ambiente.py`
4. Documentar em AMBIENTE_CONFIG.md

---

## ✨ Resumo Executivo

**Problema:** Badges idênticos confundiam ambientes  
**Causa:** Configuração automática sobrescrevendo settings  
**Solução:** 4 camadas de proteção (arquivos, docs, validação, testes)  
**Resultado:** ✅ Impossível repetir o erro  

**Validação:** Execute `python scripts\verificar_ambiente.py` para confirmar!

---

**Commit:** `8376a03d` - fix: prevenir conflitos de badges entre ambientes  
**Data:** 15 de dezembro de 2025  
**Status:** ✅ Implementado, testado e documentado
