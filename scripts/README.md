# Scripts Utilitários do Projeto OMAUM

Scripts auxiliares para tarefas de manutenção e desenvolvimento.

---

## 📁 Estrutura

```
scripts/
├── docker/              # Scripts para gestão Docker
├── migration/           # Scripts de migração de dados
├── preencher_fotos_alunos.py
├── format_code.py
├── lint.py
└── watch_tests.py
```

---

## 🖼️ Preencher Fotos de Alunos

**Arquivo:** `preencher_fotos_alunos.py`

Popula fotos para alunos ativos usando a API RandomUser, respeitando o sexo do aluno.

### Uso Básico

```bash
# Apenas alunos sem foto
python scripts/preencher_fotos_alunos.py

# Atualizar TODOS os alunos ativos (substitui fotos existentes)
python scripts/preencher_fotos_alunos.py --force

# Simular sem aplicar mudanças (dry-run)
python scripts/preencher_fotos_alunos.py --dry-run

# Força + dry-run (ver o que seria feito)
python scripts/preencher_fotos_alunos.py --force --dry-run
```

### Funcionalidades

✅ **Respeita sexo do aluno:**
- Masculino → Fotos de homens
- Feminino → Fotos de mulheres  
- Outro → Aleatório entre ambos

✅ **100 fotos por categoria** (0-99 da API RandomUser)

✅ **Relatório detalhado:**
- Total processado
- Sucessos e erros
- Distribuição por sexo

✅ **Modos de operação:**
- Normal: Apenas sem foto
- `--force`: Atualiza todos
- `--dry-run`: Simulação

### Dentro do Docker

```bash
# Desenvolvimento
docker compose -p omaum-dev exec omaum-web python scripts/preencher_fotos_alunos.py

# Com opções
docker compose -p omaum-dev exec omaum-web python scripts/preencher_fotos_alunos.py --force
```

### Exemplo de Saída

```
======================================================================
SCRIPT: Preencher Fotos de Alunos
======================================================================
📊 Total de alunos ativos: 150
📊 Alunos sem foto: 120

🚀 Processando 120 alunos...

----------------------------------------------------------------------
[1/120] João Silva (Masculino)
    ✅ Foto atribuída com sucesso!
[2/120] Maria Santos (Feminino)
    ✅ Foto atribuída com sucesso!
...

======================================================================
RELATÓRIO FINAL
======================================================================
✅ Sucessos:          118
❌ Erros:             2
👨 Masculino:         65
👩 Feminino:          55
📊 Total processado:  120
======================================================================
```

---

## 🔧 Corrigir Caminhos de Fotos

**Arquivo:** `corrigir_caminhos_fotos.py`

Corrige caminhos de fotos que usam barras invertidas (`\`) do Windows, convertendo para barras normais (`/`) compatíveis com Linux/Docker.

### Quando Usar

- Após migração de dados do Windows para Linux
- Se fotos não estão aparecendo na listagem/detalhes
- Após importação de dados legados

### Uso

```bash
# Execução direta
python scripts/corrigir_caminhos_fotos.py

# Dentro do Docker
docker compose -p omaum-dev exec omaum-web python scripts/corrigir_caminhos_fotos.py
```

### O que faz

✅ Busca todos os alunos com foto no banco  
✅ Identifica caminhos com barras invertidas (`\`)  
✅ Converte para barras normais (`/`)  
✅ Atualiza apenas o campo `foto` (rápido)  
✅ Relatório detalhado de correções

### Exemplo de Saída

```
======================================================================
SCRIPT: Corrigir Caminhos de Fotos
======================================================================

📊 Total de alunos com foto: 55

🔍 Verificando caminhos...

----------------------------------------------------------------------
[1/55] Alice Fernandes
    Antes: fotos_alunos\aluno_13.jpg
    Depois: fotos_alunos/aluno_13.jpg
    ✅ Corrigido!
...

======================================================================
RELATÓRIO FINAL
======================================================================
✅ Caminhos corrigidos: 53
✓  Já estavam corretos: 2
📊 Total processado:    55
======================================================================

⚠️  ATENÇÃO: Recarregue a página no navegador (Ctrl+Shift+R)
```

---

## 🔧 Outros Scripts

### `format_code.py`
Formata código Python usando Ruff (substituto do Black).

```bash
python scripts/format_code.py
```

### `lint.py`
Executa linting no código.

```bash
python scripts/lint.py
```

### `watch_tests.py`
Monitora mudanças e executa testes automaticamente.

```bash
python scripts/watch_tests.py
```

---

## 📚 Documentação Relacionada

- [../docs/development/](../docs/development/) - Guias de desenvolvimento
- [../docker/](../docker/) - Documentação Docker
- [../tests/fixtures/README.md](../tests/fixtures/README.md) - Fixtures de teste

---

## ⚠️ Notas Importantes

1. **Fotos de teste:** RandomUser fornece fotos fictícias para desenvolvimento
2. **Conectividade:** Requer acesso à internet para baixar fotos
3. **Situação do aluno:** Apenas alunos com `situacao='a'` (ativo) são processados
4. **Unicidade:** Cada foto tem nome único para evitar conflitos
5. **Caminhos normalizados:** Desde a versão com migration `0014_update_foto_upload_path`, todos os caminhos de foto são automaticamente normalizados para usar `/` (barras normais), garantindo compatibilidade entre Windows e Linux/Docker

---

**Última atualização:** 22 de dezembro de 2025
