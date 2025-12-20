# Estrutura de Arquivos Estáticos

## 📁 Padrão Django - App Static

### Estrutura Recomendada (Django Best Practice)

```
app_name/
├── static/
│   └── app_name/          ← IMPORTANTE: Namespace do app
│       ├── css/
│       │   └── styles.css
│       ├── js/
│       │   └── app.js
│       └── img/
│           └── logo.png
├── templates/
└── models.py
```

### ✅ Apps Padronizados Corretamente

- **alunos/** → `alunos/static/alunos/js/` (5 arquivos)
- **turmas/** → `turmas/static/turmas/js/` (4 arquivos)
- **matriculas/** → `matriculas/static/matriculas/js/` (2 arquivos)
- **atividades/** → `atividades/static/atividades/js/` (1 arquivo)
- **presencas/** → `presencas/static/presencas/`
- **relatorios_presenca/** → `relatorios_presenca/static/relatorios_presenca/`
- **pagamentos/** → `pagamentos/static/pagamentos/`
- **frequencias/** → `frequencias/static/frequencias/`

### 📂 Static Raiz (Fallback)

A pasta `static/` na raiz do projeto (`STATICFILES_DIRS`) deve conter apenas:

- **Arquivos globais compartilhados** entre todos os apps
- **Bibliotecas externas** (vendor)
- **Assets administrativos** (admin, django_extensions, django_select2, rest_framework)

```
static/
├── css/
│   └── dashboard.css        # CSS global compartilhado
├── js/
│   ├── instrutor_search.js  # JavaScript global
│   └── frequencia_form.js   # JavaScript global
├── img/
│   ├── logo.png            # Imagens globais
│   └── favicon.ico
└── vendor/                 # Bibliotecas de terceiros
```

### ❌ Anti-padrões (O que NÃO fazer)

**NÃO coloque arquivos específicos de um app em `static/app_name/`**

```
❌ ERRADO:
static/
├── alunos/              # ❌ Deve estar em alunos/static/alunos/
│   └── js/
├── turmas/              # ❌ Deve estar em turmas/static/turmas/
│   └── js/
└── atividades/          # ❌ Deve estar em atividades/static/atividades/
    └── js/
```

## 🔍 Como o Django Busca Arquivos Estáticos

### STATICFILES_FINDERS

O Django usa dois finders na seguinte ordem:

1. **AppDirectoriesFinder** (recomendado)
   - Procura em `app/static/` de cada app instalado
   - Namespace automático: `app/static/app_name/file.js`
   - Template: `{% static 'app_name/file.js' %}`

2. **FileSystemFinder** (fallback)
   - Procura em `STATICFILES_DIRS` (pasta `static/` raiz)
   - Sem namespace automático
   - Template: `{% static 'file.js' %}`

### Exemplo de Resolução

```django
{% load static %}
<script src="{% static 'alunos/js/formulario_aluno.js' %}"></script>
```

Django busca nesta ordem:
1. `alunos/static/alunos/js/formulario_aluno.js` ← **ENCONTROU! ✅**
2. `static/alunos/js/formulario_aluno.js` (não verifica se já achou)

## 📦 CollectStatic

### Comando de Coleta

```bash
# Desenvolvimento (no Docker)
docker compose -p omaum-dev exec omaum-web python manage.py collectstatic --noinput --clear

# Produção
docker compose -p omaum-prod exec omaum-web python manage.py collectstatic --noinput --clear
```

### Destino

Todos os arquivos são copiados para `STATIC_ROOT`:
- **Dev**: `/app/staticfiles/`
- **Prod**: `/app/staticfiles/`

### Estrutura Final (após collectstatic)

```
staticfiles/
├── admin/              # Django admin
├── alunos/
│   └── js/
│       ├── formulario_aluno.js
│       ├── listar_alunos.js
│       └── ...
├── turmas/
│   └── js/
│       ├── matricula_lote.js
│       └── ...
├── atividades/
│   └── js/
│       └── listar_atividades_academicas.js
└── css/
    └── dashboard.css
```

## 🔄 Migração de Estrutura Antiga

### Passo a Passo

Se você tem arquivos em `static/app_name/`:

```bash
# 1. Criar estrutura correta
mkdir -p app_name/static/app_name/js

# 2. Mover arquivos
mv static/app_name/js/*.js app_name/static/app_name/js/

# 3. Remover pasta antiga
rm -rf static/app_name
```

### Checklist Pós-Migração

- [ ] Arquivo movido para `app/static/app/`
- [ ] Template usa `{% static 'app/file.js' %}`
- [ ] Executar `collectstatic --clear`
- [ ] Testar no navegador com Hard Refresh (Ctrl+Shift+R)
- [ ] Versão do JS atualizada no template (`?v=YYYYMMDD`)

## 🚨 Cache do Navegador

### Problema Comum

Após mover arquivos, o navegador pode usar versão em cache.

### Solução

1. **Hard Refresh**: `Ctrl + Shift + R` (Windows/Linux) ou `Cmd + Shift + R` (Mac)

2. **Versão no Template**:
   ```django
   <script src="{% static 'app/js/file.js' %}?v=20251220"></script>
   ```

3. **DevTools**:
   - Abrir F12 → Network
   - Marcar "Disable cache"
   - Recarregar página

## 📝 Histórico de Mudanças

### 2025-12-20 - Padronização de Atividades

**Problema**: `static/atividades/js/` não seguia padrão Django

**Solução**: Movido para `atividades/static/atividades/js/`

**Arquivos Afetados**:
- `static/atividades/js/listar_atividades_academicas.js` → `atividades/static/atividades/js/`

**Pastas Vazias Removidas**:
- `static/relatorios_presenca/` (sem arquivos)
- `static/pagamentos/` (sem arquivos)
- `static/atividades/` (movido)

**Commit**: `[hash do commit]`

## 🔗 Referências

- [Django Static Files](https://docs.djangoproject.com/en/5.0/howto/static-files/)
- [STATICFILES_FINDERS](https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-STATICFILES_FINDERS)
- [AppDirectoriesFinder](https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#django.contrib.staticfiles.finders.AppDirectoriesFinder)
