# 🏗️ ARQUITETURA DE AMBIENTES - OMAUM (DEFINITIVO)

**Data:** 29/11/2025  
**Status:** ✅ Documentação Oficial

---

## 📋 AMBIENTES DO PROJETO

O projeto OMAUM possui **APENAS 2 AMBIENTES**, ambos em Docker:

### 1. 🔴 **PRODUÇÃO (Docker)**
- **Finalidade:** Sistema em uso pelos usuários finais
- **Arquivo:** `docker/docker-compose.prod.yml`
- **Acesso:** http://192.168.15.4 ou http://omaum.local
- **Python:** 3.11.14 (dentro do container)
- **Características:** Gunicorn + Nginx + Celery + PostgreSQL + Redis
- **Debug:** ❌ Desabilitado
- **Atualizar:** `.\atualizar_docker.bat`

### 2. 🔵 **DESENVOLVIMENTO (Docker)**
- **Finalidade:** Desenvolvimento e testes
- **Arquivo:** `docker/docker-compose.yml`
- **Acesso:** http://localhost:8000
- **Python:** 3.11.14 (dentro do container)
- **Características:** Django runserver + PostgreSQL + Redis
- **Debug:** ✅ Ativo
- **Hot Reload:** ✅ Código montado como volume
- **Iniciar:** `.\iniciar_dev_docker.bat`

---

## ❌ AMBIENTES QUE NÃO EXISTEM MAIS

### ~~💻 Ambiente Local Windows~~ (REMOVIDO)

**Foi eliminado porque:**
- ❌ Estava quebrado (venv criado por outro usuário)
- ❌ Python não instalado no sistema
- ❌ Causava confusão sobre qual ambiente usar
- ❌ Não é necessário - Docker Dev faz tudo
- ❌ Dificultava sincronização entre ambientes

**Decisão:** Usar APENAS Docker para tudo.

---

## 🎯 WORKFLOW OFICIAL

### Desenvolvimento Diário:

```powershell
# 1. Iniciar ambiente de desenvolvimento
.\iniciar_dev_docker.bat

# 2. Desenvolver normalmente
# Edite arquivos no Windows com qualquer editor
# Mudanças refletem automaticamente no container

# 3. Testar
# http://localhost:8000

# 4. Commit
git add .
git commit -m "feat: nova funcionalidade"
git push

# 5. Parar (fim do dia)
cd docker
docker-compose down
```

### Deploy para Produção:

```powershell
# Atualizar código e reiniciar produção
.\atualizar_docker.bat
```

---

## 🔧 COMANDOS ESSENCIAIS

### Desenvolvimento:
```powershell
# Iniciar
.\iniciar_dev_docker.bat

# Ver logs
cd docker
docker-compose logs -f

# Executar comandos Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py test

# Parar
docker-compose down
```

### Produção:
```powershell
# Atualizar código
.\atualizar_docker.bat

# Ver logs
docker logs omaum-web-prod

# Executar comandos Django
docker exec omaum-web-prod python manage.py migrate
docker exec omaum-web-prod python manage.py shell

# Reiniciar
docker restart omaum-web-prod
```

---

## ✅ VANTAGENS DESTA ARQUITETURA

1. **Simplicidade:** Apenas 2 ambientes para gerenciar
2. **Consistência:** Mesma versão Python (3.11) em DEV e PROD
3. **Isolamento:** Não "suja" o sistema Windows
4. **Reprodutibilidade:** Funciona igual em qualquer máquina com Docker
5. **Facilidade:** Não precisa instalar Python, PostgreSQL, Redis no Windows
6. **Sincronização:** Impossível ter "código diferente" entre ambientes

---

## 🚫 O QUE NÃO FAZER

❌ **NÃO** criar ambiente virtual local (`venv/`, `.venv/`)  
❌ **NÃO** instalar Python no Windows para o projeto  
❌ **NÃO** executar `python manage.py runserver` fora do Docker  
❌ **NÃO** editar código dentro do container (edite no Windows)  
❌ **NÃO** confundir os dois ambientes Docker  

---

## 📊 COMPARAÇÃO DOS 2 AMBIENTES

| Característica | 🔵 Desenvolvimento | 🔴 Produção |
|----------------|-------------------|-------------|
| **Arquivo** | `docker-compose.yml` | `docker-compose.prod.yml` |
| **URL** | localhost:8000 | 192.168.15.4 |
| **Python** | 3.11.14 | 3.11.14 |
| **Servidor** | runserver | Gunicorn + Nginx |
| **Debug** | ✅ Ativo | ❌ Desabilitado |
| **Hot Reload** | ✅ Sim | ❌ Não |
| **Banco** | omaum_dev | omaum_prod |
| **Celery** | ❌ Não | ✅ Sim |
| **SSL** | ❌ Não | ✅ Configurável |
| **Código** | Volume montado | Copiado na build |
| **Atualizar** | Automático | Rebuild necessário |

---

## 🎓 PERGUNTAS FREQUENTES

### P: Por que não usar ambiente local?
**R:** Não é necessário. Docker Dev oferece tudo (hot reload, debug, etc.) sem precisar instalar nada no Windows.

### P: Como edito código?
**R:** Normalmente no Windows! O Docker monta a pasta do projeto como volume. Salva o arquivo → Mudança reflete automaticamente.

### P: Preciso reiniciar o Docker quando mudo código?
**R:** NÃO no ambiente de desenvolvimento (hot reload). SIM na produção (precisa rebuild).

### P: Como uso minha IDE favorita?
**R:** Normalmente! VSCode, PyCharm, Sublime - todos funcionam. Você edita no Windows, Docker executa.

### P: E se eu quiser PyCharm com autocomplete?
**R:** PyCharm pode usar o interpretador Python dentro do container Docker. Veja documentação do PyCharm sobre "Docker Python Interpreter".

### P: Posso ter os dois ambientes rodando ao mesmo tempo?
**R:** Tecnicamente sim, mas não é recomendado (conflito de portas). Use um de cada vez.

---

## 📝 CHECKLIST DE DESENVOLVIMENTO

Sempre que for desenvolver:

- [ ] Docker Desktop está rodando?
- [ ] Executou `.\iniciar_dev_docker.bat`?
- [ ] Container `omaum-web` está rodando? (`docker ps`)
- [ ] Site acessível em http://localhost:8000?
- [ ] Edita código no Windows (não dentro do container)
- [ ] Ao terminar, executa `docker-compose down`?

---

## 🚀 ARQUIVOS IMPORTANTES

### Scripts de automação:
- ✅ `iniciar_dev_docker.bat` - Inicia desenvolvimento
- ✅ `atualizar_docker.bat` - Atualiza produção

### Documentação:
- ✅ `ARQUITETURA_AMBIENTES.md` - Este arquivo
- ✅ `DOCKER_AMBIENTES.md` - Guia detalhado Docker

### Configuração Docker:
- ✅ `docker/Dockerfile` - Imagem Python
- ✅ `docker/docker-compose.yml` - Desenvolvimento
- ✅ `docker/docker-compose.prod.yml` - Produção
- ✅ `docker/.env.production` - Variáveis de produção

---

## ⚠️ IMPORTANTE

**Esta é a arquitetura OFICIAL do projeto.**

Qualquer tentativa de criar ambiente local (venv, .venv) deve ser desconsiderada.

**Use APENAS os 2 ambientes Docker.**

---

## 📞 SUPORTE

Se tiver dúvidas sobre os ambientes:
1. Consulte este documento
2. Consulte `DOCKER_AMBIENTES.md`
3. Entre em contato: suporte@omaum.edu.br

---

**Última atualização:** 29/11/2025 - 16:00  
**Mantido por:** Equipe OMAUM  
**Status:** ✅ Documento oficial e definitivo
