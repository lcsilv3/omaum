# Script de Correção de Fixtures

## Visão Geral

Este script corrige fixtures Django exportados do ambiente de desenvolvimento para serem compatíveis com o ambiente de produção, resolvendo incompatibilidades de schema e dados.

## Problemas Corrigidos

### 1. **Permissions e Content Types**
- **Problema**: Django auto-gera `auth.permission` e `contenttypes.contenttype` causando conflitos de chave única
- **Solução**: Remove todos os registros destes modelos do fixture

### 2. **Campos de Situação (Aluno)**
- **Problema**: Campo `situacao` exportado com texto completo ("ATIVO", "INATIVO") mas model aceita apenas 1 caractere
- **Solução**: Mapeia valores:
  - `ATIVO` → `a`
  - `INATIVO` → `i`
  - `SUSPENSO` → `s`
  - `TRANCADO` → `t`

### 3. **Campos de Situação Iniciática (Aluno)**
- **Problema**: Campo `situacao_iniciatica` com texto completo
- **Solução**: Mapeia valores:
  - `ATIVO` → `A`
  - `INATIVO` → `I`
  - `EXONERADO` → `E`
  - `DESLIGADO` → `D`

### 4. **Campos Inexistentes (Turma)**
- **Problema**: Modelo de desenvolvimento tem campos que não existem em produção:
  - `data_inicio` (correto: `data_inicio_ativ`)
  - `data_fim` (correto: `data_termino_atividades`)
  - `instrutor`, `instrutor_auxiliar`, `auxiliar_instrucao`
  - `alerta_instrutor`, `alerta_mensagem`
  - `encerrada_em`, `encerrada_por`
  - `bloqueio_total`, `bloqueio_ativo_em`, `bloqueio_ativo_por`
  - `justificativa_reabertura`
- **Solução**: Remove todos os campos não presentes no modelo de produção

## Uso

### Sintaxe Básica

```bash
python scripts/corrigir_fixtures_completo.py <arquivo_entrada> <arquivo_saida>
```

### Exemplo

```bash
# Usando arquivos padrão
python scripts/corrigir_fixtures_completo.py

# Especificando arquivos
python scripts/corrigir_fixtures_completo.py dev_data.json dev_data_corrigido.json
```

### Em Container Docker

```bash
# Copiar script para container
docker cp scripts/corrigir_fixtures_completo.py omaum-web-prod:/app/

# Executar correção
docker exec omaum-web-prod python /app/corrigir_fixtures_completo.py \
    /app/dev_data_original.json \
    /app/dev_data_corrigido.json

# Importar dados corrigidos
docker exec omaum-web-prod python manage.py loaddata dev_data_corrigido.json
```

## Workflow Completo: Dev → Prod

### 1. Exportar dados de desenvolvimento

```bash
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --indent 2 \
    --exclude sessions \
    --exclude admin.logentry \
    --exclude auth.permission \
    --exclude contenttypes.contenttype \
    -o dev_data_$(date +%Y%m%d_%H%M%S).json
```

**Importante**: Já exclua `auth.permission` e `contenttypes.contenttype` no export!

### 2. Corrigir fixture

```bash
python scripts/corrigir_fixtures_completo.py \
    dev_data_20251126_090717.json \
    dev_data_corrigido.json
```

### 3. Backup de produção

```bash
docker exec omaum-db-prod pg_dump -U postgres -d omaum_db \
    -Fc -f /backups/backup_antes_importacao_$(date +%Y%m%d_%H%M%S).dump
```

### 4. Importar em produção

```bash
# Copiar fixture corrigido
docker cp dev_data_corrigido.json omaum-web-prod:/app/

# Limpar banco (CUIDADO!)
docker exec omaum-web-prod python manage.py flush --noinput

# Importar dados
docker exec omaum-web-prod python manage.py loaddata dev_data_corrigido.json
```

## Estatísticas de Correção

Exemplo de saída do script:

```
============================================================
RESUMO DA CORREÇÃO
============================================================
Registros originais: 1106
Registros finais: 936
Removidos: 170

Detalhamento:
  - removidos_permission: 136
  - removidos_contenttype: 34
  - corrigidos_situacao: 53
  - corrigidos_situacao_iniciatica: 53
  - campos_turma_removidos: 403
  - turmas_processadas: 31
============================================================
```

## Campos Válidos por Modelo

### Turma (campos aceitos em produção)

```python
campos_validos_turma = {
    'nome', 'curso', 'descricao', 'num_livro', 'perc_presenca_minima',
    'data_iniciacao', 'data_inicio_ativ', 'data_prim_aula', 
    'data_termino_atividades', 'dias_semana', 'horario', 'local',
    'vagas', 'status', 'ativo', 'created_at', 'updated_at'
}
```

## Troubleshooting

### Erro: `FieldDoesNotExist: Model has no field named 'X'`

**Solução**: Adicione o campo ao conjunto `campos_validos_turma` ou equivalente no script.

### Erro: `value too long for type character varying(1)`

**Solução**: Verifique mapeamentos de `situacao` e `situacao_iniciatica` no script.

### Erro: `duplicate key value violates unique constraint`

**Solução**: Certifique-se de excluir `auth.permission` e `contenttypes.contenttype` no dumpdata.

## Manutenção

### Adicionar nova correção

1. Abra `scripts/corrigir_fixtures_completo.py`
2. Adicione novo bloco de correção após o bloco 3
3. Atualize contador em `stats`
4. Documente neste README

### Atualizar campos válidos

Quando o modelo Turma (ou outro) mudar em produção:

1. Execute em produção: `python manage.py shell`
2. Obtenha campos: `[f.name for f in Turma._meta.get_fields()]`
3. Atualize conjunto no script

## Autor

Criado para projeto OMAUM - Sistema de Gestão Acadêmica Iniciática

## Histórico

- **2025-11-27**: Versão inicial consolidando todas as correções identificadas durante sincronização dev→prod
