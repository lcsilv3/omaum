# Estrutura de Views do Módulo Atividades

## ⚠️ IMPORTANTE: Localização das Views

As views **NÃO** estão em `atividades/views.py`! Elas foram reorganizadas em módulos especializados dentro de `views_ext/`.

## 📁 Estrutura Atual

```
atividades/
├── views.py                    ❌ DESCONTINUADO - Não usar!
└── views_ext/
    ├── academicas.py          ✅ CRUD de atividades acadêmicas
    ├── relatorios.py          ✅ Relatórios diversos
    ├── dashboard.py           ✅ Dashboard e métricas
    ├── calendario.py          ✅ Visualização em calendário
    ├── importacao.py          ✅ Importação de dados
    └── utils.py               ✅ Funções auxiliares
```

## 🔍 Como Encontrar a View Correta

### Método 1: Verificar urls.py (RECOMENDADO)

```python
# Abra: atividades/urls.py
# Procure o import da view desejada

from .views_ext.academicas import (
    listar_atividades_academicas,  # ← Está em views_ext/academicas.py
    criar_atividade_academica,
    ...
)
```

### Método 2: Usar o script helper

```bash
python scripts/find_view.py listar_atividades_academicas
```

### Método 3: Grep/busca no terminal

```bash
# PowerShell
Select-String -Pattern "def listar_atividades_academicas" -Path atividades/**/*.py

# Linux/Mac
grep -r "def listar_atividades_academicas" atividades/
```

## 📋 Mapeamento de Views Principais

| View | Arquivo | Linha Aprox. |
|------|---------|--------------|
| `listar_atividades_academicas` | `views_ext/academicas.py` | ~24 |
| `criar_atividade_academica` | `views_ext/academicas.py` | ~104 |
| `editar_atividade_academica` | `views_ext/academicas.py` | ~197 |
| `detalhar_atividade_academica` | `views_ext/academicas.py` | ~294 |
| `excluir_atividade_academica` | `views_ext/academicas.py` | ~321 |
| `dashboard_atividades` | `views_ext/dashboard.py` | ~15 |
| `relatorio_atividades` | `views_ext/relatorios.py` | ~24 |
| `calendario_atividades` | `views_ext/calendario.py` | ~12 |

## 🎯 Padrão de Resposta AJAX

**IMPORTANTE:** Todas as views AJAX devem retornar `JsonResponse`, **NÃO** `render()`!

### ❌ Errado (retorna HTML direto):
```python
if request.headers.get("x-requested-with") == "XMLHttpRequest":
    return render(request, "partial.html", context)
```

### ✅ Correto (retorna JSON com HTML renderizado):
```python
if request.headers.get("x-requested-with") == "XMLHttpRequest":
    from django.template.loader import render_to_string
    
    html_content = render_to_string("partial.html", context, request=request)
    
    return JsonResponse({
        "success": True,
        "html_content": html_content,
        "extra_data": {...}
    })
```

### JavaScript correspondente:
```javascript
fetch(url, {
    headers: {
        'X-Requested-With': 'XMLHttpRequest'
    }
})
.then(response => response.json())  // ← Espera JSON!
.then(data => {
    container.innerHTML = data.html_content;
});
```

## 📝 Checklist Antes de Editar uma View

- [ ] Verificou `atividades/urls.py` para confirmar o import?
- [ ] Localizou o arquivo correto em `views_ext/`?
- [ ] Leu a docstring da função para entender o comportamento?
- [ ] Conferiu se há testes relacionados em `tests/`?
- [ ] Para AJAX: confirmou que retorna `JsonResponse`?

## 🐛 Troubleshooting

### Problema: "Mudei a view mas não funcionou"
**Causa:** Editou `views.py` em vez de `views_ext/`
**Solução:** Veja o import em `urls.py` e edite o arquivo correto

### Problema: "AJAX retorna HTML em vez de JSON"
**Causa:** View usa `render()` em vez de `JsonResponse`
**Solução:** Use `render_to_string()` + `JsonResponse()`

### Problema: "ModuleNotFoundError: No module named 'atividades.utils'"
**Causa:** Import incorreto, deve ser `.views_ext.utils`
**Solução:** `from .views_ext.utils import get_models`

## 📚 Referências

- [Documentação de Views Django](https://docs.djangoproject.com/en/5.2/topics/http/views/)
- [JsonResponse](https://docs.djangoproject.com/en/5.2/ref/request-response/#jsonresponse-objects)
- [AJAX no Django](https://docs.djangoproject.com/en/5.2/topics/http/urls/#passing-extra-options-to-view-functions)
