# Instruções para Agentes de IA – Projeto OMAUM

> **Idioma:** Sempre utilize português brasileiro.

## Visão Geral e Arquitetura
- Projeto Django modular para gestão acadêmica, com foco em controle de presenças, frequência, relatórios e integrações.
- Módulos principais: `presencas` (núcleo), `alunos`, `turmas`, `atividades`, `cursos`, `core`, `relatorios_presenca`.
- Cada módulo possui models, views (preferencialmente function-based), services, templates e admin próprios.
- O core deve conter apenas utilitários e componentes essenciais, sem dependências circulares.
- Comunicação entre módulos: use `importlib.import_module()` para evitar importações circulares.

## Convenções e Padrões Específicos
- **Nomenclatura de URLs:**
  - Listar: `listar_[recurso]s`
  - Criar: `criar_[recurso]`
  - Editar: `editar_[recurso]`
  - Excluir: `excluir_[recurso]`
  - Detalhes: `detalhar_[recurso]`
  - Confirmar: `confirmar_exclusao_[recurso]`
  - Formulário: `formulario_atividade_[recurso]`
- **Views:** Sempre prefira function-based views.
- **Filtros Dinâmicos:** Filtros de relatórios e listagens são interdependentes e atualizados via AJAX, sem recarregar a página.
- **Validações:** Multi-camadas (JS, Django Forms, Models, Services).
- **Docstrings:** Funções e métodos devem ser documentados conforme exemplos em `AGENT.md`.
- **Admin:** Cada módulo deve ter seu próprio admin, sem dependências cruzadas.

## Workflows de Desenvolvimento
- Ative o ambiente virtual: `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac).
- Instale dependências: `pip install -r requirements.txt`.
- Migre o banco: `python manage.py migrate`.
- Execute testes: `python manage.py test` ou `python manage.py test <app>`.
- Linting: `python scripts/lint.py`, `black .`, `isort .`.
- Monitoramento automático de formatação: use a tarefa "Monitoramento automático Ruff" no VS Code.

## Arquivos Estáticos (CRÍTICO) ⚠️

### Quando aplicar este procedimento:
Sempre que modificar **QUALQUER** arquivo em:
- `static/js/` (JavaScript)
- `static/css/` (Estilos)
- `static/img/` (Imagens)
- Qualquer subdiretório de `static/` em módulos (`alunos/static/`, `turmas/static/`, etc.)

### ✅ Checklist Obrigatório:

#### 1️⃣ Coletar arquivos estáticos
Execute no container Docker apropriado:

**Desenvolvimento (porta 8000):**
```powershell
cd E:\projetos\omaum\docker
docker compose -p omaum-dev --env-file ..\.env.dev -f docker-compose.yml exec -T omaum-web python manage.py collectstatic --noinput --clear
```

**Produção (porta 80):**
```powershell
cd E:\projetos\omaum\docker
docker compose --profile production -p omaum-prod --env-file ..\.env.production -f docker-compose.yml -f docker-compose.prod.override.yml exec -T omaum-web python manage.py collectstatic --noinput --clear
```

#### 2️⃣ Limpar cache do navegador
**Avisar o usuário para fazer UM destes procedimentos:**

**Opção A - Hard Refresh (mais rápido):**
- Windows/Linux: `Ctrl + Shift + R` ou `Ctrl + F5`
- Mac: `Cmd + Shift + R`

**Opção B - DevTools (mais confiável):**
1. Abrir DevTools: `F12`
2. Ir na aba **Network**
3. Marcar **"Disable cache"**
4. Recarregar a página (`F5`)

#### 3️⃣ Verificar mudanças
- Inspecionar elemento no navegador (F12 → Sources)
- Verificar se o arquivo JavaScript/CSS foi atualizado
- Conferir timestamp do arquivo em `/app/staticfiles/`

### 🔍 Por que isso é necessário?

**Ambiente Docker:**
```
┌─────────────────────────────────────┐
│  static/js/turmas/form.js           │  ← Arquivo fonte (você edita aqui)
│  (não servido diretamente)          │
└────────────┬────────────────────────┘
             │
             │ collectstatic copia
             ↓
┌─────────────────────────────────────┐
│  /app/staticfiles/js/turmas/form.js │  ← Django serve daqui!
│  (servido via WhiteNoise/Nginx)     │
└─────────────────────────────────────┘
```

- Django em produção **NÃO** serve arquivos de `static/` diretamente
- O comando `collectstatic` copia tudo para `/app/staticfiles/`
- Sem executá-lo, o navegador continua vendo a **versão antiga**
- Cache do navegador agrava o problema

### ⚠️ Erros comuns:
- **"Mudei o JS mas não funcionou"** → Esqueceu collectstatic
- **"Rodei collectstatic mas não mudou"** → Cache do navegador
- **"Funcionava antes mas parou"** → DOMContentLoaded duplicado ou conflito de event listeners
- **"Funciona no dev mas não no prod"** → Esqueceu collectstatic em produção

### 📝 Nota para IA:
**SEMPRE** mencionar estes passos **PROATIVAMENTE** após editar arquivos estáticos. Não espere o usuário perguntar!

## Integração e APIs
- APIs REST documentadas (Swagger/ReDoc), autenticação por token, versionamento e rate limiting.
- Integrações externas devem ser feitas via services dedicados.

## Exemplos de Estrutura
- Services: veja `presencas/services/README.md` e `relatorios_presenca/services/` para exemplos de lógica de negócio desacoplada das views.
- Templates: modais e includes centralizados, uso de Bootstrap 5 e JS customizado.
- Relatórios: geração programática via services e generators, com fidelidade visual aos modelos Excel.

## Boas Práticas e Restrições
- Nunca altere funcionalidades/layouts sem solicitação explícita.
- Sempre explique e aguarde aprovação antes de modificar blocos de código relevantes.
- Mantenha histórico de alterações e verifique consistência com as premissas do projeto.
- Siga as convenções de commit e branch descritas em `README.md` e `AGENT.md`.

## Referências Rápidas
- Configuração: `omaum/settings.py`, `omaum/base.html`, `omaum/home.html`.
- Documentação detalhada: `docs/`, `README.md`, `AGENT.md`, `relatorios_presenca/README.md`.
- Suporte: suporte@omaum.edu.br

---

> **Atenção:** Antes de propor alterações, leia e explique o bloco inteiro envolvido, considerando duplicidades, indentação e fechamento de blocos. Aguarde aprovação do usuário.
